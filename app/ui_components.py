"""
UI component helpers for Streamlit.
"""
import streamlit as st
from typing import List, Tuple


def render_sidebar_config(config) -> dict:
    """
    Render sidebar configuration controls.
    
    Args:
        config: Application configuration
        
    Returns:
        Dictionary of user-selected configuration values
    """
    st.sidebar.title(config.project_name)
    st.sidebar.markdown("---")
    
    # Model provider selection
    st.sidebar.subheader("🤖 Model Settings")
    provider = st.sidebar.selectbox(
        "Provider",
        options=["openai", "ollama"],
        index=0 if config.model_provider == "openai" else 1,
        help="Select the LLM provider (OpenAI or Ollama)"
    )
    
    # Citations toggle
    st.sidebar.subheader("📚 Features")
    citations_enabled = st.sidebar.checkbox(
        "Enable Citations",
        value=config.citations_enabled,
        help="Show source documents and page numbers in responses"
    )
    
    # Retrieval settings
    st.sidebar.subheader("🔍 Retrieval Settings")
    top_k = st.sidebar.slider(
        "Top K Results",
        min_value=1,
        max_value=20,
        value=config.top_k,
        help="Number of document chunks to retrieve"
    )
    
    # Chunking settings
    st.sidebar.subheader("📄 Chunking Settings")
    st.sidebar.caption("⚠️ Changes require re-indexing documents")
    chunk_size = st.sidebar.number_input(
        "Chunk Size",
        min_value=100,
        max_value=2000,
        value=config.chunk_size,
        step=100,
        help="Size of text chunks for processing"
    )
    
    chunk_overlap = st.sidebar.number_input(
        "Chunk Overlap",
        min_value=0,
        max_value=500,
        value=config.chunk_overlap,
        step=50,
        help="Overlap between consecutive chunks"
    )
    
    return {
        'provider': provider,
        'citations_enabled': citations_enabled,
        'top_k': top_k,
        'chunk_size': chunk_size,
        'chunk_overlap': chunk_overlap
    }


def render_sidebar_actions() -> dict:
    """
    Render sidebar action buttons.
    
    Returns:
        Dictionary with button states
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Actions")
    
    reindex = st.sidebar.button(
        "🔄 Re-index Documents",
        help="Clear and re-index all documents",
        use_container_width=True
    )
    
    clear_chat = st.sidebar.button(
        "🗑️ Clear Chat History",
        help="Clear the conversation history",
        use_container_width=True
    )
    
    return {
        'reindex': reindex,
        'clear_chat': clear_chat
    }


def render_indexed_files(filenames: List[str]):
    """
    Render the list of indexed files.
    
    Args:
        filenames: List of indexed file names
    """
    if filenames:
        st.sidebar.markdown("---")
        st.sidebar.subheader("📁 Indexed Files")
        for filename in filenames:
            st.sidebar.text(f"• {filename}")
        st.sidebar.caption(f"Total: {len(filenames)} files")
    else:
        st.sidebar.markdown("---")
        st.sidebar.info("No files indexed yet")


def render_chat_message(role: str, content: str):
    """
    Render a chat message.
    
    Args:
        role: Message role (user or assistant)
        content: Message content
    """
    with st.chat_message(role):
        st.markdown(content)


def render_chat_history(messages: List[dict]):
    """
    Render chat history.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
    """
    for message in messages:
        render_chat_message(message['role'], message['content'])


def show_success(message: str):
    """Show success message."""
    st.success(message)


def show_error(message: str):
    """Show error message."""
    st.error(message)


def show_info(message: str):
    """Show info message."""
    st.info(message)


def show_warning(message: str):
    """Show warning message."""
    st.warning(message)
