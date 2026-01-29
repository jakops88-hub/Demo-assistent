"""
Vector store wrapper for Chroma.
Provides a unified interface for adding and querying documents.
"""
from typing import List, Optional
from pathlib import Path
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain.embeddings.base import Embeddings

from core.config import Config
from core.logging_utils import get_logger

logger = get_logger(__name__)


class VectorStore:
    """Wrapper for vector store operations."""
    
    def __init__(self, config: Config, embeddings: Embeddings):
        """
        Initialize vector store.
        
        Args:
            config: Application configuration
            embeddings: Embeddings model instance
        """
        self.config = config
        self.embeddings = embeddings
        self.persist_dir = str(config.vectorstore_persist_dir)
        self._store: Optional[Chroma] = None
        
        # Initialize or load existing store
        self._initialize_store()
    
    def _initialize_store(self):
        """Initialize or load the vector store."""
        try:
            logger.info(f"Initializing Chroma vector store at {self.persist_dir}")
            
            # Try to load existing store
            self._store = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings,
                collection_name="documents"
            )
            
            # Check if store has any documents
            collection = self._store._collection
            count = collection.count()
            logger.info(f"Vector store loaded with {count} documents")
            
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of Document objects with content and metadata
            
        Returns:
            List of document IDs
        """
        if not documents:
            logger.warning("No documents to add")
            return []
        
        try:
            logger.info(f"Adding {len(documents)} documents to vector store")
            ids = self._store.add_documents(documents)
            
            # Persist changes
            self._store.persist()
            
            logger.info(f"Successfully added {len(ids)} documents")
            return ids
        
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise
    
    def similarity_search(
        self,
        query: str,
        k: Optional[int] = None,
        filter: Optional[dict] = None
    ) -> List[Document]:
        """
        Search for similar documents.
        
        Args:
            query: Search query
            k: Number of results to return (uses config default if None)
            filter: Metadata filter (optional)
            
        Returns:
            List of similar documents
        """
        k = k or self.config.top_k
        
        try:
            logger.info(f"Searching for top {k} similar documents")
            results = self._store.similarity_search(
                query,
                k=k,
                filter=filter
            )
            logger.info(f"Found {len(results)} similar documents")
            return results
        
        except Exception as e:
            logger.error(f"Error during similarity search: {e}")
            raise
    
    def similarity_search_with_score(
        self,
        query: str,
        k: Optional[int] = None,
        filter: Optional[dict] = None
    ) -> List[tuple]:
        """
        Search for similar documents with relevance scores.
        
        Args:
            query: Search query
            k: Number of results to return
            filter: Metadata filter (optional)
            
        Returns:
            List of (Document, score) tuples
        """
        k = k or self.config.top_k
        
        try:
            results = self._store.similarity_search_with_score(
                query,
                k=k,
                filter=filter
            )
            return results
        
        except Exception as e:
            logger.error(f"Error during similarity search with score: {e}")
            raise
    
    def clear(self):
        """Clear all documents from the vector store."""
        try:
            logger.info("Clearing vector store")
            
            # Delete the collection and recreate
            collection = self._store._collection
            collection.delete()
            
            # Reinitialize
            self._initialize_store()
            
            logger.info("Vector store cleared")
        
        except Exception as e:
            logger.error(f"Error clearing vector store: {e}")
            raise
    
    def get_document_count(self) -> int:
        """
        Get the number of documents in the store.
        
        Returns:
            Document count
        """
        try:
            collection = self._store._collection
            return collection.count()
        except Exception as e:
            logger.error(f"Error getting document count: {e}")
            return 0
    
    def get_indexed_files(self) -> List[str]:
        """
        Get list of unique filenames in the vector store.
        
        Returns:
            List of filenames
        """
        try:
            collection = self._store._collection
            # Get all metadata
            all_metadata = collection.get(include=['metadatas'])
            
            if all_metadata and 'metadatas' in all_metadata:
                filenames = set()
                for metadata in all_metadata['metadatas']:
                    if metadata and 'filename' in metadata:
                        filenames.add(metadata['filename'])
                return sorted(list(filenames))
            
            return []
        
        except Exception as e:
            logger.error(f"Error getting indexed files: {e}")
            return []
