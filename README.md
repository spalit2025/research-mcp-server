# Research Server MCP

A Model Context Protocol (MCP) server for searching and retrieving academic papers from arXiv.

## Features

- **search_papers**: Search for papers on arXiv by topic
- **extract_info**: Extract detailed information about specific papers

## Setup

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### As MCP Server
```bash
python research_server.py
```

### Development & Testing

**Test with MCP Inspector:**
```bash
npx @modelcontextprotocol/inspector python research_server.py
```
Then open http://localhost:6274 in your browser.

**Standalone Testing:**
```bash
python -c "import research_server; print(research_server.search_papers('AI', 2))"
```

## Dependencies

- `arxiv>=2.1.0` - arXiv API client
- `mcp>=1.0.0` - Model Context Protocol server

## Development Tools

- **MCP Inspector**: `npx @modelcontextprotocol/inspector` (for testing) 