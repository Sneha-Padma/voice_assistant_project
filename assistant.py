# assistant.py
from dotenv import load_dotenv
import os
import threading
import time
import openai
from modules import speech, automation, commands

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Optional start sound
sound_path = os.path.join(os.path.dirname(__file__), "assets", "sounds", "start.wav")
if os.path.exists(sound_path):
    threading.Thread(
        target=lambda: os.system(f'start /min "" "{sound_path}"'),
        daemon=True
    ).start()
else:
    print("Start sound not found, skipping.")

# Nicknames for preprocessing
nicknames = {
    "e musk": "Elon Musk",
    "bill g": "Bill Gates",
    "taylor": "Taylor Swift"
}

print("✅ OpenAI API Key Loaded:", openai.api_key is not None)


def speak_text(text: str, use_openai=False, filename="response.mp3"):
    """Speak text using local TTS or OpenAI TTS"""
    if not text.strip():
        return
    if use_openai and openai.api_key:
        try:
            from pydub import AudioSegment
            from pydub.playback import _play_with_simpleaudio as play
            import imageio_ffmpeg as ffmpeg

            AudioSegment.converter = ffmpeg.get_ffmpeg_exe()

            response = openai.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="alloy",
                input=text
            )
            with open(filename, "wb") as f:
                f.write(response.audio_data)

            def play_audio():
                sound = AudioSegment.from_file(filename, format="mp3")
                play(sound)

            threading.Thread(target=play_audio, daemon=True).start()
        except Exception as e:
            print(f"⚠️ TTS API error: {e}")
            speech.talk(text)
    else:
        speech.talk(text)


def preprocess_command(cmd: str) -> str:
    """Replace nicknames in user command"""
    for short, full in nicknames.items():
        if short in cmd:
            cmd = cmd.replace(short, full.lower())
    return cmd.strip()


def run_assistant():
    """Main assistant logic"""
    command = speech.take_command()
    if not command:
        return

    command = preprocess_command(command)
    print(f"🎤 User said: {command}")

    # Exit commands
    if any(word in command for word in ["stop", "exit", "quit", "bye", "thank you"]):
        speak_text("Goodbye Sneha!")
        exit()

    # Play YouTube
    elif "play" in command:
        song = command.replace("play", "")
        speak_text(f"Playing {song}")
        commands.play_on_youtube(song)

    # Open apps / browser
    elif "open google" in command:
        speak_text("Opening Google")
        automation.open_google()
    elif "open youtube" in command:
        speak_text("Opening YouTube")
        automation.open_youtube()
    elif "screenshot" in command:
        filename = automation.take_screenshot()
        speak_text(f"Screenshot saved as {filename}")
    elif "open notepad" in command:
        speak_text("Opening Notepad")
        automation.open_notepad()
    elif "open calculator" in command:
        speak_text("Opening Calculator")
        automation.open_calculator()

    # Joke
    elif "joke" in command:
        speak_text(commands.tell_joke())

    # Time
    elif "time" in command:
        speak_text(f"Current time is {commands.get_time()}")

    # Wikipedia / general info
    else:
        info = commands.get_info(command)
        speak_text(info)


if __name__ == "__main__":
    while True:
        try:
            run_assistant()
        except Exception as e:
            print(f"⚠️ Error: {e}")
            speak_text("Something went wrong. Please try again.")
            time.sleep(1)
