# CT Institute of Higher Studies — AI Chatbot

A small-scale desktop chatbot built with Python and Tkinter that answers common questions about **CT Institute of Higher Studies** — courses, admissions, fees, facilities, placements, and contact info. Supports both typed text and **voice input (speech-to-text)**.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

##  Features

- **Chat GUI** — clean Tkinter interface with scrollable chat history
- **Speech-to-text** — click the mic button and speak your question instead of typing
- **Text-to-speech** — the bot reads its replies out loud
- **Rule-based responses** — answers questions about courses, admission process, fees, facilities, placements, contact details, and location
- **Lightweight** — single Python file, no external AI API keys or paid services required

## Installation

> **Note:** `pyaudio` currently has pre-built wheels for Python 3.8–3.13. If you're on a very new Python version (e.g. 3.14) and installation fails, install [Python 3.13](https://www.python.org/downloads/) alongside your existing version and use it for this project (see Step 2 below).

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/ct-college-chatbot.git
   cd ct-college-chatbot
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   py -3.13 -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3.13 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   **Platform notes for `pyaudio` (microphone access):**
   - **Windows:** `pip install pyaudio` (if it fails, see the note above about Python version)
   - **macOS:** `brew install portaudio` then `pip install pyaudio`
   - **Linux:** `sudo apt-get install portaudio19-dev` then `pip install pyaudio`

4. **Run the chatbot**
   ```bash
   python ct_college_chatbot.py
   ```

##  Usage

- Type a question in the input box and click **Send** (or press Enter)
- Or click **Speak** and ask your question out loud
- Try asking about: `courses`, `fees`, `admission`, `facilities`, `placement`, `contact`, or `location`
- Type `bye` / `exit` to end the conversation

## Customization

All college details live in the `COLLEGE_INFO` dictionary at the top of `ct_college_chatbot.py`. Update it with your college's accurate, current information:

```python
COLLEGE_INFO = {
    "name": "CT Institute of Higher Studies",
    "location": "...",
    "courses": [...],
    "fees": "...",
    ...
}
```

To add new topics the bot can respond to, add an entry to the `INTENTS` list with trigger keywords and a response function.

## Project Structure

```
ct-college-chatbot/
├── ct_college_chatbot.py   # Main application (GUI + chatbot logic)
├── requirements.txt        # Python dependencies
└── README.md                # This file
```
## Author
Jatinder Singh
