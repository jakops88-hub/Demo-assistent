"""
UI component helpers for Streamlit.
"""
import streamlit as st
from typing import List, Tuple, Dict, Optional


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
        "Force re-index",
        help="Clear and re-index all documents",
        use_container_width=True,
        key="sidebar_force_reindex"
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
        st.sidebar.subheader("Indexed files")
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


def render_demo_mode_controls(demo_questions: Dict[str, List[str]]) -> dict:
    """
    Render demo mode controls in sidebar.
    
    Args:
        demo_questions: Dictionary of demo questions by category
        
    Returns:
        Dictionary with demo mode state
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎬 Demo")
    
    demo_enabled = st.sidebar.checkbox(
        "Demo mode",
        value=False,
        help="Enable demo mode with pre-loaded sample documents"
    )
    
    demo_state = {
        'enabled': demo_enabled,
        'load_clicked': False,
        'force_reindex': False,
        'selected_question': None,
        'insert_clicked': False
    }
    
    if demo_enabled:
        # Load demo documents button
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            demo_state['load_clicked'] = st.button(
                "Load demo documents",
                help="Index demo documents (HR, Legal, Commerce)",
                use_container_width=True,
                key="load_demo_docs"
            )
        with col2:
            demo_state['force_reindex'] = st.button(
                "Force re-index",
                help="Force re-index",
                use_container_width=True,
                key="force_reindex_demo"
            )
        
        # Suggested questions
        if demo_questions:
            st.sidebar.markdown("**Suggested questions:**")
            
            # Flatten questions with category prefix
            all_questions = []
            for category, questions in demo_questions.items():
                for q in questions:
                    all_questions.append(f"[{category}] {q}")
            
            selected = st.sidebar.selectbox(
                "Suggested question",
                options=[""] + all_questions,
                help="Choose a demo question to ask"
            )
            
            if selected:
                demo_state['selected_question'] = selected.split("] ", 1)[1] if "] " in selected else selected
                
                demo_state['insert_clicked'] = st.sidebar.button(
                    "Insert question",
                    help="Insert selected question into chat input",
                    use_container_width=True
                )
    
    return demo_state


def render_demo_indicator(demo_loaded: bool):
    """
    Render demo mode indicator at top of main page.
    
    Args:
        demo_loaded: Whether demo data is loaded
    """
    if demo_loaded:
        st.info("🎬 **Demo data loaded** - Using sample documents for demonstration", icon="ℹ️")


def render_status_indicator(demo_loaded: bool, indexing: bool = False) -> str:
    """
    Render status text area showing system state.
    
    Args:
        demo_loaded: Whether demo data is loaded
        indexing: Whether indexing is in progress
        
    Returns:
        Status text string
    """
    if indexing:
        status = "Indexing demo data..."
    elif demo_loaded:
        status = "Demo data loaded"
    else:
        status = "Index ready"
    
    st.text(status)
    return status
