"""
Main Streamlit application for Document Chatbot.
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import get_config
from core.ingest import DocumentIngestor
from core.vectorstore import VectorStore
from core.models import create_embeddings
from core.rag import RAGPipeline
from core.logging_utils import get_logger
from app.ui_components import (
    render_sidebar_config,
    render_sidebar_actions,
    render_indexed_files,
    render_chat_history,
    render_chat_message,
    show_success,
    show_error,
    show_info,
    show_warning
)

logger = get_logger(__name__)

# Page config
st.set_page_config(
    page_title="Document Chatbot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'config' not in st.session_state:
        try:
            st.session_state.config = get_config()
            st.session_state.config.validate()
        except Exception as e:
            st.error(f"Configuration error: {e}")
            st.stop()
    
    if 'embeddings' not in st.session_state:
        st.session_state.embeddings = None
    
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    
    if 'rag_pipeline' not in st.session_state:
        st.session_state.rag_pipeline = None
    
    if 'indexed_files' not in st.session_state:
        st.session_state.indexed_files = []


def initialize_components(provider: str):
    """
    Initialize or reinitialize embeddings, vector store, and RAG pipeline.
    
    Args:
        provider: Model provider (openai or ollama)
    """
    try:
        # Check API key for OpenAI
        if provider == 'openai':
            import os
            if not os.getenv('OPENAI_API_KEY'):
                show_error(
                    "⚠️ OPENAI_API_KEY not found. Please set it in your .env file or environment variables."
                )
                st.stop()
        
        # Create embeddings
        with st.spinner("Initializing embeddings..."):
            st.session_state.embeddings = create_embeddings(
                st.session_state.config,
                provider
            )
        
        # Create vector store
        with st.spinner("Loading vector store..."):
            st.session_state.vector_store = VectorStore(
                st.session_state.config,
                st.session_state.embeddings
            )
        
        # Create RAG pipeline
        with st.spinner("Initializing RAG pipeline..."):
            st.session_state.rag_pipeline = RAGPipeline(
                st.session_state.config,
                st.session_state.vector_store,
                provider
            )
        
        # Load indexed files
        st.session_state.indexed_files = st.session_state.vector_store.get_indexed_files()
        
        logger.info(f"Components initialized with provider: {provider}")
        
    except Exception as e:
        logger.error(f"Error initializing components: {e}")
        show_error(f"Error initializing application: {e}")
        st.stop()


def handle_file_upload(uploaded_files, ingestor: DocumentIngestor):
    """
    Handle file upload and ingestion.
    
    Args:
        uploaded_files: Uploaded file objects from Streamlit
        ingestor: DocumentIngestor instance
    """
    if not uploaded_files:
        return
    
    try:
        with st.spinner(f"Processing {len(uploaded_files)} file(s)..."):
            # Prepare file objects
            file_objects = []
            for uploaded_file in uploaded_files:
                file_objects.append((uploaded_file, uploaded_file.name))
            
            # Ingest files
            documents = ingestor.ingest_multiple(file_objects=file_objects)
            
            if documents:
                # Add to vector store
                st.session_state.vector_store.add_documents(documents)
                
                # Update indexed files
                st.session_state.indexed_files = st.session_state.vector_store.get_indexed_files()
                
                show_success(f"✅ Successfully indexed {len(uploaded_files)} file(s) with {len(documents)} chunks!")
            else:
                show_warning("No documents were extracted from the uploaded files.")
    
    except Exception as e:
        logger.error(f"Error processing files: {e}")
        show_error(f"Error processing files: {e}")


def handle_reindex(ingestor: DocumentIngestor):
    """
    Handle re-indexing of documents.
    
    Args:
        ingestor: DocumentIngestor instance
    """
    try:
        with st.spinner("Clearing vector store..."):
            st.session_state.vector_store.clear()
            st.session_state.indexed_files = []
        
        show_success("Vector store cleared. Please upload documents to re-index.")
    
    except Exception as e:
        logger.error(f"Error during re-index: {e}")
        show_error(f"Error during re-index: {e}")


def handle_chat_input(prompt: str, top_k: int, citations_enabled: bool):
    """
    Handle user chat input and generate response.
    
    Args:
        prompt: User's question
        top_k: Number of documents to retrieve
        citations_enabled: Whether to include citations
    """
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_chat_message("user", prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer, documents = st.session_state.rag_pipeline.query(
                    prompt,
                    top_k=top_k,
                    include_citations=citations_enabled
                )
                
                st.markdown(answer)
                
                # Add assistant message to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
            
            except Exception as e:
                error_msg = f"Error generating response: {e}"
                logger.error(error_msg)
                st.error(error_msg)


def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar configuration
    config_values = render_sidebar_config(st.session_state.config)
    
    # Render sidebar actions
    actions = render_sidebar_actions()
    
    # Render indexed files in sidebar
    render_indexed_files(st.session_state.indexed_files)
    
    # Initialize components if not already done or if provider changed
    if (st.session_state.vector_store is None or 
        st.session_state.rag_pipeline is None or
        st.session_state.rag_pipeline.provider != config_values['provider']):
        initialize_components(config_values['provider'])
    
    # Handle clear chat action
    if actions['clear_chat']:
        st.session_state.messages = []
        st.rerun()
    
    # Main content area
    st.title("📚 Document Chatbot")
    st.markdown("Upload documents and ask questions about them!")
    
    # File upload section
    st.subheader("📤 Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose files",
        type=['pdf', 'docx', 'txt', 'md', 'csv'],
        accept_multiple_files=True,
        help="Supported formats: PDF, DOCX, TXT, MD, CSV"
    )
    
    # Create ingestor with current config
    ingestor = DocumentIngestor(st.session_state.config)
    
    # Update chunk settings if changed
    if (config_values['chunk_size'] != st.session_state.config.chunk_size or
        config_values['chunk_overlap'] != st.session_state.config.chunk_overlap):
        ingestor.text_splitter.chunk_size = config_values['chunk_size']
        ingestor.text_splitter.chunk_overlap = config_values['chunk_overlap']
    
    # Handle file upload
    if uploaded_files:
        if st.button("📥 Index Files", type="primary"):
            handle_file_upload(uploaded_files, ingestor)
    
    # Handle re-index action
    if actions['reindex']:
        handle_reindex(ingestor)
        st.rerun()
    
    # Chat section
    st.markdown("---")
    st.subheader("💬 Chat")
    
    # Display chat history
    render_chat_history(st.session_state.messages)
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        handle_chat_input(
            prompt,
            config_values['top_k'],
            config_values['citations_enabled']
        )


if __name__ == "__main__":
    main()
