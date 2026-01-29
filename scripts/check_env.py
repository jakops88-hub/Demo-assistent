"""
Environment diagnostics script for Document Chatbot.
Checks Python version, dependencies, and configuration.
"""
import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version meets requirements."""
    print("\n" + "="*50)
    print("  PYTHON VERSION CHECK")
    print("="*50)
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"Python version: {version_str}")
    
    if version >= (3, 10):
        print("✓ Python version is compatible (3.10+)")
        return True
    else:
        print("✗ Python 3.10 or higher is required!")
        print(f"  Current version: {version_str}")
        return False


def check_virtual_env():
    """Check if running in virtual environment."""
    print("\n" + "="*50)
    print("  VIRTUAL ENVIRONMENT CHECK")
    print("="*50)
    
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print("✓ Running in virtual environment")
        print(f"  Location: {sys.prefix}")
        return True
    else:
        print("✗ NOT running in virtual environment")
        print("  It's recommended to use a virtual environment")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    print("\n" + "="*50)
    print("  DEPENDENCIES CHECK")
    print("="*50)
    
    required_packages = [
        'streamlit',
        'langchain',
        'chromadb',
        'pypdf',
        'python-docx',
        'dotenv'
    ]
    
    missing = []
    installed = []
    
    for package in required_packages:
        # Handle package name differences
        import_name = package
        if package == 'python-docx':
            import_name = 'docx'
        elif package == 'dotenv':
            import_name = 'dotenv'
            
        try:
            __import__(import_name)
            installed.append(package)
            print(f"✓ {package}")
        except ImportError:
            missing.append(package)
            print(f"✗ {package} (NOT INSTALLED)")
    
    if missing:
        print(f"\n{len(missing)} package(s) missing!")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print(f"\n✓ All {len(installed)} required packages are installed")
        return True


def check_config_files():
    """Check for configuration files."""
    print("\n" + "="*50)
    print("  CONFIGURATION FILES CHECK")
    print("="*50)
    
    repo_root = Path(__file__).parent.parent
    
    files_to_check = {
        'requirements.txt': repo_root / 'requirements.txt',
        'config/config.example.yaml': repo_root / 'config' / 'config.example.yaml',
        '.env': repo_root / '.env',
        '.env.example': repo_root / '.env.example',
        'app/app.py': repo_root / 'app' / 'app.py'
    }
    
    all_ok = True
    for name, path in files_to_check.items():
        if path.exists():
            print(f"✓ {name}")
        else:
            if name == '.env':
                print(f"⚠ {name} (optional - copy from .env.example)")
            else:
                print(f"✗ {name} (MISSING)")
                all_ok = False
    
    return all_ok


def check_environment_variables():
    """Check for required environment variables."""
    print("\n" + "="*50)
    print("  ENVIRONMENT VARIABLES CHECK")
    print("="*50)
    
    # Load .env file if exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✓ .env file loaded")
    except Exception:
        print("⚠ Could not load .env file")
    
    # Check for OpenAI API key
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        # Mask the key for security
        masked = openai_key[:8] + "..." + openai_key[-4:] if len(openai_key) > 12 else "***"
        print(f"✓ OPENAI_API_KEY is set ({masked})")
    else:
        print("⚠ OPENAI_API_KEY not set (required if using OpenAI provider)")
    
    return True


def check_directories():
    """Check for required directories."""
    print("\n" + "="*50)
    print("  DIRECTORIES CHECK")
    print("="*50)
    
    repo_root = Path(__file__).parent.parent
    
    dirs_to_check = {
        'app': repo_root / 'app',
        'core': repo_root / 'core',
        'config': repo_root / 'config',
        'launcher': repo_root / 'launcher'
    }
    
    all_ok = True
    for name, path in dirs_to_check.items():
        if path.exists() and path.is_dir():
            print(f"✓ {name}/")
        else:
            print(f"✗ {name}/ (MISSING)")
            all_ok = False
    
    return all_ok


def main():
    """Run all diagnostic checks."""
    print("\n" + "="*60)
    print("  DOCUMENT CHATBOT - ENVIRONMENT DIAGNOSTICS")
    print("="*60)
    
    results = {
        'Python version': check_python_version(),
        'Virtual environment': check_virtual_env(),
        'Dependencies': check_dependencies(),
        'Config files': check_config_files(),
        'Environment variables': check_environment_variables(),
        'Directories': check_directories()
    }
    
    # Summary
    print("\n" + "="*60)
    print("  SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:10} {check}")
    
    print(f"\n{passed}/{total} checks passed")
    
    if passed == total:
        print("\n✓ System is ready to run!")
        return 0
    else:
        print("\n⚠ Some issues detected. Please resolve them before running.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
