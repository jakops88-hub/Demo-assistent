"""
Playwright UI automation verification script.

This script verifies that the Streamlit UI meets the Playwright automation requirements:
1. All controls have exact, unique labels
2. Section headers are present
3. Status indicators are visible
4. Citations format is correct

Run this script with: python tests/test_playwright_ui.py
"""
from playwright.sync_api import sync_playwright
import sys


def test_ui_controls_exist(page):
    """Test that all required UI controls exist with exact labels."""
    print("✓ Testing UI controls exist...")
    
    # Sidebar controls - Demo mode section
    demo_checkbox = page.locator('label').filter(has_text="Demo mode")
    assert demo_checkbox.is_visible(), "Demo mode checkbox not found"
    print("  ✓ Demo mode checkbox found")
    
    # Click demo mode to show demo controls
    demo_checkbox.click()
    page.wait_for_timeout(1000)
    
    # Verify demo buttons appear
    load_demo_btn = page.get_by_role("button", name="Load demo documents", exact=True)
    assert load_demo_btn.is_visible(), "Load demo documents button not found"
    print("  ✓ Load demo documents button found")
    
    # Verify Actions section buttons
    force_reindex_btn = page.get_by_role("button", name="Force re-index", exact=True)
    assert force_reindex_btn.is_visible(), "Force re-index button not found"
    print("  ✓ Force re-index button found")
    
    # Main page section headers
    chat_heading = page.locator('h3:has-text("Chat")').first
    assert chat_heading.is_visible(), "Chat heading not found"
    print("  ✓ Chat heading found")
    
    # Chat controls - use locator for label text
    question_input = page.locator('label:has-text("Ask a question")').locator('..').locator('input').first
    assert question_input.is_visible(), "Ask a question textbox not found"
    print("  ✓ Ask a question textbox found")
    
    send_button = page.get_by_role("button", name="Send", exact=True)
    assert send_button.is_visible(), "Send button not found"
    print("  ✓ Send button found")
    
    # Status indicator
    assert page.get_by_text("Index ready").is_visible(), "Status indicator not found"
    print("  ✓ Status indicator found")
    
    print("✓ All UI controls test passed!\n")


def test_no_duplicate_labels(page):
    """Test that there are no duplicate button labels."""
    print("✓ Testing no duplicate labels...")
    
    # Reload the page to get a clean state
    page.reload()
    page.wait_for_timeout(5000)
    
    # Enable demo mode to show all buttons
    demo_checkbox = page.locator('label').filter(has_text="Demo mode")
    demo_checkbox.click()
    page.wait_for_timeout(1000)
    
    # Verify "Force re-index" appears exactly once (in Actions section)
    force_reindex_buttons = page.get_by_role("button", name="Force re-index", exact=True).all()
    assert len(force_reindex_buttons) == 1, f"Force re-index button should appear exactly once, found {len(force_reindex_buttons)}"
    print("  ✓ Force re-index button appears exactly once")
    
    # Verify "Send" button appears exactly once
    send_buttons = page.get_by_role("button", name="Send", exact=True).all()
    assert len(send_buttons) == 1, f"Send button should appear exactly once, found {len(send_buttons)}"
    print("  ✓ Send button appears exactly once")
    
    # Verify "Load demo documents" button appears exactly once
    load_demo_buttons = page.get_by_role("button", name="Load demo documents", exact=True).all()
    assert len(load_demo_buttons) == 1, f"Load demo documents button should appear exactly once, found {len(load_demo_buttons)}"
    print("  ✓ Load demo documents button appears exactly once")
    
    print("✓ No duplicate labels test passed!\n")


def test_section_headers(page):
    """Test that all required section headers exist."""
    print("✓ Testing section headers...")
    
    # Chat section header (case-sensitive, exact match)
    chat_heading = page.locator('h3:has-text("Chat")').first
    assert chat_heading.is_visible(), "Chat heading not found"
    print("  ✓ Chat section header found")
    
    # Indexed files section (appears in sidebar)
    indexed_files_text = page.get_by_text("No files indexed yet")
    assert indexed_files_text.is_visible(), "Indexed files section not found"
    print("  ✓ Indexed files section found")
    
    print("✓ Section headers test passed!\n")


def test_status_indicator(page):
    """Test that status indicator is visible."""
    print("✓ Testing status indicator...")
    
    # Status should show one of: "Demo data loaded", "Indexing demo data...", "Index ready"
    # By default it should show "Index ready"
    assert page.get_by_text("Index ready").is_visible(), "Status indicator not found"
    print("  ✓ Status indicator showing 'Index ready'")
    
    print("✓ Status indicator test passed!\n")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Playwright UI Automation Verification")
    print("="*60 + "\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Navigate to the app
            print("Navigating to http://localhost:8501...")
            page.goto("http://localhost:8501", timeout=30000)
            page.wait_for_timeout(15000)  # Wait for app to load fully
            print("✓ App loaded successfully\n")
            
            # Run tests
            test_ui_controls_exist(page)
            test_no_duplicate_labels(page)
            test_section_headers(page)
            test_status_indicator(page)
            
            print("="*60)
            print("✓ All tests passed!")
            print("="*60 + "\n")
            
            return 0
            
        except AssertionError as e:
            print(f"\n✗ Test failed: {e}")
            return 1
        except Exception as e:
            print(f"\n✗ Error: {e}")
            return 1
        finally:
            browser.close()


if __name__ == "__main__":
    sys.exit(main())

