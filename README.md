# 🔬 Research MCP Server

A powerful Model Context Protocol (MCP) server that provides academic research capabilities through arXiv integration. This server enables AI assistants to search, retrieve, and analyze academic papers seamlessly.

## ✨ Features

- 🔍 **Paper Search** - Search arXiv by topic, author, or keywords with customizable result limits
- 📄 **Paper Analysis** - Extract detailed information from specific research papers
- 📚 **Resource Access** - Browse available topics and access organized paper collections
- 🎯 **Smart Prompts** - Generate structured research prompts for comprehensive analysis
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

### Available Resources

#### 📚 papers://folders
Lists all available topic folders with papers stored locally.

**Returns:** Markdown-formatted list of available research topics

**Usage:** Access this resource to see what topics have been previously searched and have papers available.

#### 📖 papers://{topic}
Get detailed information about all papers for a specific topic.

**Parameters:**
- `topic` (string): The research topic to retrieve papers for

**Returns:** Comprehensive markdown document with paper details including titles, authors, summaries, and PDF links

**Example:** `papers://machine_learning` or `papers://quantum_computing`

### Available Prompts

#### 🎯 generate_search_prompt
Generate a structured prompt for comprehensive academic research on a specific topic.

**Parameters:**
- `topic` (string): The research topic to generate a prompt for
- `num_papers` (integer, optional): Number of papers to search for (default: 5)

**Returns:** Detailed prompt that guides systematic research including:
- Paper search instructions
- Information extraction guidelines
- Analysis and synthesis requirements
- Structured output formatting

**Example:**
```json
{
  "topic": "neural networks",
  "num_papers": 8
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
The main development tool you'll need is the MCP Inspector for testing:

```bash
# Install MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

# Or use npx to run it directly
npx @modelcontextprotocol/inspector python research_server.py
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
4. **Resource Management** - Provides organized access to paper collections via resources
5. **Prompt Generation** - Creates structured research prompts for systematic analysis
6. **Data Processing** - Formats and structures paper information for AI consumption
7. **Error Handling** - Robust error management for network and API issues

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
- **Tool Functions** - Implement the actual research functionality (`search_papers`, `extract_info`)
- **Resource Functions** - Provide organized access to stored paper data (`get_available_folders`, `get_topic_papers`)
- **Prompt Functions** - Generate structured research prompts (`generate_search_prompt`)
- **MCP Integration** - Handle protocol communication and tool registration
- **Error Handling** - Manage API errors and edge cases
- **Data Formatting** - Structure responses for optimal AI consumption

## 📦 Dependencies

### Production
- **[arxiv](https://github.com/lukasschwab/arxiv.py)** >=2.1.0 - arXiv API client for paper search and retrieval
- **[mcp](https://github.com/modelcontextprotocol/python-sdk)** >=1.0.0 - Model Context Protocol server implementation

### Development & Testing
- **[MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)** - Web-based tool for testing MCP servers
  ```bash
  npx @modelcontextprotocol/inspector python research_server.py
  ```

*Note: Additional development tools like pytest, black, and flake8 are listed in requirements-dev.txt but not currently configured for this project.*

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
- Test your changes with MCP Inspector
- Update documentation for any changes
- Ensure MCP compatibility is maintained

