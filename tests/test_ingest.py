"""
Tests for document ingestion.
"""
import pytest
import io
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import Config
from core.ingest import DocumentIngestor


@pytest.fixture
def config():
    """Create a test configuration."""
    return Config("config/config.example.yaml")


@pytest.fixture
def ingestor(config):
    """Create a DocumentIngestor instance."""
    return DocumentIngestor(config)


def test_supported_file_types(ingestor):
    """Test supported file type detection."""
    assert ingestor.is_supported("test.pdf")
    assert ingestor.is_supported("test.docx")
    assert ingestor.is_supported("test.txt")
    assert ingestor.is_supported("test.md")
    assert ingestor.is_supported("test.csv")
    assert not ingestor.is_supported("test.exe")
    assert not ingestor.is_supported("test.jpg")


def test_ingest_text_file(ingestor):
    """Test ingesting a simple text file."""
    # Create a sample text content
    text_content = "This is a test document.\n\nIt has multiple paragraphs.\n\nEach paragraph contains information."
    text_bytes = text_content.encode('utf-8')
    
    # Create a file-like object
    file_obj = io.BytesIO(text_bytes)
    
    # Ingest the file
    documents = ingestor.ingest_file(file_obj=file_obj, filename="test.txt")
    
    # Assertions
    assert len(documents) > 0
    assert all(doc.metadata['filename'] == 'test.txt' for doc in documents)
    assert all(doc.metadata['filetype'] == 'txt' for doc in documents)
    assert all(hasattr(doc, 'page_content') for doc in documents)


def test_ingest_markdown_file(ingestor):
    """Test ingesting a markdown file."""
    # Create sample markdown content
    md_content = """# Test Document

This is a test markdown document.

## Section 1

Some content here.

## Section 2

More content here."""
    
    md_bytes = md_content.encode('utf-8')
    file_obj = io.BytesIO(md_bytes)
    
    # Ingest the file
    documents = ingestor.ingest_file(file_obj=file_obj, filename="test.md")
    
    # Assertions
    assert len(documents) > 0
    assert all(doc.metadata['filename'] == 'test.md' for doc in documents)
    assert all(doc.metadata['filetype'] == 'md' for doc in documents)


def test_chunk_metadata(ingestor):
    """Test that chunks have proper metadata."""
    # Create a longer text that will be split into multiple chunks
    long_text = " ".join([f"Sentence {i}." for i in range(200)])
    text_bytes = long_text.encode('utf-8')
    
    file_obj = io.BytesIO(text_bytes)
    
    # Ingest the file
    documents = ingestor.ingest_file(file_obj=file_obj, filename="long_test.txt")
    
    # Should create multiple chunks
    assert len(documents) > 1
    
    # Check metadata on all chunks
    for doc in documents:
        assert 'filename' in doc.metadata
        assert 'filetype' in doc.metadata
        assert doc.metadata['filename'] == 'long_test.txt'
        assert doc.metadata['filetype'] == 'txt'


def test_csv_ingestion(ingestor):
    """Test ingesting a CSV file."""
    # Create sample CSV content
    csv_content = """name,age,city
John,30,New York
Jane,25,Los Angeles
Bob,35,Chicago"""
    
    csv_bytes = csv_content.encode('utf-8')
    file_obj = io.BytesIO(csv_bytes)
    
    # Ingest the file
    documents = ingestor.ingest_file(file_obj=file_obj, filename="test.csv")
    
    # Assertions
    assert len(documents) > 0
    assert all(doc.metadata['filename'] == 'test.csv' for doc in documents)
    assert all(doc.metadata['filetype'] == 'csv' for doc in documents)
    
    # Check that CSV data is in the content
    combined_content = " ".join([doc.page_content for doc in documents])
    assert "name" in combined_content.lower()
    assert "John" in combined_content or "john" in combined_content.lower()


def test_unsupported_file_type(ingestor):
    """Test that unsupported file types raise an error."""
    file_obj = io.BytesIO(b"some content")
    
    with pytest.raises(ValueError, match="Unsupported file type"):
        ingestor.ingest_file(file_obj=file_obj, filename="test.xyz")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
