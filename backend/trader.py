import httpx
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
import json


class PolymarketAPI:
    """Polymarket API 封装"""
    
    BASE_URL = "https://clob.polymarket.com"
    GAMMA_URL = "https://gamma-api.polymarket.com"
    
    def __init__(self, private_key: str):
        self.private_key = private_key
        self.address = self._derive_address(private_key)
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": "Polymarket-Bot/1.0",
                "Accept": "application/json"
            },
            follow_redirects=True
        )
    
    def _derive_address(self, private_key: str) -> str:
        try:
            from ecdsa import SigningKey, SECP256k1
            import hashlib
            if private_key.startswith('0x'):
                private_key = private_key[2:]
            priv_key_bytes = bytes.fromhex(private_key)
            sk = SigningKey.from_string(priv_key_bytes, curve=SECP256k1)
            vk = sk.get_verifying_key()
            pub_key_hash = hashlib.sha256(vk.to_string()).digest()
            return "0x" + pub_key_hash[-20:].hex()
        except Exception as e:
            raise ValueError(f"私钥解析失败: {e}")

    async def _safe_request(self, method: str, url: str, **kwargs) -> Dict:
        try:
            if method == "GET":
                response = await self.client.get(url, **kwargs)
            elif method == "POST":
                response = await self.client.post(url, **kwargs)
            elif method == "DELETE":
                response = await self.client.delete(url, **kwargs)
            else:
                return {"error": f"不支持的方法: {method}"}
            
            status_code = response.status_code
            content_type = response.headers.get("content-type", "")
            response_text = response.text
            response_len = len(response_text) if response_text else 0
            
            if status_code == 200:
                if "application/json" in content_type or (response_text and response_text.strip().startswith(("[", "{"))):
                    try:
                        return response.json()
                    except Exception as e:
                        return {"error": f"JSON 解析失败: {str(e)}", "content_type": content_type, "response_len": response_len, "raw": response_text[:300]}
                else:
                    return {"error": f"非 JSON 响应", "content_type": content_type, "response_len": response_len, "raw": response_text[:300]}
            else:
                return {"error": f"HTTP {status_code}", "url": url, "content_type": content_type, "response_len": response_len, "raw": response_text[:300]}
        except httpx.TimeoutException:
            return {"error": "请求超时", "url": url}
        except httpx.ConnectError as e:
            return {"error": f"连接失败: {str(e)}", "url": url}
        except Exception as e:
            return {"error": f"请求异常: {type(e).__name__}: {str(e)}", "url": url}

    async def find_active_btc_updown_market(self) -> Optional[Dict]:
        """搜索当前活跃的 BTC-updown-5m 市场"""
        import time
        
        # 方法1: 通过时间戳计算当前事件的 slug 并从网页获取 condition_id
        # BTC-updown-5m 使用5分钟对齐的时间戳
        now = int(time.time())
        aligned = (now // 300) * 300
        
        # 尝试当前和前后的几个时间窗口
        for offset in [0, -1, 1, -2, 2]:
            ts = aligned + offset * 300
            try:
                # 直接从 Polymarket 网页获取 condition_id
                page_url = f"https://polymarket.com/event/btc-updown-5m-{ts}"
                response = await self.client.get(page_url)
                
                if response.status_code == 200:
                    import re
                    html = response.text
                    
                    # 从页面中提取 condition_id
                    match = re.search(r'"condition_id"\s*:\s*"([^"]+)"', html)
                    if not match:
                        match = re.search(r'"conditionId"\s*:\s*"([^"]+)"', html)
                    
                    if match:
                        condition_id = match.group(1)
                        
                        # 用 condition_id 查询 CLOB API 获取市场详情
                        market_url = f"{self.BASE_URL}/markets/{condition_id}"
                        market = await self._safe_request("GET", market_url)
                        
                        if "error" not in market:
                            active = market.get("active", False)
                            closed = market.get("closed", True)
                            question = market.get("question", "")
                            
                            if active and not closed and ("bitcoin" in question.lower() or "btc" in question.lower()):
                                return market
            except Exception:
                continue
        
        # 方法2: 遍历 CLOB API 的市场列表
        cursor = None
        for _ in range(3):
            params = {}
            if cursor:
                params["next_cursor"] = cursor
            
            result = await self._safe_request("GET", f"{self.BASE_URL}/markets", params=params)
            
            if "error" in result:
                break
            
            markets = result.get("data", []) if isinstance(result, dict) else []
            
            for market in markets:
                question = market.get("question", "").lower()
                active = market.get("active", False)
                closed = market.get("closed", True)
                
                if ("bitcoin" in question or "btc" in question) and ("up or down" in question or "updown" in question):
                    if active and not closed:
                        return market
            
            cursor = result.get("next_cursor")
            if not cursor or cursor == "LTE=":
                break
        
        return None

    async def get_balance(self) -> Dict:
        url = f"{self.GAMMA_URL}/positions?user={self.address}"
        result = await self._safe_request("GET", url)
        if isinstance(result, list):
            total_value = 0
            for pos in result:
                total_value += float(pos.get("currentValue", 0))
            return {"balance_usdc": total_value, "positions": result}
        return result

    async def get_positions(self) -> List[Dict]:
        url = f"{self.GAMMA_URL}/positions?user={self.address}"
        result = await self._safe_request("GET", url)
        return result if isinstance(result, list) else []

    async def get_trade_history(self, limit: int = 50) -> List[Dict]:
        url = f"{self.BASE_URL}/fills?address={self.address}&limit={limit}"
        result = await self._safe_request("GET", url)
        return result if isinstance(result, list) else []

    async def get_order_book(self, token_id: str) -> Dict:
        url = f"{self.BASE_URL}/orderbook/{token_id}"
        return await self._safe_request("GET", url)

    async def place_order(self, token_id: str, side: str, price: float, size: float) -> Dict:
        order_data = {
            "token_id": token_id,
            "side": side,
            "price": price,
            "size": size,
            "address": self.address,
        }
        url = f"{self.BASE_URL}/orders"
        return await self._safe_request("POST", url, json=order_data)

    async def cancel_order(self, order_id: str) -> Dict:
        url = f"{self.BASE_URL}/orders/{order_id}"
        return await self._safe_request("DELETE", url)

    async def get_orders(self) -> List[Dict]:
        url = f"{self.BASE_URL}/orders?address={self.address}"
        result = await self._safe_request("GET", url)
        return result if isinstance(result, list) else []

    async def get_fills(self) -> List[Dict]:
        url = f"{self.BASE_URL}/fills?address={self.address}"
        result = await self._safe_request("GET", url)
        return result if isinstance(result, list) else []

    async def close(self):
        await self.client.aclose()


class BTC5mTrader:
    """BTC 5分钟交易机器人"""
    
    def __init__(self, api: PolymarketAPI):
        self.api = api
        self.running = False
        self.current_period = 0
        self.up_order_id: Optional[str] = None
        self.down_order_id: Optional[str] = None
        self.up_filled = False
        self.down_filled = False
        self.logs: List[Dict] = []
        self.market_info: Optional[Dict] = None
        self.token_ids: Dict[str, str] = {}
        self.balance: Dict = {}
        self.positions: List[Dict] = []
        self.trade_history: List[Dict] = []
        self.last_market_search = 0  # 上次搜索市场的时间
    
    def log(self, level: str, message: str):
        timestamp = datetime.now().isoformat()
        self.logs.append({"timestamp": timestamp, "level": level, "message": message})
        if len(self.logs) > 1000:
            self.logs = self.logs[-1000:]
    
    async def initialize(self):
        """初始化，获取市场信息"""
        try:
            self.log("INFO", f"正在连接 Polymarket API...")
            self.log("INFO", f"钱包地址: {self.api.address}")
            
            # 测试连接
            test_url = f"{self.api.GAMMA_URL}/markets?limit=1"
            test_result = await self.api._safe_request("GET", test_url)
            
            if "error" in test_result:
                self.log("ERROR", f"API 连接失败: {test_result.get('error')}")
                return False
            
            self.log("INFO", "API 连接成功，正在搜索活跃的 BTC-updown-5m 市场...")
            
            return await self.refresh_market()
        except Exception as e:
            self.log("ERROR", f"初始化异常: {type(e).__name__}: {e}")
            return False

    async def refresh_market(self) -> bool:
        """刷新市场信息，找到最新的活跃市场"""
        try:
            market = await self.api.find_active_btc_updown_market()
            
            if not market:
                self.log("WARNING", "未找到活跃的 BTC-updown-5m 市场（可能当前时段没有开盘）")
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
                    if outcome == "up" and token_id:
                        self.token_ids["up"] = token_id
                    elif outcome == "down" and token_id:
                        self.token_ids["down"] = token_id
                
                if not self.token_ids.get("up") or not self.token_ids.get("down"):
                    self.log("WARNING", f"token 信息不完整: {self.token_ids}")
                    return False
                
                self.log("INFO", f"Up Token: {self.token_ids['up'][:30]}...")
                self.log("INFO", f"Down Token: {self.token_ids['down'][:30]}...")
                
                # 重置订单状态
                self.up_order_id = None
                self.down_order_id = None
                self.up_filled = False
                self.down_filled = False
                
                await self.update_account_info()
                return True
            else:
                self.log("INFO", f"市场未变化: {market.get('question', '')[:40]}")
                return True
                
        except Exception as e:
            self.log("ERROR", f"刷新市场失败: {type(e).__name__}: {e}")
            return False

    async def update_account_info(self):
        try:
            self.balance = await self.api.get_balance()
            self.positions = await self.api.get_positions()
            self.trade_history = await self.api.get_trade_history(20)
        except Exception as e:
            self.log("WARNING", f"更新账户信息失败: {e}")
    
    async def place_orders(self):
        """在周期开始时下单"""
        if not self.token_ids.get("up") or not self.token_ids.get("down"):
            self.log("ERROR", "无法下单：token 信息缺失")
            return
        
        try:
            price = 10
            size = 0.5
            
            self.log("INFO", f"开始下单 - 价格: {price}, 数量: {size}")
            self.log("INFO", f"市场: {self.market_info.get('question', 'N/A')[:50]}")
            
            # 下单 Up
            result = await self.api.place_order(self.token_ids["up"], "Buy", price, size)
            if "error" in result:
                self.log("ERROR", f"Up 下单失败: {result['error']}")
                if "raw" in result:
                    self.log("ERROR", f"Up 响应: {result['raw'][:200]}")
            else:
                self.up_order_id = result.get("orderID") or result.get("id")
                self.log("INFO", f"Up 订单已创建: {self.up_order_id}")
            
            # 下单 Down
            result = await self.api.place_order(self.token_ids["down"], "Buy", price, size)
            if "error" in result:
                self.log("ERROR", f"Down 下单失败: {result['error']}")
                if "raw" in result:
                    self.log("ERROR", f"Down 响应: {result['raw'][:200]}")
            else:
                self.down_order_id = result.get("orderID") or result.get("id")
                self.log("INFO", f"Down 订单已创建: {self.down_order_id}")
            
            self.up_filled = False
            self.down_filled = False
            
        except Exception as e:
            self.log("ERROR", f"下单异常: {type(e).__name__}: {e}")
    
    async def check_and_cancel(self):
        """检查订单状态并在需要时取消"""
        try:
            orders = await self.api.get_orders()
            
            if not orders:
                self.log("INFO", "当前没有挂单")
                return
            
            up_status = "unknown"
            down_status = "unknown"
            
            for order in orders:
                oid = order.get("orderID") or order.get("id")
                status = order.get("status", "unknown")
                
                if oid == self.up_order_id:
                    up_status = status
                elif oid == self.down_order_id:
                    down_status = status
            
            self.log("INFO", f"订单状态 - Up: {up_status}, Down: {down_status}")
            
            if up_status == "filled" and not self.up_filled:
                self.up_filled = True
                self.log("INFO", "Up 订单已成交，正在取消 Down 订单...")
                if self.down_order_id:
                    result = await self.api.cancel_order(self.down_order_id)
                    self.log("INFO" if "error" not in result else "ERROR", 
                             "Down 订单已取消" if "error" not in result else f"取消失败: {result['error']}")
            
            if down_status == "filled" and not self.down_filled:
                self.down_filled = True
                self.log("INFO", "Down 订单已成交，正在取消 Up 订单...")
                if self.up_order_id:
                    result = await self.api.cancel_order(self.up_order_id)
                    self.log("INFO" if "error" not in result else "ERROR",
                             "Up 订单已取消" if "error" not in result else f"取消失败: {result['error']}")
            
            if up_status in ["cancelled", "canceled"]:
                self.up_filled = True
            if down_status in ["cancelled", "canceled"]:
                self.down_filled = True
                
        except Exception as e:
            self.log("ERROR", f"检查订单状态失败: {e}")
    
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
        """运行交易循环"""
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
                
                # 每5分钟搜索一次新市场
                if now - self.last_market_search > 300:
                    self.last_market_search = now
                    await self.refresh_market()
                
                # 在第一分钟下单（仅当有活跃市场时）
                if period_info["is_first_minute"] and not self.up_order_id and self.token_ids:
                    await self.place_orders()
                
                # 在最后30秒检查并取消
                if period_info["is_last_30_seconds"]:
                    await self.check_and_cancel()
                
                # 每30秒更新账户信息
                if period_info["seconds_until_end"] % 30 == 0:
                    await self.update_account_info()
                
                # 周期结束时重置订单
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
