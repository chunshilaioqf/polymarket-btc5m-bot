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
PORT=8000

# Setup conda activation command
CONDA_ACTIVATE=""
ENV_NAME=""
if [ -f "$CONDA_ENV_FILE" ]; then
    ENV_NAME=$(cat "$CONDA_ENV_FILE")
    if command -v conda &> /dev/null; then
        CONDA_BASE=$(conda info --base)
        source "$CONDA_BASE/etc/profile.d/conda.sh"
        CONDA_ACTIVATE="conda activate $ENV_NAME"
    fi
fi

# Check if bot is running (match by full command including port)
is_running() {
    pgrep -f "uvicorn main:app --host 0.0.0.0 --port ${PORT}" > /dev/null 2>&1
}

# Get bot PID
get_pid() {
    pgrep -f "uvicorn main:app --host 0.0.0.0 --port ${PORT}" | head -1
}

# Kill uvicorn processes for this project
kill_uvicorn() {
    pkill -f "uvicorn main:app --host 0.0.0.0 --port ${PORT}" 2>/dev/null || true
    sleep 1
    pkill -9 -f "uvicorn main:app --host 0.0.0.0 --port ${PORT}" 2>/dev/null || true
    sleep 1
}

start() {
    # Check if already running
    if is_running; then
        echo "Bot is already running (PID: $(get_pid))"
        exit 1
    fi

    echo "Starting Polymarket BTC 5m Bot..."
    cd "$BACKEND_DIR"
    
    if [ -n "$CONDA_ACTIVATE" ] && [ -f "$CONDA_ENV_FILE" ]; then
        ENV_NAME=$(cat "$CONDA_ENV_FILE")
        CONDA_BASE=$(conda info --base 2>/dev/null || echo "$HOME/anaconda3")
        CONDA_SH="$CONDA_BASE/etc/profile.d/conda.sh"
        
        if [ -f "$CONDA_SH" ]; then
            nohup bash -c "source '$CONDA_SH' && conda activate $ENV_NAME && uvicorn main:app --host 0.0.0.0 --port ${PORT}" > "$LOG_FILE" 2>&1 &
        else
            nohup bash -c "uvicorn main:app --host 0.0.0.0 --port ${PORT}" > "$LOG_FILE" 2>&1 &
        fi
    else
        nohup uvicorn main:app --host 0.0.0.0 --port ${PORT} > "$LOG_FILE" 2>&1 &
    fi
    
    sleep 2

    if is_running; then
        echo "✓ Bot started successfully"
        echo "  PID: $(get_pid)"
        echo "  URL: http://localhost:${PORT}"
        echo "  Log: $LOG_FILE"
        if [ -f "$CONDA_ENV_FILE" ]; then
            echo "  Env: $(cat "$CONDA_ENV_FILE") (conda)"
        fi
    else
        echo "✗ Failed to start bot. Check log: $LOG_FILE"
        cat "$LOG_FILE"
        exit 1
    fi
}

stop() {
    if ! is_running; then
        echo "Bot is not running"
        rm -f "$PID_FILE"
        return 0
    fi

    echo "Stopping bot (PID: $(get_pid))..."
    kill_uvicorn
    rm -f "$PID_FILE"
    echo "✓ Bot stopped"
}

info() {
    echo "=== Polymarket BTC 5m Bot Status ==="
    echo ""

    if is_running; then
        echo "Status: Running ✓"
        echo "PID: $(get_pid)"
        echo "Port: ${PORT}"
        echo "URL: http://localhost:${PORT}"
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
        echo "  start   - Start the bot (port ${PORT})"
        echo "  stop    - Stop the bot"
        echo "  restart - Restart the bot"
        echo "  info    - Show current status"
        exit 1
        ;;
esac