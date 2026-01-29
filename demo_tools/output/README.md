# Demo Assets Output Directory

This directory will contain your generated demo assets after running the demo capture script.

## Directory Structure

After running the demo capture, you'll find timestamped folders here:

```
demo_tools/output/
├── 2026-01-29_182245/
│   ├── 01_indexed_files.png
│   ├── 02_answer.png
│   ├── 03_sources.png
│   └── demo.mp4
├── 2026-01-29_190330/
│   ├── 01_indexed_files.png
│   ├── 02_answer.png
│   ├── 03_sources.png
│   └── demo.mp4
└── README.md (this file)
```

Each timestamp folder (format: `YYYY-MM-DD_HHMMSS`) represents one demo capture session.

## Generated Files

### 1. 01_indexed_files.png
**Purpose:** Shows the application with demo documents successfully indexed

**What it shows:**
- Sidebar with "Indexed Files" section displaying demo documents
- Demo mode checkbox enabled
- Configuration options (Provider, Citations, etc.)
- Clean, professional view of the document management interface

**Use for:**
- Demonstrating document upload and indexing capabilities
- Showing the user interface and configuration options
- Highlighting the supported file formats

**Typical size:** 100-300 KB  
**Resolution:** 1280x720 pixels

---

### 2. 02_answer.png
**Purpose:** Shows the Q&A interaction with the chatbot

**What it shows:**
- User question in the chat interface (about HR vacation policy)
- AI-generated answer based on document content
- Chat history showing the conversation flow
- Clean, readable answer with proper formatting

**Use for:**
- Demonstrating the core RAG (Retrieval-Augmented Generation) functionality
- Showing natural language interaction capabilities
- Highlighting answer quality and relevance
- Proving the system can extract and synthesize information from documents

**Typical size:** 150-400 KB  
**Resolution:** 1280x720 pixels

---

### 3. 03_sources.png
**Purpose:** Shows the source citations and attribution

**What it shows:**
- Sources section below the answer
- File names of source documents
- Page numbers (for PDF files) or file references
- Proper citation formatting with consolidated page ranges

**Use for:**
- Demonstrating transparency and source attribution
- Showing the citation system
- Proving answers are grounded in actual document content
- Highlighting the trustworthiness of the system

**Typical size:** 150-400 KB  
**Resolution:** 1280x720 pixels

---

### 4. demo.mp4
**Purpose:** Complete video demonstration of the workflow

**What it shows:**
- Enabling demo mode
- Loading demo documents
- Indexing progress
- Selecting a question
- Submitting the question
- Answer generation
- Source citations appearing
- Smooth transitions between all steps

**Use for:**
- Product landing page hero video
- Social media demonstrations
- Presentation introductions
- Tutorial introductions
- Marketing campaigns
- Product launch announcements

**Typical duration:** 15-25 seconds  
**Typical size:** 2-5 MB  
**Format:** MP4 (H.264 if ffmpeg available, WebM in MP4 container otherwise)  
**Resolution:** 1280x720 pixels

## Using Your Assets

### For Websites
- Hero section: Use demo.mp4 as autoplay background video
- Features section: Use screenshots to illustrate capabilities
- How it works: Use screenshots as step-by-step guide

### For Documentation
- Getting started guide: Use screenshots as visual aids
- Feature documentation: Use specific screenshots to show features
- Video tutorials: Use demo.mp4 as introduction

### For Marketing
- Social media posts: Share screenshots with feature highlights
- Email campaigns: Include screenshots to show product value
- Landing pages: Use video to capture attention
- Product announcements: Attach screenshots and video

### For Presentations
- Slide decks: Insert screenshots on relevant slides
- Demos: Play video instead of live demo if time is limited
- Pitch decks: Show product capabilities visually

## Quality Specifications

All assets are generated with professional quality:

- **Resolution:** 1280x720 (720p HD) - Perfect for web use
- **Format:** PNG for screenshots (lossless), MP4 for video
- **Viewport:** Consistent 1280x720 across all captures
- **Timing:** Proper settling time between actions (1200ms for screenshots)
- **Content:** Real demo documents with meaningful questions and answers

## File Naming Convention

Files are named for easy sorting and identification:

- `01_` prefix = First step (indexed files)
- `02_` prefix = Second step (answer)
- `03_` prefix = Third step (sources)
- No prefix on video = `demo.mp4` (easy to identify)

This ensures files sort correctly in file managers.

## Timestamp Format

Each folder uses `YYYY-MM-DD_HHMMSS` format:

- `2026-01-29_182245` = January 29, 2026 at 6:22:45 PM
- This ensures folders sort chronologically
- Easy to identify when each demo was captured
- No conflicts when running multiple times

## Managing Multiple Demos

If you run the demo capture multiple times:

1. Each run creates a new timestamped folder
2. Previous demos are preserved (not overwritten)
3. You can compare different runs
4. Keep the best version for your launch

**Tip:** After generating several demos, delete the folders you don't want to keep the directory clean.

## Asset Optimization

### For Web Use

**Screenshots:**
- Already optimized as PNG at 720p
- Can compress further with tools like TinyPNG if needed
- Good balance of quality and file size

**Video:**
- MP4 format is web-friendly
- Can compress further with HandBrake if needed
- Consider hosting on YouTube/Vimeo for better streaming

### For Print/High-Res

If you need higher resolution:
- Edit `capture_demo.py` line ~203
- Change viewport to `{'width': 1920, 'height': 1080}`
- Re-run the capture

## Troubleshooting

### Missing Files

If some files are missing:
- Check terminal output for specific errors
- Look for `error.png` in the folder (debug screenshot)
- Re-run the demo capture script
- Check that demo documents exist in `demo_assets/`

### Low Quality Video

If video quality is poor:
- Install ffmpeg for proper MP4 encoding
- Check internet connection (affects OpenAI API speed)
- Ensure system isn't under heavy load during capture

### Wrong Content

If screenshots show unexpected content:
- Verify demo mode was enabled
- Check that demo documents loaded successfully
- Ensure OpenAI API key is valid and has credits
- Review terminal output for warnings

## Next Steps

1. **Review** all generated assets for quality
2. **Select** the best version if you ran multiple captures
3. **Optimize** files if needed (compression, cropping)
4. **Organize** assets into your product launch folder
5. **Backup** to cloud storage or version control
6. **Deploy** to your website, documentation, and marketing materials
7. **Launch** your product! 🚀

## Need More Assets?

To generate additional demos:
- Just run the capture script again
- Each run creates a new folder
- Experiment with different settings if needed
- Keep the best results

## Support

For help with demo assets:
- See [DEMO_CAPTURE_GUIDE.md](../DEMO_CAPTURE_GUIDE.md)
- See [DEMO_QUICK_START.md](../DEMO_QUICK_START.md)
- See [demo_tools/README.md](README.md)
- Open an issue on GitHub

---

**Your demo assets are ready to help you launch your product successfully!** 🎉
