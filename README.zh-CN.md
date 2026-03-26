# Polymarket BTC 5m Bot

> 专注于 Polymarket BTC-updown-5m 市场的自动化交易机器人

## 功能特性

- 🤖 **自动交易**: 在每个 5 分钟周期的第一分钟下单
- 📝 **限价单**: 同时买入 Yes 和 No，价格 10，数量 0.5
- 🔄 **智能取消**: 最后 30 秒内若一方成交，自动取消另一方
- 🌐 **Web UI**: 支持深色/浅色模式的现代简洁界面
- 🌍 **多语言**: 支持英语、日语、简体中文、韩语、德语、法语、西班牙语
- 💾 **本地存储**: 所有配置存储在浏览器 localStorage 中

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/whitebigfox/polymarket-btc5m-bot.git
cd polymarket-btc5m-bot

# 初始化环境
chmod +x scripts/*.sh
./scripts/init.sh

# 启动机器人
./scripts/manage.sh start
```

然后打开 http://localhost:8000

## 交易逻辑

1. **第一分钟 (0:00-1:00)**: 下达 Yes 和 No 的限价单
   - 价格: 10
   - 数量: 0.5（每个）
2. **最后 30 秒 (4:30-5:00)**: 检查订单状态
   - 如果一个订单成交 → 取消另一个订单
3. **重复**: 每 5 分钟执行一次

## 脚本命令

```bash
# 初始化环境
./scripts/init.sh

# 管理机器人
./scripts/manage.sh start    # 启动
./scripts/manage.sh stop     # 停止
./scripts/manage.sh restart  # 重启
./scripts/manage.sh info     # 查看状态
```

## 技术栈

- **后端**: Python 3 + FastAPI
- **前端**: HTML/CSS/JavaScript（原生）
- **WebSocket**: 实时状态更新

## 安全提示

⚠️ **仅供本地运行** — 不推荐部署到线上环境  
⚠️ 私钥仅存储在内存中（重启/停止后丢失）  
⚠️ 无权限鉴定 — 请仅在可信环境使用

## 许可证

MIT