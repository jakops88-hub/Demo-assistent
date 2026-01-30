# Marketing Assets Generator

This script automatically generates high-quality marketing assets (screenshot + demo video) for the DocuMind Streamlit app.

## Generated Assets

- **Screenshot**: `assets/marketing_screenshot.png` - Full-page screenshot (1920x1080)
- **Video**: `assets/demo_video.webm` - Demo video showing user interaction

## Requirements

- Python 3.8+
- Playwright browser automation library

## Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers (one-time setup)
python3 -m playwright install chromium
```

## Usage

Simply run the script:

```bash
python3 scripts/generate_marketing_assets.py
```

The script will:
1. Start the Streamlit app in the background
2. Wait for the server to be ready
3. Launch a headless browser with video recording
4. Simulate user interaction (typing a demo query)
5. Capture a full-page screenshot
6. Save the video recording
7. Clean up all processes

## Output

Generated assets will be saved to the `assets/` directory:
- `assets/marketing_screenshot.png`
- `assets/demo_video.webm`

## Features

- **Automated**: No manual intervention required
- **High Quality**: Full HD (1920x1080) resolution
- **Human-like**: Types with 100ms delay between keystrokes
- **Resilient**: Uses demo LLM mode (no API keys needed)
- **Clean**: Automatically cleans up processes

## Configuration

You can customize the following constants in the script:

- `VIEWPORT_WIDTH`: Browser width (default: 1920)
- `VIEWPORT_HEIGHT`: Browser height (default: 1080)
- `TYPING_DELAY_MS`: Delay between keystrokes (default: 100ms)
- `RESPONSE_WAIT_SECONDS`: Wait time for bot response (default: 5s)

## Troubleshooting

**Script fails with "streamlit: command not found":**
```bash
pip install streamlit
```

**Script fails with "Playwright not found":**
```bash
pip install playwright
python3 -m playwright install chromium
```

**Port 8501 already in use:**
```bash
# Kill any existing Streamlit processes
pkill -f streamlit
```
