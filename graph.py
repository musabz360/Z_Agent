import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI
import vertexai
from dotenv import load_dotenv
load_dotenv()


def _init_vertex_ai():
    project = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    location = (
        os.getenv("GOOGLE_CLOUD_LOCATION")
        or os.getenv("VERTEX_LOCATION")
        or "us-central1"
    )
    if not project:
        raise RuntimeError(
            "Vertex AI: set GOOGLE_CLOUD_PROJECT or GCP_PROJECT in your .env file"
        )

    print(f"Initializing Vertex AI with project '{project}' in location '{location}'")
    vertexai.init(project=project, location=location)


def _get_tools():
    try:
        client = MultiServerMCPClient(
        {
            "Z360 Server": {
                "url": "http://localhost:7360/mcp/z360",
                "transport": "streamable_http",
                "headers": {"org_id": "1"},
            }
        }
    )
        return asyncio.run(client.get_tools())
    except Exception as e:
        # Fall back to no tools if MCP server is unavailable/misconfigured
        print(f"Warning: Failed to load MCP tools ({e}). Continuing with no tools.")
        return []

tools = _get_tools()
_init_vertex_ai()
model = ChatVertexAI(model_name="gemini-2.5-pro", temperature=0.1)
app = create_react_agent(model, tools)  