# Demo Capture Guide

This guide will help you run the server and capture screenshots and a demo video for your product launch.

## Prerequisites

✅ **Already completed in this environment:**
- Python dependencies installed
- Playwright and Chromium browser installed
- Demo automation script ready to run

❌ **You need to provide:**
- OpenAI API key (or have Ollama running locally)

## Option 1: Using OpenAI (Recommended for Quick Demo)

### Step 1: Set up your OpenAI API Key

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file and add your OpenAI API key
# Replace 'your-openai-api-key-here' with your actual key
```

Your `.env` file should look like:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

### Step 2: Run the Demo Automation Script

The automation script will:
1. Start the Streamlit server automatically
2. Enable demo mode and load demo documents
3. Capture 3 screenshots showing different features
4. Record a demo video (15-25 seconds)
5. Stop the server and save all assets

Run the script:
```bash
python -m demo_tools.capture_demo
```

### Step 3: Find Your Demo Assets

The script will create a timestamped directory with your demo assets:
```
demo_tools/output/YYYY-MM-DD_HHMMSS/
├── 01_indexed_files.png    # Screenshot showing indexed documents
├── 02_answer.png            # Screenshot showing Q&A interaction
├── 03_sources.png           # Screenshot showing source citations
└── demo.mp4                 # Screen recording of the demo
```

## Option 2: Using Ollama (Local/Offline Mode)

If you prefer to use local models with Ollama:

### Step 1: Install and Set Up Ollama

```bash
# Install Ollama from https://ollama.ai

# Pull required models
ollama pull llama3
ollama pull nomic-embed-text

# Start Ollama (if not running)
ollama serve
```

### Step 2: Update Configuration

Edit `config/config.example.yaml` to use Ollama:
```yaml
models:
  provider: "ollama"   # Change from "openai" to "ollama"
```

### Step 3: Run the Demo Script

```bash
python -m demo_tools.capture_demo
```

Note: No OPENAI_API_KEY needed when using Ollama.

## Option 3: Manual Demo (Without Automation)

If you want to manually demonstrate the app:

### Step 1: Start the Server

```bash
python -m scripts.run_streamlit
```

The app will open at http://localhost:8501

### Step 2: Use the Demo Mode

1. In the sidebar, check the "Demo mode" checkbox
2. Click "Load demo documents" button
3. Wait for indexing to complete
4. Select a suggested question from the dropdown
5. Click "Insert question" to add it to the chat
6. Click "Send" or "Ask" to submit
7. Wait for the AI to generate an answer with citations

### Step 3: Take Screenshots Manually

Use your preferred screenshot tool to capture:
- The app with indexed files visible
- A question and answer interaction
- The sources/citations section

### Step 4: Record Video Manually

Use screen recording software like:
- **macOS**: QuickTime Player (File > New Screen Recording)
- **Windows**: Xbox Game Bar (Win + G)
- **Linux**: OBS Studio, SimpleScreenRecorder
- **Browser**: Browser extensions like Loom

Record a 15-25 second walkthrough showing:
1. Demo mode enabled
2. Loading demo documents
3. Selecting and submitting a question
4. Answer appearing with sources

## Demo Assets Overview

The demo captures showcase:

### Screenshot 1: Indexed Files
- Shows the sidebar with demo documents indexed
- Displays configuration options
- Demonstrates the file upload and indexing feature

### Screenshot 2: Q&A Interaction
- Shows a question being asked about HR policies
- Displays the AI-generated answer
- Demonstrates the chat interface

### Screenshot 3: Source Citations
- Shows the sources used to generate the answer
- Displays page numbers (for PDFs) and file names
- Demonstrates the citation system

### Demo Video
- 15-25 second recording showing the complete workflow
- Enables demo mode → loads documents → asks question → shows answer with citations
- Professional quality for product launch materials

## Troubleshooting

### "OPENAI_API_KEY not found"
- Ensure you created a `.env` file in the project root
- Verify the key is correctly formatted (starts with `sk-`)
- Check that the `.env` file contains: `OPENAI_API_KEY=your-key-here`

### "Playwright not installed"
- The dependencies should already be installed in this environment
- If needed, run: `pip install -r demo_tools/requirements-demo.txt`
- Then: `python -m playwright install chromium`

### "Demo documents not loading"
- The demo files are located in `demo_assets/` directory
- Files included: HR handbook, lease agreement, Q4 sales data
- These are automatically loaded by the demo mode

### "Streamlit not starting"
- Check if port 8501 is already in use
- Try stopping any existing Streamlit processes
- Verify all dependencies are installed: `pip install -r requirements.txt`

### "Video not capturing"
- Ensure ffmpeg is installed for MP4 conversion
- The script saves video even without ffmpeg (as webm in mp4 container)
- Video duration depends on how long the automation takes

## What's Included in Demo Assets

### Demo Documents (demo_assets/)
- **HR Handbook** (hr/employee_handbook_demo.txt) - Employee policies, benefits, vacation
- **Lease Agreement** (legal/lease_agreement_demo.txt) - Rental contract with terms
- **Q4 Sales Data** (commerce/sales_q4_demo.csv) - Product sales data with metrics

### Demo Questions (demo_assets/demo_questions.json)
Pre-written questions for each domain:
- **HR**: Vacation policies, sick days, remote work
- **Legal**: Contract terms, deposits, maintenance
- **Commerce**: Product margins, revenue, growth trends

## Using Demo Assets for Product Launch

The generated screenshots and video are perfect for:
- **Landing pages**: Show the product in action
- **Documentation**: Visual guides and tutorials
- **Social media**: Share feature highlights
- **Presentations**: Demo the product to stakeholders
- **Marketing materials**: Professional product showcase

## Best Practices

1. **Use OpenAI for demos**: Faster, more consistent responses
2. **Keep video short**: 15-25 seconds is ideal for attention span
3. **Show real value**: Use meaningful questions that demonstrate capabilities
4. **Quality matters**: 1280x720 resolution is good for web use
5. **Test first**: Run the automation once to verify everything works

## Next Steps After Demo Capture

1. Review all generated assets for quality
2. Edit/crop screenshots if needed
3. Add annotations or highlights to screenshots
4. Upload assets to your website/marketing materials
5. Share on social media for product launch
6. Include in documentation and tutorials

---

**Need help?** Check the main [README.md](README.md) for more information about the application itself.
