"""
Main Streamlit application for DocuMind - Premium SaaS UI.
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
from core.demo import DemoConfig
from app.ui_components import (
    inject_custom_css,
    render_header,
    render_settings_modal,
    render_documents_pane,
    render_chat_pane,
    render_sources_drawer,
    show_success,
    show_error,
    show_info,
    show_warning
)

logger = get_logger(__name__)

# Page config
st.set_page_config(
    page_title="DocuMind - Ask your documents",
    page_icon="💭",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start with sidebar hidden
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
            show_error(f"Configuration error: {e}", inline=False)
            st.stop()
    
    if 'embeddings' not in st.session_state:
        st.session_state.embeddings = None
    
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    
    if 'rag_pipeline' not in st.session_state:
        st.session_state.rag_pipeline = None
    
    if 'indexed_files' not in st.session_state:
        st.session_state.indexed_files = []
    
    # Demo mode state
    if 'demo_loaded' not in st.session_state:
        st.session_state.demo_loaded = False
    
    if 'demo_config' not in st.session_state:
        st.session_state.demo_config = DemoConfig()
    
    if 'demo_questions' not in st.session_state:
        st.session_state.demo_questions = {}
    
    # UI state
    if 'show_settings' not in st.session_state:
        st.session_state.show_settings = False
    
    if 'show_sources_for' not in st.session_state:
        st.session_state.show_sources_for = None
    
    if 'show_upload_dialog' not in st.session_state:
        st.session_state.show_upload_dialog = False
    
    if 'msg_count' not in st.session_state:
        st.session_state.msg_count = 0


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
                    "⚠️ OPENAI_API_KEY not found. Please set it in your .env file or environment variables.",
                    inline=False
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
        show_error(f"Error initializing application: {e}", inline=False)
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
            documents, failed_files = ingestor.ingest_multiple(file_objects=file_objects)
            
            if documents:
                # Add to vector store
                st.session_state.vector_store.add_documents(documents)
                
                # Update indexed files
                st.session_state.indexed_files = st.session_state.vector_store.get_indexed_files()
                
                success_count = len(uploaded_files) - len(failed_files)
                show_success(f"✅ Successfully indexed {success_count} file(s) with {len(documents)} chunks!")
                
                # Show failed files if any
                if failed_files:
                    show_warning(f"⚠️ Failed to process {len(failed_files)} file(s):")
                    for filename, error in failed_files:
                        st.text(f"  • {filename}: {error}")
            else:
                show_warning("No documents were extracted from the uploaded files.")
    
    except Exception as e:
        logger.error(f"Error processing files: {e}")
        show_error(f"Error processing files: {e}")


def handle_demo_load(ingestor: DocumentIngestor):
    """
    Handle loading demo documents.
    
    Args:
        ingestor: DocumentIngestor instance
    """
    # Check if already loaded
    if st.session_state.demo_loaded:
        show_info("✅ Demo documents already loaded!")
        return
    
    try:
        # Validate demo assets exist
        assets_valid, missing = st.session_state.demo_config.validate_demo_assets()
        if not assets_valid:
            show_error(f"Demo assets missing: {', '.join(missing)}")
            return
        
        # Get demo file paths
        demo_paths = st.session_state.demo_config.get_demo_file_paths()
        
        if not demo_paths:
            show_error("No demo files found!")
            return
        
        with st.spinner(f"Loading {len(demo_paths)} demo files..."):
            # Ingest demo files
            documents, failed_files = ingestor.ingest_multiple(file_paths=demo_paths)
            
            if documents:
                # Add to vector store
                st.session_state.vector_store.add_documents(documents)
                
                # Update indexed files
                st.session_state.indexed_files = st.session_state.vector_store.get_indexed_files()
                
                # Mark demo as loaded
                st.session_state.demo_loaded = True
                
                # Load demo questions
                st.session_state.demo_questions = st.session_state.demo_config.load_demo_questions()
                
                success_msg = f"✅ Demo documents indexed: {len(demo_paths)} files, {len(documents)} chunks!"
                show_success(success_msg)
                
                if failed_files:
                    show_warning(f"⚠️ Some files failed: {len(failed_files)}")
            else:
                show_error("Failed to extract documents from demo files.")
    
    except Exception as e:
        logger.error(f"Error loading demo documents: {e}")
        show_error(f"Error loading demo documents: {e}")


def handle_chat_input(prompt: str, top_k: int, citations_enabled: bool):
    """
    Handle user chat input and generate response.
    
    Args:
        prompt: User's question
        top_k: Number of documents to retrieve
        citations_enabled: Whether to include citations
    """
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})
    st.session_state.msg_count += 1
    
    # Generate response
    try:
        answer, documents = st.session_state.rag_pipeline.query(
            prompt,
            top_k=top_k,
            include_citations=citations_enabled
        )
        
        # Prepare sources for the sources drawer
        sources = []
        if citations_enabled and documents:
            for doc in documents:
                source = {
                    'filename': doc.metadata.get('filename', 'Unknown'),
                    'page': f"Page {doc.metadata.get('page', 'unknown')}",
                    'snippet': doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                }
                sources.append(source)
        
        # Add assistant message to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })
        st.session_state.msg_count += 1
        
    except Exception as e:
        error_msg = f"Error generating response: {e}"
        logger.error(error_msg)
        show_error(error_msg)
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"I encountered an error: {e}",
            "sources": []
        })


def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Inject custom CSS
    inject_custom_css()
    
    # Render header
    header_actions = render_header()
    
    # Handle settings button
    if header_actions['settings_clicked']:
        st.session_state.show_settings = not st.session_state.show_settings
    
    # Show settings modal if open
    config_values = None
    if st.session_state.show_settings:
        with st.expander("⚙️ Settings", expanded=True):
            config_values = render_settings_modal(st.session_state.config)
            if st.button("Close Settings", use_container_width=True):
                st.session_state.show_settings = False
                st.rerun()
    
    # Use current config if settings not changed
    if config_values is None:
        config_values = {
            'provider': st.session_state.config.model_provider,
            'citations_enabled': st.session_state.config.citations_enabled,
            'top_k': st.session_state.config.top_k,
            'chunk_size': st.session_state.config.chunk_size,
            'chunk_overlap': st.session_state.config.chunk_overlap
        }
    
    # Initialize components if not already done or if provider changed
    if (st.session_state.vector_store is None or 
        st.session_state.rag_pipeline is None or
        st.session_state.rag_pipeline.provider != config_values['provider']):
        initialize_components(config_values['provider'])
    
    # Create ingestor with current config
    ingestor = DocumentIngestor(st.session_state.config)
    
    # Two-pane layout
    if st.session_state.show_sources_for is not None:
        # Three-column layout with sources drawer
        left_col, middle_col, right_col = st.columns([2, 3, 2])
    else:
        # Two-column layout without sources
        left_col, middle_col = st.columns([2, 5])
        right_col = None
    
    # Left pane: Documents
    with left_col:
        doc_actions = render_documents_pane(
            st.session_state.indexed_files,
            on_upload=None,
            on_load_demo=None,
            on_search=None
        )
        
        # Handle upload button
        if doc_actions['upload_clicked']:
            st.session_state.show_upload_dialog = True
        
        # Handle load demo button
        if doc_actions['load_demo_clicked']:
            handle_demo_load(ingestor)
            st.rerun()
        
        # Show upload dialog
        if st.session_state.show_upload_dialog:
            st.markdown("---")
            st.markdown("**Upload Documents**")
            uploaded_files = st.file_uploader(
                "Choose files",
                type=['pdf', 'docx', 'txt', 'md', 'csv'],
                accept_multiple_files=True,
                help="Supported formats: PDF, DOCX, TXT, MD, CSV",
                key="file_uploader_widget"
            )
            
            upload_col1, upload_col2 = st.columns(2)
            with upload_col1:
                if st.button("Upload & Index", type="primary", use_container_width=True):
                    if uploaded_files:
                        handle_file_upload(uploaded_files, ingestor)
                        st.session_state.show_upload_dialog = False
                        st.rerun()
                    else:
                        show_warning("Please select files to upload")
            with upload_col2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.show_upload_dialog = False
                    st.rerun()
    
    # Middle pane: Chat
    with middle_col:
        # Get suggested questions if demo is loaded
        suggested_questions = []
        if st.session_state.demo_loaded and st.session_state.demo_questions:
            # Get first 3 questions from all categories
            for category, questions in st.session_state.demo_questions.items():
                suggested_questions.extend(questions[:1])  # Take first from each category
                if len(suggested_questions) >= 3:
                    break
        
        chat_actions = render_chat_pane(
            st.session_state.messages,
            suggested_questions=suggested_questions if not st.session_state.messages else [],
            on_send=None,
            show_sources_for_msg=st.session_state.show_sources_for
        )
        
        # Handle sources button click
        if chat_actions.get('sources_clicked_for') is not None:
            st.session_state.show_sources_for = chat_actions['sources_clicked_for']
            st.rerun()
        
        # Handle send/submit
        if chat_actions['send_clicked'] and chat_actions['prompt']:
            handle_chat_input(
                chat_actions['prompt'],
                config_values['top_k'],
                config_values['citations_enabled']
            )
            st.rerun()
    
    # Right pane: Sources drawer (if showing sources)
    if right_col and st.session_state.show_sources_for is not None:
        with right_col:
            msg_idx = st.session_state.show_sources_for
            if 0 <= msg_idx < len(st.session_state.messages):
                message = st.session_state.messages[msg_idx]
                sources = message.get('sources', [])
                
                def close_sources():
                    st.session_state.show_sources_for = None
                
                render_sources_drawer(sources, on_close=close_sources)
                
                if st.button("✕ Close Sources", use_container_width=True):
                    st.session_state.show_sources_for = None
                    st.rerun()


if __name__ == "__main__":
    main()
