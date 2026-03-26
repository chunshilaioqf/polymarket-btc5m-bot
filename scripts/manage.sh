#!/bin/bash
# Polymarket BTC 5m Bot - Management Script
# Usage: ./manage.sh {start|stop|restart|info}

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
PROJECT_NAME="polymarket-btc5m-bot"
PID_FILE="$PROJECT_DIR/.bot.pid"
LOG_FILE="$PROJECT_DIR/bot.log"
CONDA_ENV_FILE="$PROJECT_DIR/.conda_env"

# Setup conda activation command
CONDA_ACTIVATE=""
if [ -f "$CONDA_ENV_FILE" ]; then
    ENV_NAME=$(cat "$CONDA_ENV_FILE")
    if command -v conda &> /dev/null; then
        CONDA_BASE=$(conda info --base)
        source "$CONDA_BASE/etc/profile.d/conda.sh"
        CONDA_ACTIVATE="conda activate $ENV_NAME && "
    fi
fi

start() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "Bot is already running (PID: $PID)"
            exit 1
        else
            rm -f "$PID_FILE"
        fi
    fi

    echo "Starting Polymarket BTC 5m Bot..."
    cd "$BACKEND_DIR"
    
    if [ -n "$CONDA_ACTIVATE" ]; then
        # Use conda environment
        eval "$CONDA_ACTIVATE" && nohup uvicorn main:app --host 0.0.0.0 --port 8000 > "$LOG_FILE" 2>&1 &
    else
        # Use system Python
        nohup uvicorn main:app --host 0.0.0.0 --port 8000 > "$LOG_FILE" 2>&1 &
    fi
    
    echo $! > "$PID_FILE"
    sleep 2

    if ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
        echo "✓ Bot started successfully"
        echo "  PID: $(cat "$PID_FILE")"
        echo "  URL: http://localhost:8000"
        echo "  Log: $LOG_FILE"
        if [ -f "$CONDA_ENV_FILE" ]; then
            echo "  Env: $(cat "$CONDA_ENV_FILE") (conda)"
        fi
    else
        echo "✗ Failed to start bot. Check log: $LOG_FILE"
        cat "$LOG_FILE"
        rm -f "$PID_FILE"
        exit 1
    fi
}

stop() {
    if [ ! -f "$PID_FILE" ]; then
        echo "Bot is not running (no PID file)"
        return 0
    fi

    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Stopping bot (PID: $PID)..."
        kill "$PID" 2>/dev/null || true
        sleep 1

        if ps -p "$PID" > /dev/null 2>&1; then
            echo "Force killing..."
            kill -9 "$PID" 2>/dev/null || true
        fi

        rm -f "$PID_FILE"
        echo "✓ Bot stopped"
    else
        echo "Bot process not found (stale PID file)"
        rm -f "$PID_FILE"
    fi
}

info() {
    echo "=== Polymarket BTC 5m Bot Status ==="
    echo ""

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "Status: Running ✓"
            echo "PID: $PID"
            echo "URL: http://localhost:8000"
            echo "Log: $LOG_FILE"
        else
            echo "Status: Stopped ✗ (stale PID file)"
        fi
    else
        echo "Status: Stopped ✗"
    fi

    echo ""
    echo "Project: $PROJECT_DIR"
    echo "Backend: $BACKEND_DIR"
    
    if [ -f "$CONDA_ENV_FILE" ]; then
        echo "Environment: $(cat "$CONDA_ENV_FILE") (conda)"
    else
        echo "Environment: System Python"
    fi

    if [ -f "$LOG_FILE" ]; then
        echo ""
        echo "Last 10 log lines:"
        echo "---"
        tail -10 "$LOG_FILE"
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        echo "Restarting bot..."
        stop
        sleep 1
        start
        ;;
    info)
        info
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|info}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the bot in background"
        echo "  stop    - Stop the bot"
        echo "  restart - Restart the bot"
        echo "  info    - Show current status"
        exit 1
        ;;
esac