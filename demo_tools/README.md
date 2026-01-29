# Demo Automation Tool

Automated screenshot and video capture tool for the Document Chatbot demo.

## Overview

This tool automates the Streamlit application to generate high-quality demo assets:
- **3 PNG screenshots** showing key features
- **1 MP4 video recording** (15-25 seconds) of the complete workflow

All assets are generated in a single command with no manual interaction required.

## Prerequisites

1. **Python 3.8+** installed
2. **OpenAI API key** - Required for the chatbot functionality
3. **Main application dependencies** - Install from root `requirements.txt`

## Setup

### 1. Install Demo Dependencies

```bash
pip install -r demo_tools/requirements-demo.txt
```

This installs:
- `playwright` - Browser automation
- `requests` - HTTP polling
- `psutil` - Process management
- `python-dotenv` - Environment variable loading (optional)

### 2. Install Playwright Browser

```bash
python -m playwright install chromium
```

This downloads the Chromium browser used for automation (~130 MB).

### 3. Set OpenAI API Key

The tool requires `OPENAI_API_KEY` to be set in your environment.

**Option A: Environment Variable**

Linux/macOS:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Windows (Command Prompt):
```cmd
set OPENAI_API_KEY=your-api-key-here
```

Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY='your-api-key-here'
```

**Option B: .env File**

Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

### Run the Demo Automation

From the project root directory:

```bash
python -m demo_tools.capture_demo
```

### What Happens

The tool will:

1. **Start Streamlit** server on port 8501
2. **Wait for app** to become ready (polls for up to 60 seconds)
3. **Automate browser**:
   - Enable demo mode
   - Load demo documents (HR, Legal, Commerce)
   - Wait for indexing to complete
   - Select a suggested question
   - Submit the question
   - Wait for the answer
   - Capture 3 screenshots and 1 video
4. **Stop Streamlit** server cleanly

### Output Location

Assets are saved to timestamped folders:

```
demo_tools/output/YYYY-MM-DD_HHMMSS/
├── 01_indexed_files.png
├── 02_answer.png
├── 03_sources.png
└── demo.mp4
```

Example:
```
demo_tools/output/2026-01-29_153045/
```

## Generated Assets

### Screenshots

1. **01_indexed_files.png** - Shows the indexed documents after loading demo data
2. **02_answer.png** - Shows the chatbot answer to the demo question
3. **03_sources.png** - Shows the sources/citations section

### Video

- **demo.mp4** - Complete workflow recording (15-25 seconds)
  - Shows the entire interaction flow
  - Viewport: 1280x720
  - Format: MP4 (converted from WebM if ffmpeg available)

## Troubleshooting

### "OPENAI_API_KEY not set" Error

Make sure your API key is properly exported:
```bash
echo $OPENAI_API_KEY  # Should print your key
```

If empty, set it again and retry.

### "Playwright is not installed" Error

Install Playwright and the browser:
```bash
pip install playwright
python -m playwright install chromium
```

### "Streamlit did not become ready" Error

- Check if port 8501 is already in use
- Try stopping any running Streamlit instances
- Check firewall settings

### "Indexing did not complete" Error

- Ensure you have a stable internet connection (for OpenAI API calls)
- Check that demo assets exist in `demo_assets/` directory
- Verify your OpenAI API key is valid and has credits

### Video Not Generated

If `demo.mp4` is missing:
- Check if `ffmpeg` is installed (optional but recommended)
- Without ffmpeg, video is saved as WebM in MP4 container
- Install ffmpeg: `apt install ffmpeg` (Linux) or `brew install ffmpeg` (macOS)

### Debug Screenshot

If automation fails, a debug screenshot is saved as `error.png` in the output folder.

## Platform Support

✅ **Windows** - Fully supported  
✅ **macOS** - Fully supported  
✅ **Linux** - Fully supported

## Advanced Options

### Custom Output Directory

Edit `capture_demo.py` and modify the `output_dir` variable in the `main()` function.

### Timeout Adjustments

If your system is slower, increase timeouts in `capture_demo.py`:
- `wait_for_streamlit_ready(timeout=60)` - Streamlit startup
- Indexing wait loop (line 236) - Document indexing
- Answer wait loop (line 337) - Answer generation

### Headless Mode

The browser runs in headless mode by default. To see the browser (for debugging):

Edit `capture_demo.py`, line 195:
```python
browser = p.chromium.launch(headless=False)  # Changed to False
```

## Dependencies Isolation

Demo dependencies are kept separate from main app dependencies:
- **Main app**: `requirements.txt`
- **Demo tool**: `demo_tools/requirements-demo.txt`

This ensures demo tooling doesn't interfere with production dependencies.

## License

Same as parent project.
