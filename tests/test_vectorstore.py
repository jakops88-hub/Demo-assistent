"""
Tests for vector store operations.
"""
import pytest
import tempfile
import shutil
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import Config
from core.vectorstore import VectorStore
from langchain.schema import Document
from langchain_community.embeddings.fake import FakeEmbeddings


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def test_config(temp_dir):
    """Create a test configuration with temporary directory."""
    # Create a minimal config
    config = Config("config/config.example.yaml")
    # Override persist directory to use temp directory
    config._config['vectorstore']['persist_dir'] = str(temp_dir / "chroma")
    return config


@pytest.fixture
def fake_embeddings():
    """Create fake embeddings for testing."""
    return FakeEmbeddings(size=384)


@pytest.fixture
def vector_store(test_config, fake_embeddings):
    """Create a vector store instance for testing."""
    return VectorStore(test_config, fake_embeddings)


def test_vector_store_initialization(vector_store):
    """Test vector store initialization."""
    assert vector_store is not None
    assert vector_store._store is not None


def test_add_documents(vector_store):
    """Test adding documents to vector store."""
    # Create test documents
    documents = [
        Document(
            page_content="This is the first test document.",
            metadata={"filename": "test1.txt", "filetype": "txt"}
        ),
        Document(
            page_content="This is the second test document.",
            metadata={"filename": "test2.txt", "filetype": "txt"}
        )
    ]
    
    # Add documents
    ids = vector_store.add_documents(documents)
    
    # Assertions
    assert len(ids) == 2
    assert vector_store.get_document_count() == 2


def test_similarity_search(vector_store):
    """Test similarity search."""
    # Add test documents
    documents = [
        Document(
            page_content="Python is a programming language.",
            metadata={"filename": "python.txt", "filetype": "txt"}
        ),
        Document(
            page_content="JavaScript is also a programming language.",
            metadata={"filename": "javascript.txt", "filetype": "txt"}
        ),
        Document(
            page_content="Cats are animals.",
            metadata={"filename": "cats.txt", "filetype": "txt"}
        )
    ]
    
    vector_store.add_documents(documents)
    
    # Search for programming-related content
    results = vector_store.similarity_search("programming language", k=2)
    
    # Should return results (exact content depends on embeddings)
    assert len(results) > 0
    assert len(results) <= 2


def test_get_indexed_files(vector_store):
    """Test getting list of indexed files."""
    # Add test documents
    documents = [
        Document(
            page_content="Content 1",
            metadata={"filename": "file1.txt", "filetype": "txt"}
        ),
        Document(
            page_content="Content 2",
            metadata={"filename": "file2.txt", "filetype": "txt"}
        ),
        Document(
            page_content="Content 3",
            metadata={"filename": "file1.txt", "filetype": "txt"}  # Same file
        )
    ]
    
    vector_store.add_documents(documents)
    
    # Get indexed files
    files = vector_store.get_indexed_files()
    
    # Should have 2 unique files
    assert len(files) == 2
    assert "file1.txt" in files
    assert "file2.txt" in files


def test_clear_vector_store(vector_store):
    """Test clearing the vector store."""
    # Add documents
    documents = [
        Document(
            page_content="Test content",
            metadata={"filename": "test.txt", "filetype": "txt"}
        )
    ]
    
    vector_store.add_documents(documents)
    assert vector_store.get_document_count() > 0
    
    # Clear
    vector_store.clear()
    
    # Should be empty
    assert vector_store.get_document_count() == 0


def test_document_with_page_metadata(vector_store):
    """Test that documents with page metadata are stored correctly."""
    documents = [
        Document(
            page_content="Content from page 1",
            metadata={"filename": "doc.pdf", "filetype": "pdf", "page": 1}
        ),
        Document(
            page_content="Content from page 2",
            metadata={"filename": "doc.pdf", "filetype": "pdf", "page": 2}
        )
    ]
    
    ids = vector_store.add_documents(documents)
    
    assert len(ids) == 2
    
    # Search and verify metadata is preserved
    results = vector_store.similarity_search("content", k=2)
    
    # At least one result should have page metadata
    page_found = any('page' in doc.metadata for doc in results)
    assert page_found


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
