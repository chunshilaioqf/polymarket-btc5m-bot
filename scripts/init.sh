#!/bin/bash
# Polymarket BTC 5m Bot - Environment Initialization Script

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"

echo "=== Polymarket BTC 5m Bot - Environment Setup ==="
echo ""

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✓ Python $PYTHON_VERSION found"
else
    echo "✗ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check pip
echo "Checking pip..."
if python3 -m pip --version &> /dev/null; then
    echo "✓ pip found"
else
    echo "Installing pip..."
    apt-get update -qq && apt-get install -y -qq python3-pip
fi

# Install Python dependencies
echo "Installing Python dependencies..."
cd "$BACKEND_DIR"
python3 -m pip install --break-system-packages -q -r requirements.txt
echo "✓ Python dependencies installed"

# Check uvicorn
echo "Checking uvicorn..."
if command -v uvicorn &> /dev/null || python3 -c "import uvicorn" 2>/dev/null; then
    echo "✓ uvicorn available"
else
    echo "✗ uvicorn not found. Installing..."
    python3 -m pip install --break-system-packages -q uvicorn
fi

echo ""
echo "=== Initialization Complete ==="
echo ""
echo "Usage:"
echo "  ./scripts/manage.sh start    - Start the bot"
echo "  ./scripts/manage.sh stop     - Stop the bot"
echo "  ./scripts/manage.sh restart  - Restart the bot"
echo "  ./scripts/manage.sh info     - Show status"
echo ""