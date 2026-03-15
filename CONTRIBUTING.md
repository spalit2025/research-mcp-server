# Contributing

Thank you for your interest in contributing to Research MCP Server.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/spalit2025/research-mcp-server.git
   cd research-mcp-server
   ```

2. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

3. Run tests:
   ```bash
   pytest -v
   ```

4. Run linting:
   ```bash
   ruff check .
   ruff format --check .
   ```

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting. Run `ruff format .` to auto-format your code before submitting.

## Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes with tests
4. Ensure all tests pass and linting is clean
5. Submit a pull request

## Reporting Issues

Please use GitHub Issues for bug reports and feature requests. Include:
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Python version and OS
