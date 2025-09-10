import webbrowser
import os
import platform
import subprocess
import pyautogui


def open_google():
    webbrowser.open("https://www.google.com")


def open_youtube():
    webbrowser.open("https://www.youtube.com")


def take_screenshot(filename="screenshot.png"):
    ss = pyautogui.screenshot()
    ss.save(filename)
    return filename


def open_notepad():
    if platform.system() == "Windows":
        try:
            os.system("notepad")
        except Exception as e:
            print(f"⚠️ Could not open Notepad: {e}")
    else:
        print("Notepad is only available on Windows.")


def open_calculator():
    system = platform.system()
    if system == "Windows":
        os.system("calc")
    elif system == "Darwin":
        subprocess.Popen(["open", "-a", "Calculator"])
    elif system == "Linux":
        subprocess.Popen(["gnome-calculator"])