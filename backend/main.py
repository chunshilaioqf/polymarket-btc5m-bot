import asyncio
import json
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from starlette.staticfiles import StaticFiles
from typing import Optional, List, Dict
import os

from trader import PolymarketAPI, BTC5mTrader


# 全局变量
trader: Optional[BTC5mTrader] = None
api: Optional[PolymarketAPI] = None
task: Optional[asyncio.Task] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global trader, api
    yield
    if trader:
        trader.stop()
    if api:
        await api.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_message(self, message: Dict):
        for connection in self.active_connections[:]:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


async def broadcast_status():
    while True:
        if trader and trader.running:
            status = trader.get_status()
            await manager.send_message({"type": "status", "data": status})
        await asyncio.sleep(2)


async def broadcast_logs():
    last_log_count = 0
    while True:
        if trader:
            logs = trader.logs[last_log_count:]
            if logs:
                await manager.send_message({"type": "logs", "data": logs})
                last_log_count = len(trader.logs)
        await asyncio.sleep(0.5)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        if trader:
            await websocket.send_json({"type": "status", "data": trader.get_status()})
            await websocket.send_json({"type": "logs", "data": trader.logs[-50:]})
        
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.post("/api/start")
async def start_trading(request: dict):
    global trader, api, task
    
    private_key = request.get("private_key", "")
    proxy = request.get("proxy", "") or None
    signature_type = int(request.get("signature_type", 2))
    
    if not private_key:
        return {"status": "error", "message": "私钥不能为空"}
    
    if trader and trader.running:
        return {"status": "error", "message": "交易已在运行中"}
    
    try:
        api = PolymarketAPI(private_key, proxy=proxy, signature_type=signature_type)
        trader = BTC5mTrader(api)
        task = asyncio.create_task(trader.run())
        asyncio.create_task(broadcast_status())
        asyncio.create_task(broadcast_logs())
        
        proxy_msg = f" (代理: {proxy})" if proxy else ""
        type_names = {0: "EOA", 1: "POLY_PROXY", 2: "GNOSIS_SAFE"}
        type_msg = type_names.get(signature_type, str(signature_type))
        return {"status": "success", "message": f"交易已启动{proxy_msg} (钱包类型: {type_msg})"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/stop")
async def stop_trading():
    global trader, api, task
    
    if not trader:
        return {"status": "error", "message": "交易未启动"}
    
    try:
        trader.stop()
        if api:
            await api.close()
            api = None
        return {"status": "success", "message": "交易已停止"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/status")
async def get_status():
    if not trader:
        return {"running": False, "message": "交易未启动"}
    return trader.get_status()


@app.get("/api/logs")
async def get_logs(limit: int = 100):
    if not trader:
        return {"logs": []}
    return {"logs": trader.logs[-limit:]}


@app.get("/api/balance")
async def get_balance():
    if not api:
        return {"error": "请先启动交易"}
    return await api.get_balance()


@app.get("/api/positions")
async def get_positions():
    if not api:
        return []
    return await api.get_positions()


@app.get("/api/trades")
async def get_trades(limit: int = 50):
    if not api:
        return []
    return await api.get_trade_history(limit)


@app.get("/")
async def root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>Polymarket BTC 5m Bot</h1>")


if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
