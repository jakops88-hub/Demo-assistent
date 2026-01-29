# 📋 Demo Capture Checklist

Use this checklist to track your progress through the demo capture process.

## Pre-Flight Checklist

### System Requirements
- [ ] Python 3.10 or higher installed
- [ ] Git installed (for repository management)
- [ ] Text editor available (nano, vim, notepad, VS Code, etc.)
- [ ] Internet connection (for OpenAI API or to download Ollama)

### Repository Setup
- [x] Repository cloned ✓
- [x] Python dependencies installed ✓
- [x] Playwright installed ✓
- [x] Chromium browser installed ✓
- [x] Demo automation script ready ✓
- [x] Demo documents present in `demo_assets/` ✓

## API Key Setup (Choose One)

### Option A: OpenAI (Recommended)
- [ ] OpenAI account created at https://platform.openai.com
- [ ] API key generated at https://platform.openai.com/api-keys
- [ ] `.env` file created: `cp .env.example .env`
- [ ] API key added to `.env` file
- [ ] API key format verified (starts with `sk-`)
- [ ] `.env` file saved

### Option B: Ollama (Local/Free)
- [ ] Ollama downloaded from https://ollama.ai
- [ ] Ollama installed
- [ ] Ollama service started: `ollama serve`
- [ ] llama3 model pulled: `ollama pull llama3`
- [ ] nomic-embed-text model pulled: `ollama pull nomic-embed-text`
- [ ] `config/config.example.yaml` edited to use `provider: "ollama"`

## Running the Demo

### Execute the Script
- [ ] Terminal/command prompt opened
- [ ] Navigated to project directory: `cd Demo-assistent`
- [ ] Script executed:
  - [ ] Linux/macOS: `./run_demo_capture.sh`
  - [ ] Windows: `run_demo_capture.bat`
  - [ ] Or: `python -m demo_tools.capture_demo`

### Monitor Progress
- [ ] Streamlit server started successfully
- [ ] Browser automation launched
- [ ] Demo mode enabled
- [ ] Demo documents loaded
- [ ] Question selected and submitted
- [ ] Answer received
- [ ] Screenshots captured (3 total)
- [ ] Video recorded
- [ ] Server stopped cleanly
- [ ] Script completed without errors

## Verify Output

### Check Output Files
- [ ] Output directory created: `demo_tools/output/[timestamp]/`
- [ ] Navigate to output directory
- [ ] File 1 exists: `01_indexed_files.png`
  - [ ] Size: 100-300 KB
  - [ ] Resolution: 1280x720
  - [ ] Content: Shows indexed documents in sidebar
- [ ] File 2 exists: `02_answer.png`
  - [ ] Size: 150-400 KB
  - [ ] Resolution: 1280x720
  - [ ] Content: Shows Q&A interaction in chat
- [ ] File 3 exists: `03_sources.png`
  - [ ] Size: 150-400 KB
  - [ ] Resolution: 1280x720
  - [ ] Content: Shows source citations
- [ ] File 4 exists: `demo.mp4`
  - [ ] Size: 2-5 MB
  - [ ] Duration: 15-25 seconds
  - [ ] Format: MP4
  - [ ] Content: Complete workflow demonstration

### Quality Check
- [ ] Open all screenshots to verify clarity
- [ ] Play demo video to verify smoothness
- [ ] Check that text is readable in screenshots
- [ ] Verify video shows complete workflow
- [ ] Confirm no UI glitches or errors visible
- [ ] Verify professional appearance

## Post-Capture Tasks

### Asset Organization
- [ ] Copy assets to a dedicated folder for product launch
- [ ] Rename files if needed for your naming convention
- [ ] Backup assets to cloud storage or version control

### Asset Optimization (Optional)
- [ ] Compress PNG files if needed (use tools like TinyPNG)
- [ ] Compress video if needed (use tools like HandBrake)
- [ ] Add watermark or branding if desired
- [ ] Crop/edit screenshots if needed

### Asset Usage
- [ ] Upload screenshots to website
- [ ] Embed video on landing page
- [ ] Add to documentation/tutorials
- [ ] Share on social media
- [ ] Include in presentations
- [ ] Use in marketing materials
- [ ] Add to product launch announcement

## Troubleshooting (If Needed)

### Common Issues
- [ ] Issue: "OPENAI_API_KEY not found"
  - [ ] Solution: Create `.env` file and add API key
  - [ ] Verified: Key starts with `sk-`
  
- [ ] Issue: "Port 8501 already in use"
  - [ ] Solution: Kill existing Streamlit: `pkill -f streamlit`
  - [ ] Verified: Port is now free
  
- [ ] Issue: "Playwright not installed"
  - [ ] Solution: `pip install -r demo_tools/requirements-demo.txt`
  - [ ] Solution: `python -m playwright install chromium`
  
- [ ] Issue: "Indexing timeout"
  - [ ] Check: Internet connection stable
  - [ ] Check: OpenAI API key is valid
  - [ ] Check: OpenAI account has credits
  
- [ ] Issue: "Video not generated"
  - [ ] Check: ffmpeg installed for MP4 conversion
  - [ ] Fallback: Video may be WebM in MP4 container (still playable)

### Get Help
- [ ] Read [DEMO_QUICK_START.md](DEMO_QUICK_START.md)
- [ ] Read [DEMO_CAPTURE_GUIDE.md](DEMO_CAPTURE_GUIDE.md)
- [ ] Read [demo_tools/README.md](demo_tools/README.md)
- [ ] Check terminal output for specific error messages
- [ ] Look for `error.png` in output folder (debug screenshot)
- [ ] Open GitHub issue if problem persists

## Success Criteria

You've successfully completed the demo capture when:

✅ All 4 files generated (3 PNGs + 1 MP4)  
✅ All files are correct size and format  
✅ Screenshots show the intended features  
✅ Video plays smoothly and shows complete workflow  
✅ Assets are professional quality  
✅ Ready to use for product launch  

## Final Steps

- [ ] Celebrate! 🎉 You have professional demo assets
- [ ] Share your demo assets with your team
- [ ] Update your product launch materials
- [ ] Schedule your product launch
- [ ] Launch your product! 🚀

---

## Quick Reference

**Fastest path to completion:**

```bash
# 1. Setup (30 seconds)
cp .env.example .env
nano .env  # Add API key

# 2. Run (2-3 minutes)
./run_demo_capture.sh

# 3. Verify (30 seconds)
ls -lh demo_tools/output/*/

# Done! ✅
```

---

**Current Status:** 
- Repository setup: ✅ Complete
- Dependencies: ✅ Installed
- Scripts: ✅ Ready
- Documentation: ✅ Available
- **Your action needed:** Add API key and run script!

**Next step:** Create `.env` file and add your OpenAI API key, then run `./run_demo_capture.sh`
