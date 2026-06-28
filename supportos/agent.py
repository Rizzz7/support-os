# from google.adk.agents import LlmAgent
#
# from .tools import (
#     search_docs,
#     escalate,
# )
#
# root_agent = LlmAgent(
#     name="SupportOS",
#
#     model="gemini-2.5-flash",
#
#     description="Google Technical Support Engineer",
#
#     instruction="""
# You are SupportOS.
#
# Workflow:
#
# 1. Always search local documentation first.
#
# 2. If local docs are insufficient,
# use fetch_latest_docs().
#
# 3. Never hallucinate.
#
# 4. If still uncertain,
# escalate.
#
# 5. Always answer using retrieved evidence.
# """,
#
#     tools=[
#         search_docs,
#         fetch_latest_docs,
#         escalate,
#     ]
# )