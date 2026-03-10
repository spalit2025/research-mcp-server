# Research MCP Server

Researchers context-switch constantly between search tools and AI assistants.
You find a paper in one tab, copy the title into another, ask questions in a
third. The workflow is fragmented by design.

This MCP server brings arXiv paper discovery directly into any AI assistant
that supports the Model Context Protocol. Search for papers, extract metadata,
and browse saved collections -- all without leaving your conversation.

## Why I built this

MCP is the emerging standard for connecting AI assistants to external tools.
I wanted to build a practical MCP server that solves a real workflow problem
while exploring the protocol's three core primitives:

1. **Tools** -- `search_papers` and `extract_info` let the AI search arXiv
   and pull structured paper metadata on your behalf
2. **Resources** -- `papers://folders` and `papers://{topic}` expose saved
   research as browsable context the AI can read directly
3. **Prompts** -- `generate_search_prompt` creates structured research
   workflows that guide systematic literature review

## Quick start

```bash
# Clone and install
git clone https://github.com/spalit2025/research-mcp-server.git
cd research-mcp-server
pip install -r requirements.txt

# Run the server
python research_server.py
```

### Connect to Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "research": {
      "command": "python",
      "args": ["/path/to/research-mcp-server/research_server.py"]
    }
  }
}
```

Then ask Claude: *"Search for recent papers on transformer architectures"*

### Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector python research_server.py
# Opens web UI at http://localhost:6274
```

## How it works

```
AI Assistant (Claude, etc.)
    |
    | MCP Protocol (stdio)
    |
Research MCP Server
    ├── search_papers(topic, max_results)
    |   └── arXiv API → results saved to papers/{topic}/papers_info.json
    ├── extract_info(paper_id)
    |   └── looks up saved paper metadata across all topics
    ├── papers://folders (resource)
    |   └── lists all previously searched topics
    ├── papers://{topic} (resource)
    |   └── returns full paper details for a topic
    └── generate_search_prompt (prompt)
        └── structured research workflow template
```

## API reference

### Tools

**`search_papers`** -- Search arXiv for papers on a topic

```json
{ "topic": "machine learning transformers", "max_results": 10 }
```

Returns list of paper IDs. Results cached locally in `papers/` directory.

**`extract_info`** -- Get metadata for a specific paper

```json
{ "paper_id": "2401.12345v1" }
```

Returns title, authors, summary, PDF URL, publication date.

### Resources

- **`papers://folders`** -- List all saved topic directories
- **`papers://{topic}`** -- Full paper details for a topic (titles, authors, summaries, PDF links)

### Prompts

- **`generate_search_prompt`** -- Generates a structured research workflow: search, extract, analyze, synthesize

## Key design decisions

- **stdio transport:** MCP supports both stdio and HTTP. stdio is simpler for local development and works out of the box with Claude Desktop.

- **File-based persistence:** Papers are saved as JSON files organized by topic. Simple, inspectable, no database dependency. Good enough for a personal research tool.

- **Path traversal protection:** Topic names are sanitized and validated against directory traversal attacks before any file operations.

- **Bounded results:** `max_results` is capped at 50 to prevent accidental API abuse.

## Project structure

```
research-mcp-server/
├── research_server.py     # MCP server (tools, resources, prompts)
├── requirements.txt       # arxiv, mcp dependencies
├── papers/                # auto-generated paper storage by topic
├── LICENSE                # MIT
└── README.md
```

## Requirements

- Python 3.8+
- Internet connection (arXiv API access)
- An MCP-compatible client (Claude Desktop, MCP Inspector, or custom)

## License

MIT
