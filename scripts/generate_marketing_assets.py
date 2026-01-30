#!/usr/bin/env python3
"""
Marketing Assets Generator for DocuMind Streamlit App
Automatically generates screenshots and demo videos using Playwright.
"""
import sys
import time
import subprocess
import traceback
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

# Add parent directory to path
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Paths
APP_PATH = PROJECT_ROOT / "app" / "app.py"
ASSETS_DIR = PROJECT_ROOT / "assets"
SCREENSHOT_PATH = ASSETS_DIR / "marketing_screenshot.png"
VIDEO_PATH = ASSETS_DIR / "demo_video.webm"

# Configuration
STREAMLIT_PORT = 8501
STREAMLIT_URL = f"http://localhost:{STREAMLIT_PORT}"
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080
TYPING_DELAY_MS = 100
RESPONSE_WAIT_SECONDS = 5


def start_streamlit_app():
    """Start the Streamlit app in the background."""
    print("🚀 Starting Streamlit app...")
    
    # Start Streamlit process
    process = subprocess.Popen(
        ["streamlit", "run", str(APP_PATH), "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(PROJECT_ROOT)
    )
    
    # Wait for Streamlit to be ready
    print(f"⏳ Waiting for Streamlit server to be ready on port {STREAMLIT_PORT}...")
    max_retries = 30
    retry_count = 0
    
    try:
        while retry_count < max_retries:
            try:
                urllib.request.urlopen(STREAMLIT_URL, timeout=1)
                print("✅ Streamlit server is ready!")
                return process
            except (urllib.error.URLError, OSError):
                retry_count += 1
                time.sleep(1)
        
        # If we get here, server didn't start
        process.kill()
        raise RuntimeError("Failed to start Streamlit server")
    except Exception:
        # Ensure process is cleaned up on any error
        process.kill()
        raise


def capture_marketing_assets(streamlit_process):
    """Capture screenshot and video of the app using Playwright."""
    print("\n🎬 Launching browser and recording...")
    
    with sync_playwright() as p:
        # Launch browser with video recording
        browser = p.chromium.launch(headless=True)
        
        context = browser.new_context(
            viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            record_video_dir=str(ASSETS_DIR),
            record_video_size={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT}
        )
        
        page = context.new_page()
        
        try:
            # Navigate to the app
            print(f"🌐 Navigating to {STREAMLIT_URL}...")
            page.goto(STREAMLIT_URL, wait_until="networkidle", timeout=30000)
            
            # Wait for the app to load
            print("⏳ Waiting for app to load...")
            time.sleep(3)
            
            # Simulate user interaction
            print("👤 Simulating user interaction...")
            
            # Locate the chat input box (it's an input element with aria-label="Message")
            chat_input_selector = 'input[aria-label="Message"]'
            
            print("🔍 Looking for chat input...")
            page.wait_for_selector(chat_input_selector, timeout=30000)
            
            # Type the message slowly to simulate human behavior
            print("⌨️  Typing message...")
            page.type(
                chat_input_selector, 
                "Summarize the key points in this contract.",
                delay=TYPING_DELAY_MS
            )
            
            # Press Enter to submit
            print("↵  Pressing Enter...")
            page.keyboard.press("Enter")
            
            # Wait for bot response to appear
            print(f"⏳ Waiting {RESPONSE_WAIT_SECONDS} seconds for bot response...")
            time.sleep(RESPONSE_WAIT_SECONDS)
            
            # Take full-page screenshot
            print("📸 Capturing screenshot...")
            page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
            print(f"✅ Screenshot saved to: {SCREENSHOT_PATH}")
            
        finally:
            # Close browser to finalize video
            print("🎥 Finalizing video recording...")
            page.close()
            context.close()
            browser.close()
    
    # Rename the video file to the expected name
    print("📝 Renaming video file...")
    video_files = list(ASSETS_DIR.glob("*.webm"))
    if video_files:
        # Get the most recently created video file (excluding the target file)
        latest_video = max(
            [v for v in video_files if v != VIDEO_PATH],
            key=lambda p: p.stat().st_mtime,
            default=None
        )
        if latest_video and latest_video != VIDEO_PATH:
            # Use replace() to overwrite if exists
            latest_video.replace(VIDEO_PATH)
        print(f"✅ Video saved to: {VIDEO_PATH}")
    else:
        print("⚠️  Warning: No video file found")


def cleanup(streamlit_process):
    """Kill the Streamlit process."""
    print("\n🧹 Cleaning up...")
    if streamlit_process:
        streamlit_process.terminate()
        try:
            streamlit_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            streamlit_process.kill()
        print("✅ Streamlit process terminated")


def main():
    """Main execution function."""
    print("=" * 60)
    print("🎨 Marketing Assets Generator for DocuMind")
    print("=" * 60)
    
    # Ensure assets directory exists
    ASSETS_DIR.mkdir(exist_ok=True)
    
    streamlit_process = None
    
    try:
        # Start Streamlit app
        streamlit_process = start_streamlit_app()
        
        # Capture assets
        capture_marketing_assets(streamlit_process)
        
        print("\n" + "=" * 60)
        print("✨ Marketing assets generated successfully!")
        print("=" * 60)
        print(f"📸 Screenshot: {SCREENSHOT_PATH}")
        print(f"🎥 Video: {VIDEO_PATH}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        cleanup(streamlit_process)


if __name__ == "__main__":
    main()
