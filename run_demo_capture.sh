#!/bin/bash
# Quick start script for demo capture

echo "========================================"
echo "Demo Capture - Quick Start"
echo "========================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found!"
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: You need to add your OpenAI API key to the .env file"
    echo ""
    echo "Edit the .env file and replace 'your-openai-api-key-here' with your actual key:"
    echo "  nano .env    (or use your preferred text editor)"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Check if OPENAI_API_KEY is set in .env
if grep -q "your-openai-api-key-here" .env; then
    echo "⚠️  OPENAI_API_KEY is not configured!"
    echo ""
    echo "Please edit the .env file and add your OpenAI API key:"
    echo "  nano .env    (or use your preferred text editor)"
    echo ""
    echo "Replace 'your-openai-api-key-here' with your actual API key (starts with 'sk-')"
    exit 1
fi

# Source the .env file
export $(cat .env | grep -v '^#' | xargs)

# Check if API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY environment variable is empty!"
    echo ""
    echo "Please add your OpenAI API key to the .env file:"
    echo "  nano .env"
    exit 1
fi

echo "✓ Environment configured"
echo ""
echo "Starting demo automation..."
echo "This will:"
echo "  1. Start the Streamlit server"
echo "  2. Load demo documents"
echo "  3. Capture 3 screenshots"
echo "  4. Record a demo video"
echo "  5. Save all assets to demo_tools/output/"
echo ""
echo "Estimated time: 2-3 minutes"
echo ""

# Run the demo capture script
python -m demo_tools.capture_demo

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✓ Demo capture completed successfully!"
    echo "========================================"
    echo ""
    echo "Your demo assets are ready in:"
    echo "  demo_tools/output/[timestamp]/"
    echo ""
    echo "Files generated:"
    echo "  • 01_indexed_files.png"
    echo "  • 02_answer.png"
    echo "  • 03_sources.png"
    echo "  • demo.mp4"
    echo ""
    echo "These assets are ready for your product launch! 🚀"
    echo ""
else
    echo ""
    echo "❌ Demo capture failed!"
    echo ""
    echo "Please check the error messages above and try again."
    echo "For help, see DEMO_CAPTURE_GUIDE.md"
    exit 1
fi
