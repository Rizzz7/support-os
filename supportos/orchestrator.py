import os
import time

from dotenv import load_dotenv
from google import genai

from .tools import search_docs
from .verification_agent import verify_answer

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def emit(callback, **event):
    if callback:
        callback(event)


def generate(prompt):

    models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash"
    ]

    last = None

    for model in models:

        for _ in range(3):

            try:

                return client.models.generate_content(
                    model=model,
                    contents=prompt
                )

            except Exception as e:

                last = e

                time.sleep(2)

    raise last


def extract_sources(context):

    sources = []

    for line in context.splitlines():

        if line.startswith("SOURCE:"):

            src = line.replace("SOURCE:", "").strip()

            if src not in sources:

                sources.append(src)

    return sources


def run_supportos(query, callback=None):

    # ---------------- SEARCH ----------------

    start = time.perf_counter()

    emit(
        callback,
        stage="search",
        status="start"
    )

    context = search_docs(query)

    elapsed = time.perf_counter() - start

    sources = extract_sources(context)

    emit(
        callback,
        stage="search",
        status="done",
        elapsed=elapsed,
        chunks=max(
            0,
            len(context.split("SOURCE:")) - 1
        ),
        sources=sources
    )

    # ---------------- REASON ----------------

    prompt = f"""
You are SupportOS.

Answer ONLY from the documentation.

Question:

{query}

Documentation:

{context}

Never hallucinate.
"""

    start = time.perf_counter()

    emit(
        callback,
        stage="reason",
        status="start"
    )

    response = generate(prompt)

    answer = response.text.strip()

    elapsed = time.perf_counter() - start

    emit(
        callback,
        stage="reason",
        status="done",
        elapsed=elapsed
    )

    # ---------------- VERIFY ----------------

    start = time.perf_counter()

    emit(
        callback,
        stage="verify",
        status="start"
    )

    verification = verify_answer(
        query,
        context,
        answer
    )

    elapsed = time.perf_counter() - start

    emit(
       callback,
       stage="verify",
       status="done",
       elapsed=elapsed,
       grounded=verification["grounded"],
       risk=verification["risk"],
       action=verification["action"],
       escalate=verification["escalate"],
       reason=verification["reason"]
    )

    return {

        "answer": answer,

        "context": context,

        "sources": sources,

        "verification": verification

    }