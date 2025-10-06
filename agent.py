import asyncio
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI
import vertexai


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

    print(f"✅ Initializing Vertex AI with project '{project}' in location '{location}'")
    vertexai.init(project=project, location=location)


async def main():
    # MCP servers config with only "Z360 Server"
    client = MultiServerMCPClient(
        {
            "Z360 Server": {
                "url": "http://localhost:7360/mcp/z360",
                "transport": "streamable_http",
                "headers": {"org_id": "1"},
            }
        }
    )

    # Fetch tools from MCP server
    tools = await client.get_tools()

    # Initialize Vertex AI
    _init_vertex_ai()

    # Initialize Vertex AI model
    model = ChatVertexAI(model_name="gemini-2.5-pro", temperature=0.1)

    # Create React agent with MCP tools
    agent = create_react_agent(model, tools)

    # Interactive chat loop
    print("\nType 'exit' or 'quit' to end the chat.\n")
    while True:
        try:
            user_input = await asyncio.to_thread(input, "You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if not user_input:
            continue
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        # Invoke the agent
        response = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]})

        # Extract and print AI response
        messages = response.get("messages", [])
        last_message = messages[-1] if messages else None
        text = last_message.content if last_message else ""
        print(f"Assistant: {text}")


if __name__ == "__main__":
    asyncio.run(main())
