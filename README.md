# Research MCP Server

[![CI](https://github.com/spalit2025/research-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/spalit2025/research-mcp-server/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

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
pip install -e .

# Run the server
python -m research_mcp_server.server
```

### Connect to Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "research": {
      "command": "python",
      "args": ["-m", "research_mcp_server.server"]
    }
  }
}
```

Then ask Claude: *"Search for recent papers on transformer architectures"*

### Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector python -m research_mcp_server.server
# Opens web UI at http://localhost:6274
```

## Example

Ask your AI assistant to search for papers:

> "Find recent papers on transformer architectures"

The assistant calls `search_papers("transformer architectures")` and returns:

```json
["2401.12345v1", "2401.23456v1", "2401.34567v1"]
```

Then it can call `extract_info("2401.12345v1")` to get details:

```json
{
  "title": "A Comprehensive Survey of Transformer Architectures",
  "authors": ["Alice Smith", "Bob Jones"],
  "summary": "This paper reviews the evolution of transformer architectures...",
  "pdf_url": "https://arxiv.org/pdf/2401.12345v1",
  "published": "2024-01-15"
}
```

Papers are saved locally in `papers/transformer_architectures/papers_info.json`
for future reference.

## How it works

```
+-----------------------+
|    AI Assistant        |
|  (Claude Desktop,     |
|   MCP Inspector)      |
+-----------+-----------+
            |
            | stdio (JSON-RPC)
            |
+-----------v-----------+
|  Research MCP Server   |
|                        |
|  Tools:                |        +------------------+
|   search_papers -------+------->|   arXiv API      |
|   extract_info         |        |   (external)     |
|                        |        +------------------+
|  Resources:            |
|   papers://folders     |        +------------------+
|   papers://{topic} ----+------->| papers/          |
|                        |        |  {topic}/        |
|  Prompts:              |        |   papers_info    |
|   generate_search_     |        |   .json          |
|   prompt               |        +------------------+
+------------------------+
```

## API reference

### Tools

**`search_papers`** -- Search arXiv for papers on a topic

```json
{ "topic": "machine learning transformers", "max_results": 10 }
```

Returns list of paper IDs. Results cached locally in `papers/` directory.
Input validation: empty topics rejected, `max_results` clamped to 1-50,
path traversal attempts blocked.

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

- **Path traversal protection:** Topic names are validated against directory traversal attacks before any file operations.

- **Bounded results:** `max_results` is capped at 50 to prevent accidental API abuse.

- **Graceful error handling:** Network failures, HTTP errors, and disk errors return structured error messages instead of crashing the server.

## Project structure

```
research-mcp-server/
+-- src/research_mcp_server/
|     +-- __init__.py          # Package version
|     +-- server.py            # MCP server (tools, resources, prompts)
|     +-- storage.py           # File-based paper persistence
|     +-- models.py            # Paper dataclass
+-- tests/
|     +-- conftest.py          # Shared fixtures
|     +-- test_search.py       # search_papers tests
|     +-- test_extract.py      # extract_info tests
|     +-- test_resources.py    # Resource endpoint tests
|     +-- test_storage.py      # PaperStorage tests
|     +-- test_server.py       # Prompt generation tests
+-- .github/workflows/ci.yml   # CI: lint + test (Python 3.10-3.13)
+-- pyproject.toml              # Package config, dependencies, tool settings
+-- CONTRIBUTING.md
+-- TODOS.md
+-- LICENSE                     # MIT
+-- README.md
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest -v

# Lint and format
ruff check .
ruff format .
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## Requirements

- Python 3.10+
- Internet connection (arXiv API access)
- An MCP-compatible client (Claude Desktop, MCP Inspector, or custom)

## License

MIT
