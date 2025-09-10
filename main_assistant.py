from modules.speech import take_command, talk
from modules.commands import get_info, play_on_youtube, get_time, tell_joke
import webbrowser
import os
import platform
import pyautogui
import subprocess

def main():
    talk("Hello! I am your assistant. How can I help you today?")

    while True:
        query = take_command()

        if not query:
            continue

        # Exit condition
        if "exit" in query or "quit" in query or "stop" in query:
            talk("Goodbye! Have a great day.")
            break

        # Wikipedia queries
        elif "wikipedia" in query or "who is" in query or "tell me about" in query:
            short_answer = get_info(query)  # Get summary
            talk("Here is the answer.")
            talk(short_answer)

            # Open full Wikipedia page
            topic = query.lower().replace("who is", "").replace("tell me about", "").replace("wikipedia", "").strip()
            if topic:
                url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
                webbrowser.open(url)

        # YouTube search
        elif "play" in query and "youtube" in query:
            song = query.replace("play", "").replace("on youtube", "").strip()
            play_on_youtube(song)
            talk(f"Playing {song} on YouTube.")

        # Time
        elif "time" in query:
            current_time = get_time()
            talk(f"The time is {current_time}")

        # Joke
        elif "joke" in query:
            joke = tell_joke()
            talk(joke)

        # Open Google
        elif "open google" in query:
            webbrowser.open("https://www.google.com")
            talk("Opening Google.")

        # Open Notepad
        elif "open notepad" in query:
            if platform.system() == "Windows":
                subprocess.Popen(["notepad.exe"])
            talk("Opening Notepad.")

        # Take Screenshot
        elif "screenshot" in query:
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            talk("Screenshot taken and saved as screenshot.png.")

        else:
            talk("Sorry, I didn't understand that.")

if __name__ == "__main__":
    main()
