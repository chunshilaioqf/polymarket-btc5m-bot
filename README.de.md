# Polymarket BTC 5m Bot

> Automatisierter Trading-Bot, spezialisiert auf den BTC-updown-5m-Markt von Polymarket

## Funktionen

- 🤖 **Automatisiertes Trading**: Platziert Orders in der ersten Minute jedes 5-Minuten-Intervalls
- 📝 **Limit-Orders**: Kauft gleichzeitig Yes und No, Preis 10, Menge 0,5
- 🔄 **Smart Cancellation**: Automatisches Abbrechen der anderen Order, wenn eine in den letzten 30 Sekunden ausgeführt wird
- 🌐 **Web UI**: Moderne, saubere Oberfläche mit Dark/Light-Modus
- 🌍 **Mehrsprachig**: Englisch, Japanisch, Chinesisch, Koreanisch, Deutsch, Französisch, Spanisch
- 💾 **Lokaler Speicher**: Alle Konfigurationen im Browser-localStorage

## Schnellstart

```bash
# Repository klonen
git clone https://github.com/whitebigfox/polymarket-btc5m-bot.git
cd polymarket-btc5m-bot

# Umgebung initialisieren
chmod +x scripts/*.sh
./scripts/init.sh

# Bot starten
./scripts/manage.sh start
```

Dann http://localhost:8000 öffnen

## Trading-Logik

1. **Erste Minute (0:00-1:00)**: Limit-Orders für Yes und No platzieren
   - Preis: 10
   - Menge: 0,5 (je)
2. **Letzte 30 Sekunden (4:30-5:00)**: Bestellstatus prüfen
   - Wenn eine Order ausgeführt → andere abbrechen
3. **Wiederholen**: Alle 5 Minuten

## Skripte

```bash
# Umgebung initialisieren
./scripts/init.sh

# Bot verwalten
./scripts/manage.sh start    # Starten
./scripts/manage.sh stop     # Stoppen
./scripts/manage.sh restart  # Neustarten
./scripts/manage.sh info     # Status anzeigen
```

## Technologie-Stack

- **Backend**: Python 3 + FastAPI
- **Frontend**: HTML/CSS/JavaScript (Vanilla)
- **WebSocket**: Echtzeit-Status-Updates

## Sicherheit

⚠️ **Nur lokale Nutzung** — Deploy nicht empfohlen  
⚠️ Privater Schlüssel nur im Speicher (verloren bei Neustart/Stop)  
⚠️ Keine Authentifizierung — nur in vertrauenswürdiger Umgebung verwenden

## Lizenz

MIT