# Research Server MCP

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Repository Topics

When setting up this repository on GitHub, consider adding these topics for better discoverability:
- `mcp`
- `model-context-protocol`
- `arxiv`
- `research`
- `academic-papers`
- `python`
- `research-tools`
- `ai-tools` 