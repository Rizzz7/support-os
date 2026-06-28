import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def verify_answer(query, context, answer):

    prompt = f"""
You are the SupportOS Verification Agent.

Your ONLY job is to verify whether the generated answer is grounded in the retrieved documentation.

USER QUERY
{query}

RETRIEVED DOCUMENTATION
{context}

GENERATED ANSWER
{answer}

Return ONLY valid JSON.

{{
    "grounded": true,
    "reason": ""
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    result = json.loads(text)

    query_lower = query.lower()

    critical_keywords = [
        "api key",
        "apikey",
        "secret",
        "token",
        "credential",
        "credentials",
        "leaked",
        "exposed",
        "github",
        "public repo",
        "private key",
        "service account"
    ]

    high_keywords = [
        "hacked",
        "hack",
        "compromised",
        "compromise",
        "account hacked",
        "account compromise",
        "security",
        "breach",
        "fraud",
        "billing",
        "payment",
        "unauthorized",
        "privacy",
        "gdpr",
        "legal",
        "abuse"
    ]

    medium_keywords = [
        "oauth",
        "authentication",
        "authorization",
        "permission denied",
        "401",
        "403",
        "quota",
        "rate limit",
        "timeout"
    ]

    risk = "LOW"
    escalate = False
    action = "RESOLVE"
    reason = ""

    if any(word in query_lower for word in critical_keywords):
        risk = "CRITICAL"
        escalate = True
        action = "ESCALATE"
        reason = "Potential credential compromise detected."

    elif any(word in query_lower for word in high_keywords):
        risk = "HIGH"
        escalate = True
        action = "ESCALATE"
        reason = "Potential account or security incident detected."

    elif any(word in query_lower for word in medium_keywords):
        risk = "MEDIUM"

    result["risk"] = risk
    result["action"] = action
    result["escalate"] = escalate

    if reason:
        result["reason"] = reason

    return result