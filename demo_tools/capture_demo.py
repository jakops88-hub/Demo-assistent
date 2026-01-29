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
import re
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
                    page.wait_for_timeout(1000)  # Smooth transition for video
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
                    page.wait_for_timeout(1000)  # Smooth transition for video
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
            
            # Screenshot 1: Indexed files visible (improved scrolling)
            print_substep("Step 3.4: Capturing screenshot 1 (Indexed files)...")
            # Ensure sidebar is visible and scroll to top
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(1200)  # Extra settling time for layout
            page.screenshot(path=str(output_dir / "01_indexed_files.png"))
            print_substep("  ✓ Screenshot 1 saved")
            
            # Step 4: Select suggested question (Streamlit selectbox = combobox)
            print_substep("Step 3.5: Selecting HR question...")
            target_question = "vacation policy"  # Search term
            selection_successful = False
            
            for attempt in range(3):
                try:
                    print_substep(f"  Attempt {attempt + 1}/3 to select question...")
                    
                    # Strategy 1: Use combobox role (Streamlit's selectbox implementation)
                    try:
                        combobox = page.get_by_role("combobox", name="Suggested question")
                        print_substep("  Found combobox, clicking to open dropdown...")
                        combobox.click(timeout=5000)
                        page.wait_for_timeout(800)
                        
                        # Try to select the option by role
                        try:
                            option = page.get_by_role("option", name=re.compile(target_question, re.I))
                            print_substep(f"  Found option containing '{target_question}', clicking...")
                            option.click(timeout=3000)
                            page.wait_for_timeout(800)
                            print_substep("  ✓ Selected HR question (vacation policy)")
                            selection_successful = True
                            break
                        except Exception as e:
                            print_substep(f"  Option role not found: {e}")
                            # Fallback: Type the search term
                            print_substep("  Trying keyboard fallback...")
                            page.keyboard.type(target_question)
                            page.wait_for_timeout(500)
                            page.keyboard.press("Enter")
                            page.wait_for_timeout(800)
                            
                            # Verify selection by checking combobox value
                            combobox_text = combobox.text_content() or combobox.input_value()
                            if target_question.lower() in combobox_text.lower():
                                print_substep("  ✓ Selected question via keyboard input")
                                selection_successful = True
                                break
                            else:
                                raise Exception("Keyboard fallback did not select correctly")
                    
                    except Exception as combobox_error:
                        print_substep(f"  Combobox strategy failed: {combobox_error}")
                        
                        # Strategy 2: Legacy fallback - try native select element
                        # (in case Streamlit changes implementation)
                        print_substep("  Trying legacy select element fallback...")
                        selectbox = page.locator('div').filter(has_text="Suggested question").locator('select').first
                        options = selectbox.locator('option').all()
                        
                        for option in options:
                            text = option.text_content()
                            if text and target_question in text.lower():
                                option_value = option.get_attribute('value') or text
                                selectbox.select_option(value=option_value)
                                page.wait_for_timeout(800)
                                print_substep("  ✓ Selected question via select element")
                                selection_successful = True
                                break
                        
                        if selection_successful:
                            break
                        else:
                            raise Exception("No matching option found")
                
                except Exception as e:
                    if attempt == 2:
                        print_substep(f"  ⚠ All strategies failed: {e}")
                        # Last resort - try to click first available option
                        try:
                            print_substep("  Last resort: trying first option...")
                            combobox = page.get_by_role("combobox", name="Suggested question")
                            combobox.click(timeout=5000)
                            page.wait_for_timeout(500)
                            # Click first option
                            first_option = page.get_by_role("option").first
                            first_option.click(timeout=3000)
                            page.wait_for_timeout(800)
                            print_substep("  ✓ Selected first available question")
                            selection_successful = True
                        except Exception as last_error:
                            raise Exception(f"Failed all selection strategies: {last_error}")
                    else:
                        print_substep(f"  Retry after error: {e}")
                        page.wait_for_timeout(1000)
            
            if not selection_successful:
                raise Exception("Failed to select question after all attempts")
            
            # Step 5: Click "Insert question"
            print_substep("Step 3.6: Inserting question...")
            for attempt in range(3):
                try:
                    insert_btn = page.get_by_role("button", name="Insert question", exact=True)
                    insert_btn.click(timeout=5000)
                    page.wait_for_timeout(1000)  # Smooth transition for video
                    print_substep("  ✓ Question inserted")
                    break
                except Exception as e:
                    if attempt == 2:
                        raise Exception(f"Failed to insert question: {e}")
                    page.wait_for_timeout(1000)
            
            # Step 6: Submit question - handle both pending and normal modes
            print_substep("Step 3.7: Submitting question...")
            page.wait_for_timeout(500)  # Small wait for UI to update after insert
            
            for attempt in range(3):
                try:
                    # Check for pending question mode (textarea + "Ask" button)
                    pending_mode = False
                    question_text = ""
                    
                    try:
                        # Look for pending question textarea
                        textarea = page.get_by_label("Edit and press Ask to submit:", exact=True)
                        if textarea.is_visible(timeout=1000):
                            pending_mode = True
                            question_text = textarea.input_value()
                            print_substep("  Detected pending question mode (textarea + Ask)")
                    except Exception:
                        pass
                    
                    if not pending_mode:
                        # Normal mode - check text_input
                        try:
                            text_input = page.get_by_label("Ask a question", exact=True)
                            if text_input.is_visible(timeout=1000):
                                question_text = text_input.input_value()
                                print_substep("  Detected normal mode (text_input + Send)")
                        except Exception:
                            pass
                    
                    # Verify non-empty text
                    if not question_text or not question_text.strip():
                        raise Exception("No question text found in input")
                    
                    print_substep(f"  Question text present: {question_text[:50]}...")
                    
                    # Click appropriate button
                    if pending_mode:
                        ask_btn = page.get_by_role("button", name="Ask", exact=True)
                        ask_btn.click(timeout=5000)
                        print_substep("  ✓ Clicked Ask button (pending mode)")
                    else:
                        send_btn = page.get_by_role("button", name="Send", exact=True)
                        send_btn.click(timeout=5000)
                        print_substep("  ✓ Clicked Send button (normal mode)")
                    
                    page.wait_for_timeout(800)
                    print_substep("  ✓ Question submitted successfully")
                    break
                    
                except Exception as e:
                    if attempt == 2:
                        raise Exception(f"Failed to submit question after 3 attempts: {e}")
                    print_substep(f"  Retry after error: {e}")
                    page.wait_for_timeout(1000)
            
            # Step 7: Wait for answer to appear - improved detection
            print_substep("Step 3.8: Waiting for answer (up to 60s)...")
            answer_appeared = False
            
            for attempt in range(120):  # 60 seconds with 0.5s intervals
                try:
                    # Strategy 1: Count chat messages (need at least 2: user + assistant)
                    chat_messages = page.locator('[data-testid="stChatMessage"]').count()
                    if chat_messages >= 2:
                        # Verify the last message has substantial content (not just loading)
                        last_message = page.locator('[data-testid="stChatMessage"]').last
                        message_text = last_message.text_content()
                        if message_text and len(message_text) > 50:
                            answer_appeared = True
                            print_substep(f"  ✓ Answer appeared! ({chat_messages} messages, {len(message_text)} chars)")
                            break
                    
                    # Strategy 2: Look for assistant role specifically
                    assistant_messages = page.locator('[data-testid="stChatMessage"]').filter(has_text="assistant")
                    if assistant_messages.count() > 0:
                        assistant_text = assistant_messages.last.text_content()
                        if assistant_text and len(assistant_text) > 50:
                            answer_appeared = True
                            print_substep(f"  ✓ Assistant answer detected ({len(assistant_text)} chars)")
                            break
                
                except Exception:
                    pass
                
                # Progress indicator every 10 seconds
                if attempt > 0 and attempt % 20 == 0:
                    print_substep(f"  Still waiting... ({attempt // 2}s elapsed)")
                
                time.sleep(0.5)
            
            if not answer_appeared:
                raise Exception("Answer did not appear within 60s")
            
            # Wait for UI to settle
            page.wait_for_timeout(1500)
            
            # Screenshot 2: Answer in chat (improved scrolling)
            print_substep("Step 3.9: Capturing screenshot 2 (Answer)...")
            # Scroll to show the chat area with both question and answer
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1200)  # Extra settling time
            page.screenshot(path=str(output_dir / "02_answer.png"))
            print_substep("  ✓ Screenshot 2 saved")
            
            # Step 8: Look for Sources section (improved detection)
            print_substep("Step 3.10: Looking for Sources section...")
            try:
                sources_found = False
                
                # Try multiple detection strategies
                try:
                    # Strategy 1: Look for "Sources" header
                    if page.get_by_text("Sources", exact=True).is_visible(timeout=2000):
                        sources_found = True
                        print_substep("  ✓ Found 'Sources' header")
                except Exception:
                    pass
                
                if not sources_found:
                    try:
                        # Strategy 2: Look for source citations (inline or section)
                        if page.get_by_text(re.compile(r"source|citation|reference", re.I)).is_visible(timeout=1000):
                            sources_found = True
                            print_substep("  ✓ Found source/citation references")
                    except Exception:
                        pass
                
                if sources_found:
                    # Scroll to ensure sources are visible
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(800)
                else:
                    print_substep("  ℹ No explicit Sources section found (may be inline citations)")
                    # Still scroll to bottom to capture whatever is there
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(800)
                    
            except Exception as e:
                print_substep(f"  ⚠ Error detecting sources: {e}")
                # Continue anyway - scroll to bottom
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(800)
            
            # Screenshot 3: Sources visible (improved settling time)
            print_substep("Step 3.11: Capturing screenshot 3 (Sources)...")
            page.wait_for_timeout(1200)  # Extra settling time
            page.screenshot(path=str(output_dir / "03_sources.png"))
            print_substep("  ✓ Screenshot 3 saved")
            
            # Wait 2 seconds before closing to ensure clean video ending
            print_substep("Waiting 2 seconds before closing...")
            page.wait_for_timeout(2000)
            
            # Close to save video
            print_substep("Closing browser to save video...")
            context.close()
            browser.close()
            
            # Find and process video file
            print_substep("Processing video file...")
            video_temp_dir = output_dir / 'video_temp'
            video_files = list(video_temp_dir.glob('*.webm')) + list(video_temp_dir.glob('*.mp4'))
            
            if video_files:
                video_file = video_files[0]
                target_video = output_dir / 'demo.mp4'
                
                # Check if ffmpeg is available
                ffmpeg_available = False
                try:
                    result = subprocess.run(
                        ['ffmpeg', '-version'],
                        capture_output=True,
                        timeout=5
                    )
                    ffmpeg_available = (result.returncode == 0)
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    ffmpeg_available = False
                
                if ffmpeg_available:
                    # Convert webm to mp4 with ffmpeg
                    print_substep("  ffmpeg detected, converting to MP4...")
                    try:
                        result = subprocess.run(
                            ['ffmpeg', '-i', str(video_file), '-y', '-c:v', 'libx264', '-preset', 'fast', str(target_video)],
                            capture_output=True,
                            timeout=60
                        )
                        if result.returncode == 0:
                            print_substep(f"  ✓ Video converted to MP4: demo.mp4")
                        else:
                            raise subprocess.CalledProcessError(result.returncode, 'ffmpeg')
                    except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                        print_substep(f"  ⚠ ffmpeg conversion failed: {e}")
                        # Fallback to copying
                        shutil.copy(video_file, target_video)
                        print_substep(f"  ✓ Video saved as MP4 container (webm format): demo.mp4")
                else:
                    # No ffmpeg - copy webm to mp4 (playable in most browsers)
                    print_substep("  ffmpeg not available, copying as MP4 container...")
                    shutil.copy(video_file, target_video)
                    print_substep(f"  ✓ Video saved: demo.mp4 (webm in mp4 container)")
                    print_substep(f"  ℹ Install ffmpeg for proper MP4 conversion")
                
                # Clean up temp directory
                shutil.rmtree(video_temp_dir)
                print_substep("  ✓ Temp video folder removed")
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
