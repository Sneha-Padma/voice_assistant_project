import wikipedia
import pywhatkit
import datetime
import pyjokes

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
        person = query.lower().replace("who is", "").replace("tell me about", "").strip()

        # Replace nicknames and aliases
        for short, full in {**nicknames, **aliases}.items():
            if short in person:
                person = full

        return wikipedia.summary(person, sentences=2)

    except wikipedia.exceptions.DisambiguationError:
        return "That is too broad, please be more specific."
    except wikipedia.exceptions.PageError:
        return f"Sorry, I could not find information about {person}."
    except Exception as e:
        return f"I had trouble connecting to Wikipedia: {e}"


def play_on_youtube(song: str):
    pywhatkit.playonyt(song)


def get_time() -> str:
    return datetime.datetime.now().strftime("%I:%M %p")


def tell_joke() -> str:
    return pyjokes.get_joke()
