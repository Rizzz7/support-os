from vector_store import search


def search_docs(query: str) -> str:

    print(f"\n TOOL -> search_docs('{query}')")

    results = search(query)

    if not results:
        return "NO_DOCS"

    context = ""

    for r in results:
        context += f"\nSOURCE: {r['source']}\n"
        context += r["text"]
        context += "\n"

    return context


def escalate(reason: str):

    print(f"\n🚨 TOOL -> escalate('{reason}')")

    return f"Escalated: {reason}"