import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import tempfile

r = sr.Recognizer()

# Record audio using sounddevice
duration = 5  # seconds
fs = 44100  # sample rate
print("🎤 Speak now...")
audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
print("✅ Recording complete")

# Save to temporary WAV file
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
    wav.write(f.name, fs, (audio_data * 32767).astype(np.int16))
    wav_filename = f.name

# Recognize using SpeechRecognition
with sr.AudioFile(wav_filename) as source:
    audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        print(f"📝 You said: {text}")
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
    except sr.RequestError as e:
        print(f"⚠️ Could not request results; {e}")
