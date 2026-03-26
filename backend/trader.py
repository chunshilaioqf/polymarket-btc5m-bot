import httpx
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
import time


class PolymarketAPI:
    """Polymarket API 封装"""
    
    BASE_URL = "https://clob.polymarket.com"
    GRAPH_URL = "https://clob.polymarket.com/graphql"
    
    def __init__(self, private_key: str):
        self.private_key = private_key
        self.address = self._derive_address(private_key)
        self.client = httpx.AsyncClient(timeout=30.0)
    
    def _derive_address(self, private_key: str) -> str:
        """从私钥派生地址"""
        try:
            from ecdsa import SigningKey, SECP256k1
            import hashlib
            
            # 移除 0x 前缀
            if private_key.startswith('0x'):
                private_key = private_key[2:]
            
            # 将私钥转换为字节
            priv_key_bytes = bytes.fromhex(private_key)
            
            # 使用 ecdsa 生成公钥
            sk = SigningKey.from_string(priv_key_bytes, curve=SECP256k1)
            vk = sk.get_verifying_key()
            
            # 公钥的 SHA256 哈希
            pub_key_hash = hashlib.sha256(vk.to_string()).digest()
            
            # 取最后 20 字节作为地址
            address = pub_key_hash[-20:].hex()
            return "0x" + address
        except Exception as e:
            raise ValueError(f"私钥解析失败: {e}")
    
    async def get_markets(self, condition_id: str) -> List[Dict]:
        """获取市场信息"""
        query = """
        query GetCondition($conditionId: String!) {
            condition(conditionId: $conditionId) {
                markets {
                    id
                    question
                    description
                    tokens {
                        id
                        symbol
                        color
                    }
                }
            }
        }
        """
        variables = {"conditionId": condition_id}
        
        response = await self.client.post(
            self.GRAPH_URL,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"}
        )
        
        data = response.json()
        return data.get("data", {}).get("condition", {}).get("markets", [])
    
    async def get_order_book(self, token_id: str) -> Dict:
        """获取订单簿"""
        url = f"{self.BASE_URL}/orderbook/{token_id}"
        response = await self.client.get(url)
        return response.json()
    
    async def place_order(self, token_id: str, side: str, price: float, size: float) -> Dict:
        """下单"""
        order_data = {
            "token_id": token_id,
            "side": side,  # "Buy" or "Sell"
            "price": price,
            "size": size,
            "address": self.address,
        }
        
        # 这里需要实际签名
        # 简化版本，实际需要使用私钥签名
        url = f"{self.BASE_URL}/orders"
        response = await self.client.post(url, json=order_data)
        return response.json()
    
    async def cancel_order(self, order_id: str) -> Dict:
        """取消订单"""
        url = f"{self.BASE_URL}/orders/{order_id}"
        response = await self.client.delete(url)
        return response.json()
    
    async def get_orders(self) -> List[Dict]:
        """获取当前订单"""
        url = f"{self.BASE_URL}/orders?address={self.address}"
        response = await self.client.get(url)
        return response.json()
    
    async def get_fills(self) -> List[Dict]:
        """获取成交记录"""
        url = f"{self.BASE_URL}/fills?address={self.address}"
        response = await self.client.get(url)
        return response.json()
    
    async def close(self):
        """关闭连接"""
        await self.client.aclose()


class BTC5mTrader:
    """BTC 5分钟交易机器人"""
    
    # Polymarket BTC-updown-5m 的 condition ID
    CONDITION_ID = "0x3c8fbc4acd7152e5aa4e7ed5b96f6c7f"  # 示例，实际需要查询
    
    def __init__(self, api: PolymarketAPI):
        self.api = api
        self.running = False
        self.current_period = 0
        self.yes_order_id: Optional[str] = None
        self.no_order_id: Optional[str] = None
        self.yes_filled = False
        self.no_filled = False
        self.logs: List[Dict] = []
        self.market_info: Optional[Dict] = None
        self.token_ids: Dict[str, str] = {}
    
    def log(self, level: str, message: str):
        """记录日志"""
        timestamp = datetime.now().isoformat()
        self.logs.append({
            "timestamp": timestamp,
            "level": level,
            "message": message
        })
        # 只保留最近 1000 条日志
        if len(self.logs) > 1000:
            self.logs = self.logs[-1000:]
    
    async def initialize(self):
        """初始化，获取市场信息"""
        try:
            self.log("INFO", "正在获取市场信息...")
            markets = await self.api.get_markets(self.CONDITION_ID)
            
            if not markets:
                self.log("ERROR", "未找到市场信息")
                return False
            
            self.market_info = markets[0]
            
            # 获取 token ID
            for token in self.market_info.get("tokens", []):
                symbol = token.get("symbol", "").upper()
                token_id = token.get("id", "")
                if "YES" in symbol:
                    self.token_ids["yes"] = token_id
                elif "NO" in symbol:
                    self.token_ids["no"] = token_id
            
            self.log("INFO", f"市场: {self.market_info.get('question', 'Unknown')}")
            self.log("INFO", f"Yes Token: {self.token_ids.get('yes', 'N/A')}")
            self.log("INFO", f"No Token: {self.token_ids.get('no', 'N/A')}")
            
            return True
        except Exception as e:
            self.log("ERROR", f"初始化失败: {e}")
            return False
    
    async def place_orders(self):
        """在周期开始时下单"""
        try:
            price = 10
            size = 0.5
            
            self.log("INFO", f"开始下单 - 价格: {price}, 数量: {size}")
            
            # 下单 Yes
            try:
                result = await self.api.place_order(
                    self.token_ids["yes"],
                    "Buy",
                    price,
                    size
                )
                self.yes_order_id = result.get("orderID") or result.get("id")
                self.log("INFO", f"Yes 订单已创建: {self.yes_order_id}")
            except Exception as e:
                self.log("ERROR", f"Yes 下单失败: {e}")
            
            # 下单 No
            try:
                result = await self.api.place_order(
                    self.token_ids["no"],
                    "Buy",
                    price,
                    size
                )
                self.no_order_id = result.get("orderID") or result.get("id")
                self.log("INFO", f"No 订单已创建: {self.no_order_id}")
            except Exception as e:
                self.log("ERROR", f"No 下单失败: {e}")
            
            self.yes_filled = False
            self.no_filled = False
            
        except Exception as e:
            self.log("ERROR", f"下单失败: {e}")
    
    async def check_and_cancel(self):
        """检查订单状态并在需要时取消"""
        try:
            orders = await self.api.get_orders()
            
            yes_status = "unknown"
            no_status = "unknown"
            
            for order in orders:
                oid = order.get("orderID") or order.get("id")
                if oid == self.yes_order_id:
                    yes_status = order.get("status", "unknown")
                elif oid == self.no_order_id:
                    no_status = order.get("status", "unknown")
            
            self.log("INFO", f"订单状态 - Yes: {yes_status}, No: {no_status}")
            
            # 检查是否成交
            if yes_status == "filled" and not self.yes_filled:
                self.yes_filled = True
                self.log("INFO", "Yes 订单已成交，正在取消 No 订单...")
                if self.no_order_id:
                    await self.api.cancel_order(self.no_order_id)
                    self.log("INFO", "No 订单已取消")
            
            if no_status == "filled" and not self.no_filled:
                self.no_filled = True
                self.log("INFO", "No 订单已成交，正在取消 Yes 订单...")
                if self.yes_order_id:
                    await self.api.cancel_order(self.yes_order_id)
                    self.log("INFO", "Yes 订单已取消")
            
            # 检查是否都被取消
            if yes_status in ["cancelled", "canceled"]:
                self.yes_filled = True  # 视为已处理
            if no_status in ["cancelled", "canceled"]:
                self.no_filled = True  # 视为已处理
                
        except Exception as e:
            self.log("ERROR", f"检查订单状态失败: {e}")
    
    def get_current_period_info(self) -> Dict:
        """获取当前周期信息"""
        timestamp = datetime.now().timestamp()
        period = int(timestamp // 300)  # 5分钟周期
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
        """运行交易循环"""
        self.running = True
        self.log("INFO", "交易机器人已启动")
        
        # 初始化
        if not await self.initialize():
            self.running = False
            self.log("ERROR", "初始化失败，机器人停止")
            return
        
        while self.running:
            try:
                period_info = self.get_current_period_info()
                
                # 每个周期开始的第一分钟内下单
                if period_info["is_first_minute"] and not self.yes_order_id:
                    await self.place_orders()
                
                # 最后30秒检查并取消
                if period_info["is_last_30_seconds"]:
                    await self.check_and_cancel()
                
                # 如果周期结束，重置订单
                if period_info["seconds_until_end"] <= 0:
                    self.yes_order_id = None
                    self.no_order_id = None
                    self.yes_filled = False
                    self.no_filled = False
                
                await asyncio.sleep(1)  # 每秒检查一次
                
            except Exception as e:
                self.log("ERROR", f"交易循环错误: {e}")
                await asyncio.sleep(5)
        
        self.log("INFO", "交易机器人已停止")
    
    def stop(self):
        """停止交易"""
        self.running = False
        self.yes_order_id = None
        self.no_order_id = None
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            "running": self.running,
            "current_period": self.get_current_period_info(),
            "orders": {
                "yes_order_id": self.yes_order_id,
                "no_order_id": self.no_order_id,
                "yes_filled": self.yes_filled,
                "no_filled": self.no_filled
            },
            "market": self.market_info
        }
