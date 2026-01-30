"""
UI component helpers for Streamlit - Premium SaaS Design.
"""
import streamlit as st
from typing import List, Tuple, Dict, Optional


def inject_custom_css():
    """Inject custom CSS for premium SaaS look."""
    st.markdown("""
    <style>
    /* Premium SaaS styling */
    .main {
        padding-top: 1rem;
    }
    
    /* Header styling */
    .documind-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0 1.5rem 0;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    
    .documind-logo {
        font-size: 1.75rem;
        font-weight: 700;
        color: #6366f1;
        margin: 0;
    }
    
    .documind-tagline {
        font-size: 0.875rem;
        color: #64748b;
        margin-top: 0.25rem;
    }
    
    /* Pane styling */
    .documind-pane {
        background: white;
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
        height: 700px;
        overflow-y: auto;
    }
    
    .documind-pane-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0 0 1rem 0;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .status-indexed {
        background: #dcfce7;
        color: #166534;
    }
    
    .status-processing {
        background: #fef3c7;
        color: #92400e;
    }
    
    .status-failed {
        background: #fee2e2;
        color: #991b1b;
    }
    
    /* Document list items */
    .doc-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        background: #ffffff;
    }
    
    .doc-item:hover {
        background: #f8fafc;
        border-color: #cbd5e1;
    }
    
    .doc-info {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        flex: 1;
    }
    
    .doc-icon {
        font-size: 1.5rem;
    }
    
    .doc-name {
        font-weight: 500;
        color: #1e293b;
    }
    
    /* Suggested question chips */
    .question-chip {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 9999px;
        margin: 0.25rem;
        cursor: pointer;
        font-size: 0.875rem;
        color: #475569;
        transition: all 0.2s;
    }
    
    .question-chip:hover {
        background: #e0e7ff;
        border-color: #6366f1;
        color: #4f46e5;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
    
    .empty-state-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .empty-state-text {
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    
    /* Sources drawer */
    .sources-drawer {
        background: white;
        border-left: 1px solid #e2e8f0;
        padding: 1.5rem;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .source-item {
        padding: 1rem;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        margin-bottom: 0.75rem;
        background: #f8fafc;
    }
    
    .source-filename {
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.25rem;
    }
    
    .source-page {
        font-size: 0.875rem;
        color: #64748b;
        margin-bottom: 0.5rem;
    }
    
    .source-snippet {
        font-size: 0.875rem;
        color: #475569;
        font-style: italic;
    }
    
    /* Button hierarchy */
    .stButton button[kind="primary"] {
        background: #6366f1;
        border: none;
    }
    
    .stButton button[kind="primary"]:hover {
        background: #4f46e5;
    }
    
    .stButton button[kind="secondary"] {
        background: white;
        border: 1px solid #e2e8f0;
        color: #475569;
    }
    
    /* Fix focus outline to purple accent instead of red */
    .stButton button:focus,
    .stButton button:focus-visible {
        outline: 2px solid #6366f1 !important;
        outline-offset: 2px;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
    
    .stTextInput input:focus,
    .stTextInput input:focus-visible,
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextInput"] input:focus-visible {
        border-color: #6366f1 !important;
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
    
    .stSelectbox [data-testid="stSelectbox"]:focus-within,
    .stNumberInput input:focus,
    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Override Streamlit's default red focus ring */
    *:focus {
        outline-color: #6366f1 !important;
    }
    
    *:focus-visible {
        outline-color: #6366f1 !important;
    }
    
    /* Hide sidebar by default for clean two-pane layout */
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    /* Show sidebar when settings are open */
    section[data-testid="stSidebar"].show-sidebar {
        display: block;
    }
    
    /* Inline notice (not banner) */
    .inline-notice {
        padding: 0.75rem;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        margin: 0.5rem 0;
    }
    
    .inline-notice-error {
        background: #fef2f2;
        color: #991b1b;
        border-left: 3px solid #dc2626;
    }
    
    .inline-notice-warning {
        background: #fffbeb;
        color: #92400e;
        border-left: 3px solid #f59e0b;
    }
    
    .inline-notice-info {
        background: #eff6ff;
        color: #1e40af;
        border-left: 3px solid #3b82f6;
    }
    
    .inline-notice-success {
        background: #f0fdf4;
        color: #166534;
        border-left: 3px solid #22c55e;
    }
    </style>
    """, unsafe_allow_html=True)


def render_settings_modal(config) -> dict:
    """
    Render settings modal with advanced options.
    
    Args:
        config: Application configuration
        
    Returns:
        Dictionary of user-selected configuration values
    """
    # Basic settings (always visible)
    provider = st.selectbox(
        "Model Provider",
        options=["openai", "ollama"],
        index=0 if config.model_provider == "openai" else 1,
        help="Select the LLM provider (OpenAI or Ollama)"
    )
    
    citations_enabled = st.checkbox(
        "Enable Citations",
        value=config.citations_enabled,
        help="Show source documents and page numbers in responses"
    )
    
    # Advanced settings (inline, no nested expander)
    st.markdown("---")
    st.caption("🔍 **Retrieval Settings**")
    top_k = st.slider(
        "Top K Results",
        min_value=1,
        max_value=20,
        value=config.top_k,
        help="Number of document chunks to retrieve"
    )
    
    st.caption("📄 **Chunking Settings**")
    st.caption("⚠️ Changes require re-indexing documents")
    chunk_size = st.number_input(
        "Chunk Size",
        min_value=100,
        max_value=2000,
        value=config.chunk_size,
        step=100,
        help="Size of text chunks for processing"
    )
    
    chunk_overlap = st.number_input(
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


def render_header(on_settings_click=None, on_export_click=None):
    """
    Render the DocuMind header.
    
    Args:
        on_settings_click: Callback for settings button
        on_export_click: Callback for export button
    """
    st.markdown("""
    <div class="documind-header">
        <div>
            <div class="documind-logo">DocuMind</div>
            <div class="documind-tagline">Ask your documents with sources</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Settings and Export buttons in columns
    header_col1, header_col2, header_col3 = st.columns([6, 1, 1])
    with header_col2:
        settings_clicked = st.button("⚙️ Settings", use_container_width=True, key="header_settings_btn")
    with header_col3:
        export_clicked = st.button("📤 Export", use_container_width=True, key="header_export_btn", disabled=True, help="Export feature coming soon")
    
    return {
        'settings_clicked': settings_clicked,
        'export_clicked': export_clicked
    }


def render_document_item(filename: str, status: str = "Indexed", on_remove=None):
    """
    Render a single document item with icon, name, status badge, and actions.
    
    Args:
        filename: Name of the file
        status: Status (Indexed, Processing, Failed)
        on_remove: Callback for remove action
    """
    # Determine icon based on file extension
    ext = filename.lower().split('.')[-1]
    icon_map = {
        'pdf': '📄',
        'docx': '📝',
        'txt': '📃',
        'md': '📋',
        'csv': '📊'
    }
    icon = icon_map.get(ext, '📄')
    
    # Status badge color
    status_class = f"status-{status.lower()}"
    
    col1, col2, col3 = st.columns([0.5, 4, 1])
    with col1:
        st.markdown(f'<div class="doc-icon">{icon}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="doc-name">{filename}</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="status-badge {status_class}">{status}</span>', unsafe_allow_html=True)
    with col3:
        if on_remove:
            if st.button("🗑️", key=f"remove_{filename}", help="Remove document"):
                on_remove(filename)


def render_documents_pane(indexed_files: List[str], on_upload=None, on_load_demo=None, on_search=None):
    """
    Render the Documents pane (left side).
    
    Args:
        indexed_files: List of indexed file names
        on_upload: Callback for upload action
        on_load_demo: Callback for load demo action
        on_search: Callback for search action
        
    Returns:
        Dictionary with action states
    """
    st.markdown('<div class="documind-pane">', unsafe_allow_html=True)
    st.markdown('<h2 class="documind-pane-title">Documents</h2>', unsafe_allow_html=True)
    
    # Search input
    search_query = st.text_input("🔍 Search documents", placeholder="Search by filename...", label_visibility="collapsed", key="doc_search")
    
    st.markdown("") # Spacing
    
    # Action buttons
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        upload_clicked = st.button("📤 Upload", use_container_width=True, type="primary", key="upload_docs_btn")
    with btn_col2:
        load_demo_clicked = st.button("🎬 Load demo data", use_container_width=True, key="load_demo_btn")
    
    st.markdown("---")
    
    # Document list or empty state
    if indexed_files:
        # Filter files based on search
        filtered_files = [f for f in indexed_files if not search_query or search_query.lower() in f.lower()]
        
        if filtered_files:
            for filename in filtered_files:
                render_document_item(filename, status="Indexed")
        else:
            st.info(f"No documents match '{search_query}'")
        
        st.caption(f"📊 Total: {len(indexed_files)} document(s)")
    else:
        # Empty state with illustration
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📚</div>
            <div class="empty-state-title">No documents yet</div>
            <div class="empty-state-text">Upload your documents or load demo data to get started</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'upload_clicked': upload_clicked,
        'load_demo_clicked': load_demo_clicked,
        'search_query': search_query
    }


def render_suggested_questions(questions: List[str], on_click=None):
    """
    Render suggested question chips.
    
    Args:
        questions: List of suggested questions
        on_click: Callback when a question is clicked
    """
    if not questions:
        return None
    
    st.markdown("**💡 Suggested questions:**")
    
    # Display questions as clickable chips
    selected_question = None
    cols = st.columns(len(questions))
    for idx, question in enumerate(questions[:3]):  # Show max 3
        with cols[idx]:
            if st.button(question, key=f"suggested_q_{idx}", use_container_width=True):
                selected_question = question
    
    return selected_question


def render_sources_button(num_sources: int, msg_idx: int) -> bool:
    """
    Render a "Sources (N)" button.
    
    Args:
        num_sources: Number of sources
        msg_idx: Index of the message
        
    Returns:
        True if button was clicked
    """
    return st.button(f"📚 Sources ({num_sources})", key=f"sources_btn_msg_{msg_idx}")


def render_sources_drawer(sources: List[Dict], on_close=None):
    """
    Render the sources drawer/panel.
    
    Args:
        sources: List of source dictionaries with filename, page, snippet
        on_close: Callback for close action
    """
    st.markdown('<div class="sources-drawer">', unsafe_allow_html=True)
    
    # Header with close button
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown("### 📚 Sources")
    with col2:
        if st.button("✕", key="close_sources"):
            if on_close:
                on_close()
    
    st.markdown("---")
    
    # Source items
    for idx, source in enumerate(sources):
        st.markdown(f"""
        <div class="source-item">
            <div class="source-filename">{source.get('filename', 'Unknown')}</div>
            <div class="source-page">{source.get('page', 'Page unknown')}</div>
            <div class="source-snippet">"{source.get('snippet', 'No snippet available')}"</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_chat_pane(messages: List[dict], suggested_questions: List[str] = None, on_send=None, show_sources_for_msg=None):
    """
    Render the Chat pane (right side).
    
    Args:
        messages: List of message dictionaries
        suggested_questions: List of suggested questions to show as chips
        on_send: Callback for send action
        show_sources_for_msg: Index of message to show sources for (or None)
        
    Returns:
        Dictionary with action states including which message's sources button was clicked
    """
    st.markdown('<div class="documind-pane">', unsafe_allow_html=True)
    st.markdown('<h2 class="documind-pane-title">Chat</h2>', unsafe_allow_html=True)
    
    # Suggested questions at top (only if no messages yet)
    selected_suggested = None
    if not messages and suggested_questions:
        selected_suggested = render_suggested_questions(suggested_questions)
    
    st.markdown("---")
    
    # Chat messages
    sources_clicked_for = None
    if messages:
        for idx, message in enumerate(messages):
            render_chat_message(message['role'], message['content'])
            
            # Show sources button for assistant messages
            if message['role'] == 'assistant' and message.get('sources'):
                if render_sources_button(len(message['sources']), idx):
                    sources_clicked_for = idx
    else:
        st.info("👋 Ask a question to get started!")
    
    st.markdown("---")
    
    # Chat input at bottom
    prompt = st.text_input(
        "Message",
        placeholder="Ask about your documents...",
        label_visibility="collapsed",
        key="chat_input_new"
    )
    
    send_clicked = False
    if prompt:
        send_col1, send_col2 = st.columns([6, 1])
        with send_col2:
            send_clicked = st.button("Send", type="primary", use_container_width=True, key="send_msg_btn")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'prompt': prompt if send_clicked else (selected_suggested or ""),
        'send_clicked': send_clicked or bool(selected_suggested),
        'sources_clicked_for': sources_clicked_for
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


def show_success(message: str, inline: bool = True):
    """Show success message as inline notice or banner."""
    if inline:
        st.markdown(f'<div class="inline-notice inline-notice-success">{message}</div>', unsafe_allow_html=True)
    else:
        st.success(message)


def show_error(message: str, inline: bool = True):
    """Show error message as inline notice or banner."""
    if inline:
        st.markdown(f'<div class="inline-notice inline-notice-error">{message}</div>', unsafe_allow_html=True)
    else:
        st.error(message)


def show_info(message: str, inline: bool = True):
    """Show info message as inline notice or banner."""
    if inline:
        st.markdown(f'<div class="inline-notice inline-notice-info">{message}</div>', unsafe_allow_html=True)
    else:
        st.info(message)


def show_warning(message: str, inline: bool = True):
    """Show warning message as inline notice or banner."""
    if inline:
        st.markdown(f'<div class="inline-notice inline-notice-warning">{message}</div>', unsafe_allow_html=True)
    else:
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
                "🔄",
                help="Force re-index demo documents",
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
