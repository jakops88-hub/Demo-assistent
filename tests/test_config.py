"""
Tests for configuration loader.
"""
import pytest
import os
import tempfile
import yaml
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import Config


def test_load_config():
    """Test loading configuration from YAML."""
    config = Config("config/config.example.yaml")
    
    assert config.project_name == "Document Chatbot"
    assert config.vectorstore_type == "chroma"
    assert config.chunk_size == 900
    assert config.chunk_overlap == 150
    assert config.top_k == 5
    assert config.model_provider in ["openai", "ollama"]


def test_config_properties():
    """Test configuration properties."""
    config = Config("config/config.example.yaml")
    
    # Test path properties
    assert isinstance(config.storage_dir, Path)
    assert isinstance(config.vectorstore_persist_dir, Path)
    
    # Test model properties
    assert config.openai_chat_model == "gpt-4o-mini"
    assert config.openai_embeddings_model == "text-embedding-3-small"


def test_config_get_nested():
    """Test nested configuration access."""
    config = Config("config/config.example.yaml")
    
    assert config.get("models.provider") == "openai"
    assert config.get("vectorstore.type") == "chroma"
    assert config.get("chunking.chunk_size") == 900
    assert config.get("nonexistent.key", "default") == "default"


def test_custom_config():
    """Test loading a custom configuration."""
    # Create a temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_data = {
            'project_name': 'Test Project',
            'storage_dir': './test_data',
            'vectorstore': {'type': 'chroma', 'persist_dir': './test_data/chroma'},
            'chunking': {'chunk_size': 500, 'chunk_overlap': 100},
            'retrieval': {'top_k': 3},
            'models': {
                'provider': 'openai',
                'openai': {
                    'chat_model': 'gpt-4',
                    'embeddings_model': 'text-embedding-ada-002'
                }
            },
            'features': {'citations': False}
        }
        yaml.dump(config_data, f)
        temp_config_path = f.name
    
    try:
        config = Config(temp_config_path)
        
        assert config.project_name == "Test Project"
        assert config.chunk_size == 500
        assert config.chunk_overlap == 100
        assert config.top_k == 3
        assert config.openai_chat_model == "gpt-4"
        assert config.citations_enabled == False
    
    finally:
        # Clean up
        os.unlink(temp_config_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
