"""
CT Institute of Higher Studies - AI Chatbot (GUI + Speech-to-Text)
-------------------------------------------------------------------
A small-scale desktop chatbot built with Tkinter that answers common
questions about CT Institute of Higher Studies. Supports both typed
text input and voice input (speech-to-text via microphone).

HOW TO RUN:
    1. Install dependencies (see requirements.txt / instructions below):
         pip install SpeechRecognition pyaudio pyttsx3

       Notes on pyaudio (needed for microphone access):
         - Windows: pip install pyaudio
           (if that fails, install a prebuilt wheel: pip install pipwin && pipwin install pyaudio)
         - macOS:   brew install portaudio  then  pip install pyaudio
         - Linux:   sudo apt-get install python3-pyaudio  (or) 
                    sudo apt-get install portaudio19-dev && pip install pyaudio

    2. Run:
         python ct_college_chatbot.py

CUSTOMIZE:
    - Edit COLLEGE_INFO below with the college's real, up-to-date details.
    - Add more topics/keywords in the INTENTS list to expand what the bot can answer.
"""

import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import random

# Optional dependencies - handled gracefully if not installed yet
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


# ------------------------------------------------------------------
# 1. COLLEGE INFO - EDIT WITH REAL / UP-TO-DATE DETAILS
# ------------------------------------------------------------------
COLLEGE_INFO = {
    "name": "CT Institute of Higher Studies",
    "location": "Jalandhar, Punjab, India",
    "established": "part of the CT Group of Institutions",
    "courses": [
        "B,VOC",
        "BCA / MCA",
        "BBA / MBA",
        "B.Com / M.Com",
        "Diploma courses in Engineering",
        "B.A / M.A",
    ],
    "fees": "Fees vary by course and category. Please check the official website or contact admissions for the current fee structure.",
    "admission_process": "Admissions are based on merit in 12th followed by counselling and document verification.",
    "facilities": [
        "Library", "Hostel (Boys & Girls)", "Sports Complex", "Wi-Fi Campus",
        "Computer Labs", "Cafeteria", "Auditorium", "Transport Facility",
        "Placement Cell",
    ],
    "placement": "The Institute has a dedicated Training & Placement Cell that organizes campus placement drives, internships, and skill-development workshops with various companies.",
    "contact_email": "info@ctgroup.in",
    "contact_phone": "1800-137-2227",
    "website": "www.ctgroup.in",
}


# ------------------------------------------------------------------
# 2. CHATBOT RESPONSE LOGIC
# ------------------------------------------------------------------
def about_response():
    return (f"{COLLEGE_INFO['name']} is located in {COLLEGE_INFO['location']}. "
            f"It is {COLLEGE_INFO['established']}.")

def courses_response():
    courses = "\n  • " + "\n  • ".join(COLLEGE_INFO["courses"])
    return f"We offer the following courses:{courses}"

def fees_response():
    return f"Fee Information: {COLLEGE_INFO['fees']}"

def admission_response():
    return f"Admission Process: {COLLEGE_INFO['admission_process']}"

def facilities_response():
    facilities = ", ".join(COLLEGE_INFO["facilities"])
    return f"Campus facilities include: {facilities}."

def placement_response():
    return COLLEGE_INFO["placement"]

def contact_response():
    return (f"You can reach us at:\n"
            f"  📧 Email: {COLLEGE_INFO['contact_email']}\n"
            f"  📞 Phone: {COLLEGE_INFO['contact_phone']}\n"
            f"  🌐 Website: {COLLEGE_INFO['website']}")

def location_response():
    return f"{COLLEGE_INFO['name']} is located in {COLLEGE_INFO['location']}."

def greeting_response():
    return random.choice([
        "Hello! Welcome to CT Institute of Higher Studies chatbot. How can I help you?",
        "Hi there! Ask me about courses, admission, fees, facilities, or placements.",
        "Hey! What would you like to know about our college?",
    ])

def thanks_response():
    return "You're welcome! Feel free to ask anything else about the college."

def fallback_response():
    return ("Sorry, I didn't quite understand that. You can ask me about:\n"
            "  • college / about\n"
            "  • courses\n"
            "  • fees\n"
            "  • admission\n"
            "  • facilities\n"
            "  • placement\n"
            "  • contact\n"
            "  • location")

INTENTS = [
    (["hello", "hi", "hey"], greeting_response),
    (["thank", "thanks"], thanks_response),
    (["about", "college", "institute", "history", "established"], about_response),
    (["course", "courses", "program", "programs", "degree", "branch"], courses_response),
    (["fee", "fees", "cost", "tuition"], fees_response),
    (["admission", "apply", "application", "entrance", "eligibility"], admission_response),
    (["facility", "facilities", "hostel", "library", "campus"], facilities_response),
    (["placement", "job", "career", "company", "companies"], placement_response),
    (["contact", "email", "phone", "number", "website"], contact_response),
    (["location", "where", "address", "city"], location_response),
]

EXIT_WORDS = {"bye", "exit", "quit", "goodbye"}


def get_response(user_input: str) -> str:
    text = user_input.lower()
    if any(word in text for word in EXIT_WORDS):
        return "Goodbye! Have a great day. 👋"
    for keywords, response_fn in INTENTS:
        if any(keyword in text for keyword in keywords):
            return response_fn()
    return fallback_response()


# ------------------------------------------------------------------
# 3. GUI APPLICATION
# ------------------------------------------------------------------
class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{COLLEGE_INFO['name']} - Chatbot")
        self.root.geometry("520x620")
        self.root.configure(bg="#f0f2f5")
        self.root.resizable(False, False)

        # Text-to-speech engine (optional)
        self.tts_engine = pyttsx3.init() if TTS_AVAILABLE else None

        self._build_widgets()
        self._display_bot_message(greeting_response())

    def _build_widgets(self):
        # Header
        header = tk.Frame(self.root, bg="#0b5394", height=60)
        header.pack(fill=tk.X)
        tk.Label(
            header, text=f"🎓 {COLLEGE_INFO['name']}", bg="#0b5394", fg="white",
            font=("Segoe UI", 14, "bold"), pady=15
        ).pack()

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state="disabled", font=("Segoe UI", 10),
            bg="white", relief=tk.FLAT, padx=10, pady=10
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_display.tag_config("user", foreground="#0b5394", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("bot", foreground="#333333", font=("Segoe UI", 10, "bold"))

        # Bottom input frame
        input_frame = tk.Frame(self.root, bg="#f0f2f5")
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.entry = tk.Entry(input_frame, font=("Segoe UI", 11))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 6))
        self.entry.bind("<Return>", lambda event: self._on_send())

        send_btn = tk.Button(
            input_frame, text="Send", command=self._on_send,
            bg="#0b5394", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, padx=12
        )
        send_btn.pack(side=tk.LEFT, padx=(0, 6))

        mic_btn = tk.Button(
            input_frame, text="🎤 Speak", command=self._on_mic_click,
            bg="#34a853", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, padx=12
        )
        mic_btn.pack(side=tk.LEFT)
        self.mic_btn = mic_btn

        if not SPEECH_RECOGNITION_AVAILABLE:
            mic_btn.config(state="disabled", bg="#999999")

        # Status label
        self.status_label = tk.Label(
            self.root, text="", bg="#f0f2f5", fg="#666666", font=("Segoe UI", 9)
        )
        self.status_label.pack(pady=(0, 6))

    # ---------------- Chat display helpers ----------------
    def _display_user_message(self, text):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, "You: ", "user")
        self.chat_display.insert(tk.END, text + "\n\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def _display_bot_message(self, text):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, "Bot: ", "bot")
        self.chat_display.insert(tk.END, text + "\n\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)
        self._speak(text)

    def _speak(self, text):
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception:
                pass  # Fail silently if TTS has issues

    # ---------------- Actions ----------------
    def _on_send(self):
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.entry.delete(0, tk.END)
        self._display_user_message(user_text)
        response = get_response(user_text)
        self._display_bot_message(response)

    def _on_mic_click(self):
        if not SPEECH_RECOGNITION_AVAILABLE:
            messagebox.showwarning(
                "Speech Recognition Unavailable",
                "Please install the required packages:\npip install SpeechRecognition pyaudio"
            )
            return
        # Run recognition in a background thread so the GUI doesn't freeze
        self.mic_btn.config(state="disabled", bg="#999999")
        self.status_label.config(text="🎤 Listening... please speak now")
        thread = threading.Thread(target=self._listen_and_process, daemon=True)
        thread.start()

    def _listen_and_process(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

            self.status_label.config(text="🔎 Recognizing speech...")
            text = recognizer.recognize_google(audio)

            self.root.after(0, self._handle_recognized_text, text)
        except sr.WaitTimeoutError:
            self.root.after(0, self._reset_status, "No speech detected. Try again.")
        except sr.UnknownValueError:
            self.root.after(0, self._reset_status, "Sorry, couldn't understand the audio.")
        except sr.RequestError:
            self.root.after(0, self._reset_status, "Speech service unavailable (check internet connection).")
        except Exception as e:
            self.root.after(0, self._reset_status, f"Error: {e}")
        finally:
            self.root.after(0, lambda: self.mic_btn.config(state="normal", bg="#34a853"))

    def _handle_recognized_text(self, text):
        self.status_label.config(text="")
        self._display_user_message(text)
        response = get_response(text)
        self._display_bot_message(response)

    def _reset_status(self, message):
        self.status_label.config(text=message)


# ------------------------------------------------------------------
# 4. MAIN ENTRY POINT
# ------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()
