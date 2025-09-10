import wikipedia
import datetime
import pyjokes
import webbrowser
import os
# Nicknames and aliases
nicknames = {
    "e musk": "Elon Musk",
    "bill g": "Bill Gates",
    "taylor": "Taylor Swift"
}

aliases = {
    "elon": "Elon Musk",
    "e musk": "Elon Musk",
    "br ambedkar": "B. R. Ambedkar",
    "ambedkar": "B. R. Ambedkar",
    "modi": "Narendra Modi",
    "mamata baner": "Mamata Banerjee",
    "mamata": "Mamata Banerjee",
    "zucker": "Mark Zuckerberg"
}


def get_info(query: str) -> str:
    try:
        # Clean query
        person = query.lower().replace("who is", "").replace("tell me about", "").strip()

        # Replace nicknames and aliases
        for short, full in {**nicknames, **aliases}.items():
            if short in person:
                person = full

        # Capitalize properly for Wikipedia
        person = person.title()

        # Fetch summary
        return wikipedia.summary(person, sentences=2)

    except wikipedia.exceptions.DisambiguationError:
        return "That is too broad, please be more specific."
    except wikipedia.exceptions.PageError:
        return f"Sorry, I could not find information about {person}."
    except Exception as e:
        return f"I had trouble connecting to Wikipedia: {e}"


def play_on_youtube(song: str):
    """Open YouTube search results in Chrome or Edge only"""
    url = f"https://www.youtube.com/results?search_query={song}"

    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s"

    if os.path.exists(chrome_path.split()[0]):
        import webbrowser
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open(url)
    elif os.path.exists(edge_path.split()[0]):
        import webbrowser
        webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
        webbrowser.get('edge').open(url)
    else:
        print("⚠️ No browser found, cannot open YouTube.")




def get_time() -> str:
    return datetime.datetime.now().strftime("%I:%M %p")


def tell_joke() -> str:
    return pyjokes.get_joke()

