# Polymarket BTC 5m Bot

> Polymarket의 BTC-updown-5m 시장에 특화된 자동 거래 봇

## 기능

- 🤖 **자동 거래**: 5분 간격의 첫 1분 이내에 주문 배치
- 📝 **지정가 주문**: Yes와 No를 동시에 매수, 가격 10, 수량 0.5
- 🔄 **스마트 취소**: 마지막 30초에서 하나가 체결되면 다른 주문 자동 취소
- 🌐 **Web UI**: 다크/라이트 모드를 지원하는 모던한 인터페이스
- 🌍 **다국어 지원**: 영어, 일본어, 중국어, 한국어, 독일어, 프랑스어, 스페인어
- 💾 **로컬 저장**: 모든 설정은 브라우저 localStorage에 저장

## 빠른 시작

```bash
# 저장소 클론
git clone https://github.com/whitebigfox/polymarket-btc5m-bot.git
cd polymarket-btc5m-bot

# 환경 초기화
chmod +x scripts/*.sh
./scripts/init.sh

# 봇 시작
./scripts/manage.sh start
```

http://localhost:8000 을 열어주세요

## 거래 로직

1. **첫 1분 (0:00-1:00)**: Yes와 No의 지정가 주문 배치
   - 가격: 10
   - 수량: 0.5 (각각)
2. **마지막 30초 (4:30-5:00)**: 주문 상태 확인
   - 하나가 체결되면 → 다른 주문 취소
3. **반복**: 5분마다

## 스크립트

```bash
# 환경 초기화
./scripts/init.sh

# 봇 관리
./scripts/manage.sh start    # 시작
./scripts/manage.sh stop     # 중지
./scripts/manage.sh restart  # 재시작
./scripts/manage.sh info     # 상태 표시
```

## 기술 스택

- **백엔드**: Python 3 + FastAPI
- **프론트엔드**: HTML/CSS/JavaScript (바닐라)
- **WebSocket**: 실시간 상태 업데이트

## 보안

⚠️ **로컬 사용 전용** — 배포 비추천  
⚠️ 비밀키는 메모리에만 저장 (재시작/중지 시 소멸)  
⚠️ 인증 없음 — 신뢰할 수 있는 환경에서만 사용

## 라이선스

MIT