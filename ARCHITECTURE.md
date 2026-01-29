# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface (Streamlit)                │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ File Upload  │  │ Chat Input   │  │  Settings Sidebar  │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Application Layer (app/)                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  app.py - Main application logic & state management     │  │
│  │  ui_components.py - UI helper functions                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Core Layer (core/)                        │
│                                                                  │
│  ┌────────────────┐    ┌────────────────┐   ┌──────────────┐  │
│  │   config.py    │    │   models.py    │   │  ingest.py   │  │
│  │                │    │                │   │              │  │
│  │ Load config    │    │ LLM Factory    │   │ Parse docs   │  │
│  │ from YAML      │    │ - OpenAI       │   │ - PDF        │  │
│  │ & env vars     │    │ - Ollama       │   │ - DOCX       │  │
│  └────────────────┘    │ Embeddings     │   │ - TXT/MD     │  │
│                        │ Factory        │   │ - CSV        │  │
│                        └────────────────┘   │ Chunking     │  │
│                                             └──────────────┘  │
│                                                                  │
│  ┌────────────────┐    ┌────────────────┐   ┌──────────────┐  │
│  │ vectorstore.py │    │    rag.py      │   │ citations.py │  │
│  │                │    │                │   │              │  │
│  │ Chroma DB      │◄───│ Retrieval      │   │ Format       │  │
│  │ - Add docs     │    │ Generation     │───│ sources      │  │
│  │ - Search       │    │ Prompting      │   │ Page ranges  │  │
│  │ - Persist      │    └────────────────┘   └──────────────┘  │
│  └────────────────┘                                            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  logging_utils.py - Structured logging                 │   │
│  └────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External Services & Storage                   │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌─────────────────┐  │
│  │  OpenAI API  │    │  Ollama API  │    │  Chroma DB      │  │
│  │  (optional)  │    │  (optional)  │    │  (persistent)   │  │
│  │              │    │              │    │  ./data/chroma  │  │
│  │ • GPT models │    │ • llama3     │    │                 │  │
│  │ • Embeddings │    │ • nomic-embed│    │ • Vector index  │  │
│  └──────────────┘    └──────────────┘    │ • Metadata      │  │
│                                           └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Document Ingestion Flow
```
User Upload → File Parser (ingest.py) → Text Chunker → Metadata Extraction
     │              │                        │                │
     │         (PDF/DOCX/TXT/CSV)     (RecursiveText)    (filename,
     │                                  (900 chars)      page, type)
     │                                      │                │
     └──────────────────────────────────────┴────────────────┘
                                            │
                                            ▼
                                    Embedding Model
                                    (OpenAI/Ollama)
                                            │
                                            ▼
                                    Vector Store (Chroma)
                                    [Persistent Storage]
```

### 2. Query Flow (RAG Pipeline)
```
User Question → Embedding Model → Vector Search (top_k) → Context Assembly
      │               │                  │                       │
      │         (vectorize)        (similarity)            (format chunks)
      │               │                  │                       │
      └───────────────┴──────────────────┴───────────────────────┘
                                            │
                                            ▼
                            Prompt Template + Context + Question
                                            │
                                            ▼
                                      LLM (ChatGPT/Llama3)
                                            │
                                            ▼
                                    Generated Answer
                                            │
                                            ▼
                            (if citations enabled) → Format Sources
                                            │
                                            ▼
                                    Return to User
```

## Component Responsibilities

### Core Components

| Component | File | Responsibility |
|-----------|------|----------------|
| Configuration | `core/config.py` | Load YAML config and environment variables |
| Document Ingestion | `core/ingest.py` | Parse documents, extract text, create chunks |
| Vector Store | `core/vectorstore.py` | Manage Chroma DB, add/search documents |
| RAG Pipeline | `core/rag.py` | Retrieve context, generate answers |
| Citations | `core/citations.py` | Format source attributions |
| Models | `core/models.py` | Factory for LLMs and embeddings |
| Logging | `core/logging_utils.py` | Structured logging utilities |

### Application Layer

| Component | File | Responsibility |
|-----------|------|----------------|
| Main App | `app/app.py` | Streamlit UI, state management, orchestration |
| UI Components | `app/ui_components.py` | Reusable UI widgets and helpers |

### Scripts

| Script | File | Purpose |
|--------|------|---------|
| Run App | `scripts/run_streamlit.py` | Launch Streamlit application |
| CLI Ingest | `scripts/ingest_cli.py` | Command-line document ingestion |
| Demo | `scripts/demo.py` | System demonstration |

## Configuration Hierarchy

```
Environment Variables (.env)
        ↓
YAML Configuration (config.example.yaml)
        ↓
Runtime Overrides (UI Sidebar)
        ↓
Application State (session_state)
```

## Data Models

### Document Chunk
```python
Document(
    page_content: str,           # Actual text content
    metadata: {
        'filename': str,         # Source file name
        'filetype': str,         # pdf, docx, txt, md, csv
        'page': int (optional)   # Page number for PDFs
    }
)
```

### Vector Store Entry
```
{
    'id': str,                   # Unique document chunk ID
    'embedding': List[float],    # Vector representation
    'document': str,             # Text content
    'metadata': Dict             # Chunk metadata
}
```

## State Management (Streamlit)

```python
session_state = {
    'messages': List[Dict],           # Chat history
    'config': Config,                 # Application config
    'embeddings': Embeddings,         # Embedding model
    'vector_store': VectorStore,      # Vector DB instance
    'rag_pipeline': RAGPipeline,      # RAG instance
    'indexed_files': List[str]        # List of filenames
}
```

## Design Patterns Used

1. **Factory Pattern** - `ModelFactory` for creating LLMs and embeddings
2. **Singleton Pattern** - Global config instance via `get_config()`
3. **Strategy Pattern** - Pluggable providers (OpenAI vs Ollama)
4. **Chain of Responsibility** - LangChain LCEL chains
5. **Repository Pattern** - `VectorStore` abstraction over Chroma

## Key Design Decisions

### Why LangChain?
- Standard RAG components pre-built
- Easy switching between LLM providers
- LCEL for composable chains
- Active community and updates

### Why Chroma?
- Lightweight and easy to set up
- Persistent storage out of the box
- No separate server needed
- Good for prototyping and small-scale deployments

### Why Streamlit?
- Rapid UI development
- Python-native (no JavaScript)
- Built-in session state
- Perfect for data apps and demos

### Chunking Strategy
- **RecursiveCharacterTextSplitter**: Preserves semantic meaning
- **900 characters**: Balance between context and precision
- **150 overlap**: Maintains continuity across chunks
- **Separators**: Prioritizes natural boundaries (\n\n, \n, ., space)

### Retrieval Strategy
- **Similarity Search**: Vector-based semantic search
- **Top K = 5**: Good balance for most use cases
- **No Re-ranking**: Keep it simple for MVP
- **Metadata Filtering**: Available but not used by default

## Extension Points

### Adding New Document Types
1. Add parser method to `DocumentIngestor`
2. Update `SUPPORTED_EXTENSIONS`
3. Handle metadata appropriately
4. Add tests

### Adding New Vector Stores
1. Create wrapper class similar to `VectorStore`
2. Implement same interface
3. Update config to support selection
4. Update `vectorstore.py` with factory pattern

### Adding New LLM Providers
1. Update `ModelFactory.create_chat_model()`
2. Add config section for new provider
3. Handle authentication
4. Test thoroughly

### Custom Prompts
1. Modify `RAG_PROMPT_TEMPLATE` in `rag.py`
2. Add prompt templates to config
3. Allow runtime selection

## Security Considerations

- ✅ API keys in environment variables, not code
- ✅ No hardcoded secrets
- ✅ Input validation on file uploads
- ✅ Error messages don't leak sensitive info
- ✅ Local storage of vector data
- ⚠️ No authentication (add for production)
- ⚠️ No rate limiting (add for production)
- ⚠️ No input sanitization for prompts (low risk for private use)

## Performance Considerations

### Bottlenecks
1. **Document Parsing**: Large PDFs can be slow
2. **Embedding Generation**: Network latency for OpenAI
3. **Vector Search**: Scales sub-linearly with document count
4. **LLM Response**: Network latency + generation time

### Optimizations
- Batch embedding generation for multiple documents
- Use local Ollama for faster embeddings
- Reduce chunk_size for faster processing
- Lower top_k for faster retrieval
- Use faster models (e.g., gpt-3.5-turbo vs gpt-4)

## Testing Strategy

### Unit Tests
- Config loading and validation
- Document parsing and chunking
- Citation formatting
- Vector store operations

### Integration Tests
- End-to-end RAG pipeline
- Multi-document ingestion
- Search and retrieval accuracy

### Manual Tests
- UI functionality
- Error handling
- Edge cases (empty docs, large files)
- Provider switching

---

This architecture is designed to be:
- **Modular**: Easy to swap components
- **Extensible**: Add features without major refactoring  
- **Testable**: Clear interfaces and separation of concerns
- **Maintainable**: Simple, readable code with good documentation
- **Reusable**: Perfect template for client deliveries
