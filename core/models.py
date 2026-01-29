"""
LLM and embeddings model factory.
Creates instances based on configuration.
"""
from typing import Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.embeddings.base import Embeddings
from langchain.chat_models.base import BaseChatModel

from core.config import Config
from core.logging_utils import get_logger
from core.offline_embeddings import ResilientEmbeddings
from core.demo_llm import ResilientChatModel

logger = get_logger(__name__)


class ModelFactory:
    """Factory for creating LLM and embedding models."""
    
    def __init__(self, config: Config):
        """
        Initialize model factory.
        
        Args:
            config: Application configuration
        """
        self.config = config
    
    def create_chat_model(self, provider: Optional[str] = None) -> BaseChatModel:
        """
        Create a chat model based on provider with demo fallback.
        
        Args:
            provider: Model provider (openai or ollama). Uses config default if None.
            
        Returns:
            Chat model instance with demo fallback support
        """
        provider = provider or self.config.model_provider
        
        if provider == 'openai':
            logger.info(f"Creating OpenAI chat model with demo fallback: {self.config.openai_chat_model}")
            primary = ChatOpenAI(
                model=self.config.openai_chat_model,
                temperature=0,
                api_key=self.config.openai_api_key
            )
            # Wrap with resilient fallback for demo mode
            return ResilientChatModel(primary=primary)
        elif provider == 'ollama':
            logger.info(f"Creating Ollama chat model: {self.config.ollama_chat_model}")
            try:
                from langchain_community.chat_models import ChatOllama
                # Ollama is local, no need for fallback
                return ChatOllama(
                    model=self.config.ollama_chat_model,
                    temperature=0
                )
            except ImportError:
                raise ImportError(
                    "Ollama support requires langchain-community. "
                    "Install it with: pip install langchain-community"
                )
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def create_embeddings(self, provider: Optional[str] = None) -> Embeddings:
        """
        Create embeddings model based on provider with offline fallback.
        
        Args:
            provider: Model provider (openai or ollama). Uses config default if None.
            
        Returns:
            Embeddings instance with offline fallback support
        """
        provider = provider or self.config.model_provider
        
        if provider == 'openai':
            logger.info(f"Creating OpenAI embeddings with offline fallback: {self.config.openai_embeddings_model}")
            primary = OpenAIEmbeddings(
                model=self.config.openai_embeddings_model,
                api_key=self.config.openai_api_key
            )
            # Wrap with resilient fallback
            return ResilientEmbeddings(primary, dimension=1536)
        elif provider == 'ollama':
            logger.info(f"Creating Ollama embeddings: {self.config.ollama_embeddings_model}")
            try:
                from langchain_community.embeddings import OllamaEmbeddings
                # Ollama is local, no need for fallback
                return OllamaEmbeddings(
                    model=self.config.ollama_embeddings_model
                )
            except ImportError:
                raise ImportError(
                    "Ollama support requires langchain-community. "
                    "Install it with: pip install langchain-community"
                )
        else:
            raise ValueError(f"Unsupported provider: {provider}")


def create_chat_model(config: Config, provider: Optional[str] = None) -> BaseChatModel:
    """
    Convenience function to create a chat model.
    
    Args:
        config: Application configuration
        provider: Model provider (optional)
        
    Returns:
        Chat model instance
    """
    factory = ModelFactory(config)
    return factory.create_chat_model(provider)


def create_embeddings(config: Config, provider: Optional[str] = None) -> Embeddings:
    """
    Convenience function to create embeddings.
    
    Args:
        config: Application configuration
        provider: Model provider (optional)
        
    Returns:
        Embeddings instance
    """
    factory = ModelFactory(config)
    return factory.create_embeddings(provider)
