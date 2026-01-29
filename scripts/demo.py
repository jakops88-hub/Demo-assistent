#!/usr/bin/env python3
"""
Demo script showing the RAG system in action.
This demonstrates the core functionality without the Streamlit UI.
"""
import sys
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import Config
from core.ingest import DocumentIngestor
from core.vectorstore import VectorStore
from core.models import create_embeddings
from langchain_community.embeddings.fake import FakeEmbeddings


def demo():
    """Run a simple demonstration of the RAG system."""
    print("=" * 60)
    print("Document Chatbot - RAG System Demo")
    print("=" * 60)
    
    # Create a temporary directory for this demo
    temp_dir = Path(tempfile.mkdtemp())
    print(f"\n📁 Using temporary directory: {temp_dir}")
    
    try:
        # Load config
        print("\n1️⃣  Loading configuration...")
        config = Config("config/config.example.yaml")
        # Override persist directory to use temp
        config._config['vectorstore']['persist_dir'] = str(temp_dir / "chroma")
        print(f"   ✓ Project: {config.project_name}")
        print(f"   ✓ Chunk size: {config.chunk_size}")
        print(f"   ✓ Top K: {config.top_k}")
        
        # Create embeddings (using fake for demo)
        print("\n2️⃣  Initializing embeddings (using test embeddings)...")
        embeddings = FakeEmbeddings(size=384)
        print("   ✓ Embeddings ready")
        
        # Create vector store
        print("\n3️⃣  Setting up vector store...")
        vector_store = VectorStore(config, embeddings)
        print(f"   ✓ Vector store initialized")
        print(f"   ✓ Current document count: {vector_store.get_document_count()}")
        
        # Create sample documents
        print("\n4️⃣  Creating sample documents...")
        sample_docs = {
            "ai_basics.txt": """
Artificial Intelligence Overview

Artificial Intelligence (AI) is transforming the world. It includes machine learning, 
natural language processing, and computer vision. AI systems can learn from data and 
make intelligent decisions.

Key areas:
- Machine Learning: Algorithms that improve with experience
- Deep Learning: Neural networks with multiple layers
- NLP: Understanding and generating human language
- Computer Vision: Analyzing and understanding images
            """,
            "python_guide.txt": """
Python Programming Guide

Python is a high-level, interpreted programming language. It's known for its simple 
syntax and readability. Python is widely used in web development, data science, and 
artificial intelligence.

Popular Python frameworks:
- Django and Flask for web development
- NumPy and Pandas for data analysis
- TensorFlow and PyTorch for machine learning
- Streamlit for building data apps

Python's extensive library ecosystem makes it a top choice for developers.
            """
        }
        
        for filename, content in sample_docs.items():
            print(f"   ✓ Created: {filename}")
        
        # Ingest documents
        print("\n5️⃣  Ingesting documents...")
        ingestor = DocumentIngestor(config)
        
        all_chunks = []
        for filename, content in sample_docs.items():
            import io
            file_obj = io.BytesIO(content.encode('utf-8'))
            chunks = ingestor.ingest_file(file_obj=file_obj, filename=filename)
            all_chunks.extend(chunks)
            print(f"   ✓ {filename}: {len(chunks)} chunks")
        
        # Add to vector store
        print("\n6️⃣  Adding documents to vector store...")
        vector_store.add_documents(all_chunks)
        print(f"   ✓ Total documents in store: {vector_store.get_document_count()}")
        
        # Show indexed files
        indexed_files = vector_store.get_indexed_files()
        print(f"   ✓ Indexed files: {', '.join(indexed_files)}")
        
        # Demonstrate search
        print("\n7️⃣  Testing similarity search...")
        queries = [
            "What is artificial intelligence?",
            "Tell me about Python frameworks",
            "What is machine learning?"
        ]
        
        for query in queries:
            print(f"\n   Query: '{query}'")
            results = vector_store.similarity_search(query, k=2)
            print(f"   Found {len(results)} relevant chunks:")
            for i, doc in enumerate(results, 1):
                preview = doc.page_content[:100].replace('\n', ' ')
                print(f"     {i}. [{doc.metadata['filename']}] {preview}...")
        
        # Demonstrate citation formatting
        print("\n8️⃣  Testing citation formatting...")
        from core.citations import format_citations
        
        test_results = vector_store.similarity_search("Python", k=3)
        citations = format_citations(test_results)
        print("   Citations:")
        for line in citations.split('\n'):
            print(f"     {line}")
        
        print("\n" + "=" * 60)
        print("✅ Demo completed successfully!")
        print("=" * 60)
        
        print("\n📊 Summary:")
        print(f"   • Processed {len(sample_docs)} documents")
        print(f"   • Created {len(all_chunks)} text chunks")
        print(f"   • Stored in vector database")
        print(f"   • Retrieved relevant chunks for queries")
        print(f"   • Generated citations")
        
        print("\n💡 Next steps:")
        print("   1. Set your OPENAI_API_KEY in .env")
        print("   2. Run: python -m scripts.run_streamlit")
        print("   3. Upload your own documents")
        print("   4. Start chatting with your documents!")
        
    finally:
        # Cleanup
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print(f"\n🧹 Cleaned up temporary directory")


if __name__ == "__main__":
    demo()
