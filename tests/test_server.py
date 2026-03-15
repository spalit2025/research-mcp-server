"""Tests for MCP prompt generation and server setup."""

from research_mcp_server.server import generate_search_prompt


class TestGenerateSearchPrompt:
    def test_default_num_papers(self):
        result = generate_search_prompt("quantum computing")
        assert "quantum computing" in result
        assert "5" in result

    def test_custom_num_papers(self):
        result = generate_search_prompt("AI safety", num_papers=10)
        assert "AI safety" in result
        assert "10" in result
