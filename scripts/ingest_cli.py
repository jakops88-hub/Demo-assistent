"""
CLI script for ingesting documents from command line.
"""
import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import get_config
from core.ingest import DocumentIngestor
from core.vectorstore import VectorStore
from core.models import create_embeddings
from core.logging_utils import setup_logger

logger = setup_logger(__name__)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Ingest documents into the vector store"
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="Files to ingest"
    )
    parser.add_argument(
        "--config",
        default="config/config.example.yaml",
        help="Path to config file"
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "ollama"],
        help="Model provider (overrides config)"
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear vector store before ingesting"
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        logger.info("Loading configuration...")
        config = get_config(args.config)
        config.validate()
        
        # Set provider if specified
        provider = args.provider or config.model_provider
        
        # Create embeddings
        logger.info(f"Creating embeddings with provider: {provider}")
        embeddings = create_embeddings(config, provider)
        
        # Create vector store
        logger.info("Initializing vector store...")
        vector_store = VectorStore(config, embeddings)
        
        # Clear if requested
        if args.clear:
            logger.info("Clearing vector store...")
            vector_store.clear()
        
        # Create ingestor
        ingestor = DocumentIngestor(config)
        
        # Process files
        logger.info(f"Processing {len(args.files)} file(s)...")
        documents = ingestor.ingest_multiple(file_paths=args.files)
        
        if documents:
            # Add to vector store
            logger.info(f"Adding {len(documents)} documents to vector store...")
            vector_store.add_documents(documents)
            
            logger.info("✅ Ingestion complete!")
            logger.info(f"Total documents in store: {vector_store.get_document_count()}")
            
            # Show indexed files
            indexed_files = vector_store.get_indexed_files()
            logger.info(f"Indexed files ({len(indexed_files)}):")
            for filename in indexed_files:
                logger.info(f"  • {filename}")
        else:
            logger.warning("No documents were extracted from the files")
    
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
