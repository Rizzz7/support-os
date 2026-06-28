from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioServerParameters

from .tools import search_docs, escalate

root_agent = LlmAgent(

    name="SupportOS",

    model="gemini-2.5-flash",

    instruction="""
You are SupportOS.

Workflow:

1. Search local knowledge first.

2. If local knowledge is insufficient,
use Context7.

3. Never hallucinate.

4. If still uncertain,
escalate.

Always cite retrieved information.
""",

    tools=[

        search_docs,

        escalate,

        MCPToolset(

            connection_params=StdioServerParameters(

                command="npx",

                args=[
                    "-y",
                    "@upstash/context7-mcp"
                ]

            )

        )

    ]
)