========================================
  DOCUMENT CHATBOT - FIRST RUN GUIDE
========================================

Welcome! This guide helps you start the chatbot in just a few steps.

STEP 1: INSTALL PYTHON
-----------------------
You need Python 3.10 or higher installed on your computer.

Download from: https://www.python.org/downloads/

IMPORTANT for Windows users:
  ✓ Check "Add Python to PATH" during installation

STEP 2: SET UP YOUR API KEY (OpenAI users only)
------------------------------------------------
If you're using OpenAI models:

1. Copy the file ".env.example" to ".env" (same folder)
2. Open ".env" in a text editor
3. Replace "your-openai-api-key-here" with your actual OpenAI API key
4. Save the file

Get your API key from: https://platform.openai.com/api-keys

STEP 3: START THE CHATBOT
--------------------------
Windows:  Double-click "Start Chatbot.bat" in the launcher folder
macOS:    First run: chmod +x "launcher/Start Chatbot.command"
          Then double-click "Start Chatbot.command"
Linux:    Run: ./launcher/start.sh

First run takes 2-3 minutes to set up dependencies.
Next runs are instant!

STEP 4: USE THE CHATBOT
------------------------
1. Upload your documents (PDF, DOCX, TXT, CSV)
2. Click "Re-index Documents" button
3. Wait for indexing to complete
4. Ask questions about your documents!

TROUBLESHOOTING
---------------

Problem: "Python not found"
Solution: Install Python 3.10+ and make sure it's in your PATH
          Restart your computer after installation

Problem: "OPENAI_API_KEY not found"
Solution: Follow Step 2 above to create a .env file with your API key
          Make sure the file is named ".env" (not ".env.txt")

Problem: "Port 8501 already in use"
Solution: Another app is using that port. Close other Streamlit apps
          Or kill the process using: taskkill /F /IM streamlit.exe (Windows)
          Or: pkill -f streamlit (macOS/Linux)

NEED MORE HELP?
---------------
Check the main README.md file for detailed documentation.
