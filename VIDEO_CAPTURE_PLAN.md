# DocuMind Demo Video Capture Plan

## Overview
This document outlines the "happy path" demo video capture plan for DocuMind, showcasing the premium SaaS UI and key features.

## Video Specifications
- **Duration**: 20-30 seconds
- **Resolution**: 1280x720 (720p) minimum
- **Frame Rate**: 30 fps
- **Format**: MP4 (H.264 codec)

## Scene Breakdown (Total: ~25 seconds)

### Scene 1: Landing Page (3 seconds)
**What to show:**
- Clean DocuMind header with tagline "Ask your documents with sources"
- Two-pane layout: empty Documents pane on left, Chat pane on right
- Settings and Export buttons in header
- Empty state with "No documents yet" message and call-to-action buttons

**Actions:**
- Pan slightly across the interface to show the clean design
- Highlight the modern, spacious layout

### Scene 2: Loading Demo Data (4 seconds)
**What to show:**
- Click "🎬 Load demo data" button in Documents pane
- Brief loading animation
- Documents appear with file icons and "Indexed" status badges
- Document counter shows "📊 Total: 3 document(s)"

**Actions:**
1. Move cursor to "Load demo data" button
2. Click button
3. Show brief loading (1-2 seconds)
4. Documents populate with smooth transition

### Scene 3: Suggested Questions (2 seconds)
**What to show:**
- Chat pane displays three suggested question chips
- Clean, clickable chip design with hover state

**Actions:**
- Hover over suggested question chips to show hover effect
- Pause briefly to let viewers read the questions

### Scene 4: Ask a Question (5 seconds)
**What to show:**
- Click on first suggested question chip
- Question appears in chat as user message
- Loading/thinking indicator
- AI-generated answer appears with formatting

**Actions:**
1. Click first suggested question: "What is the vacation policy..."
2. Show question appearing in chat bubble
3. Show brief "thinking" state
4. Answer streams in with proper formatting

### Scene 5: View Sources (6 seconds)
**What to show:**
- "📚 Sources (N)" button below the answer
- Click sources button
- Sources drawer slides in from right side
- Three-column layout: Documents | Chat | Sources
- Sources displayed with filename, page number, and snippet preview

**Actions:**
1. Highlight the "Sources" button
2. Click sources button
3. Sources drawer animates in smoothly
4. Pan through 2-3 source items to show detail
5. Pause on sources drawer (2 seconds)

### Scene 6: Closing Shot (5 seconds)
**What to show:**
- Zoom out slightly to show complete three-column layout
- Fade to DocuMind logo/branding

**Actions:**
- Smooth zoom out
- Show complete interface with all three panes visible
- Optional: Add "DocuMind - Ask your documents with sources" text overlay

## Pre-Recording Checklist

### Environment Setup
- [ ] Streamlit server running on localhost:8501
- [ ] Browser window sized to 1280x720 or 1920x1080
- [ ] Browser zoom at 100%
- [ ] Demo data ready to load (3 files: HR handbook, lease agreement, Q4 sales)
- [ ] Valid API key configured (or demo mode enabled)

### UI Preparation
- [ ] Clear any existing chat history
- [ ] Clear vector store (fresh state)
- [ ] Close all unnecessary browser tabs
- [ ] Hide browser bookmarks bar
- [ ] Disable browser extensions that might show notifications
- [ ] Turn off system notifications

### Recording Software Setup
- [ ] Screen recording software installed (OBS Studio, Camtasia, or QuickTime)
- [ ] Recording area set to capture full browser window
- [ ] Audio muted (no narration needed for this demo)
- [ ] Recording quality set to at least 720p at 30fps
- [ ] Output format set to MP4 (H.264)

## Recording Steps

### 1. Start Recording
```bash
# Option 1: Using FFmpeg (command line)
ffmpeg -f x11grab -s 1280x720 -i :0.0+100,100 -r 30 -vcodec libx264 -preset medium documind_demo.mp4

# Option 2: Using OBS Studio
# Configure scene with browser window capture
# Start recording
```

### 2. Execute Demo Actions
Follow the scene breakdown above, performing each action smoothly and deliberately:
- Take 1-2 second pauses between major actions
- Move cursor smoothly (not too fast)
- Click precisely on buttons/chips
- Allow UI transitions to complete before next action

### 3. Stop Recording
- Wait 2 seconds after final scene
- Stop recording software
- Save video file

## Post-Production (Optional)

### Editing Suggestions
- Trim any dead time at start/end
- Add subtle background music (royalty-free)
- Add text overlays for key features:
  - "Two-Pane Layout"
  - "Suggested Questions"
  - "AI-Powered Answers"
  - "Source Citations with Preview"
- Add fade in/out transitions at start/end
- Add DocuMind logo watermark in corner

### Quality Check
- [ ] Video plays smoothly at 30fps
- [ ] All UI elements are clearly visible
- [ ] Text is readable at 720p
- [ ] No audio issues (if music added)
- [ ] Video duration is 20-30 seconds
- [ ] File size is reasonable (< 50MB)

## Video Script / Narration (Optional)

If adding voice-over narration:

> "DocuMind - the premium document Q&A platform. Load your documents with one click. Ask natural language questions. Get AI-powered answers with full source citations. See exactly where each answer comes from with our intuitive sources drawer. DocuMind - Ask your documents with sources."

## Automated Capture Script

For automated video capture using Playwright, use the `capture_documind_demo.py` script:

```bash
# Run automated demo capture
python capture_documind_demo.py

# Output will be saved to:
# demo_tools/output/YYYY-MM-DD_HHMMSS/demo.mp4
```

The automated script will:
1. Start Streamlit server automatically
2. Navigate to the app
3. Execute all demo actions
4. Capture video
5. Save screenshots
6. Stop server

## Distribution

### Where to Use the Video
1. **GitHub Repository**: Embed in README.md
2. **Landing Page**: Hero section autoplay video
3. **Social Media**: Twitter, LinkedIn product announcements
4. **Documentation**: Getting started guide
5. **Product Hunt**: Launch video
6. **YouTube**: Product demo channel

### Video Hosting Options
- GitHub Releases (< 25MB)
- YouTube (unlisted for embedding)
- Vimeo Pro
- Self-hosted on CDN
- Cloudinary/Imgix for video optimization

## Success Metrics

A successful demo video should:
- ✅ Load in < 3 seconds
- ✅ Show all key features in < 30 seconds
- ✅ Be viewable on mobile devices
- ✅ Work without audio (visual-only storytelling)
- ✅ Have clear, professional UI throughout
- ✅ Demonstrate the "wow factor" of sources drawer

## Notes

### Best Practices
- Keep cursor movements smooth and purposeful
- Don't rush through interactions
- Let animations/transitions complete
- Show real, meaningful demo data
- Highlight the premium, polished UI

### Common Pitfalls to Avoid
- ❌ Don't show loading errors or timeouts
- ❌ Don't use placeholder/lorem ipsum text
- ❌ Don't rush through important features
- ❌ Don't show browser chrome/tabs (full screen app only)
- ❌ Don't show personal information or API keys

## Timeline

| Task | Duration | Deliverable |
|------|----------|-------------|
| Environment setup | 5 minutes | Clean demo environment |
| Recording | 3-5 takes | Raw video file |
| Review & select best take | 5 minutes | Selected raw video |
| Post-production (optional) | 15-30 minutes | Edited video |
| Upload & distribute | 10 minutes | Video available online |

**Total time**: 35-55 minutes for complete video production

---

**Last Updated**: 2026-01-30
**Version**: 1.0
**Status**: Ready for production
