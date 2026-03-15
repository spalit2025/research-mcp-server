"""Tests for the search_papers MCP tool."""

import urllib.error
from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from research_mcp_server.server import search_papers
from research_mcp_server.storage import PaperStorage


@pytest.fixture(autouse=True)
def mock_storage(tmp_path):
    """Replace global storage with tmp_path-based storage for all tests."""
    test_storage = PaperStorage(base_dir=str(tmp_path / "papers"))
    with patch("research_mcp_server.server.storage", test_storage):
        yield test_storage


def _make_mock_paper(paper_id="2401.12345v1", title="Test Paper"):
    """Create a mock arXiv paper result."""
    paper = MagicMock()
    paper.get_short_id.return_value = paper_id
    paper.title = title

    author = MagicMock()
    author.name = "Author One"
    paper.authors = [author]

    paper.summary = "A test paper summary."
    paper.pdf_url = f"https://arxiv.org/pdf/{paper_id}"

    published = MagicMock()
    published.date.return_value = date(2024, 1, 15)
    paper.published = published

    return paper


class TestSearchPapers:
    @patch("research_mcp_server.server.arxiv.Client")
    def test_happy_path_returns_paper_ids(self, MockClient):
        client = MockClient.return_value
        client.results.return_value = [_make_mock_paper()]

        result = search_papers("transformers", max_results=5)

        assert result == ["2401.12345v1"]

    def test_empty_topic_returns_error(self):
        result = search_papers("", max_results=5)
        assert result == ["Error: Topic cannot be empty."]

    def test_whitespace_topic_returns_error(self):
        result = search_papers("   ", max_results=5)
        assert result == ["Error: Topic cannot be empty."]

    def test_path_traversal_topic_returns_error(self):
        result = search_papers("../../etc/passwd", max_results=5)
        assert result == ["Error: Invalid topic name."]

    @patch("research_mcp_server.server.arxiv.Client")
    @patch("research_mcp_server.server.arxiv.Search")
    def test_max_results_clamped_to_50(self, MockSearch, MockClient):
        client = MockClient.return_value
        client.results.return_value = []

        search_papers("test", max_results=100)

        MockSearch.assert_called_once()
        _, kwargs = MockSearch.call_args
        assert kwargs["max_results"] == 50

    @patch("research_mcp_server.server.arxiv.Client")
    @patch("research_mcp_server.server.arxiv.Search")
    def test_max_results_minimum_is_1(self, MockSearch, MockClient):
        client = MockClient.return_value
        client.results.return_value = []

        search_papers("test", max_results=0)

        MockSearch.assert_called_once()
        _, kwargs = MockSearch.call_args
        assert kwargs["max_results"] == 1

    @patch("research_mcp_server.server.arxiv.Client")
    def test_api_network_error_returns_error(self, MockClient):
        client = MockClient.return_value
        client.results.side_effect = urllib.error.URLError("timeout")

        result = search_papers("test", max_results=5)

        assert len(result) == 1
        assert "unavailable" in result[0].lower()

    @patch("research_mcp_server.server.arxiv.Client")
    def test_api_connection_error_returns_error(self, MockClient):
        client = MockClient.return_value
        client.results.side_effect = ConnectionError("refused")

        result = search_papers("test", max_results=5)

        assert len(result) == 1
        assert "unavailable" in result[0].lower()
