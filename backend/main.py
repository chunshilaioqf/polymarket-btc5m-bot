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
    # 关闭时停止交易
    if trader:
        trader.stop()
    if api:
        await api.close()


app = FastAPI(lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取当前目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")


# WebSocket 连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_message(self, message: Dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


async def broadcast_status():
    """定期广播状态"""
    while True:
        if trader and trader.running:
            status = trader.get_status()
            await manager.send_message({
                "type": "status",
                "data": status
            })
        await asyncio.sleep(2)


async def broadcast_logs():
    """定期广播日志"""
    last_log_count = 0
    while True:
        if trader:
            logs = trader.logs[last_log_count:]
            if logs:
                await manager.send_message({
                    "type": "logs",
                    "data": logs
                })
                last_log_count = len(trader.logs)
        await asyncio.sleep(0.5)


# WebSocket 路由
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # 发送初始状态
        if trader:
            await websocket.send_json({
                "type": "status",
                "data": trader.get_status()
            })
            await websocket.send_json({
                "type": "logs",
                "data": trader.logs[-50:] if trader.logs else []
            })
        
        while True:
            data = await websocket.receive_text()
            # 处理前端消息（如果需要）
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# API 路由
@app.post("/api/start")
async def start_trading(request: dict):
    global trader, api, task
    
    private_key = request.get("private_key", "")
    if not private_key:
        return {"status": "error", "message": "私钥不能为空"}
    
    if trader and trader.running:
        return {"status": "error", "message": "交易已在运行中"}
    
    try:
        # 创建 API 实例
        api = PolymarketAPI(private_key)
        
        # 创建交易机器人
        trader = BTC5mTrader(api)
        
        # 启动交易任务
        task = asyncio.create_task(trader.run())
        
        # 启动广播任务
        asyncio.create_task(broadcast_status())
        asyncio.create_task(broadcast_logs())
        
        return {"status": "success", "message": "交易已启动"}
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
        return {
            "running": False,
            "message": "交易未启动"
        }
    
    return trader.get_status()


@app.get("/api/logs")
async def get_logs(limit: int = 100):
    if not trader:
        return {"logs": []}
    
    return {"logs": trader.logs[-limit:]}


# 首页路由 (必须在静态文件之前)
@app.get("/")
async def root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Polymarket BTC 5m Bot</title>
    </head>
    <body>
        <h1>Polymarket BTC 5m Bot</h1>
        <p>Please place index.html in the frontend folder</p>
    </body>
    </html>
    """)


# 挂载静态文件 (放在最后)
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")