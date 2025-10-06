import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
# from langchain_google_vertexai import ChatVertexAI
# import vertexai

def _get_tools():
    try:
        client = MultiServerMCPClient(
            {
                 "Z360 Server": {
                    "url": "http://localhost:7360/mcp/z360",
                    "transport": "streamable_http",
                    "headers": {"X-Org-Id": "1"}
                }            
            }
        )
        return asyncio.run(client.get_tools())
    except Exception as e:
        # Fall back to no tools if MCP server is unavailable/misconfigured
        print(f"Warning: Failed to load MCP tools ({e}). Continuing with no tools.")
        return []

tools = _get_tools()
model = ChatOpenAI(model="gpt-4o-mini")
# model = ChatVertexAI(model_name="gemini-2.0-flash-001", temperature=0.1)
app = create_react_agent(model, tools)  # Studio looks for 'app'