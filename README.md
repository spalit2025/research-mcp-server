# 🔬 Research MCP Server

A powerful Model Context Protocol (MCP) server that provides academic research capabilities through arXiv integration. This server enables AI assistants to search, retrieve, and analyze academic papers seamlessly.

## ✨ Features

- 🔍 **Paper Search** - Search arXiv by topic, author, or keywords with customizable result limits
- 📄 **Paper Analysis** - Extract detailed information from specific research papers
- 🚀 **MCP Compatible** - Full Model Context Protocol implementation for seamless AI integration
- ⚡ **Fast & Reliable** - Efficient arXiv API integration with robust error handling
- 🛠️ **Easy Integration** - Simple setup for use with MCP clients and AI assistants

## 🔗 Related Projects

- [research-mcp-client](https://github.com/spalit2025/research-mcp-client) - A Claude AI chatbot that uses this server for intelligent research assistance

## 📋 Prerequisites

- **Python 3.8+**
- **Internet connection** for arXiv API access
- **MCP client** (like the [research-mcp-client](https://github.com/spalit2025/research-mcp-client))

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/spalit2025/research-mcp-server.git
cd research-mcp-server
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Server
```bash
python research_server.py
```

## 💡 Usage Examples

### As MCP Server
The server runs as a stdio-based MCP server, perfect for integration with AI assistants:

```bash
python research_server.py
```

### Available Tools

#### 🔍 search_papers
Search for academic papers on arXiv by topic.

**Parameters:**
- `topic` (string): Search query for papers
- `max_results` (integer, optional): Maximum number of results (default: 5)

**Example:**
```json
{
  "topic": "machine learning transformers",
  "max_results": 10
}
```

#### 📄 extract_info
Extract detailed information from a specific paper.

**Parameters:**
- `paper_id` (string): The paper identifier from search results

**Example:**
```json
{
  "paper_id": "paper_1"
}
```

## 🧪 Development & Testing

### Test with MCP Inspector
The MCP Inspector provides a web interface for testing your server:

```bash
npx @modelcontextprotocol/inspector python research_server.py
```

Then open http://localhost:6274 in your browser to interact with the server.

### Standalone Testing
Test the server functions directly:

```bash
python -c "
import research_server
result = research_server.search_papers('artificial intelligence', 3)
print(result)
"
```

### Development Setup
For development work, install additional tools:

```bash
pip install -r requirements-dev.txt
```

## 🏗️ Project Structure

```
research-mcp-server/
├── research_server.py      # Main MCP server implementation
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── .gitignore             # Git ignore rules
├── LICENSE                # MIT License
└── README.md              # This file
```

## 🔧 How It Works

1. **MCP Server** - Implements the Model Context Protocol for tool communication
2. **arXiv Integration** - Uses the arXiv API to search and retrieve academic papers
3. **Tool Registration** - Exposes `search_papers` and `extract_info` as MCP tools
4. **Data Processing** - Formats and structures paper information for AI consumption
5. **Error Handling** - Robust error management for network and API issues

## 🛠️ Configuration

### Customizing Search Parameters
You can modify the default search behavior in `research_server.py`:

```python
# Adjust default result limits
DEFAULT_MAX_RESULTS = 5

# Modify search categories or sorting
# See arXiv API documentation for options
```

### Integration with Clients
This server is designed to work with MCP clients. Configure your client to connect using:

```python
server_params = StdioServerParameters(
    command="python",
    args=["/path/to/research-mcp-server/research_server.py"],
    env=None,
)
```

## 🐛 Troubleshooting

### Connection Issues
- ✅ Ensure Python 3.8+ is installed and accessible
- ✅ Verify all dependencies are installed correctly
- ✅ Check that the server starts without errors

### API Issues
- ✅ Verify internet connection for arXiv API access
- ✅ Check if arXiv is accessible from your network
- ✅ Ensure no firewall blocking outbound connections

### Search Problems
- ✅ Try simpler search terms if no results found
- ✅ Check arXiv.org directly to verify paper availability
- ✅ Reduce `max_results` if getting timeout errors

### Common Solutions
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Test arXiv connectivity
python -c "import arxiv; print('arXiv accessible')"

# Check server startup
python research_server.py --help
```

## 🔄 Development

### Adding New Features
1. Implement new tool functions in `research_server.py`
2. Register tools with the MCP server
3. Update tool schemas and documentation
4. Test with MCP Inspector

### Code Structure
- **Tool Functions** - Implement the actual research functionality
- **MCP Integration** - Handle protocol communication and tool registration
- **Error Handling** - Manage API errors and edge cases
- **Data Formatting** - Structure responses for optimal AI consumption

## 📦 Dependencies

### Production
- **[arxiv](https://github.com/lukasschwab/arxiv.py)** >=2.1.0 - arXiv API client for paper search and retrieval
- **[mcp](https://github.com/modelcontextprotocol/python-sdk)** >=1.0.0 - Model Context Protocol server implementation

### Development
- **[pytest](https://pytest.org/)** - Testing framework
- **[black](https://black.readthedocs.io/)** - Code formatting
- **[flake8](https://flake8.pycqa.org/)** - Code linting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Ensure code follows style guidelines
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation for any changes
- Ensure MCP compatibility is maintained

## 🙏 Acknowledgments

- [arXiv](https://arxiv.org/) for providing free access to academic papers
- [Model Context Protocol](https://modelcontextprotocol.io/) for the excellent framework
- The academic research community for making knowledge freely available

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review existing [Issues](https://github.com/spalit2025/research-mcp-server/issues)
3. Create a new issue with detailed information about your problem
4. For integration help, also check the [research-mcp-client](https://github.com/spalit2025/research-mcp-client) documentation

## 🏷️ Repository Topics

For better discoverability, this repository includes these topics:
- `mcp` - Model Context Protocol
- `model-context-protocol` - Full protocol name
- `arxiv` - arXiv integration
- `research` - Academic research tools
- `academic-papers` - Paper search and analysis
- `python` - Python implementation
- `research-tools` - Research assistance
- `ai-tools` - AI integration tools
- `server` - MCP server implementation

---

**Happy researching! 🔬✨** 