"""
Citation formatting utilities.
"""
from typing import List, Dict, Any
from collections import defaultdict
from langchain.schema import Document

from core.logging_utils import get_logger

logger = get_logger(__name__)


def format_citations(documents: List[Document]) -> str:
    """
    Format citations from retrieved documents as plain text list.
    
    Args:
        documents: List of retrieved documents with metadata
        
    Returns:
        Formatted citation string
    """
    if not documents:
        return ""
    
    # Group by filename and collect page numbers
    citations_by_file: Dict[str, Any] = defaultdict(lambda: {
        'pages': set(),
        'filetype': None
    })
    
    for doc in documents:
        metadata = doc.metadata
        filename = metadata.get('filename', 'Unknown')
        filetype = metadata.get('filetype', '')
        page = metadata.get('page')
        
        citations_by_file[filename]['filetype'] = filetype
        if page is not None:
            citations_by_file[filename]['pages'].add(page)
    
    # Format citations as plain text list
    citation_parts = []
    for filename, data in sorted(citations_by_file.items()):
        pages = sorted(data['pages']) if data['pages'] else []
        
        if pages:
            # Format page ranges
            page_str = _format_page_ranges(pages)
            citation_parts.append(f"• {filename} (pages {page_str})")
        else:
            citation_parts.append(f"• {filename}")
    
    return "\n".join(citation_parts)


def _format_page_ranges(pages: List[int]) -> str:
    """
    Format a list of page numbers into ranges.
    
    Args:
        pages: Sorted list of page numbers
        
    Returns:
        Formatted string like "1-3, 5, 7-9"
    """
    if not pages:
        return ""
    
    ranges = []
    start = pages[0]
    end = pages[0]
    
    for page in pages[1:]:
        if page == end + 1:
            end = page
        else:
            if start == end:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}–{end}")
            start = page
            end = page
    
    # Add the last range
    if start == end:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}–{end}")
    
    return ", ".join(ranges)


def create_sources_section(documents: List[Document]) -> str:
    """
    Create a formatted sources section for display.
    
    Args:
        documents: List of retrieved documents
        
    Returns:
        Formatted sources section with header
    """
    if not documents:
        return ""
    
    citations = format_citations(documents)
    
    if citations:
        return f"\n\nSources:\n\n{citations}"
    
    return ""
