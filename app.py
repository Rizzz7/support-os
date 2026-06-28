import gradio as gr
from supportos.orchestrator import run_supportos


def ask(question):

    if not question.strip():
        return "", "", ""

    result = run_supportos(question)

    verification = result["verification"]

    verify = f"""Grounded : {"YES" if verification["grounded"] else "NO"}

Risk : {verification["risk"]}

Action : {verification["action"]}
"""

    if verification["escalate"]:
        verify += f"""

Human Escalation Required

Reason:
{verification["reason"]}
"""

    sources = "\n".join(result["sources"])

    return (
        result["answer"],
        verify,
        sources
    )


demo = gr.Interface(
    fn=ask,
    inputs=gr.Textbox(
        lines=2,
        placeholder="Ask SupportOS..."
    ),
    outputs=[
        gr.Textbox(label="Answer", lines=10),
        gr.Textbox(label="Verification"),
        gr.Textbox(label="Sources")
    ],
    title="SupportOS",
    description="AI Technical Support Agent powered by Google ADK, Gemini, Qdrant, Context7 and Lyzr."
)

import os

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ["PORT"])
)
