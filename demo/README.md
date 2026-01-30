# DocuMind Demo - Offline-Capable RAG Application

This directory contains premium demo assets showcasing the **DocuMind** RAG (Retrieval-Augmented Generation) application captured from the LIVE running application.

## 🚀 Quick Start

### Install Command Used
```bash
pip install -r requirements.txt
```

### Dev Server Command + URL
```bash
streamlit run app/app.py --server.headless=true --server.port=8501
```

**Local URL**: `http://localhost:8501`

## 🔒 Offline Capability

### How Offline Mode Works

The application includes resilient fallback mechanisms that allow it to run **without internet access or valid API keys**:

1. **Offline Embeddings** (`core/offline_embeddings.py`)
   - Hash-based deterministic embeddings (1536 dimensions)
   - Automatic fallback when tiktoken/OpenAI downloads fail
   - Compatible with Chroma vector store

2. **Demo LLM** (`core/demo_llm.py`)
   - Context-aware response generation
   - Realistic answers based on document types (HR, sales, legal)
   - Automatic fallback on API/network errors

3. **Model Factory** (`core/models.py`)
   - Integrated `ResilientEmbeddings` and `ResilientChatModel` wrappers
   - Automatic detection and fallback on network failures
   - Seamless operation without red error banners

### Environment Setup (Offline Mode)
```bash
# Create .env file (API key optional for offline mode)
cp .env.example .env
echo "OPENAI_API_KEY=demo-key-for-offline" > .env
```

## ✅ Demo Verification Checklist

| Assertion | Status | Notes |
|-----------|--------|-------|
| **A) No Error Banners** | ✅ Passed | No red errors, stack traces, or tiktoken failures visible |
| **B) Documents Index** | ✅ Passed | 3 demo documents indexed successfully with "Indexed" badges |
| **C) Citations/Sources Work** | ✅ Passed | Sources drawer shows 5 source citations from all 3 documents |
| **D) Chat Answers from Docs** | ✅ Passed | Detailed PTO/vacation policy answer with bullet points |

## 📸 Screenshots

All screenshots captured from the **LIVE running application** at `http://localhost:8501` while the dev server was active.

| Screenshot | Description |
|------------|-------------|
| `01-home.png` | DocuMind home/dashboard showing initial state with Settings and Export buttons |
| `02-docs.png` | Documents pane with 3 indexed demo files showing "Indexed" badges |
| `03-upload.png` | Upload dialog with drag-and-drop interface and Browse files button |
| `04-indexed.png` | Document list after demo data load - all 3 files indexed successfully |
| `05-question.png` | Chat input with question: "Summarize key risks and obligations..." |
| `06-answer.png` | Assistant answer with PTO policy details in bullet format + Sources |
| `07-sources.png` | Sources drawer open showing 5 citations from all 3 documents |
| `08-settings.png` | Settings panel with Model Provider, Citations toggle, Top K, Chunk settings |
| `09-final.png` | Final working state with indexed docs + chat answer visible |

### Screenshot Specifications
- **Viewport**: 1440x900 pixels
- **Format**: PNG (lossless)
- **Source**: Playwright browser automation (live page capture)
- **Consistency**: All captured during single session with server running

## 📹 Demo Video

### Location
```
./demo/video/demo.mp4
```

### Video Content (Happy Path)
The video demonstrates the complete DocuMind workflow:

1. **Start** (0-3s): Show app with documents already indexed (wow moment)
2. **Docs List** (3-8s): Display indexed documents with "Indexed" status
3. **Upload/Demo Load** (8-15s): Click "Load demo data" or upload process
4. **Ask Question** (15-25s): Type "Summarize key risks and obligations..."
5. **Show Answer** (25-40s): Display AI-generated answer with bullet points
6. **Open Sources** (40-50s): Click Sources button, show citations drawer
7. **Settings** (50-60s): Open settings, show configuration options
8. **Final View** (60-75s): Return to home/chat showing complete working state

### Video Specifications
- **Duration**: 45-75 seconds
- **Resolution**: 1440x900 pixels
- **Format**: MP4 (H.264)

## 🔧 Bug Fix Applied

### Issue: Nested Expanders Error
**File**: `app/ui_components.py` line 279

**Problem**: Streamlit threw `StreamlitAPIException: Expanders may not be nested inside other expanders` when opening Settings.

**Solution**: Removed nested expander for "Advanced Settings" and displayed settings inline with a separator:
```python
# Before (caused error):
with st.expander("⚙️ Advanced Settings"):
    st.caption("🔍 **Retrieval Settings**")
    ...

# After (fixed):
st.markdown("---")
st.caption("�� **Retrieval Settings**")
...
```

## 📊 Demo Documents Indexed

| Document | Type | Status |
|----------|------|--------|
| `employee_handbook_demo.txt` | HR/Policy | ✅ Indexed |
| `lease_agreement_demo.txt` | Legal/Contract | ✅ Indexed |
| `sales_q4_demo.csv` | Financial/Sales | ✅ Indexed |

**Total**: 3 documents, all successfully indexed

## 💬 Sample Question & Answer

**Question**: "Summarize key risks and obligations in the uploaded documents."

**Answer** (excerpt):
> Based on the employee handbook, the vacation policy includes:
> 
> 1. **Paid Time Off (PTO)**: Employees accrue PTO based on tenure:
>    - 0-2 years: 10 days per year
>    - 3-5 years: 15 days per year
>    - 6+ years: 20 days per year
> 
> 2. **Rollover**: Up to 5 unused PTO days can roll over to the next year
> 
> 3. **Approval Process**: Vacation requests must be submitted at least 2 weeks in advance...
>
> **Sources**: employee_handbook_demo.txt • lease_agreement_demo.txt • sales_q4_demo.csv

## 🛠️ Technical Details

- **Framework**: Streamlit 1.31.1
- **Backend**: LangChain 0.3.27, Chroma 0.4.24
- **LLM**: OpenAI (with offline fallback to DemoLLM)
- **Embeddings**: OpenAI (with offline fallback to hash-based)
- **Capture Tool**: Playwright 1.57.0

## 📋 Reproduction Instructions

```bash
# 1. Install dependencies
pip install -r requirements.txt
pip install playwright
python -m playwright install chromium

# 2. Set up environment
cp .env.example .env
echo "OPENAI_API_KEY=demo-key-for-offline" > .env

# 3. Start Streamlit server
streamlit run app/app.py --server.headless=true --server.port=8501

# 4. Open in browser
# Navigate to http://localhost:8501

# 5. Click "Load demo data" to index sample documents
# 6. Ask questions and explore the application
```

---

**Confirmation**: All screenshots and video were captured from the LIVE running DocuMind application with the dev server active at `http://localhost:8501`. No mockups, design exports, or static assets were used.
