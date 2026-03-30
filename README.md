# Polymarket BTC 5m Bot

> 自动化交易机器人，专注于 Polymarket 的 BTC-updown-5m 市场

[English](./README.md) | [日本語](./README.ja.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko.md) | [Deutsch](./README.de.md) | [Français](./README.fr.md) | [Español](./README.es.md)

## Features

- 🤖 **Automated Trading**: Places orders at the first minute of each 5-minute period
- 📝 **Limit Orders**: Simultaneously buys Up and Down at price 0.10, quantity 0.5
- 🔄 **Smart Cancellation**: Auto-cancels the other order if one gets filled in the last 30 seconds
- 🌐 **Web UI**: Modern sidebar layout with dark/light mode support
- 🌍 **Multi-language**: English, Japanese, Chinese, Korean, German, French, Spanish
- 💾 **Local Storage**: All config stored in browser localStorage
- 🔐 **Proxy Support**: Bypass region restrictions with HTTP proxy
- 💰 **Account Info**: Real-time balance, positions, and trade history

## Quick Start

```bash
# Clone the repository
git clone https://github.com/chunshilaioqf/polymarket-btc5m-bot.git
cd polymarket-btc5m-bot

# Initialize environment (supports conda)
chmod +x scripts/*.sh
./scripts/init.sh

# Start the bot
./scripts/manage.sh start
```

Then open http://localhost:8000

## Configuration

### Required
- **Private Key**: Your Polymarket wallet private key (stored in memory only)

### Optional
- **Proxy**: HTTP proxy address (e.g., `http://127.0.0.1:7890`) to bypass region restrictions
- **Wallet Type**:
  - `GNOSIS_SAFE` (default): Most Polymarket web users
  - `EOA`: MetaMask wallets
  - `POLY_PROXY`: Magic Link users
- **Funder Address**: Polymarket proxy wallet address (for GNOSIS_SAFE/POLY_PROXY users)

### How to get Funder Address
1. Login to https://polymarket.com/settings
2. Find your wallet address (Polymarket proxy wallet, not MetaMask address)

## Trading Logic

1. **First minute (0:00-1:00)**: Place limit orders for Up and Down
   - Price: 0.10 (10%)
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

- **Backend**: Python 3 + FastAPI + py-clob-client (official SDK)
- **Frontend**: HTML/CSS/JavaScript (vanilla)
- **WebSocket**: Real-time status updates

## UI Features

- 🌙 Dark/Light mode (follows system)
- 📊 Real-time market data
- 💼 Balance and positions display
- 📜 Trade history
- 📝 Live logs with timestamps

## Security

⚠️ **Local use only** — not recommended for deployment  
⚠️ Private key stored in memory only (lost on restart/stop)  
⚠️ No authentication — use in trusted environment only  
⚠️ Use VPN/proxy in supported regions

## Troubleshooting

### "invalid signature" error
- Try different wallet types (GNOSIS_SAFE / EOA / POLY_PROXY)
- Check if funder address is correct

### "Trading restricted in your region" error
- Configure HTTP proxy in the UI
- Use VPN to connect to supported region

### ModuleNotFoundError
```bash
./scripts/init.sh
```

## License

MIT