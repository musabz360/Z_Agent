## ZAgent

Minimal LangGraph agent wired to an MCP server with an interactive CLI and a graph export for LangGraph Studio.

### Requirements

- Python 3.10+
- OpenAI API key

### Quickstart (Windows PowerShell)

```powershell
cd Z:\MCP\Z_Agent
python -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Set your environment variable (replace with your key):

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

### Run the interactive agent

```powershell
python agent.py
```

Type `exit` or `quit` to end.

### LangGraph Studio (Dev Server)

This repo includes `langgraph.json` pointing to the graph at `graph.py:app`.

```powershell
pip install -U "langgraph-cli[inmem]"
langgraph dev --config langgraph.json
```

You’ll see the local API and a Studio URL printed in the console. Open the Studio link to inspect and test the graph.

### MCP configuration

The agent connects to the MCP "Z360 Server" at `http://localhost:7360/mcp/z360` with header `org_id=1`.
Adjust `agent.py` and `graph.py` if you need different values.

### Project Files

- `agent.py` — Interactive CLI agent using LangGraph prebuilt ReAct and MCP tools
- `graph.py` — Graph export (`app`) for LangGraph Studio
- `langgraph.json` — Studio configuration
- `requirements.txt` — Python dependencies
- `.gitignore` — Excludes `.venv`, `.env`, and Python cache files

### Troubleshooting

- If `langgraph dev` complains about missing packages, run: `pip install -U "langgraph-cli[inmem]"`.
- If environment variables aren’t loading from a file, ensure your shell env has `OPENAI_API_KEY` set.
