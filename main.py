
import gradio as gr

from marker_search import (
    find_formal_markers,
    find_informal_markers,
    analyze_style,
)

from pronoun_conjunction_counter import analyze_grammar

from text_comparator import get_statistics, compare_texts


def analyze_one(text):
    """Аналізує один текст."""
    if not text or not text.strip():
        return "Введіть текст для аналізу.", "", "", ""

    stats = get_statistics(text)

    stats_result = "\n".join(
        f"- **{key}:** {value}"
        for key, value in stats.items()
    )

    formal = find_formal_markers(text)
    informal = find_informal_markers(text)

    marker_result = (
        "**Формальні маркери:**\n"
        + (
            ", ".join(item["marker"] for item in formal)
            or "Не знайдено"
        )
        + "\n\n**Розмовні маркери:**\n"
        + (
            ", ".join(item["marker"] for item in informal)
            or "Не знайдено"
        )
    )

    grammar = analyze_grammar(text)

    grammar_result = (
        f"**Займенники ({grammar['pronoun_count']}):**\n"
        f"{', '.join(grammar['pronouns']) or 'Не знайдено'}\n\n"
        f"**Сполучники ({grammar['conjunction_count']}):**\n"
        f"{', '.join(grammar['conjunctions']) or 'Не знайдено'}"
    )

    style = analyze_style(text)

    style_result = (
        f"**Переважний стиль:** {style['style']}\n\n"
        f"- Формальні маркери: {style['counts']['formal']}\n"
        f"- Розмовні маркери: {style['counts']['informal']}"
    )

    return stats_result, marker_result, grammar_result, style_result


def compare_ui(text1, text2):
    """Порівнює два тексти."""
    if not text1.strip() or not text2.strip():
        return "Введіть обидва тексти для порівняння."

    results = compare_texts(text1, text2)

    output = (
        "| Показник | Текст 1 | Текст 2 | Різниця |\n"
        "|---|---:|---:|---:|\n"
    )

    for indicator, values in results.items():
        output += (
            f"| {indicator} "
            f"| {values['Текст 1']} "
            f"| {values['Текст 2']} "
            f"| {values['Різниця']} |\n"
        )

    return output


with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="pink",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("Roboto"),
    ),
    title="Аналізатор українських текстів",
) as demo:

    gr.Markdown(
        """
        # Аналізатор українських текстів

        Аналіз маркерів, займенників, сполучників
        та порівняння двох текстів.
        """
    )

    with gr.Tab("Аналіз одного тексту"):
        text_input = gr.Textbox(
            label="Введіть текст",
            placeholder="Вставте текст сюди...",
            lines=8,
        )

        analyze_button = gr.Button(
            "Проаналізувати",
            variant="primary",
        )

        stats_output = gr.Markdown(
            label="Статистика"
        )

        markers_output = gr.Markdown(
            label="Маркери"
        )

        grammar_output = gr.Markdown(
            label="Займенники та сполучники"
        )

        style_output = gr.Markdown(
            label="Стиль тексту"
        )

        analyze_button.click(
            fn=analyze_one,
            inputs=text_input,
            outputs=[
                stats_output,
                markers_output,
                grammar_output,
                style_output,
            ],
        )

    with gr.Tab("Порівняння двох текстів"):
        with gr.Row():
            text1_input = gr.Textbox(
                label="Перший текст",
                lines=8,
            )

            text2_input = gr.Textbox(
                label="Другий текст",
                lines=8,
            )

        compare_button = gr.Button(
            "Порівняти тексти",
            variant="primary",
        )

        comparison_output = gr.Markdown(
            label="Результат порівняння"
        )

        compare_button.click(
            fn=compare_ui,
            inputs=[text1_input, text2_input],
            outputs=comparison_output,
        )

    gr.Markdown(
        """
        ---
        *Результати залежать від словників, які використовують модулі.*
        """
    )

   

if __name__ == "__main__":
    demo.launch()
