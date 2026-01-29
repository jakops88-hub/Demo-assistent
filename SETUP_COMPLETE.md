# ✅ Demo Capture Setup Complete!

Everything is ready for you to capture professional demo assets for your product launch.

## What's Been Prepared

✅ **Dependencies Installed**
- All Python packages (Streamlit, LangChain, OpenAI, etc.)
- Playwright browser automation framework
- Chromium browser for headless automation

✅ **Automation Scripts Created**
- `run_demo_capture.sh` - One-command demo capture (Linux/macOS)
- `run_demo_capture.bat` - One-command demo capture (Windows)
- Both scripts include automatic validation and error checking

✅ **Comprehensive Documentation**
- `DEMO_QUICK_START.md` - Quick reference card (fastest way to start)
- `DEMO_CAPTURE_GUIDE.md` - Complete step-by-step instructions
- `DEMO_WORKFLOW.md` - Visual diagrams of the entire process
- `demo_tools/README.md` - Technical documentation

✅ **Demo Assets Ready**
- Demo documents in `demo_assets/` (HR, Legal, Commerce)
- Pre-written questions in `demo_assets/demo_questions.json`
- Demo mode built into the app

## What You Need to Do (3 Steps)

### Step 1: Add Your OpenAI API Key

```bash
# Copy the template
cp .env.example .env

# Edit the file
nano .env   # or vim, notepad, VS Code, etc.

# Add your key (replace the placeholder)
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

💡 **Get an API key at:** https://platform.openai.com/api-keys

### Step 2: Run the Demo Capture

**On Linux/macOS:**
```bash
./run_demo_capture.sh
```

**On Windows:**
```cmd
run_demo_capture.bat
```

**Or directly:**
```bash
python -m demo_tools.capture_demo
```

### Step 3: Get Your Assets!

After 2-3 minutes, find your demo assets in:
```
demo_tools/output/[timestamp]/
├── 01_indexed_files.png  ← Shows indexed documents
├── 02_answer.png          ← Shows Q&A interaction
├── 03_sources.png         ← Shows source citations
└── demo.mp4               ← 15-25 second demo video
```

## Alternative: Use Ollama (No API Key Needed)

If you don't want to use OpenAI:

```bash
# 1. Install Ollama from https://ollama.ai

# 2. Pull models
ollama pull llama3
ollama pull nomic-embed-text

# 3. Update config
nano config/config.example.yaml
# Change line 16: provider: "ollama"

# 4. Run demo (no API key needed!)
python -m demo_tools.capture_demo
```

## What the Automation Does

The script automatically:

1. ✅ Starts the Streamlit server
2. ✅ Opens the app in a headless browser
3. ✅ Enables demo mode
4. ✅ Loads 3 demo documents (HR, Legal, Commerce)
5. ✅ Selects and submits a demo question
6. ✅ Waits for the AI to generate an answer
7. ✅ Captures 3 professional screenshots
8. ✅ Records a complete demo video
9. ✅ Stops the server and saves everything

**Total time: 2-3 minutes**

## Your Demo Assets

The generated assets are perfect for:

🌐 **Website** - Landing pages, product showcase  
📚 **Documentation** - Visual guides and tutorials  
📱 **Social Media** - Feature highlights and demos  
📊 **Presentations** - Stakeholder demonstrations  
🎯 **Marketing** - Professional product materials  

## Need Help?

📘 **Quick start?** → Read [DEMO_QUICK_START.md](DEMO_QUICK_START.md)  
📗 **Step-by-step?** → Read [DEMO_CAPTURE_GUIDE.md](DEMO_CAPTURE_GUIDE.md)  
📕 **Visual guide?** → Read [DEMO_WORKFLOW.md](DEMO_WORKFLOW.md)  
🔧 **Technical details?** → Read [demo_tools/README.md](demo_tools/README.md)  

## Common Issues

### "OPENAI_API_KEY not found"
```bash
# Make sure .env file exists
ls -la .env

# Check the key is set
cat .env | grep OPENAI_API_KEY

# If not set, edit .env and add your key
nano .env
```

### "Port 8501 already in use"
```bash
# Find and kill existing Streamlit
pkill -f streamlit

# Or find the process
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows
```

### "Playwright not installed"
```bash
# This should already be done, but if needed:
pip install -r demo_tools/requirements-demo.txt
python -m playwright install chromium
```

## Manual Demo (Alternative)

Don't want automation? Run manually:

```bash
# Start the app
python -m scripts.run_streamlit

# In browser (http://localhost:8501):
# 1. Check "Demo mode"
# 2. Click "Load demo documents"
# 3. Select a question
# 4. Click "Insert question"
# 5. Click "Send"
# 6. Take screenshots manually
# 7. Record with screen recorder
```

## File Structure

```
Demo-assistent/
├── run_demo_capture.sh        ← Run this (Linux/macOS)
├── run_demo_capture.bat        ← Run this (Windows)
├── .env                        ← You create this (API key)
├── .env.example                ← Template
│
├── DEMO_QUICK_START.md         ← Quick reference
├── DEMO_CAPTURE_GUIDE.md       ← Complete guide
├── DEMO_WORKFLOW.md            ← Visual diagrams
│
├── demo_tools/
│   ├── README.md               ← Technical docs
│   ├── capture_demo.py         ← Automation script
│   ├── requirements-demo.txt   ← Dependencies
│   └── output/                 ← Generated assets go here
│       └── [timestamp]/
│           ├── 01_indexed_files.png
│           ├── 02_answer.png
│           ├── 03_sources.png
│           └── demo.mp4
│
├── demo_assets/                ← Demo content
│   ├── hr/
│   ├── legal/
│   ├── commerce/
│   └── demo_questions.json
│
├── app/                        ← Main application
├── core/                       ← Business logic
└── config/                     ← Configuration
```

## Next Steps After Demo Capture

Once you have your demo assets:

1. ✅ Review screenshots for quality
2. ✅ Watch the demo video
3. ✅ Crop/edit if needed
4. ✅ Add to your website
5. ✅ Share on social media
6. ✅ Include in documentation
7. ✅ Use in presentations
8. ✅ Launch your product! 🚀

## Summary

**Everything is ready!** Just add your OpenAI API key and run the script.

You're literally 3 minutes away from having professional demo assets for your product launch.

```bash
# The fastest way to get started:
cp .env.example .env
nano .env  # Add your API key
./run_demo_capture.sh
```

That's it! 🎉

---

**Questions?** Check the documentation files listed above or open an issue on GitHub.

**Ready to launch?** Get your API key and run the script! 🚀
