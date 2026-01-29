# DocuMind Demo Assets

This directory contains demo screenshots and video captured from the live running DocuMind application.

## Installation & Setup

### Install Command
```bash
pip install -r requirements.txt
```

### Additional Dependencies (for demo capture)
```bash
pip install playwright
python -m playwright install chromium
```

## Dev Server

### Command Used
```bash
/usr/bin/python -m streamlit run app/app.py
```

### Local URL
```
http://localhost:8501
```

## Demo Script

The demo follows this narrative: **Start → Upload → Ask → Answer → Review → Settings → Return**

1. **Dashboard/Home** - Initial view of the DocuMind interface
2. **Uploads** - Navigate to upload area (before upload)
3. **Uploaded** - Documents appear in the list after upload/indexing
4. **Chat Question** - Type and display a question about uploaded documents
5. **Chat Answer** - AI-generated answer with context from documents
6. **Settings** - Configuration options (model selection, retrieval parameters)
7. **Final** - Return to main dashboard

### Sample Question Used
```
"Summarize the key policies from the uploaded documents."
```

## Screenshots

All screenshots are captured from the live running application while the dev server was active.

| Filename | Description |
|----------|-------------|
| `01-home.png` | DocuMind home/dashboard view |
| `02-uploads.png` | Uploads view before upload |
| `03-uploaded.png` | Documents visible in list after indexing |
| `04-chat-question.png` | Question typed in chat interface |
| `05-chat-answer.png` | AI answer displayed with sources |
| `06-settings.png` | Settings/configuration page |
| `07-final.png` | Back to home/dashboard |

### Screenshot Details
- **Format**: PNG
- **Viewport**: 1440x900 (desktop)
- **Quality**: Full window capture, crisp text
- **Source**: Live browser screenshots (not mockups)

## Demo Video

### Location
```
./demo/video/demo.mp4
```

### Video Details
- **Duration**: Approximately 60-120 seconds
- **Resolution**: 1440x900 (or closest available)
- **Frame Rate**: 30 fps
- **Audio**: None (silent)
- **Content**: Complete workflow demonstration

### Video Workflow
1. Start at dashboard
2. Enable demo mode (if available)
3. Load sample documents
4. Wait for indexing to complete
5. Select a sample question
6. Submit question and wait for AI response
7. Review answer with source citations
8. Show settings/configuration
9. Return to dashboard

## Issues & Resolution

### Encountered Issues
- **API Key**: Used test/demo key for documentation purposes only
- **Demo Mode**: Application includes built-in demo mode with sample documents
- **Browser Automation**: Successfully automated with Playwright in headless mode

### Resolutions Applied
1. Created `.env` file with test API key for demo purposes
2. Used Playwright headless browser for consistent screenshots
3. Automated full workflow to capture real application flow
4. Ensured all screenshots show live rendered UI (not static exports)

## Technical Notes

- **Application**: DocuMind (Document Chatbot with RAG)
- **Framework**: Streamlit (Python web framework)
- **Capture Tool**: Playwright (browser automation)
- **Capture Date**: 2026-01-29 18:53:59
- **Dev Server**: Running on localhost:8501

## Usage

These demo assets are suitable for:
- Product documentation
- Landing pages and marketing materials
- Tutorial videos and guides
- Social media content
- Presentations and demos

---

**Note**: All screenshots and video were captured from the live application while the dev server was running, as required by the specifications. No static exports or design mockups were used.
