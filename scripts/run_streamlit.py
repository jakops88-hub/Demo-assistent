"""
Script to run the Streamlit application.
"""
import sys
import subprocess
from pathlib import Path


def main():
    """Run the Streamlit application."""
    # Get the app directory
    app_file = Path(__file__).parent.parent / "app" / "app.py"
    
    if not app_file.exists():
        print(f"Error: Application file not found at {app_file}")
        sys.exit(1)
    
    print(f"Starting Streamlit application from {app_file}...")
    
    # Run streamlit
    try:
        subprocess.run(
            ["streamlit", "run", str(app_file)],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == "__main__":
    main()
