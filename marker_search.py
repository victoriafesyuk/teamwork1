
import re

# Словник формальних і розмовних маркерів
MARKERS = {
    "formal": [
        "відповідно до",
        "згідно з",
        "таким чином",
        "у зв'язку з",
        "прошу повідомити",
        "з повагою",
        "на підставі",
    ],
    "informal": [
        "привіт",
        "ну",
        "типу",
        "короче",
        "до речі",
        "як справи",
        "класно",
        "ага",
    ],
}


def normalize_text(text: str) -> str:
    """Нормалізує текст для пошуку."""
    return re.sub(r"\s+", " ", text.casefold()).strip()


def find_markers(text: str, dictionary: dict) -> list:
    """Знаходить усі входження маркерів зі словника."""
    normalized = normalize_text(text)
    results = []

    for category, markers in dictionary.items():
        for marker in markers:
            marker = normalize_text(marker)
            pattern = (
                r"(?<!\w)" + re.escape(marker) + r"(?!\w)"
            )

            for match in re.finditer(pattern, normalized):
                results.append({
                    "marker": marker,
                    "category": category,
                    "position": match.start(),
                })

    return sorted(results, key=lambda item: item["position"])


def find_formal_markers(text: str) -> list:
    """Шукає формальні маркери."""
    return find_markers(text, {"formal": MARKERS["formal"]})


def find_informal_markers(text: str) -> list:
    """Шукає розмовні маркери."""
    return find_markers(text, {"informal": MARKERS["informal"]})


def count_markers(text: str) -> dict:
    """Підраховує кількість формальних і розмовних маркерів."""
    found = find_markers(text, MARKERS)

    counts = {"formal": 0, "informal": 0}
    for item in found:
        counts[item["category"]] += 1

    return counts


def analyze_style(text: str) -> dict:
    """Визначає переважний стиль за знайденими маркерами."""
    counts = count_markers(text)

    if counts["formal"] > counts["informal"]:
        style = "формальний"
    elif counts["informal"] > counts["formal"]:
        style = "розмовний"
    else:
        style = "змішаний або невизначений"

    return {
        "style": style,
        "counts": counts,
        "markers": find_markers(text, MARKERS),
    }
