"""
Configuration loader for the RAG application.
Loads config.yaml and environment variables.
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


class Config:
    """Configuration manager for the application."""
    
    def __init__(self, config_path: str = "config/config.example.yaml"):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to the configuration YAML file
        """
        # Load environment variables
        load_dotenv()
        
        # Load YAML configuration
        self.config_path = Path(config_path)
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(self.config_path, 'r') as f:
            self._config: Dict[str, Any] = yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'models.provider')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    @property
    def project_name(self) -> str:
        """Get project name."""
        return self.get('project_name', 'Document Chatbot')
    
    @property
    def storage_dir(self) -> Path:
        """Get storage directory path."""
        path = Path(self.get('storage_dir', './data'))
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @property
    def vectorstore_type(self) -> str:
        """Get vector store type."""
        return self.get('vectorstore.type', 'chroma')
    
    @property
    def vectorstore_persist_dir(self) -> Path:
        """Get vector store persistence directory."""
        path = Path(self.get('vectorstore.persist_dir', './data/chroma'))
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @property
    def chunk_size(self) -> int:
        """Get chunk size for text splitting."""
        return self.get('chunking.chunk_size', 900)
    
    @property
    def chunk_overlap(self) -> int:
        """Get chunk overlap for text splitting."""
        return self.get('chunking.chunk_overlap', 150)
    
    @property
    def top_k(self) -> int:
        """Get top k results for retrieval."""
        return self.get('retrieval.top_k', 5)
    
    @property
    def model_provider(self) -> str:
        """Get model provider (openai or ollama)."""
        return self.get('models.provider', 'openai')
    
    @property
    def openai_chat_model(self) -> str:
        """Get OpenAI chat model name."""
        return self.get('models.openai.chat_model', 'gpt-4o-mini')
    
    @property
    def openai_embeddings_model(self) -> str:
        """Get OpenAI embeddings model name."""
        return self.get('models.openai.embeddings_model', 'text-embedding-3-small')
    
    @property
    def ollama_chat_model(self) -> str:
        """Get Ollama chat model name."""
        return self.get('models.ollama.chat_model', 'llama3')
    
    @property
    def ollama_embeddings_model(self) -> str:
        """Get Ollama embeddings model name."""
        return self.get('models.ollama.embeddings_model', 'nomic-embed-text')
    
    @property
    def citations_enabled(self) -> bool:
        """Check if citations are enabled by default."""
        return self.get('features.citations', True)
    
    @property
    def openai_api_key(self) -> str:
        """Get OpenAI API key from environment."""
        key = os.getenv('OPENAI_API_KEY', '')
        if not key and self.model_provider == 'openai':
            raise ValueError(
                "OPENAI_API_KEY environment variable is required when using OpenAI provider. "
                "Please set it in your .env file or environment."
            )
        return key
    
    def validate(self):
        """Validate configuration and raise errors if invalid."""
        if self.model_provider not in ['openai', 'ollama']:
            raise ValueError(f"Invalid model provider: {self.model_provider}")
        
        if self.model_provider == 'openai':
            # Check for API key
            _ = self.openai_api_key


# Global configuration instance
_config_instance = None


def reset_config():
    """Reset the global configuration instance."""
    global _config_instance
    _config_instance = None


def get_config(config_path: str = "config/config.example.yaml") -> Config:
    """
    Get or create global configuration instance.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Config instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance
