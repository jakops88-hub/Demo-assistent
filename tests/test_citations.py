"""
Tests for citation formatting.
"""
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.citations import format_citations, create_sources_section, _format_page_ranges
from langchain.schema import Document


def test_format_page_ranges():
    """Test page range formatting."""
    assert _format_page_ranges([1]) == "1"
    assert _format_page_ranges([1, 2, 3]) == "1–3"
    assert _format_page_ranges([1, 3, 5]) == "1, 3, 5"
    assert _format_page_ranges([1, 2, 3, 5, 6, 8]) == "1–3, 5–6, 8"
    assert _format_page_ranges([]) == ""


def test_format_citations_with_pages():
    """Test citation formatting with page numbers."""
    documents = [
        Document(
            page_content="Content 1",
            metadata={"filename": "doc.pdf", "filetype": "pdf", "page": 1}
        ),
        Document(
            page_content="Content 2",
            metadata={"filename": "doc.pdf", "filetype": "pdf", "page": 2}
        ),
        Document(
            page_content="Content 3",
            metadata={"filename": "doc.pdf", "filetype": "pdf", "page": 3}
        )
    ]
    
    citations = format_citations(documents)
    
    assert "doc.pdf" in citations
    assert "pages" in citations.lower()
    # Should show range 1-3
    assert "1–3" in citations or "1-3" in citations


def test_format_citations_without_pages():
    """Test citation formatting without page numbers."""
    documents = [
        Document(
            page_content="Content 1",
            metadata={"filename": "notes.txt", "filetype": "txt"}
        ),
        Document(
            page_content="Content 2",
            metadata={"filename": "data.csv", "filetype": "csv"}
        )
    ]
    
    citations = format_citations(documents)
    
    assert "notes.txt" in citations
    assert "data.csv" in citations
    # Should not have "pages" for these file types
    assert "pages" not in citations.lower()


def test_format_citations_mixed():
    """Test citation formatting with mixed documents."""
    documents = [
        Document(
            page_content="PDF content",
            metadata={"filename": "paper.pdf", "filetype": "pdf", "page": 5}
        ),
        Document(
            page_content="Text content",
            metadata={"filename": "notes.txt", "filetype": "txt"}
        )
    ]
    
    citations = format_citations(documents)
    
    assert "paper.pdf" in citations
    assert "notes.txt" in citations
    assert "page 5" in citations.lower() or "pages 5" in citations.lower()


def test_format_citations_multiple_files_with_pages():
    """Test citation formatting with multiple files."""
    documents = [
        Document(
            page_content="Content",
            metadata={"filename": "doc1.pdf", "filetype": "pdf", "page": 1}
        ),
        Document(
            page_content="Content",
            metadata={"filename": "doc1.pdf", "filetype": "pdf", "page": 2}
        ),
        Document(
            page_content="Content",
            metadata={"filename": "doc2.pdf", "filetype": "pdf", "page": 10}
        )
    ]
    
    citations = format_citations(documents)
    
    assert "doc1.pdf" in citations
    assert "doc2.pdf" in citations


def test_create_sources_section():
    """Test creating a sources section."""
    documents = [
        Document(
            page_content="Content",
            metadata={"filename": "test.pdf", "filetype": "pdf", "page": 1}
        )
    ]
    
    sources = create_sources_section(documents)
    
    assert sources.startswith("\n\n---\n\n")
    assert "Sources" in sources or "sources" in sources
    assert "test.pdf" in sources


def test_create_sources_section_empty():
    """Test creating sources section with empty documents."""
    sources = create_sources_section([])
    
    assert sources == ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
