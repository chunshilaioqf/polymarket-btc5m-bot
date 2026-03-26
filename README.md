# Polymarket BTC 5m Bot

自动化交易机器人，专门用于 Polymarket 上的 BTC-updown-5m 市场。

## 功能特性

- 🤖 **自动交易**: 在每个 5 分钟周期的第一分钟下单
- 📝 **限价单**: 同时买入 Yes 和 No，价格 10，数量 0.5
- 🔄 **智能取消**: 最后 30 秒内若一方成交，自动取消另一方
- 🌐 **Web UI**: 现代简洁界面，支持深色/浅色模式
- 🌍 **多语言**: 支持英语、日语、简体中文、韩语、德语、法语、西班牙语
- 💾 **本地存储**: 所有配置存储在浏览器 localStorage 中

## 运行要求

- Python 3.8+
- 现代浏览器

## 安装

```bash
cd backend
pip install -r requirements.txt
```

## 启动

```bash
cd backend
python main.py
# 或者使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

然后打开浏览器访问: http://localhost:8000

## 使用说明

1. 在界面中输入你的 Polymarket 私钥
2. 点击"开始交易"按钮
3. 机器人会自动在每个 5 分钟周期的第一分钟下单
4. 在最后 30 秒检查订单状态，若一方成交则取消另一方
5. 点击"停止交易"可以停止机器人，私钥会从内存中清除

## 配置

所有配置存储在浏览器本地：
- 主题模式 (跟随系统/浅色/深色)
- 语言选择
- 私钥 (可选保存)

## 安全注意事项

⚠️ 本项目仅供本地运行，不推荐部署到线上环境
⚠️ 私钥仅存储在内存中，停止交易或重启后丢失
⚠️ 无权限鉴定，请仅在可信环境使用

## 项目结构

```
polymarket-btc5m-bot/
├── SPEC.md              # 项目规格文档
├── backend/
│   ├── main.py          # FastAPI 主程序
│   ├── trader.py        # 交易逻辑
│   └── requirements.txt # Python 依赖
└── frontend/
    ├── index.html       # 主页面
    ├── css/style.css    # 样式
    └── js/
        ├── i18n.js      # 多语言
        ├── ws.js        # WebSocket
        └── app.js       # 应用逻辑
```

## License

MIT