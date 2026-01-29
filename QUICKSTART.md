# Quick Start Guide

## Installation & Setup (5 minutes)

### 1. Clone and Install
```bash
git clone https://github.com/jakops88-hub/Demo-assistent.git
cd Demo-assistent
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure API Key
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-key-here
```

### 3. Run the Application
```bash
python -m scripts.run_streamlit
```

The app will open at http://localhost:8501

## First Time Usage

### Upload Documents
1. Click **Browse files** in the Upload Documents section
2. Select one or more files (PDF, DOCX, TXT, MD, CSV)
3. Click **📥 Index Files** button
4. Wait for "✅ Successfully indexed..." message

### Ask Questions
1. Type your question in the chat input at the bottom
2. Press Enter
3. Wait for the AI to generate an answer
4. Sources will be shown if citations are enabled

### Adjust Settings (Sidebar)
- **Provider**: Switch between OpenAI and Ollama
- **Enable Citations**: Toggle sources on/off
- **Top K Results**: More = more context, slower response
- **Chunk Size**: Larger = more context per chunk
- **Chunk Overlap**: Helps preserve context across boundaries

## Example Workflow

### 1. Upload Technical Documentation
```
Files to upload:
- api_documentation.pdf (100 pages)
- user_manual.docx
- changelog.md
```

### 2. Ask Specific Questions
```
"What are the authentication requirements for the API?"
"How do I configure SSL certificates?"
"What changed in version 2.0?"
```

### 3. Get Cited Answers
```
Response:
The API requires OAuth 2.0 authentication with a client_id 
and client_secret. You must include the access token in the 
Authorization header for all requests.

📚 Sources:
**api_documentation.pdf** (pages 12–15)
```

## Tips for Best Results

### Document Quality
- ✅ Well-formatted PDFs with selectable text
- ✅ Clean DOCX files without excessive formatting
- ✅ Plain text files with clear structure
- ❌ Scanned PDFs (OCR quality affects results)
- ❌ Heavily formatted documents with complex layouts

### Question Phrasing
- ✅ "What are the requirements for X?"
- ✅ "How do I configure Y?"
- ✅ "Explain the difference between A and B"
- ❌ "Tell me everything" (too broad)
- ❌ Questions about content not in documents

### Configuration Tuning
- **Small documents** (< 10 pages): chunk_size=500, top_k=3
- **Medium documents** (10-100 pages): chunk_size=900, top_k=5
- **Large documents** (100+ pages): chunk_size=1200, top_k=7

## Using Ollama (Local Models)

### Setup
```bash
# Install Ollama from https://ollama.ai

# Pull models
ollama pull llama3
ollama pull nomic-embed-text

# Start Ollama (if not running)
ollama serve
```

### Switch to Ollama
1. In sidebar, select **Provider**: ollama
2. Or edit config/config.example.yaml:
   ```yaml
   models:
     provider: "ollama"
   ```

### Benefits
- ✅ No API costs
- ✅ Complete privacy (runs locally)
- ✅ Works offline
- ❌ Slower than OpenAI
- ❌ May have lower quality answers

## Troubleshooting

### "OPENAI_API_KEY not found"
```bash
# Check .env file exists
ls -la .env

# Verify key is set correctly
cat .env | grep OPENAI_API_KEY

# Reload environment
source .env  # On macOS/Linux
```

### "No documents have been indexed"
1. Upload documents using the file uploader
2. Click "📥 Index Files" button
3. Check for success message
4. Verify files appear in "Indexed Files" sidebar

### "Error initializing vector store"
```bash
# Clear the database
rm -rf data/chroma

# Restart the application
python -m scripts.run_streamlit
```

### Documents Not Processing
- Check file format is supported
- Ensure file is not corrupted
- Check file size (very large files may timeout)
- Look for error messages in terminal

### Slow Response Times
- Reduce **Top K Results** in sidebar
- Use smaller **Chunk Size**
- Check internet connection (for OpenAI)
- Consider using Ollama locally

## Advanced Usage

### CLI Ingestion
```bash
# Ingest documents from command line
python -m scripts.ingest_cli docs/*.pdf docs/*.txt

# Clear and re-ingest
python -m scripts.ingest_cli --clear docs/*.pdf

# Use specific provider
python -m scripts.ingest_cli --provider ollama docs/*.pdf
```

### Custom Configuration
```bash
# Copy and edit config
cp config/config.example.yaml config/config.yaml

# Edit settings
nano config/config.yaml

# Application will use config.yaml if it exists
```

### Batch Processing
```python
# Custom script example
from core.config import get_config
from core.ingest import DocumentIngestor
from core.vectorstore import VectorStore
from core.models import create_embeddings

config = get_config()
embeddings = create_embeddings(config)
vector_store = VectorStore(config, embeddings)
ingestor = DocumentIngestor(config)

# Process all PDFs in a directory
import glob
files = glob.glob("documents/**/*.pdf", recursive=True)
docs = ingestor.ingest_multiple(file_paths=files)
vector_store.add_documents(docs)
```

## Next Steps

1. **Customize for Your Use Case**
   - Update project_name in config
   - Adjust default chunk_size for your documents
   - Set preferred model provider

2. **Prepare for Clients**
   - Add client's documents
   - Test with expected questions
   - Adjust retrieval parameters
   - Create custom prompts if needed

3. **Deploy (Optional)**
   - Use Streamlit Cloud
   - Deploy on AWS/Azure/GCP
   - Use Docker for containerization

## Getting Help

- 📖 Read the full README.md
- 🧪 Check tests/ for code examples
- 🐛 Review error messages in terminal
- 💬 Open GitHub issue for bugs

---

**You're ready to deliver document chat solutions to clients!** 🚀
