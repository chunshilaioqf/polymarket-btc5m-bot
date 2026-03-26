# Polymarket BTC 5m Bot

> Bot de trading automatizado, especializado en el mercado BTC-updown-5m de Polymarket

## Características

- 🤖 **Trading Automatizado**: Coloca órdenes en el primer minuto de cada período de 5 minutos
- 📝 **Órdenes Limitadas**: Compra simultáneamente Yes y No, precio 10, cantidad 0,5
- 🔄 **Cancelación Inteligente**: Cancela automáticamente la otra orden si una se ejecuta en los últimos 30 segundos
- 🌐 **Interfaz Web**: Interfaz moderna y limpia con modo oscuro/claro
- 🌍 **Multi-idioma**: Inglés, Japonés, Chino, Coreano, Alemán, Francés, Español
- 💾 **Almacenamiento Local**: Toda la configuración se almacena en el localStorage del navegador

## Inicio Rápido

```bash
# Clonar el repositorio
git clone https://github.com/whitebigfox/polymarket-btc5m-bot.git
cd polymarket-btc5m-bot

# Inicializar entorno
chmod +x scripts/*.sh
./scripts/init.sh

# Iniciar el bot
./scripts/manage.sh start
```

Luego abrir http://localhost:8000

## Lógica de Trading

1. **Primer Minuto (0:00-1:00)**: Coloca órdenes limitadas para Yes y No
   - Precio: 10
   - Cantidad: 0,5 (cada uno)
2. **Últimos 30 Segundos (4:30-5:00)**: Verifica el estado de las órdenes
   - Si una orden se ejecuta → cancela la otra
3. **Repetir**: Cada 5 minutos

## Scripts

```bash
# Inicializar entorno
./scripts/init.sh

# Gestionar el bot
./scripts/manage.sh start    # Iniciar
./scripts/manage.sh stop     # Detener
./scripts/manage.sh restart  # Reiniciar
./scripts/manage.sh info     # Mostrar estado
```

## Stack Tecnológico

- **Backend**: Python 3 + FastAPI
- **Frontend**: HTML/CSS/JavaScript (vanilla)
- **WebSocket**: Actualizaciones de estado en tiempo real

## Seguridad

⚠️ **Solo uso local** — no se recomienda el despliegue  
⚠️ La clave privada se almacena solo en memoria (se pierde al reiniciar/detener)  
⚠️ Sin autenticación — usar solo en un entorno de confianza

## Licencia

MIT