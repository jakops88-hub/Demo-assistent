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
- `playwright` - Browser automation framework
- `requests` - HTTP polling for Streamlit readiness check
- `psutil` - Process management for clean shutdown
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
3. **Automate browser** workflow:
   - ✓ Enable demo mode checkbox
   - ✓ Click "Load demo documents" button
   - ✓ Wait for indexing to complete (up to 120 seconds)
   - ✓ Select HR question from Streamlit combobox (vacation policy)
   - ✓ Click "Insert question" button
   - ✓ Submit question (handles both "Ask" and "Send" button modes)
   - ✓ Wait for assistant answer (up to 60 seconds)
   - ✓ Capture 3 professional screenshots
   - ✓ Record smooth video of entire workflow
4. **Stop Streamlit** server cleanly using process tree termination

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

All screenshots use 1280x720 viewport with proper settling time (1200ms) for professional quality:

1. **01_indexed_files.png** - Shows the indexed documents after loading demo data (scrolled to top)
2. **02_answer.png** - Shows the chatbot answer to the demo question in chat area (scrolled to chat)
3. **03_sources.png** - Shows the sources/citations section (scrolled to bottom)

### Video

- **demo.mp4** - Complete workflow recording (15-25 seconds)
  - Shows the entire interaction flow with smooth transitions
  - Viewport: 1280x720
  - Format: MP4 (converted from WebM if ffmpeg available, otherwise WebM in MP4 container)
  - Includes 0.5-1.0 second pauses between actions for professional appearance

## Key Features

### Robust Streamlit Selectbox Handling

The automation handles Streamlit's custom combobox implementation (not native `<select>`):

1. **Primary Strategy**: Locates combobox by role and label
   - `page.get_by_role("combobox", name="Suggested question")`
   - Clicks to open dropdown
   - Selects option using `get_by_role("option")`

2. **Fallback Strategy**: Keyboard input
   - Types "vacation policy" 
   - Presses Enter
   - Verifies selection

3. **Last Resort**: Selects first available option if target not found

### Dual Chat Submission Mode Support

The automation detects and handles both UI modes:

- **Pending Mode**: When "Insert question" is clicked
  - Detects textarea labeled "Edit and press Ask to submit:"
  - Clicks "Ask" button
  
- **Normal Mode**: Standard chat input
  - Detects text_input labeled "Ask a question"
  - Clicks "Send" button

Always verifies non-empty text before submission.

### Reliable Answer Detection

Uses multiple strategies with 60-second timeout:

1. Counts chat messages (needs ≥2: user + assistant)
2. Verifies last message has substantial content (>50 chars)
3. Looks for assistant-specific messages
4. Progress updates every 10 seconds

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

- Check if port 8501 is already in use: `lsof -i :8501` (macOS/Linux) or `netstat -ano | findstr :8501` (Windows)
- Try stopping any running Streamlit instances
- Check firewall settings

### "Indexing did not complete" Error

- Ensure you have a stable internet connection (for OpenAI API calls)
- Check that demo assets exist in `demo_assets/` directory
- Verify your OpenAI API key is valid and has credits
- Check `demo_assets/` contains: `hr/`, `legal/`, `commerce/` folders and `demo_questions.json`

### "Failed to select question" Error

The automation includes 3 retry attempts with multiple strategies:
1. Role-based combobox selection
2. Keyboard input fallback
3. Select first available option

If all fail, check:
- Demo mode is enabled
- Demo documents loaded successfully
- `demo_questions.json` is valid JSON

### Video Not Generated or Wrong Format

**If `demo.mp4` is missing:**
- Check browser automation completed (look for "✓ Screenshot 3 saved")
- Check for `video_temp/` folder - if it exists, video didn't finalize

**If video is WebM format in MP4 container:**
- Install ffmpeg for proper conversion:
  - Linux: `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: Download from https://ffmpeg.org
- The tool will use ffmpeg if available, otherwise copies WebM bytes to .mp4
- WebM-in-MP4 plays in most browsers and can be uploaded to Fiverr

### Debug Screenshot

If automation fails, check `error.png` in the output folder for visual debugging.

The tool also prints any visible Streamlit error messages (st.error/st.warning) to console.

## Platform Support

✅ **Windows** - Fully supported  
✅ **macOS** - Fully supported  
✅ **Linux** - Fully supported

## Advanced Options

### Headless Mode

The browser runs in headless mode by default. To see the browser (for debugging):

Edit `capture_demo.py`, line ~203:
```python
browser = p.chromium.launch(headless=False)  # Changed from True
```

### Timeout Adjustments

If your system is slower, increase timeouts in `capture_demo.py`:
- `wait_for_streamlit_ready(timeout=60)` - Streamlit startup (line ~112)
- Indexing wait loop - Document indexing (line ~245, max 120s)
- Answer wait loop - Answer generation (line ~385, max 60s)

### Custom Output Directory

Edit `capture_demo.py` line ~505 to change output location:
```python
output_dir = repo_root / 'demo_tools' / 'output' / timestamp
```

## Technical Details

### Streamlit Selectbox Implementation

Streamlit does NOT use native HTML `<select>` elements. Instead, it renders a custom combobox using:
- ARIA role: `combobox`
- ARIA label: matches the label parameter
- Dropdown options with role: `option`

Our automation uses Playwright's role-based selectors for reliability:
```python
combobox = page.get_by_role("combobox", name="Suggested question")
option = page.get_by_role("option", name=re.compile("vacation policy", re.I))
```

### Process Management

Uses `psutil` for clean shutdown:
1. Finds all child processes of Streamlit
2. Terminates children first
3. Waits up to 3 seconds
4. Force kills any remaining processes
5. Finally terminates parent Streamlit process

This prevents orphaned processes and port conflicts.

### Video Recording

Playwright's built-in video recording:
- Records to temporary directory during automation
- Finalized when browser context closes
- Output format: WebM (VP8/VP9 video codec)
- Converted to H.264 MP4 if ffmpeg available

## Dependencies Isolation

Demo dependencies are kept separate from main app dependencies:
- **Main app**: `requirements.txt` (Streamlit, OpenAI, LangChain, etc.)
- **Demo tool**: `demo_tools/requirements-demo.txt` (Playwright, psutil, requests)

This ensures demo tooling doesn't interfere with production dependencies.

## License

Same as parent project.
