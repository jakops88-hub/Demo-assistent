#!/usr/bin/env python3
"""
Demo automation script for capturing screenshots and video.

This script automates the Streamlit app to generate demo assets:
- 3 high-quality screenshots  
- 1 MP4 screen recording (15-25 seconds)

Usage:
    python -m demo_tools.capture_demo
"""
import os
import sys
import time
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import requests
import psutil
from dotenv import load_dotenv

# Load .env file if present (don't require it)
load_dotenv()

# Configuration constants
STREAMLIT_PORT = 8501
STREAMLIT_URL = f"http://localhost:{STREAMLIT_PORT}"


def print_step(step_num: int, message: str):
    """Print a numbered step message."""
    print(f"\n[Step {step_num}] {message}")


def print_substep(message: str):
    """Print a sub-step message."""
    print(f"  → {message}")


def check_openai_api_key() -> bool:
    """
    Check if OPENAI_API_KEY is set in environment.
    
    Returns:
        True if key is set, False otherwise
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\n❌ ERROR: OPENAI_API_KEY environment variable is not set!")
        print("\nPlease set your OpenAI API key:")
        print("  - Linux/macOS: export OPENAI_API_KEY='your-key-here'")
        print("  - Windows: set OPENAI_API_KEY=your-key-here")
        print("  - Or add it to a .env file in the project root")
        return False
    
    print_substep(f"OPENAI_API_KEY is set (length: {len(api_key)})")
    return True


def start_streamlit(repo_root: Path) -> subprocess.Popen:
    """
    Start Streamlit as a subprocess.
    
    Args:
        repo_root: Path to repository root
        
    Returns:
        Subprocess handle
    """
    print_step(1, "Starting Streamlit server...")
    
    # Set environment variables for stability
    env = os.environ.copy()
    env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    env['STREAMLIT_SERVER_HEADLESS'] = 'true'
    env['STREAMLIT_SERVER_PORT'] = str(STREAMLIT_PORT)
    
    # Start Streamlit
    app_path = repo_root / 'app' / 'app.py'
    cmd = [
        sys.executable, '-m', 'streamlit', 'run',
        str(app_path),
        '--server.headless', 'true',
        '--server.port', str(STREAMLIT_PORT)
    ]
    
    print_substep(f"Command: {' '.join(cmd)}")
    
    process = subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(repo_root)
    )
    
    print_substep(f"Streamlit started with PID: {process.pid}")
    return process


def wait_for_streamlit_ready(timeout: int = 60) -> bool:
    """
    Poll Streamlit until it's ready to accept requests.
    
    Args:
        timeout: Maximum seconds to wait
        
    Returns:
        True if ready, False if timeout
    """
    print_step(2, "Waiting for Streamlit to be ready...")
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(STREAMLIT_URL, timeout=5)
            if response.status_code == 200 and 'streamlit' in response.text.lower():
                elapsed = time.time() - start_time
                print_substep(f"Streamlit is ready! (took {elapsed:.1f}s)")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(0.5)
    
    print(f"\n❌ ERROR: Streamlit did not become ready within {timeout}s")
    return False


def stop_process_tree(pid: int):
    """
    Stop a process and all its children using psutil.
    
    Args:
        pid: Process ID to stop
    """
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        
        # Terminate children first
        for child in children:
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                pass
        
        # Wait for children to terminate
        gone, alive = psutil.wait_procs(children, timeout=3)
        
        # Force stop any remaining
        for p in alive:
            try:
                p.kill()  # Use kill for processes that didn't terminate
            except psutil.NoSuchProcess:
                pass
        
        # Finally terminate parent
        try:
            parent.terminate()
            parent.wait(timeout=3)
        except psutil.TimeoutExpired:
            parent.kill()  # Use kill instead of terminate on timeout
        except psutil.NoSuchProcess:
            pass
            
    except psutil.NoSuchProcess:
        pass


def perform_playwright_automation(output_dir: Path) -> bool:
    """
    Perform Playwright automation to capture screenshots and video.
    
    Args:
        output_dir: Directory to save output files
        
    Returns:
        True if successful, False otherwise
    """
    print_step(3, "Starting Playwright automation...")
    
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("\n❌ ERROR: Playwright is not installed!")
        print("\nPlease install it:")
        print("  pip install -r demo_tools/requirements-demo.txt")
        print("  python -m playwright install chromium")
        return False
    
    page = None
    try:
        with sync_playwright() as p:
            # Launch browser with video recording
            print_substep("Launching Chromium browser...")
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 720},
                record_video_dir=str(output_dir / 'video_temp')
            )
            page = context.new_page()
            
            # Navigate to app
            print_substep(f"Navigating to {STREAMLIT_URL}...")
            page.goto(STREAMLIT_URL, timeout=30000)
            page.wait_for_timeout(3000)
            
            # Step 1: Enable demo mode
            print_substep("Step 3.1: Enabling demo mode...")
            for attempt in range(3):
                try:
                    demo_checkbox = page.get_by_role("checkbox", name="Demo mode")
                    demo_checkbox.check(timeout=5000)
                    page.wait_for_timeout(800)
                    print_substep("  ✓ Demo mode enabled")
                    break
                except Exception as e:
                    if attempt == 2:
                        raise Exception(f"Failed to enable demo mode: {e}")
                    page.wait_for_timeout(1000)
            
            # Step 2: Click "Load demo documents"
            print_substep("Step 3.2: Loading demo documents...")
            for attempt in range(3):
                try:
                    load_btn = page.get_by_role("button", name="Load demo documents", exact=True)
                    load_btn.click(timeout=5000)
                    page.wait_for_timeout(800)
                    print_substep("  ✓ Clicked Load demo documents")
                    break
                except Exception as e:
                    if attempt == 2:
                        raise Exception(f"Failed to click Load demo documents: {e}")
                    page.wait_for_timeout(1000)
            
            # Step 3: Wait for indexing to complete
            print_substep("Step 3.3: Waiting for indexing to complete (up to 120s)...")
            for attempt in range(240):  # 120 seconds with 0.5s intervals
                try:
                    # Look for success message or indexed files indicator
                    if (page.get_by_text("Demo documents indexed").is_visible(timeout=500) or
                        page.get_by_text("Demo data loaded").is_visible(timeout=500) or
                        page.get_by_text("Index ready").is_visible(timeout=500) or
                        page.get_by_text("Indexed files").is_visible(timeout=500)):
                        print_substep("  ✓ Indexing complete!")
                        break
                except Exception:  # Catch Playwright timeout and other exceptions
                    pass
                
                if attempt == 239:  # After 240 attempts * 0.5s = 120s timeout
                    raise Exception("Indexing did not complete within 120s")
                
                time.sleep(0.5)
            
            # Wait for UI to settle
            page.wait_for_timeout(1000)
            
            # Screenshot 1: Indexed files visible
            print_substep("Step 3.4: Capturing screenshot 1 (Indexed files)...")
            # Scroll to ensure indexed files section is visible
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(1000)
            page.screenshot(path=str(output_dir / "01_indexed_files.png"))
            print_substep("  ✓ Screenshot 1 saved")
            
            # Step 4: Select suggested question
            print_substep("Step 3.5: Selecting HR question...")
            target_question = "What is the vacation policy for employees in Sweden vs Germany?"
            for attempt in range(3):
                try:
                    # Find the selectbox using text-based filter locator
                    # Note: We use a text filter because the selectbox doesn't have a proper role attribute
                    selectbox_container = page.locator('div').filter(has_text="Suggested question").locator('select').first
                    
                    # Strategy 1: Try to find option with exact target question
                    options = selectbox_container.locator('option').all()
                    question_found = False
                    for option in options:
                        text = option.text_content()
                        if text and target_question in text:
                            option_value = option.get_attribute('value') or text
                            selectbox_container.select_option(value=option_value)
                            page.wait_for_timeout(800)
                            print_substep(f"  ✓ Selected HR question: {target_question}")
                            question_found = True
                            break
                    
                    if question_found:
                        break
                    
                    # Strategy 2: Try selecting by label text with category prefix
                    try:
                        selectbox_container.select_option(label=f"[hr] {target_question}")
                        page.wait_for_timeout(800)
                        print_substep("  ✓ Selected HR question by label")
                        break
                    except Exception:
                        pass
                    
                    # Strategy 3: Search for partial match with "vacation policy"
                    for option in options:
                        text = option.text_content()
                        if text and "vacation policy" in text.lower():
                            option_value = option.get_attribute('value') or text
                            selectbox_container.select_option(value=option_value)
                            page.wait_for_timeout(800)
                            print_substep("  ✓ Selected vacation policy question")
                            break
                    else:
                        # No match found, raise exception to trigger retry
                        raise Exception("Target question not found in options")
                    
                    # If we reach here, strategy 3 succeeded
                    break
                        
                except Exception as e:
                    if attempt == 2:
                        # Last attempt - try first available demo question
                        print_substep(f"  ⚠ Could not select specific question, trying first available...")
                        try:
                            selectbox_container = page.locator('div').filter(has_text="Suggested question").locator('select').first
                            selectbox_container.select_option(index=1)  # Select first non-empty option
                            page.wait_for_timeout(800)
                            print_substep("  ✓ Selected first available question")
                            break
                        except Exception:  # Catch Playwright errors
                            raise Exception(f"Failed to select question: {e}")
                    page.wait_for_timeout(1000)
            
            # Step 5: Click "Insert question"
            print_substep("Step 3.6: Inserting question...")
            for attempt in range(3):
                try:
                    insert_btn = page.get_by_role("button", name="Insert question", exact=True)
                    insert_btn.click(timeout=5000)
                    page.wait_for_timeout(800)
                    print_substep("  ✓ Question inserted")
                    break
                except Exception as e:
                    if attempt == 2:
                        raise Exception(f"Failed to insert question: {e}")
                    page.wait_for_timeout(1000)
            
            # Step 6: Verify question text is in input and click Ask/Send
            print_substep("Step 3.7: Submitting question...")
            for attempt in range(3):
                try:
                    # Look for Ask or Send button
                    try:
                        ask_btn = page.get_by_role("button", name="Ask", exact=True)
                        ask_btn.click(timeout=5000)
                    except Exception:  # Catch Playwright errors, try Send button
                        send_btn = page.get_by_role("button", name="Send", exact=True)
                        send_btn.click(timeout=5000)
                    
                    page.wait_for_timeout(800)
                    print_substep("  ✓ Question submitted")
                    break
                except Exception as e:
                    if attempt == 2:
                        raise Exception(f"Failed to submit question: {e}")
                    page.wait_for_timeout(1000)
            
            # Step 7: Wait for answer to appear
            print_substep("Step 3.8: Waiting for answer (up to 60s)...")
            answer_appeared = False
            for attempt in range(120):  # 60 seconds with 0.5s intervals
                try:
                    # Check if assistant message appeared in chat
                    # Look for common answer patterns
                    chat_messages = page.locator('[data-testid="stChatMessage"]').count()
                    if chat_messages >= 2:
                        answer_appeared = True
                        print_substep("  ✓ Answer appeared!")
                        break
                except Exception:  # Catch Playwright errors
                    pass
                
                time.sleep(0.5)
            
            if not answer_appeared:
                raise Exception("Answer did not appear within 60s")
            
            # Wait for UI to settle
            page.wait_for_timeout(1500)
            
            # Screenshot 2: Answer in chat
            print_substep("Step 3.9: Capturing screenshot 2 (Answer)...")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000)
            page.screenshot(path=str(output_dir / "02_answer.png"))
            print_substep("  ✓ Screenshot 2 saved")
            
            # Step 8: Scroll to Sources section if present
            print_substep("Step 3.10: Looking for Sources section...")
            try:
                # Try to find Sources section or citations
                sources_found = False
                try:
                    if page.get_by_text("Sources").is_visible(timeout=2000) or page.get_by_text("source").is_visible(timeout=1000):
                        sources_found = True
                except Exception:  # Catch Playwright timeout errors
                    pass
                
                if sources_found:
                    # Scroll to make sources visible
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(800)
                    print_substep("  ✓ Sources section visible")
                else:
                    print_substep("  ℹ Sources section not explicitly found (may be inline citations)")
            except Exception as e:
                print_substep(f"  ⚠ Could not locate sources: {e}")
            
            # Screenshot 3: Sources visible  
            print_substep("Step 3.11: Capturing screenshot 3 (Sources)...")
            page.wait_for_timeout(1000)
            page.screenshot(path=str(output_dir / "03_sources.png"))
            print_substep("  ✓ Screenshot 3 saved")
            
            # Wait 2 seconds before closing to ensure clean video ending
            print_substep("Waiting 2 seconds before closing...")
            page.wait_for_timeout(2000)
            
            # Close to save video
            print_substep("Closing browser to save video...")
            context.close()
            browser.close()
            
            # Find and rename video file
            print_substep("Processing video file...")
            video_temp_dir = output_dir / 'video_temp'
            video_files = list(video_temp_dir.glob('*.webm')) + list(video_temp_dir.glob('*.mp4'))
            
            if video_files:
                video_file = video_files[0]
                target_video = output_dir / 'demo.mp4'
                
                # Try to convert to mp4 if ffmpeg is available
                try:
                    result = subprocess.run(
                        ['ffmpeg', '-i', str(video_file), '-y', str(target_video)],
                        capture_output=True,
                        timeout=30
                    )
                    if result.returncode == 0:
                        print_substep(f"  ✓ Video converted to MP4: demo.mp4")
                    else:
                        raise subprocess.CalledProcessError(result.returncode, 'ffmpeg')
                except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
                    # If ffmpeg not available or failed, just rename .webm to .mp4
                    shutil.copy(video_file, target_video)
                    print_substep(f"  ✓ Video saved: demo.mp4 (webm format)")
                
                # Clean up temp directory
                shutil.rmtree(video_temp_dir)
            else:
                print_substep("  ⚠ Warning: No video file found")
            
            print_substep("✓ Automation completed successfully!")
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR during automation: {e}")
        
        # Try to capture debug screenshot
        if page:
            try:
                page.screenshot(path=str(output_dir / "error.png"))
                print(f"\n📸 Debug screenshot saved: {output_dir}/error.png")
                
                # Try to get visible error text
                error_elements = page.locator('[role="alert"]').all()
                if error_elements:
                    error_texts = [elem.text_content() for elem in error_elements]
                    print(f"\n🔍 Visible error messages: {error_texts}")
            except Exception:  # Catch any errors during debug screenshot capture
                pass
        
        return False


def main():
    """Main entry point."""
    print("="*70)
    print("Demo Automation Tool - Screenshot & Video Capture")
    print("="*70)
    
    # Get repository root
    repo_root = Path(__file__).parent.parent.absolute()
    print(f"\nRepository root: {repo_root}")
    
    # Check for OPENAI_API_KEY
    if not check_openai_api_key():
        return 1
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_dir = repo_root / 'demo_tools' / 'output' / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nOutput directory: {output_dir}")
    
    streamlit_process = None
    
    try:
        # Start Streamlit
        streamlit_process = start_streamlit(repo_root)
        
        # Wait for Streamlit to be ready
        if not wait_for_streamlit_ready():
            return 1
        
        # Perform automation
        if not perform_playwright_automation(output_dir):
            return 1
        
        print("\n" + "="*70)
        print("✓ Demo automation completed successfully!")
        print("="*70)
        print(f"\nOutput files saved to: {output_dir}")
        print("\nGenerated assets:")
        for file in sorted(output_dir.glob('*')):
            if file.is_file():
                size_kb = file.stat().st_size / 1024
                print(f"  • {file.name} ({size_kb:.1f} KB)")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Clean shutdown
        if streamlit_process:
            print_step(4, "Shutting down Streamlit...")
            try:
                stop_process_tree(streamlit_process.pid)
                print_substep("✓ Streamlit stopped")
            except Exception as e:
                print_substep(f"⚠ Error stopping Streamlit: {e}")


if __name__ == "__main__":
    sys.exit(main())
