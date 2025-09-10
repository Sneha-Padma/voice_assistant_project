import sounddevice as sd
import numpy as np
import pyttsx3
import speech_recognition as sr
import tempfile


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
    
    print(f"🤖 Assistant: {text}")
    
    def speak():
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"⚠️ Error in talk(): {e}")
    
    speak()


def take_command(duration: int = 5) -> str:
    """
    Record from the microphone using sounddevice (PyAudio-free)
    and return recognized text using SpeechRecognition.
    duration: seconds to record
    """
    r = sr.Recognizer()
    fs = 44100  # sampling rate

    print("🎤 Listening...")
    try:
        # Record audio
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished
        print("✅ Recording complete")

        # Save to temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            from scipy.io import wavfile
            wavfile.write(f.name, fs, (audio_data * 32767).astype(np.int16))
            wav_filename = f.name

        # Recognize using SpeechRecognition
        with sr.AudioFile(wav_filename) as source:
            audio = r.record(source)
            try:
                text = r.recognize_google(audio)
                print(f"📝 You said: {text}")
                return text.lower().strip()
            except sr.UnknownValueError:
                print("❌ Could not understand audio.")
                return ""
            except sr.RequestError as e:
                print(f"⚠️ Could not request results; {e}")
                return ""

    except Exception as e:
        print(f"⚠️ Error recording audio: {e}")
        return ""