import speech_recognition as sr
import pyttsx3
import threading

# Initialize recognizer and engine globally
listener = sr.Recognizer()

try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
    print("✅ Speech engine initialized")
except Exception as e:
    engine = None
    print(f"⚠️ pyttsx3 initialization failed: {e}")


def talk(text: str):
    """Speak text using pyttsx3 in a non-blocking thread"""
    if not text.strip() or engine is None:
        print(f"🗣️ {text}")
        return

    def speak():
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"⚠️ Error in talk(): {e}")

    threading.Thread(target=speak, daemon=True).start()


def take_command(timeout: int = 5, phrase_time_limit: int = 8) -> str:
    """Listen and return user's command as text"""
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print("🎤 Listening...")
            voice = listener.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            command = listener.recognize_google(voice)
            return command.lower().strip()
    except sr.WaitTimeoutError:
        print("⏳ No speech detected.")
        return ""
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return ""
    except sr.RequestError:
        print("⚠️ Network issue.")
        return ""
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        return ""
