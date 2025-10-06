import asyncio
import os
import json
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
# from langchain_google_vertexai import ChatVertexAI
# import vertexai  



async def main():
    # MCP servers config with only "Z360 Server"
    client = MultiServerMCPClient(
    {
        "Z360 Server": {
            "url": "http://localhost:7360/mcp/z360",
            "transport": "streamable_http",
            "headers": {"org_id": "1"}
        }
    }
    )    
    
    tools = await client.get_tools()

    # _init_vertex_ai()

    # Initialize your LLM
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    # model = ChatVertexAI(model_name="gemini-2.5-pro", temperature=0.1)


    # Create React agent with MCP tools
    agent = create_react_agent(model, tools)

    # Interactive chat loop
    print("Type 'exit' or 'quit' to end the chat.\n")
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

        response = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]})
        print(response)
        # Extract the last message content (AI response)
        messages = response.get("messages", [])
        last_message = messages[-1] if messages else None
        text = last_message.content if last_message is not None else ""

        print(f"Assistant: {text}")

if __name__ == "__main__":
    asyncio.run(main())
