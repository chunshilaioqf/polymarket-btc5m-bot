# Polymarket BTC 5m Bot

> 自动化交易机器人，专注于 Polymarket 的 BTC-updown-5m 市场

[English](./README.md) | [日本語](./README.ja.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko.md) | [Deutsch](./README.de.md) | [Français](./README.fr.md) | [Español](./README.es.md)

## Features

- 🤖 **Automated Trading**: Places orders at the first minute of each 5-minute period
- 📝 **Limit Orders**: Simultaneously buys Yes and No at price 10, quantity 0.5
- 🔄 **Smart Cancellation**: Auto-cancels the other order if one gets filled in the last 30 seconds
- 🌐 **Web UI**: Modern, clean interface with dark/light mode support
- 🌍 **Multi-language**: English, Japanese, Chinese, Korean, German, French, Spanish
- 💾 **Local Storage**: All config stored in browser localStorage

## Quick Start

```bash
# Clone the repository
git clone https://github.com/whitebigfox/polymarket-btc5m-bot.git
cd polymarket-btc5m-bot

# Initialize environment
chmod +x scripts/*.sh
./scripts/init.sh

# Start the bot
./scripts/manage.sh start
```

Then open http://localhost:8000

## Trading Logic

1. **First minute (0:00-1:00)**: Place limit orders for Yes and No
   - Price: 10
   - Quantity: 0.5 each
2. **Last 30 seconds (4:30-5:00)**: Check order status
   - If one order filled → cancel the other
3. **Repeat** for every 5-minute period

## Scripts

```bash
# Initialize environment
./scripts/init.sh

# Manage the bot
./scripts/manage.sh start    # Start
./scripts/manage.sh stop     # Stop
./scripts/manage.sh restart  # Restart
./scripts/manage.sh info     # Show status
```

## Tech Stack

- **Backend**: Python 3 + FastAPI
- **Frontend**: HTML/CSS/JavaScript (vanilla)
- **WebSocket**: Real-time status updates

## Security

⚠️ **Local use only** — not recommended for deployment  
⚠️ Private key stored in memory only (lost on restart/stop)  
⚠️ No authentication — use in trusted environment only

## License

MIT