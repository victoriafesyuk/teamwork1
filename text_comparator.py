
import re

from marker_search import count_markers
from pronoun_conjunction_counter import (
    count_pronouns,
    count_conjunctions,
)


def count_words(text: str) -> int:
    """Підраховує кількість слів у тексті."""
    return len(re.findall(r"\b[^\W\d_]+\b", text, re.UNICODE))


def count_sentences(text: str) -> int:
    """Підраховує кількість речень."""
    sentences = re.findall(r"[^.!?]+[.!?]+", text)
    return len(sentences) + (
        1 if text.strip() and not re.search(r"[.!?]\s*$", text) else 0
    )


def count_unique_words(text: str) -> int:
    """Підраховує кількість унікальних слів."""
    words = re.findall(r"\b[^\W\d_]+\b", text.casefold(), re.UNICODE)
    return len(set(words))


def get_statistics(text: str) -> dict:
    """Збирає всі показники одного тексту."""
    markers = count_markers(text)

    return {
        "Кількість слів": count_words(text),
        "Кількість речень": count_sentences(text),
        "Унікальні слова": count_unique_words(text),
        "Займенники": count_pronouns(text),
        "Сполучники": count_conjunctions(text),
        "Формальні маркери": markers["formal"],
        "Розмовні маркери": markers["informal"],
    }


def compare_texts(text1: str, text2: str) -> dict:
    """Порівнює два тексти за всіма показниками."""
    stats1 = get_statistics(text1)
    stats2 = get_statistics(text2)

    return {
        key: {
            "Текст 1": stats1[key],
            "Текст 2": stats2[key],
            "Різниця": stats1[key] - stats2[key],
        }
        for key in stats1
    }


def print_comparison(text1: str, text2: str) -> None:
    """Виводить результати порівняння у вигляді таблиці."""
    results = compare_texts(text1, text2)

    print(f"{'Показник':<25} {'Текст 1':>10} {'Текст 2':>10} {'Різниця':>10}")
    print("-" * 59)

    for indicator, values in results.items():
        print(
            f"{indicator:<25} "
            f"{values['Текст 1']:>10} "
            f"{values['Текст 2']:>10} "
            f"{values['Різниця']:>10}"
        )
