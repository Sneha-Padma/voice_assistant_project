# __init__.py
import speech_recognition as sr
import pyttsx3
from .speech import talk, take_command
from .automation import open_google, open_youtube, open_notepad, open_calculator, take_screenshot
from .commands import get_info, play_on_youtube, get_time, tell_joke

listener = sr.Recognizer()

try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Try to set a female voice if available
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    else:
        engine.setProperty('voice', voices[0].id)  # fallback

    print("✅ Voice Assistant package initialized with pyttsx3")

except Exception as e:
    engine = None
    print(f"⚠️ pyttsx3 initialization failed: {e}")
