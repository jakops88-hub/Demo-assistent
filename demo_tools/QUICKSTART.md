# Quick Start Guide - Demo Automation

## TL;DR

Generate professional demo assets (3 screenshots + 1 video) in one command:

```bash
# 1. Install dependencies
pip install -r demo_tools/requirements-demo.txt
python -m playwright install chromium

# 2. Set API key
export OPENAI_API_KEY='your-key-here'  # Linux/macOS
# or
set OPENAI_API_KEY=your-key-here       # Windows

# 3. Run automation
python -m demo_tools.capture_demo
```

**Output Location**: `demo_tools/output/YYYY-MM-DD_HHMMSS/`

## What You Get

```
demo_tools/output/2026-01-29_153045/
├── 01_indexed_files.png    # Shows indexed documents in sidebar
├── 02_answer.png            # Shows chat with Q&A
├── 03_sources.png           # Shows citations/sources
└── demo.mp4                 # 15-25 second video (1280x720)
```

## Expected Output Messages

```
======================================================================
Demo Automation Tool - Screenshot & Video Capture
======================================================================

Repository root: /path/to/Demo-assistent

[Step 1] Starting Streamlit server...
  → Command: python -m streamlit run app/app.py --server.headless true --server.port 8501
  → Streamlit started with PID: 12345

[Step 2] Waiting for Streamlit to be ready...
  → Streamlit is ready! (took 5.2s)

[Step 3] Starting Playwright automation...
  → Launching Chromium browser...
  → Navigating to http://localhost:8501...
  → Step 3.1: Enabling demo mode...
  → Step 3.2: Loading demo documents...
  → Step 3.3: Waiting for indexing to complete (up to 120s)...
  → Step 3.4: Capturing screenshot 1 (Indexed files)...
  → Step 3.5: Selecting HR question...
    Attempt 1/3 to select question...
    Found combobox, clicking to open dropdown...
    Found option containing 'vacation policy', clicking...
    ✓ Selected HR question (vacation policy)
  → Step 3.6: Inserting question...
  → Step 3.7: Submitting question...
    Detected pending question mode (textarea + Ask)
    Question text present: What is the vacation policy for employees in...
    ✓ Clicked Ask button (pending mode)
  → Step 3.8: Waiting for answer (up to 60s)...
    ✓ Answer appeared! (2 messages, 312 chars)
  → Step 3.9: Capturing screenshot 2 (Answer)...
  → Step 3.10: Looking for Sources section...
    ✓ Found source/citation references
  → Step 3.11: Capturing screenshot 3 (Sources)...
  → Waiting 2 seconds before closing...
  → Closing browser to save video...
  → Processing video file...
    ffmpeg detected, converting to MP4...
    ✓ Video converted to MP4: demo.mp4
    ✓ Temp video folder removed
  → ✓ Automation completed successfully!

[Step 4] Shutting down Streamlit...
  → ✓ Streamlit stopped

======================================================================
✓ Demo automation completed successfully!
======================================================================

Output files saved to: demo_tools/output/2026-01-29_153045

Generated assets:
  • 01_indexed_files.png (234.5 KB)
  • 02_answer.png (187.2 KB)
  • 03_sources.png (156.8 KB)
  • demo.mp4 (2.4 MB)
```

## Troubleshooting

### "OPENAI_API_KEY not set"
```bash
# Check if set
echo $OPENAI_API_KEY  # Should print your key

# Set it
export OPENAI_API_KEY='sk-...'  # Linux/macOS
set OPENAI_API_KEY=sk-...       # Windows CMD
$env:OPENAI_API_KEY='sk-...'    # Windows PowerShell
```

### "Streamlit did not become ready"
```bash
# Check if port 8501 is in use
lsof -i :8501           # macOS/Linux
netstat -ano | findstr :8501  # Windows

# Kill existing Streamlit processes
pkill -f streamlit      # macOS/Linux
taskkill /F /IM python.exe    # Windows (kills all Python)
```

### "Failed to select question"
- Demo mode might not be enabled
- Demo documents might not be loaded
- Check that `demo_assets/demo_questions.json` exists

### Video is WebM format
```bash
# Install ffmpeg for proper MP4 conversion
sudo apt install ffmpeg        # Linux
brew install ffmpeg            # macOS
# Windows: Download from https://ffmpeg.org
```

## Platform-Specific Notes

### Linux
```bash
# All commands work as shown
export OPENAI_API_KEY='your-key'
python -m demo_tools.capture_demo
```

### macOS
```bash
# Same as Linux
export OPENAI_API_KEY='your-key'
python -m demo_tools.capture_demo
```

### Windows CMD
```cmd
set OPENAI_API_KEY=your-key
python -m demo_tools.capture_demo
```

### Windows PowerShell
```powershell
$env:OPENAI_API_KEY='your-key'
python -m demo_tools.capture_demo
```

## Advanced Usage

### See Browser (Debug Mode)
Edit `demo_tools/capture_demo.py` line ~203:
```python
browser = p.chromium.launch(headless=False)  # Changed from True
```

### Increase Timeouts (Slow System)
Edit `demo_tools/capture_demo.py`:
- Line ~112: `wait_for_streamlit_ready(timeout=120)` (was 60)
- Line ~245: Change `range(240)` to `range(480)` for 240s indexing
- Line ~385: Change `range(120)` to `range(240)` for 120s answer wait

### Custom Output Location
Edit `demo_tools/capture_demo.py` line ~505:
```python
output_dir = Path('/path/to/custom/output') / timestamp
```

## Technical Requirements

- **Python**: 3.8 or higher
- **RAM**: 2 GB minimum, 4 GB recommended
- **Disk**: ~200 MB for Playwright browser + 5-10 MB per demo run
- **Network**: Required for OpenAI API calls
- **Port 8501**: Must be available

## Time Estimates

| Phase | Typical Time |
|-------|--------------|
| Streamlit startup | 5-10 seconds |
| Document indexing | 20-60 seconds |
| Question selection | 2-5 seconds |
| Answer generation | 10-30 seconds |
| Screenshot capture | 3-5 seconds |
| Video processing | 5-10 seconds |
| **Total** | **45-120 seconds** |

## Success Indicators

✅ **Successful Run:**
- All steps show ✓ checkmarks
- No error messages
- 4 files in output directory
- Video is playable
- Screenshots show UI content

❌ **Failed Run:**
- Error messages with ❌
- `error.png` saved in output
- Missing output files
- Check console output for specific error

## Next Steps

After successful generation:
1. Review screenshots for quality
2. Play video to verify flow
3. Use assets in presentations, documentation, or marketing
4. Re-run if needed with different configuration

## Getting Help

If automation fails:
1. Check `error.png` in output directory for visual debugging
2. Review console output for specific error message
3. Verify all prerequisites are installed
4. Check network connection (for OpenAI API)
5. Ensure demo assets exist in `demo_assets/` directory
6. Try with `headless=False` to see what's happening

## File Locations

```
Demo-assistent/
├── demo_tools/
│   ├── capture_demo.py          # Main automation script
│   ├── requirements-demo.txt    # Dependencies
│   ├── README.md                # Full documentation
│   ├── CHANGES.md               # Technical changes summary
│   ├── QUICKSTART.md            # This file
│   └── output/                  # Generated assets
│       └── YYYY-MM-DD_HHMMSS/
│           ├── 01_indexed_files.png
│           ├── 02_answer.png
│           ├── 03_sources.png
│           └── demo.mp4
├── demo_assets/
│   ├── demo_questions.json      # Demo questions
│   ├── hr/                      # HR demo files
│   ├── legal/                   # Legal demo files
│   └── commerce/                # Commerce demo files
└── app/
    ├── app.py                   # Streamlit app
    └── ui_components.py         # UI components

```

## FAQ

**Q: Do I need ffmpeg?**  
A: No, but recommended. Without it, video is saved as WebM in MP4 container (still playable).

**Q: Can I run this on a server?**  
A: Yes, but Playwright requires X11 or Xvfb on Linux. Use `headless=True` (default).

**Q: How do I run multiple times?**  
A: Just run the command again. Each run creates a new timestamped directory.

**Q: Can I change the question?**  
A: Edit `demo_tools/capture_demo.py` line 272, change `target_question` variable.

**Q: Why does it take so long?**  
A: Indexing and OpenAI API calls are the bottleneck. Typical total time: 1-2 minutes.

**Q: Can I customize screenshots?**  
A: Yes, edit the scrolling and capture sections in `capture_demo.py` (lines 260-530).
