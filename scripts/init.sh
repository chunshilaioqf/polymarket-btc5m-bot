#!/bin/bash
# Polymarket BTC 5m Bot - Environment Initialization Script

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
PROJECT_NAME="polymarket-btc5m-bot"

echo "=== Polymarket BTC 5m Bot - Environment Setup ==="
echo ""

# Check conda
HAS_CONDA=false
if command -v conda &> /dev/null; then
    HAS_CONDA=true
    echo "✓ Conda detected: $(conda --version)"
else
    echo "ℹ Conda not found, using system Python"
fi

# Check Python
echo "Checking Python..."
if [ "$HAS_CONDA" = true ]; then
    PYTHON="python"
    PIP="pip"
else
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        echo "✓ Python $PYTHON_VERSION found"
        PYTHON="python3"
        PIP="python3 -m pip"
    else
        echo "✗ Python 3 not found. Please install Python 3.8+"
        exit 1
    fi

    # Check pip
    echo "Checking pip..."
    if $PIP --version &> /dev/null; then
        echo "✓ pip found"
    else
        echo "Installing pip..."
        apt-get update -qq && apt-get install -y -qq python3-pip
    fi
fi

# Setup conda environment if available
if [ "$HAS_CONDA" = true ]; then
    echo ""
    echo "Setting up conda environment..."
    
    # Initialize conda for shell
    CONDA_BASE=$(conda info --base)
    source "$CONDA_BASE/etc/profile.d/conda.sh"
    
    # Check if environment already exists
    if conda env list | grep -q "^$PROJECT_NAME "; then
        echo "✓ Conda environment '$PROJECT_NAME' already exists"
        echo "  Activating environment..."
        conda activate "$PROJECT_NAME"
    else
        echo "Creating conda environment '$PROJECT_NAME' with Python 3.11..."
        conda create -n "$PROJECT_NAME" python=3.11 -y -q
        conda activate "$PROJECT_NAME"
        echo "✓ Conda environment created and activated"
    fi
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
cd "$BACKEND_DIR"
$PIP install --break-system-packages -q -r requirements.txt 2>/dev/null || $PIP install -q -r requirements.txt
echo "✓ Python dependencies installed"

# Check uvicorn
echo "Checking uvicorn..."
if command -v uvicorn &> /dev/null || $PYTHON -c "import uvicorn" 2>/dev/null; then
    echo "✓ uvicorn available"
else
    echo "Installing uvicorn..."
    $PIP install --break-system-packages -q uvicorn 2>/dev/null || $PIP install -q uvicorn
fi

# Save conda env name to file for manage.sh
if [ "$HAS_CONDA" = true ]; then
    echo "$PROJECT_NAME" > "$PROJECT_DIR/.conda_env"
    echo ""
    echo "✓ Environment info saved to .conda_env"
fi

echo ""
echo "=== Initialization Complete ==="
echo ""
if [ "$HAS_CONDA" = true ]; then
    echo "Conda environment: $PROJECT_NAME"
    echo "Activate with: conda activate $PROJECT_NAME"
else
    echo "Python: $PYTHON"
fi
echo ""
echo "Usage:"
echo "  ./scripts/manage.sh start    - Start the bot"
echo "  ./scripts/manage.sh stop     - Stop the bot"
echo "  ./scripts/manage.sh restart  - Restart the bot"
echo "  ./scripts/manage.sh info     - Show status"
echo ""