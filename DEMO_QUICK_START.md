# 🚀 Quick Reference: Demo Capture

## One-Command Demo Capture

```bash
# Linux/macOS
./run_demo_capture.sh

# Windows
run_demo_capture.bat

# Direct Python
python -m demo_tools.capture_demo
```

## Prerequisites Checklist

- ✅ Python 3.10+ installed
- ✅ Dependencies installed (already done in this environment)
- ✅ Playwright + Chromium installed (already done in this environment)  
- ⚠️ **YOU NEED**: OpenAI API key in `.env` file

## Setup Your API Key (Required)

```bash
# 1. Copy template
cp .env.example .env

# 2. Edit .env file
nano .env   # or vim, notepad, etc.

# 3. Add your key (replace the placeholder)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxx
```

## What You Get

After running the script (2-3 minutes):

```
demo_tools/output/2026-01-29_182245/
├── 01_indexed_files.png    ← Sidebar with indexed documents
├── 02_answer.png            ← Q&A interaction
├── 03_sources.png           ← Source citations
└── demo.mp4                 ← 15-25 second demo video
```

## Alternative: Use Ollama (No API Key)

```bash
# Install Ollama
# Download from: https://ollama.ai

# Pull models
ollama pull llama3
ollama pull nomic-embed-text

# Edit config
nano config/config.example.yaml
# Change line 16 to: provider: "ollama"

# Run demo (no API key needed!)
python -m demo_tools.capture_demo
```

## Manual Demo (No Automation)

```bash
# 1. Start app
python -m scripts.run_streamlit

# 2. In browser (http://localhost:8501):
#    - Check "Demo mode" checkbox
#    - Click "Load demo documents"
#    - Select a question
#    - Click "Insert question"
#    - Click "Send"
#    - Take screenshots manually
#    - Record with screen recorder
```

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| "API key not found" | Create `.env` file and add your key |
| "Playwright not installed" | `pip install -r demo_tools/requirements-demo.txt` |
| "Browser not installed" | `python -m playwright install chromium` |
| "Port 8501 in use" | Kill existing Streamlit: `pkill -f streamlit` |
| "Indexing timeout" | Check internet connection and API key validity |

## File Locations

- **Main app**: `app/app.py`
- **Demo script**: `demo_tools/capture_demo.py`
- **Demo docs**: `demo_assets/` (HR, Legal, Commerce)
- **Demo questions**: `demo_assets/demo_questions.json`
- **Output**: `demo_tools/output/[timestamp]/`
- **Config**: `config/config.example.yaml`
- **Environment**: `.env` (you create this)

## Documentation

- 📘 Full guide: [DEMO_CAPTURE_GUIDE.md](DEMO_CAPTURE_GUIDE.md)
- 📗 Demo tools: [demo_tools/README.md](demo_tools/README.md)
- 📕 Main README: [README.md](README.md)

## Need Help?

1. Check [DEMO_CAPTURE_GUIDE.md](DEMO_CAPTURE_GUIDE.md) for detailed instructions
2. Read [demo_tools/README.md](demo_tools/README.md) for technical details
3. See error messages in terminal for specific issues
4. Open an issue on GitHub if stuck

---

**TL;DR**: Create `.env` with your OpenAI key, then run `./run_demo_capture.sh` ✨
