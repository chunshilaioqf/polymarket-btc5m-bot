import httpx
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime


class PolymarketAPI:
    """Polymarket API 封装"""
    
    BASE_URL = "https://clob.polymarket.com"
    GRAPH_URL = "https://clob.polymarket.com/graphql"
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
        """从私钥派生地址"""
        try:
            from ecdsa import SigningKey, SECP256k1
            import hashlib
            
            if private_key.startswith('0x'):
                private_key = private_key[2:]
            
            priv_key_bytes = bytes.fromhex(private_key)
            sk = SigningKey.from_string(priv_key_bytes, curve=SECP256k1)
            vk = sk.get_verifying_key()
            pub_key_hash = hashlib.sha256(vk.to_string()).digest()
            address = pub_key_hash[-20:].hex()
            return "0x" + address
        except Exception as e:
            raise ValueError(f"私钥解析失败: {e}")

    async def _safe_request(self, method: str, url: str, **kwargs) -> Dict:
        """安全的 HTTP 请求，带错误处理"""
        try:
            if method == "GET":
                response = await self.client.get(url, **kwargs)
            elif method == "POST":
                response = await self.client.post(url, **kwargs)
            elif method == "DELETE":
                response = await self.client.delete(url, **kwargs)
            else:
                return {"error": f"不支持的方法: {method}"}
            
            content_type = response.headers.get("content-type", "")
            response_text = response.text[:500] if response.text else "(空响应)"
            
            if response.status_code == 200:
                if "application/json" in content_type or response.text.startswith(("[", "{")):
                    try:
                        return response.json()
                    except Exception as e:
                        return {"error": f"JSON 解析失败: {str(e)}", "raw": response_text}
                else:
                    return {"error": f"非 JSON 响应 (Content-Type: {content_type})", "raw": response_text}
            else:
                return {"error": f"HTTP {response.status_code}", "detail": response_text}
        except httpx.TimeoutException:
            return {"error": "请求超时"}
        except httpx.ConnectError as e:
            return {"error": f"连接失败: {str(e)}"}
        except Exception as e:
            return {"error": f"请求异常: {type(e).__name__}: {str(e)}"}

    async def get_balance(self) -> Dict:
        """获取用户余额"""
        url = f"{self.GAMMA_URL}/positions?user={self.address}"
        result = await self._safe_request("GET", url)
        if isinstance(result, list):
            total_value = 0
            for pos in result:
                total_value += float(pos.get("currentValue", 0))
            return {"balance_usdc": total_value, "positions": result}
        return result

    async def get_positions(self) -> List[Dict]:
        """获取用户持仓"""
        url = f"{self.GAMMA_URL}/positions?user={self.address}"
        result = await self._safe_request("GET", url)
        if isinstance(result, list):
            return result
        return []

    async def get_trade_history(self, limit: int = 50) -> List[Dict]:
        """获取交易历史"""
        url = f"{self.BASE_URL}/fills?address={self.address}&limit={limit}"
        result = await self._safe_request("GET", url)
        if isinstance(result, list):
            return result
        return []

    async def get_market_by_slug(self, slug: str) -> Optional[Dict]:
        """通过 slug 获取市场信息"""
        url = f"{self.GAMMA_URL}/markets?slug={slug}"
        result = await self._safe_request("GET", url)
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        return None

    async def get_market_by_condition(self, condition_id: str) -> Optional[Dict]:
        """通过 condition_id 获取市场信息"""
        url = f"{self.GAMMA_URL}/markets?conditionId={condition_id}"
        result = await self._safe_request("GET", url)
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        return None

    async def get_order_book(self, token_id: str) -> Dict:
        """获取订单簿"""
        url = f"{self.BASE_URL}/orderbook/{token_id}"
        return await self._safe_request("GET", url)

    async def place_order(self, token_id: str, side: str, price: float, size: float) -> Dict:
        """下单"""
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
        """取消订单"""
        url = f"{self.BASE_URL}/orders/{order_id}"
        return await self._safe_request("DELETE", url)

    async def get_orders(self) -> List[Dict]:
        """获取当前订单"""
        url = f"{self.BASE_URL}/orders?address={self.address}"
        result = await self._safe_request("GET", url)
        if isinstance(result, list):
            return result
        return []

    async def get_fills(self) -> List[Dict]:
        """获取成交记录"""
        url = f"{self.BASE_URL}/fills?address={self.address}"
        result = await self._safe_request("GET", url)
        if isinstance(result, list):
            return result
        return []

    async def close(self):
        """关闭连接"""
        await self.client.aclose()


class BTC5mTrader:
    """BTC 5分钟交易机器人"""
    
    # Polymarket BTC-updown-5m 的市场 slug
    MARKET_SLUG = "btc-updown-5m"
    
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
        self.balance: Dict = {}
        self.positions: List[Dict] = []
        self.trade_history: List[Dict] = []
    
    def log(self, level: str, message: str):
        """记录日志"""
        timestamp = datetime.now().isoformat()
        self.logs.append({
            "timestamp": timestamp,
            "level": level,
            "message": message
        })
        if len(self.logs) > 1000:
            self.logs = self.logs[-1000:]
    
    async def initialize(self):
        """初始化，获取市场信息"""
        try:
            self.log("INFO", f"正在连接 Polymarket API...")
            self.log("INFO", f"钱包地址: {self.api.address}")
            
            # 测试连接
            test_url = f"{self.api.GAMMA_URL}/markets?limit=1"
            self.log("INFO", f"测试连接: {test_url}")
            test_result = await self.api._safe_request("GET", test_url)
            
            if "error" in test_result:
                self.log("ERROR", f"API 连接失败: {test_result['error']}")
                if "raw" in test_result:
                    self.log("ERROR", f"响应内容: {test_result['raw'][:100]}")
                return False
            
            self.log("INFO", "API 连接成功，正在获取市场信息...")
            
            # 通过 slug 获取市场
            market_url = f"{self.api.GAMMA_URL}/markets?slug={self.MARKET_SLUG}"
            self.log("INFO", f"查询市场: {market_url}")
            market_result = await self.api._safe_request("GET", market_url)
            
            market = None
            if "error" not in market_result and isinstance(market_result, list) and len(market_result) > 0:
                market = market_result[0]
                self.log("INFO", f"通过 slug 找到市场")
            else:
                if "error" in market_result:
                    self.log("WARNING", f"slug 查询失败: {market_result['error']}")
                
                # 使用第一个可用市场
                self.log("INFO", "使用第一个可用市场...")
                list_result = await self.api._safe_request("GET", f"{self.api.GAMMA_URL}/markets?limit=1")
                if "error" not in list_result and isinstance(list_result, list) and len(list_result) > 0:
                    market = list_result[0]
                    self.log("INFO", f"使用市场: {market.get('question', 'Unknown')[:50]}")
            
            if not market:
                self.log("ERROR", "无法获取市场信息")
                return False
            
            self.market_info = market
            
            # 获取 token 信息
            clob_token_ids = market.get("clobTokenIds")
            if clob_token_ids:
                import json
                try:
                    tokens = json.loads(clob_token_ids) if isinstance(clob_token_ids, str) else clob_token_ids
                    if isinstance(tokens, list) and len(tokens) >= 2:
                        self.token_ids["yes"] = tokens[0]
                        self.token_ids["no"] = tokens[1]
                except Exception as e:
                    self.log("WARNING", f"解析 clobTokenIds 失败: {e}")
            
            # 从 tokens 字段获取
            if not self.token_ids:
                tokens = market.get("tokens", [])
                for token in tokens if isinstance(tokens, list) else []:
                    outcome = str(token.get("outcome", "")).upper()
                    token_id = token.get("tokenId", token.get("id", ""))
                    if outcome == "YES" and token_id:
                        self.token_ids["yes"] = token_id
                    elif outcome == "NO" and token_id:
                        self.token_ids["no"] = token_id
            
            self.log("INFO", f"市场: {market.get('question', 'Unknown')[:60]}")
            self.log("INFO", f"Yes Token: {self.token_ids.get('yes', '未找到')[:20]}...")
            self.log("INFO", f"No Token: {self.token_ids.get('no', '未找到')[:20]}...")
            
            await self.update_account_info()
            
            return True
        except Exception as e:
            self.log("ERROR", f"初始化异常: {type(e).__name__}: {e}")
            return False

    async def update_account_info(self):
        """更新账户信息"""
        try:
            # 获取余额
            balance_result = await self.api.get_balance()
            self.balance = balance_result
            
            # 获取持仓
            self.positions = await self.api.get_positions()
            
            # 获取交易历史
            self.trade_history = await self.api.get_trade_history(20)
            
        except Exception as e:
            self.log("WARNING", f"更新账户信息失败: {e}")
    
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
                if "error" in result:
                    self.log("ERROR", f"Yes 下单失败: {result['error']}")
                else:
                    self.yes_order_id = result.get("orderID") or result.get("id")
                    self.log("INFO", f"Yes 订单已创建: {self.yes_order_id}")
            except Exception as e:
                self.log("ERROR", f"Yes 下单异常: {e}")
            
            # 下单 No
            try:
                result = await self.api.place_order(
                    self.token_ids["no"],
                    "Buy",
                    price,
                    size
                )
                if "error" in result:
                    self.log("ERROR", f"No 下单失败: {result['error']}")
                else:
                    self.no_order_id = result.get("orderID") or result.get("id")
                    self.log("INFO", f"No 订单已创建: {self.no_order_id}")
            except Exception as e:
                self.log("ERROR", f"No 下单异常: {e}")
            
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
            
            if yes_status == "filled" and not self.yes_filled:
                self.yes_filled = True
                self.log("INFO", "Yes 订单已成交，正在取消 No 订单...")
                if self.no_order_id:
                    result = await self.api.cancel_order(self.no_order_id)
                    if "error" not in result:
                        self.log("INFO", "No 订单已取消")
                    else:
                        self.log("ERROR", f"取消 No 订单失败: {result['error']}")
            
            if no_status == "filled" and not self.no_filled:
                self.no_filled = True
                self.log("INFO", "No 订单已成交，正在取消 Yes 订单...")
                if self.yes_order_id:
                    result = await self.api.cancel_order(self.yes_order_id)
                    if "error" not in result:
                        self.log("INFO", "Yes 订单已取消")
                    else:
                        self.log("ERROR", f"取消 Yes 订单失败: {result['error']}")
            
            if yes_status in ["cancelled", "canceled"]:
                self.yes_filled = True
            if no_status in ["cancelled", "canceled"]:
                self.no_filled = True
                
        except Exception as e:
            self.log("ERROR", f"检查订单状态失败: {e}")
    
    def get_current_period_info(self) -> Dict:
        """获取当前周期信息"""
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
                period_info = self.get_current_period_info()
                
                if period_info["is_first_minute"] and not self.yes_order_id:
                    await self.place_orders()
                
                if period_info["is_last_30_seconds"]:
                    await self.check_and_cancel()
                
                # 每 30 秒更新一次账户信息
                if period_info["seconds_until_end"] % 30 == 0:
                    await self.update_account_info()
                
                if period_info["seconds_until_end"] <= 0:
                    self.yes_order_id = None
                    self.no_order_id = None
                    self.yes_filled = False
                    self.no_filled = False
                
                await asyncio.sleep(1)
                
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
            "market": self.market_info,
            "balance": self.balance,
            "positions": self.positions,
            "trade_history": self.trade_history,
            "address": self.api.address
        }
