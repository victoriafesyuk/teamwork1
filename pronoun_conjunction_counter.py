
import re

# Словник займенників
PRONOUNS = {
    "я", "ти", "він", "вона", "воно", "ми", "ви", "вони",
    "мене", "мені", "мною", "тебе", "тобі", "тобою",
    "його", "йому", "неї", "ній", "нами", "нас",
    "ними", "їх", "їм", "їхній", "мій", "моя", "моє",
    "мої", "твій", "твоя", "свій", "себе", "собі",
    "хто", "що", "який", "чий", "котрий", "скільки",
    "цей", "ця", "це", "ці", "той", "та", "те", "ті",
    "весь", "кожний", "кожен", "інший", "сам", "сама",
    "хтось", "щось", "ніхто", "ніщо", "будь-хто",
    "будь-що", "дехто", "дещо", "ніякий", "нічий",
    "ніякого", "своя", "свої", "наші", "ваші"
}

# Словник сполучників
CONJUNCTIONS = {
    "і", "й", "та", "а", "але", "проте", "однак",
    "або", "чи", "як", "ніж", "бо", "бо́", "тому що",
    "оскільки", "щоб", "якщо", "коли", "поки",
    "хоча", "мов", "немов", "наче", "ніби",
    "якби", "адже", "причому", "зате", "отже",
    "тобто", "для того щоб", "після того як",
    "не тільки", "але й", "як ... так і"
}


def tokenize(text: str) -> list:
    """Розбиває текст на слова та розпізнає дефісні форми."""
    return re.findall(
        r"[^\W\d_]+(?:['’ʼ-][^\W\d_]+)*",
        text.casefold(),
        flags=re.UNICODE
    )


def count_pronouns(text: str) -> int:
    """Підраховує займенники в тексті."""
    words = tokenize(text)
    return sum(word in PRONOUNS for word in words)


def count_conjunctions(text: str) -> int:
    """Підраховує сполучники за словником."""
    words = tokenize(text)
    count = 0
    i = 0

    while i < len(words):
        # Перевіряємо багатослівні сполучники
        matched = False

        for phrase in sorted(CONJUNCTIONS, key=len, reverse=True):
            parts = phrase.split()

            if len(parts) > 1 and words[i:i + len(parts)] == parts:
                count += 1
                i += len(parts)
                matched = True
                break

        if matched:
            continue

        if words[i] in CONJUNCTIONS:
            count += 1

        i += 1

    return count


def find_pronouns(text: str) -> list:
    """Повертає список знайдених займенників."""
    return [word for word in tokenize(text) if word in PRONOUNS]


def find_conjunctions(text: str) -> list:
    """Повертає список знайдених сполучників."""
    words = tokenize(text)
    found = []
    i = 0

    while i < len(words):
        matched = False

        for phrase in sorted(CONJUNCTIONS, key=len, reverse=True):
            parts = phrase.split()

            if len(parts) > 1 and words[i:i + len(parts)] == parts:
                found.append(phrase)
                i += len(parts)
                matched = True
                break

        if matched:
            continue

        if words[i] in CONJUNCTIONS:
            found.append(words[i])

        i += 1

    return found


def analyze_grammar(text: str) -> dict:
    """Повертає загальну статистику займенників і сполучників."""
    pronouns = find_pronouns(text)
    conjunctions = find_conjunctions(text)

    return {
        "pronoun_count": len(pronouns),
        "conjunction_count": len(conjunctions),
        "pronouns": pronouns,
        "conjunctions": conjunctions,
    }
