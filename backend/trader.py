import asyncio
import httpx
import json
import time
from typing import Optional, Dict, Any, List
from datetime import datetime

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY, SELL
import py_clob_client.http_helpers.helpers as http_helpers


class PolymarketAPI:
    """Polymarket API 封装 (使用官方 SDK)"""
    
    CLOB_HOST = "https://clob.polymarket.com"
    GAMMA_URL = "https://gamma-api.polymarket.com"
    CHAIN_ID = 137  # Polygon mainnet
    
    def __init__(self, private_key: str, proxy: str = None, signature_type: int = 2):
        self.private_key = private_key
        self.proxy = proxy
        self.signature_type = signature_type
        self.client: Optional[ClobClient] = None
        self.http_client = httpx.AsyncClient(
            timeout=30.0,
            headers={"User-Agent": "Polymarket-Bot/1.0", "Accept": "application/json"},
            follow_redirects=True,
            proxy=proxy if proxy else None
        )
        self.address = self._derive_address(private_key)
        self.api_creds = None
    
    def _derive_address(self, private_key: str) -> str:
        """从私钥派生地址"""
        try:
            from eth_account import Account
            if private_key.startswith('0x'):
                private_key = private_key[2:]
            account = Account.from_key(private_key)
            return account.address
        except Exception as e:
            raise ValueError(f"私钥解析失败: {e}")
    
    async def init_client(self):
        """初始化 CLOB 客户端"""
        try:
            # 如果有代理，注入到 SDK 的 HTTP 客户端中
            if self.proxy:
                import py_clob_client.http_helpers.helpers as http_helpers
                http_helpers._http_client = httpx.Client(
                    http2=False,  # 禁用 HTTP/2 以兼容更多代理
                    proxy=self.proxy,
                    timeout=30.0,
                    verify=False  # 某些代理需要禁用证书验证
                )
            
            # 创建临时客户端获取 API credentials
            temp_client = ClobClient(
                self.CLOB_HOST,
                key=self.private_key,
                chain_id=self.CHAIN_ID
            )
            
            # 创建或获取 API 凭证
            self.api_creds = temp_client.create_or_derive_api_creds()
            
            # 创建正式交易客户端
            self.client = ClobClient(
                self.CLOB_HOST,
                key=self.private_key,
                chain_id=self.CHAIN_ID,
                creds=self.api_creds,
                signature_type=self.signature_type,
                funder=self.address
            )
            
            return True
        except Exception as e:
            raise Exception(f"初始化 CLOB 客户端失败: {e}")
    
    async def check_geoblock(self) -> Dict:
        """检查地区限制"""
        try:
            resp = await self.http_client.get("https://polymarket.com/api/geoblock")
            return resp.json()
        except Exception as e:
            return {"error": str(e), "blocked": True}
    
    async def _safe_gamma_request(self, url: str) -> Any:
        """安全的 Gamma API 请求"""
        try:
            resp = await self.http_client.get(url)
            if resp.status_code == 200:
                return resp.json()
            return {"error": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def find_active_btc_updown_market(self) -> Optional[Dict]:
        """搜索当前活跃的 BTC-updown-5m 市场"""
        import re
        
        now = int(time.time())
        aligned = (now // 300) * 300
        
        # 通过网页获取当前活跃市场的 condition_id
        for offset in [0, -1, 1, -2, 2]:
            ts = aligned + offset * 300
            try:
                resp = await self.http_client.get(f"https://polymarket.com/event/btc-updown-5m-{ts}")
                if resp.status_code == 200:
                    html = resp.text
                    match = re.search(r'"condition_id"\s*:\s*"([^"]+)"', html)
                    if not match:
                        match = re.search(r'"conditionId"\s*:\s*"([^"]+)"', html)
                    
                    if match:
                        condition_id = match.group(1)
                        # 用 SDK 获取市场详情
                        market = self.client.get_market(condition_id)
                        if market:
                            return market
            except Exception:
                continue
        
        return None
    
    def get_market_info(self, condition_id: str) -> Dict:
        """获取市场信息"""
        return self.client.get_market(condition_id)
    
    def create_order(self, token_id: str, price: float, size: float, side: int) -> Dict:
        """创建并提交订单"""
        try:
            # 获取市场信息以获取 tick_size 和 neg_risk
            # 这里我们需要直接传入参数
            
            order_args = OrderArgs(
                token_id=token_id,
                price=price,
                size=size,
                side=side
            )
            
            # 创建并签名订单
            signed_order = self.client.create_order(order_args)
            
            # 提交订单
            response = self.client.post_order(signed_order)
            
            return response
        except Exception as e:
            return {"error": str(e)}
    
    def get_orders(self) -> List[Dict]:
        """获取当前挂单"""
        try:
            return self.client.get_orders()
        except Exception as e:
            return []
    
    def cancel_order(self, order_id: str) -> Dict:
        """取消订单"""
        try:
            return self.client.cancel(order_id=order_id)
        except Exception as e:
            return {"error": str(e)}
    
    def get_trades(self, limit: int = 50) -> List[Dict]:
        """获取交易历史"""
        try:
            return self.client.get_trades(limit=limit)
        except Exception as e:
            return []
    
    async def get_positions(self) -> List[Dict]:
        """获取持仓"""
        url = f"{self.GAMMA_URL}/positions?user={self.address}"
        result = await self._safe_gamma_request(url)
        return result if isinstance(result, list) else []
    
    async def get_balance(self) -> Dict:
        """获取余额"""
        positions = await self.get_positions()
        total_value = sum(float(p.get("currentValue", 0)) for p in positions)
        return {"balance_usdc": total_value, "positions": positions}
    
    async def close(self):
        """关闭连接"""
        await self.http_client.aclose()


class BTC5mTrader:
    """BTC 5分钟交易机器人"""
    
    def __init__(self, api: PolymarketAPI):
        self.api = api
        self.running = False
        self.up_order_id: Optional[str] = None
        self.down_order_id: Optional[str] = None
        self.up_filled = False
        self.down_filled = False
        self.logs: List[Dict] = []
        self.market_info: Optional[Dict] = None
        self.token_ids: Dict[str, str] = {}
        self.tick_size: str = "0.01"
        self.neg_risk: bool = False
        self.balance: Dict = {}
        self.positions: List[Dict] = []
        self.trade_history: List[Dict] = []
        self.last_market_search = 0
    
    def log(self, level: str, message: str):
        timestamp = datetime.now().isoformat()
        self.logs.append({"timestamp": timestamp, "level": level, "message": message})
        if len(self.logs) > 1000:
            self.logs = self.logs[-1000:]
    
    async def initialize(self) -> bool:
        """初始化"""
        try:
            self.log("INFO", f"正在初始化...")
            self.log("INFO", f"钱包地址: {self.api.address}")
            
            # 检查地区限制
            geo = await self.api.check_geoblock()
            if geo.get("blocked"):
                country = geo.get("country", "Unknown")
                self.log("WARNING", f"当前地区 ({country}) 可能受限制")
                if "error" not in geo:
                    self.log("INFO", f"IP: {geo.get('ip', 'N/A')}")
            
            # 初始化 CLOB 客户端
            self.log("INFO", "正在初始化 CLOB 客户端...")
            await self.api.init_client()
            self.log("INFO", "CLOB 客户端初始化成功")
            
            return await self.refresh_market()
            
        except Exception as e:
            self.log("ERROR", f"初始化失败: {type(e).__name__}: {e}")
            return False
    
    async def refresh_market(self) -> bool:
        """刷新市场"""
        try:
            market = await self.api.find_active_btc_updown_market()
            
            if not market:
                self.log("WARNING", "未找到活跃的 BTC-updown-5m 市场")
                return False
            
            # 检查是否是新市场
            new_condition_id = market.get("condition_id", "")
            old_condition_id = self.market_info.get("condition_id", "") if self.market_info else ""
            
            if new_condition_id != old_condition_id:
                self.log("INFO", f"发现新市场: {market.get('question', 'Unknown')[:60]}")
                self.market_info = market
                
                # 获取 token 信息
                self.token_ids = {}
                tokens = market.get("tokens", [])
                for token in tokens:
                    outcome = str(token.get("outcome", "")).lower()
                    token_id = token.get("token_id", "")
                    if outcome == "up":
                        self.token_ids["up"] = token_id
                    elif outcome == "down":
                        self.token_ids["down"] = token_id
                
                # 获取 tick_size 和 neg_risk
                self.tick_size = str(market.get("minimum_tick_size", "0.01"))
                self.neg_risk = market.get("neg_risk", False)
                
                self.log("INFO", f"Tick Size: {self.tick_size}")
                self.log("INFO", f"Neg Risk: {self.neg_risk}")
                self.log("INFO", f"Up Token: {self.token_ids.get('up', 'N/A')[:30]}...")
                self.log("INFO", f"Down Token: {self.token_ids.get('down', 'N/A')[:30]}...")
                
                # 重置订单
                self.up_order_id = None
                self.down_order_id = None
                self.up_filled = False
                self.down_filled = False
                
                await self.update_account_info()
                return True
            else:
                return True
                
        except Exception as e:
            self.log("ERROR", f"刷新市场失败: {type(e).__name__}: {e}")
            return False
    
    async def update_account_info(self):
        try:
            self.balance = await self.api.get_balance()
            self.positions = await self.api.get_positions()
            self.trade_history = self.api.get_trades(20)
        except Exception as e:
            self.log("WARNING", f"更新账户信息失败: {e}")
    
    async def place_orders(self):
        """下单"""
        if not self.token_ids.get("up") or not self.token_ids.get("down"):
            self.log("ERROR", "无法下单：token 信息缺失")
            return
        
        price = 0.10  # 价格 0.10 = 10%
        size = 0.5
        
        self.log("INFO", f"开始下单 - 价格: {price}, 数量: {size}")
        self.log("INFO", f"市场: {self.market_info.get('question', 'N/A')[:50]}")
        
        # 下单 Up
        try:
            result = self.api.create_order(
                token_id=self.token_ids["up"],
                price=price,
                size=size,
                side=BUY
            )
            if "error" in result:
                self.log("ERROR", f"Up 下单失败: {result['error']}")
            else:
                self.up_order_id = result.get("orderID", result.get("success", {}).get("orderID"))
                self.log("INFO", f"Up 订单已创建: {self.up_order_id}")
        except Exception as e:
            self.log("ERROR", f"Up 下单异常: {e}")
        
        # 下单 Down
        try:
            result = self.api.create_order(
                token_id=self.token_ids["down"],
                price=price,
                size=size,
                side=BUY
            )
            if "error" in result:
                self.log("ERROR", f"Down 下单失败: {result['error']}")
            else:
                self.down_order_id = result.get("orderID", result.get("success", {}).get("orderID"))
                self.log("INFO", f"Down 订单已创建: {self.down_order_id}")
        except Exception as e:
            self.log("ERROR", f"Down 下单异常: {e}")
        
        self.up_filled = False
        self.down_filled = False
    
    async def check_and_cancel(self):
        """检查并取消订单"""
        try:
            orders = self.api.get_orders()
            
            up_status = "unknown"
            down_status = "unknown"
            
            for order in orders:
                oid = order.get("order_id") or order.get("orderID")
                status = order.get("status", "unknown")
                
                if oid == self.up_order_id:
                    up_status = status
                elif oid == self.down_order_id:
                    down_status = status
            
            self.log("INFO", f"订单状态 - Up: {up_status}, Down: {down_status}")
            
            if up_status == "matched" and not self.up_filled:
                self.up_filled = True
                self.log("INFO", "Up 订单已成交，取消 Down 订单...")
                if self.down_order_id:
                    result = self.api.cancel_order(self.down_order_id)
                    self.log("INFO" if "error" not in result else "ERROR",
                             "Down 已取消" if "error" not in result else f"取消失败: {result['error']}")
            
            if down_status == "matched" and not self.down_filled:
                self.down_filled = True
                self.log("INFO", "Down 订单已成交，取消 Up 订单...")
                if self.up_order_id:
                    result = self.api.cancel_order(self.up_order_id)
                    self.log("INFO" if "error" not in result else "ERROR",
                             "Up 已取消" if "error" not in result else f"取消失败: {result['error']}")
                
        except Exception as e:
            self.log("ERROR", f"检查订单失败: {e}")
    
    def get_current_period_info(self) -> Dict:
        timestamp = datetime.now().timestamp()
        period = int(timestamp // 300)
        period_start = period * 300
        period_end = period_start + 300
        return {
            "period": period,
            "period_start": datetime.fromtimestamp(period_start).isoformat(),
            "period_end": datetime.fromtimestamp(period_end).isoformat(),
            "seconds_until_end": int(period_end - timestamp),
            "is_first_minute": (timestamp - period_start) < 60,
            "is_last_30_seconds": (period_end - timestamp) < 30
        }
    
    async def run(self):
        self.running = True
        self.log("INFO", "交易机器人已启动")
        
        if not await self.initialize():
            self.running = False
            self.log("ERROR", "初始化失败，机器人停止")
            return
        
        while self.running:
            try:
                now = datetime.now().timestamp()
                period_info = self.get_current_period_info()
                
                # 每5分钟刷新市场
                if now - self.last_market_search > 300:
                    self.last_market_search = now
                    await self.refresh_market()
                
                # 第一分钟下单
                if period_info["is_first_minute"] and not self.up_order_id and self.token_ids:
                    await self.place_orders()
                
                # 最后30秒检查
                if period_info["is_last_30_seconds"]:
                    await self.check_and_cancel()
                
                # 每30秒更新账户
                if period_info["seconds_until_end"] % 30 == 0:
                    await self.update_account_info()
                
                # 周期结束重置
                if period_info["seconds_until_end"] <= 0:
                    self.up_order_id = None
                    self.down_order_id = None
                    self.up_filled = False
                    self.down_filled = False
                
                await asyncio.sleep(1)
                
            except Exception as e:
                self.log("ERROR", f"交易循环错误: {e}")
                await asyncio.sleep(5)
        
        self.log("INFO", "交易机器人已停止")
    
    def stop(self):
        self.running = False
        self.up_order_id = None
        self.down_order_id = None
    
    def get_status(self) -> Dict:
        return {
            "running": self.running,
            "current_period": self.get_current_period_info(),
            "orders": {
                "up_order_id": self.up_order_id,
                "down_order_id": self.down_order_id,
                "up_filled": self.up_filled,
                "down_filled": self.down_filled
            },
            "market": self.market_info,
            "balance": self.balance,
            "positions": self.positions,
            "trade_history": self.trade_history,
            "address": self.api.address,
            "token_ids": self.token_ids
        }
