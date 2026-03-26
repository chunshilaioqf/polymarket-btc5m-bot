# Polymarket BTC 5m Bot

> Polymarket の BTC-updown-5m 市場に特化した自動取引ボット

## 特徴

- 🤖 **自動取引**: 5分間隔の最初の1分間に注文を発注
- 📝 **指値注文**: Yes と No を同時に購入、価格 10、数量 0.5
- 🔄 **スマートキャンセル**: 最後の30秒で片方が約定したら、もう片方を自動キャンセル
- 🌐 **Web UI**: ダーク/ライトモード対応のモダンでクリーンなインターフェース
- 🌍 **多言語対応**: 英語、日本語、中国語、韓国語、ドイツ語、フランス語、スペイン語
- 💾 **ローカルストレージ**: すべての設定はブラウザの localStorage に保存

## クイックスタート

```bash
# リポジトリのクローン
git clone https://github.com/whitebigfox/polymarket-btc5m-bot.git
cd polymarket-btc5m-bot

# 環境の初期化
chmod +x scripts/*.sh
./scripts/init.sh

# ボットの起動
./scripts/manage.sh start
```

http://localhost:8000 を開いてください

## 取引ロジック

1. **最初の1分間 (0:00-1:00)**: Yes と No の指値注文を発注
   - 価格: 10
   - 数量: 0.5（各）
2. **最後の30秒 (4:30-5:00)**: 注文ステータスを確認
   - 片方が約定したら → もう片方をキャンセル
3. **繰り返し**: 5分ごとに

## スクリプト

```bash
# 環境の初期化
./scripts/init.sh

# ボットの管理
./scripts/manage.sh start    # 起動
./scripts/manage.sh stop     # 停止
./scripts/manage.sh restart  # 再起動
./scripts/manage.sh info     # ステータス表示
```

## 技術スタック

- **バックエンド**: Python 3 + FastAPI
- **フロントエンド**: HTML/CSS/JavaScript（バニラ）
- **WebSocket**: リアルタイムステータス更新

## セキュリティ

⚠️ **ローカルでのみ使用** — 本番環境へのデプロイは推奨しません  
⚠️ 秘密鍵はメモリ内のみに保存（再起動/停止で消失）  
⚠️ 認証なし — 信頼できる環境でのみ使用してください

## ライセンス

MIT