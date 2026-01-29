# Document Chatbot - RAG Application

A production-ready, reusable **Retrieval-Augmented Generation (RAG)** application that enables users to upload documents and interact with them through natural language conversations. Built with Streamlit, LangChain, and Chroma vector store.

## 🎯 What It Is

This is a "ChatGPT for Documents" application that allows you to:
- Upload multiple documents (PDF, DOCX, TXT, MD, CSV)
- Ask questions about the content in natural language
- Get accurate answers with citations showing source documents and page numbers
- Switch between OpenAI and Ollama (local) models
- Customize retrieval and chunking parameters

## ✨ Features

- **Multi-format Support**: PDF, DOCX, TXT, Markdown, CSV
- **Smart Citations**: Automatic source attribution with page numbers for PDFs
- **Configurable RAG Pipeline**: Adjust chunk size, overlap, and retrieval parameters
- **Provider Flexibility**: Switch between OpenAI and Ollama models
- **Persistent Storage**: Vector store persists across sessions
- **Clean UI**: Intuitive Streamlit interface with chat history
- **Safe Fallbacks**: Honest responses when information isn't found in documents

## 📋 Supported File Types

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Extracts text with page numbers |
| Word | `.docx` | Full document text extraction |
| Text | `.txt` | Plain text files |
| Markdown | `.md` | Formatted text files |
| CSV | `.csv` | Converts to text summaries (up to 1000 rows) |

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- OpenAI API key (for OpenAI provider)
- Optional: Ollama installed locally (for local models)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jakops88-hub/Demo-assistent.git
   cd Demo-assistent
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # On Windows: copy .env.example .env
   ```

   Edit `.env` and add:
   ```
   OPENAI_API_KEY=your-openai-api-key-here
   ```

5. **Copy the configuration file**
   ```bash
   # This step is optional - the app uses config.example.yaml by default
   cp config/config.example.yaml config/config.yaml
   ```

### Running the Application

**Option 1: Using the run script (recommended)**
```bash
python -m scripts.run_streamlit
```

**Option 2: Direct Streamlit command**
```bash
streamlit run app/app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 How to Use

### Uploading Documents

1. Use the file uploader in the main area
2. Select one or more files (PDF, DOCX, TXT, MD, CSV)
3. Click "📥 Index Files" to process and store them
4. Wait for the success message

### Chatting with Documents

1. Type your question in the chat input at the bottom
2. Press Enter to submit
3. The system will:
   - Retrieve relevant document chunks
   - Generate an answer using only the document content
   - Show citations if enabled

### Configuration Options (Sidebar)

- **Provider**: Choose between OpenAI or Ollama
- **Enable Citations**: Toggle source attribution on/off
- **Top K Results**: Number of document chunks to retrieve (1-20)
- **Chunk Size**: Text chunk size for processing (100-2000)
- **Chunk Overlap**: Overlap between chunks (0-500)

### Actions

- **🔄 Re-index Documents**: Clear the vector store and start fresh
- **🗑️ Clear Chat History**: Reset the conversation

## ⚙️ Configuration

The main configuration file is `config/config.example.yaml`:

```yaml
project_name: "Document Chatbot"
storage_dir: "./data"

vectorstore:
  type: "chroma"
  persist_dir: "./data/chroma"

chunking:
  chunk_size: 900
  chunk_overlap: 150

retrieval:
  top_k: 5

models:
  provider: "openai"   # openai | ollama
  openai:
    chat_model: "gpt-4o-mini"
    embeddings_model: "text-embedding-3-small"
  ollama:
    chat_model: "llama3"
    embeddings_model: "nomic-embed-text"

features:
  citations: true
```

### Switching to Ollama (Local Models)

1. **Install Ollama** from [ollama.ai](https://ollama.ai)

2. **Pull the required models**
   ```bash
   ollama pull llama3
   ollama pull nomic-embed-text
   ```

3. **Update configuration** (or use sidebar)
   - Set `models.provider: "ollama"` in config file
   - Or select "ollama" from the Provider dropdown in the UI

4. **No API key required** for Ollama

## 📚 How Citations Work

When citations are enabled:
- The system tracks which documents and pages were used to generate answers
- Citations are displayed below the answer in a "Sources" section
- Format for PDFs: `filename.pdf (pages 1-3, 5)`
- Format for other files: `filename.txt`
- Page ranges are automatically consolidated (e.g., 1, 2, 3 becomes 1-3)

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_config.py -v

# Run with coverage
pytest tests/ --cov=core --cov=app
```

## 🛠️ CLI Tools

### Ingest Documents via CLI

You can also ingest documents from the command line:

```bash
python -m scripts.ingest_cli file1.pdf file2.txt file3.docx

# With options
python -m scripts.ingest_cli --clear --provider openai documents/*.pdf
```

Options:
- `--clear`: Clear vector store before ingesting
- `--provider`: Specify model provider (openai/ollama)
- `--config`: Path to config file

## 📁 Project Structure

```
Demo-assistent/
├── app/
│   ├── app.py              # Main Streamlit application
│   └── ui_components.py    # UI helper components
├── core/
│   ├── config.py           # Configuration loader
│   ├── ingest.py           # Document ingestion and chunking
│   ├── vectorstore.py      # Chroma vector store wrapper
│   ├── rag.py              # RAG pipeline
│   ├── citations.py        # Citation formatting
│   ├── models.py           # LLM and embeddings factory
│   └── logging_utils.py    # Logging utilities
├── scripts/
│   ├── run_streamlit.py    # Streamlit launcher
│   └── ingest_cli.py       # CLI ingestion tool
├── config/
│   └── config.example.yaml # Example configuration
├── tests/                  # Test suite
├── data/                   # Data directory (created on first run)
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore patterns
└── README.md              # This file
```

## 🔒 Security & Privacy

- **No hardcoded secrets**: API keys are loaded from environment variables
- **Local storage**: All data stays on your machine
- **No telemetry**: No data is sent anywhere except to your chosen LLM provider

## ⚠️ Limitations

1. **Context Window**: Limited by the LLM's context window (handled by chunk retrieval)
2. **Accuracy**: Depends on document quality and LLM capabilities
3. **Large Files**: Very large files (100+ MB) may take time to process
4. **No Training**: This is RAG only - the model is not fine-tuned on your data
5. **Honest Fallbacks**: If the answer isn't in the documents, the system will say so

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you've created a `.env` file
- Ensure `OPENAI_API_KEY` is set correctly
- On Windows, check that environment variables are loaded

### "No module named 'streamlit'"
- Activate your virtual environment
- Run `pip install -r requirements.txt`

### "Error initializing vector store"
- Check that the `data/chroma` directory is writable
- Try deleting `data/chroma` and restarting

### Ollama not connecting
- Ensure Ollama is running: `ollama serve`
- Check that models are installed: `ollama list`
- Verify Ollama host (default: http://localhost:11434)

### Documents not indexing
- Check file format is supported
- Ensure files aren't corrupted
- Check logs for specific error messages

## 🤝 Contributing

This is a reusable base template for Fiverr deliveries. Feel free to:
- Fork and customize for your clients
- Add new file format support
- Implement additional vector stores
- Enhance the UI/UX

## 📄 License

This project is provided as-is for reuse and customization.

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web UI framework
- [LangChain](https://langchain.com/) - RAG framework
- [Chroma](https://www.trychroma.com/) - Vector database
- [OpenAI](https://openai.com/) - LLM and embeddings
- [Ollama](https://ollama.ai/) - Local LLM support

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the test files for usage examples
3. Open an issue on GitHub

---

**Ready to use for your next Fiverr client delivery!** 🚀
