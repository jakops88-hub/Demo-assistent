#!/bin/bash
# Linux/macOS launcher for Document Chatbot
# Make executable: chmod +x launcher/start.sh

echo "========================================"
echo "  Document Chatbot Launcher"
echo "========================================"
echo ""

# Change to script's parent directory (repository root)
cd "$(dirname "$0")/.." || exit 1

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 not found!"
    echo ""
    echo "Please install Python 3.10 or higher:"
    echo "  Ubuntu/Debian: sudo apt install python3.10 python3.10-venv"
    echo "  Fedora/RHEL:   sudo dnf install python3.10"
    echo "  macOS:         brew install python@3.10"
    echo ""
    exit 1
fi

echo "[OK] Found Python: $(which python3)"

# Verify Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version: $PYTHON_VERSION"

python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"
if [ $? -ne 0 ]; then
    echo "[ERROR] Python 3.10 or higher is required!"
    echo "Current version: $PYTHON_VERSION"
    echo ""
    echo "Please upgrade Python to 3.10 or higher"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "[OK] Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if dependencies need to be installed
NEED_INSTALL=0
if [ ! -f ".venv/.requirements_hash" ]; then
    NEED_INSTALL=1
    echo "First run detected - will install dependencies..."
else
    # Compare requirements.txt hash
    if command -v md5sum &> /dev/null; then
        NEW_HASH=$(md5sum requirements.txt | cut -d' ' -f1)
        OLD_HASH=$(cat .venv/.requirements_hash 2>/dev/null || echo "")
    elif command -v md5 &> /dev/null; then
        NEW_HASH=$(md5 -q requirements.txt)
        OLD_HASH=$(cat .venv/.requirements_hash 2>/dev/null || echo "")
    else
        # No hash command available, always install
        NEED_INSTALL=1
        echo "Cannot verify hash - will update dependencies..."
    fi
    
    if [ "$NEED_INSTALL" -eq 0 ] && [ "$NEW_HASH" != "$OLD_HASH" ]; then
        NEED_INSTALL=1
        echo "Requirements changed - will update dependencies..."
    fi
fi

# Install/update dependencies if needed
if [ "$NEED_INSTALL" -eq 1 ]; then
    echo ""
    echo "Installing dependencies (this may take a few minutes)..."
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    # Save hash for next time
    if command -v md5sum &> /dev/null; then
        md5sum requirements.txt | cut -d' ' -f1 > .venv/.requirements_hash
    elif command -v md5 &> /dev/null; then
        md5 -q requirements.txt > .venv/.requirements_hash
    fi
    echo "[OK] Dependencies installed"
else
    echo "[OK] Dependencies already up to date"
fi

# Load .env file if it exists
echo ""
echo "Checking configuration..."
if [ -f ".env" ]; then
    echo "[OK] Found .env file"
    # Load environment variables safely
    set -a
    source .env
    set +a
else
    # Check if OpenAI provider is configured in actual config or example
    CONFIG_FILE=""
    if [ -f "config/config.yaml" ]; then
        CONFIG_FILE="config/config.yaml"
    elif [ -f "config/config.example.yaml" ]; then
        CONFIG_FILE="config/config.example.yaml"
    fi
    
    if [ -n "$CONFIG_FILE" ] && grep -q 'provider: "openai"' "$CONFIG_FILE"; then
        echo "[WARNING] No .env file found!"
        echo ""
        echo "If you're using OpenAI, you need to:"
        echo "1. Copy .env.example to .env"
        echo "2. Add your OPENAI_API_KEY to the .env file"
        echo ""
        echo "Continuing without .env file..."
    fi
fi

# Start Streamlit
echo ""
echo "========================================"
echo "  Starting Document Chatbot..."
echo "========================================"
echo ""
echo "The application will open in your browser automatically."
echo "Keep this terminal open while using the chatbot."
echo "Press Ctrl+C to stop the application."
echo ""

# Open browser after a short delay (in background)
(sleep 3 && python scripts/open_browser.py http://localhost:8501) &

# Run Streamlit
streamlit run app/app.py --server.headless true --server.address localhost --server.port 8501

echo ""
echo "Application stopped."
