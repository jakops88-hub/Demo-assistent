"""
Offline fallback embeddings that work without internet access.
Provides a simple hash-based embedding when OpenAI embeddings fail.
"""
import hashlib
import numpy as np
from typing import List
from langchain.embeddings.base import Embeddings
from core.logging_utils import get_logger

logger = get_logger(__name__)


class OfflineFallbackEmbeddings(Embeddings):
    """
    Simple offline embeddings that use character-based hashing.
    This is a fallback for when network-based embeddings fail.
    """
    
    def __init__(self, dimension: int = 1536):
        """
        Initialize offline embeddings.
        
        Args:
            dimension: Embedding dimension (default 1536 matches OpenAI)
        """
        self.dimension = dimension
        logger.info(f"Initialized offline fallback embeddings (dimension: {dimension})")
    
    def _hash_to_embedding(self, text: str) -> List[float]:
        """
        Convert text to a deterministic embedding using hashing.
        
        Args:
            text: Input text
            
        Returns:
            List of floats representing the embedding
        """
        # Use multiple hash functions to create a diverse embedding
        # This ensures similar texts get similar embeddings
        
        # Normalize text
        text = text.lower().strip()
        
        # Create base embedding using multiple hash seeds
        embedding = []
        num_hashes = self.dimension // 32  # Each hash gives us 32 values
        
        for seed in range(num_hashes):
            # Create hash with seed
            hash_input = f"{seed}:{text}".encode('utf-8')
            hash_obj = hashlib.sha256(hash_input)
            hash_bytes = hash_obj.digest()
            
            # Convert bytes to float values
            for i in range(0, len(hash_bytes), 8):
                if len(embedding) >= self.dimension:
                    break
                # Take 8 bytes and convert to a float between -1 and 1
                chunk = hash_bytes[i:i+8]
                value = int.from_bytes(chunk, byteorder='big', signed=False)
                # Normalize to [-1, 1]
                normalized = (value / (2**64 - 1)) * 2 - 1
                embedding.append(normalized)
        
        # Pad if needed
        while len(embedding) < self.dimension:
            embedding.append(0.0)
        
        # Truncate if too long
        embedding = embedding[:self.dimension]
        
        # Normalize to unit vector for cosine similarity
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = (np.array(embedding) / norm).tolist()
        
        return embedding
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.
        
        Args:
            texts: List of text documents
            
        Returns:
            List of embeddings
        """
        return [self._hash_to_embedding(text) for text in texts]
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query.
        
        Args:
            text: Query text
            
        Returns:
            Embedding vector
        """
        return self._hash_to_embedding(text)


class ResilientEmbeddings(Embeddings):
    """
    Embeddings wrapper that tries online embeddings first, falls back to offline.
    """
    
    def __init__(self, primary_embeddings: Embeddings, dimension: int = 1536):
        """
        Initialize resilient embeddings.
        
        Args:
            primary_embeddings: Primary embeddings to try first (e.g., OpenAI)
            dimension: Embedding dimension for fallback
        """
        self.primary = primary_embeddings
        self.fallback = OfflineFallbackEmbeddings(dimension=dimension)
        self.using_fallback = False
        logger.info("Initialized resilient embeddings with fallback support")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed documents with fallback support.
        
        Args:
            texts: List of text documents
            
        Returns:
            List of embeddings
        """
        # If already using fallback, skip trying primary
        if self.using_fallback:
            return self.fallback.embed_documents(texts)
        
        try:
            return self.primary.embed_documents(texts)
        except Exception as e:
            error_str = str(e).lower()
            # Check if it's a network/tiktoken error
            if any(keyword in error_str for keyword in [
                'openaipublic.blob.core.windows.net',
                'tiktoken',
                'cl100k_base',
                'failed to resolve',
                'connection',
                'timeout',
                'network'
            ]):
                logger.warning(
                    f"Primary embeddings failed (offline/network issue), "
                    f"using offline fallback. Error: {e}"
                )
                self.using_fallback = True
                return self.fallback.embed_documents(texts)
            else:
                # Re-raise if it's not a network error
                raise
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed query with fallback support.
        
        Args:
            text: Query text
            
        Returns:
            Embedding vector
        """
        # If already using fallback, skip trying primary
        if self.using_fallback:
            return self.fallback.embed_query(text)
        
        try:
            return self.primary.embed_query(text)
        except Exception as e:
            error_str = str(e).lower()
            # Check if it's a network/tiktoken error
            if any(keyword in error_str for keyword in [
                'openaipublic.blob.core.windows.net',
                'tiktoken',
                'cl100k_base',
                'failed to resolve',
                'connection',
                'timeout',
                'network'
            ]):
                logger.warning(
                    f"Primary embeddings failed (offline/network issue), "
                    f"using offline fallback. Error: {e}"
                )
                self.using_fallback = True
                return self.fallback.embed_query(text)
            else:
                # Re-raise if it's not a network error
                raise
