"""
Robust browser opener for Document Chatbot.
Opens the specified URL in the default browser with retry logic.
"""
import webbrowser
import sys
import time
import urllib.request
import urllib.error


def wait_for_server(url, timeout=30, interval=1):
    """
    Wait for the server to be available.
    
    Args:
        url: URL to check
        timeout: Maximum time to wait in seconds
        interval: Time between checks in seconds
    
    Returns:
        True if server is available, False otherwise
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            urllib.request.urlopen(url, timeout=2)
            return True
        except (urllib.error.URLError, urllib.error.HTTPError):
            # Server not ready yet, wait and retry
            time.sleep(interval)
        except OSError as e:
            # Network-related errors (connection refused, etc.)
            time.sleep(interval)
        except Exception as e:
            # Log unexpected errors but continue trying
            print(f"Unexpected error while checking server: {e}")
            time.sleep(interval)
    
    return False


def open_browser(url):
    """
    Open the specified URL in the default browser.
    
    Args:
        url: URL to open
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Try to open with default browser
        webbrowser.open(url, new=2)  # new=2 opens in a new tab if possible
        return True
    except Exception as e:
        print(f"Warning: Could not automatically open browser: {e}")
        print(f"Please manually open: {url}")
        return False


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python open_browser.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Wait a bit before trying to open (let server start)
    time.sleep(2)
    
    # Wait for server to be available
    print(f"Waiting for server at {url}...")
    if wait_for_server(url, timeout=30):
        print(f"Server is ready! Opening browser...")
        if open_browser(url):
            print(f"Browser opened: {url}")
        else:
            print(f"\nPlease manually open: {url}")
    else:
        print(f"Warning: Server did not respond within timeout")
        print(f"Please manually open: {url}")
        # Try to open anyway
        open_browser(url)


if __name__ == '__main__':
    main()
