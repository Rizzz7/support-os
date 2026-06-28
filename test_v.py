from supportos.verification_agent import verify_answer

context = """
Firebase deployment errors can occur because
firebase.json is missing.
"""

answer = """
The deployment failed because firebase.json
is missing.
"""

print(
    verify_answer(
        "firebase deploy failed",
        context,
        answer
    )
)