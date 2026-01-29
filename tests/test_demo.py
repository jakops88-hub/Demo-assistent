"""
Test script to verify Demo Mode functionality.
This demonstrates that the demo mode code works correctly.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.demo import DemoConfig
from core.ingest import DocumentIngestor
from core.config import get_config

def test_demo_assets():
    """Test that demo assets exist and are valid."""
    print("=" * 60)
    print("Testing Demo Assets")
    print("=" * 60)
    
    demo_config = DemoConfig()
    
    # Test asset validation
    valid, missing = demo_config.validate_demo_assets()
    print(f"\n✓ Assets valid: {valid}")
    if missing:
        print(f"✗ Missing files: {missing}")
        return False
    
    # Test file paths
    file_paths = demo_config.get_demo_file_paths()
    print(f"\n✓ Found {len(file_paths)} demo files:")
    for path in file_paths:
        print(f"  - {Path(path).name}")
    
    # Test questions loading
    questions = demo_config.load_demo_questions()
    print(f"\n✓ Loaded {sum(len(q) for q in questions.values())} demo questions:")
    for category, qs in questions.items():
        print(f"  - {category}: {len(qs)} questions")
        for i, q in enumerate(qs, 1):
            print(f"    {i}. {q[:80]}{'...' if len(q) > 80 else ''}")
    
    # Test config overrides
    overrides = demo_config.get_demo_config_overrides()
    print(f"\n✓ Demo config overrides:")
    for key, value in overrides.items():
        print(f"  - {key}: {value}")
    
    return True


def test_demo_ingestion():
    """Test that demo files can be ingested."""
    print("\n" + "=" * 60)
    print("Testing Demo Document Ingestion")
    print("=" * 60)
    
    demo_config = DemoConfig()
    config = get_config()
    ingestor = DocumentIngestor(config)
    
    # Get demo file paths
    file_paths = demo_config.get_demo_file_paths()
    
    # Ingest files
    print(f"\n→ Ingesting {len(file_paths)} demo files...")
    documents, failed_files = ingestor.ingest_multiple(file_paths=file_paths)
    
    print(f"\n✓ Successfully ingested {len(documents)} document chunks")
    
    if failed_files:
        print(f"✗ Failed to ingest {len(failed_files)} files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")
        return False
    
    # Show document breakdown
    doc_counts = {}
    for doc in documents:
        filename = doc.metadata.get('filename', 'unknown')
        doc_counts[filename] = doc_counts.get(filename, 0) + 1
    
    print(f"\n✓ Document breakdown:")
    for filename, count in doc_counts.items():
        print(f"  - {filename}: {count} chunks")
    
    # Verify content samples
    print(f"\n✓ Content samples:")
    for doc in documents[:3]:
        filename = doc.metadata.get('filename', 'unknown')
        content_preview = doc.page_content[:100].replace('\n', ' ')
        print(f"  - {filename}: {content_preview}...")
    
    return True


def test_demo_questions_content():
    """Test the content of demo questions matches requirements."""
    print("\n" + "=" * 60)
    print("Testing Demo Questions Content")
    print("=" * 60)
    
    demo_config = DemoConfig()
    questions = demo_config.load_demo_questions()
    
    # Required questions
    required_questions = {
        'HR': 'vacation policy for employees in Sweden vs Germany',
        'Legal': 'flood insurance or special conditions',
        'Commerce': 'highest margin in Q4'
    }
    
    print("\n✓ Verifying required questions exist:")
    for category, keyword in required_questions.items():
        found = False
        for question in questions.get(category, []):
            if keyword.lower() in question.lower():
                print(f"  ✓ {category}: Found '{keyword}'")
                print(f"    Question: {question}")
                found = True
                break
        if not found:
            print(f"  ✗ {category}: Missing question about '{keyword}'")
            return False
    
    return True


def main():
    """Run all demo tests."""
    print("\n" + "=" * 60)
    print("DEMO MODE FUNCTIONALITY TEST")
    print("=" * 60)
    
    tests = [
        ("Demo Assets Validation", test_demo_assets),
        ("Demo Document Ingestion", test_demo_ingestion),
        ("Demo Questions Content", test_demo_questions_content),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All demo functionality tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
