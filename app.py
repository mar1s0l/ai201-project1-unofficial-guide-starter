"""
app.py
------
Gradio interface for the UCLA Dining RAG pipeline.

Run:
    python app.py
"""

import gradio as gr
from query import ask, reset_conversation


def handle_query(question: str) -> tuple[str, str]:
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

def handle_reset():
    reset_conversation()
    return "", "", ""

# if __name__=="__main__":
#     print(handle_query("Are dishes properly labeled for food allergens?"))
#     print(handle_query("Can I take food to go from the dining halls?"))
#     print(handle_query("What is the cost of a salad?"))

with gr.Blocks(title="UCLA Dining Assistant") as demo:
    gr.Markdown("## 🍽️ UCLA Dining Assistant")
    gr.Markdown(
        "Ask anything about UCLA dining halls, meal plans, food options, "
        "or dietary restrictions. Answers are grounded in student reviews "
        "and campus resources only."
    )

    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. Which dining hall has the best vegan options?",
    )
    btn = gr.Button("Ask", variant="primary")
    
    reset_btn = gr.Button("Reset conversation")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])
    reset_btn.click(handle_reset, outputs=[inp, answer, sources])

demo.launch()
