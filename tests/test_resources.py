"""Tests for MCP resources (papers://folders, papers://{topic})."""

import json
from unittest.mock import patch

import pytest

from research_mcp_server.server import get_available_folders, get_topic_papers
from research_mcp_server.storage import PaperStorage

from .conftest import SAMPLE_PAPER_DICT


@pytest.fixture(autouse=True)
def mock_storage(tmp_path):
    """Replace global storage with tmp_path-based storage for all tests."""
    test_storage = PaperStorage(base_dir=str(tmp_path / "papers"))
    with patch("research_mcp_server.server.storage", test_storage):
        yield test_storage


class TestGetAvailableFolders:
    def test_no_topics_returns_empty_message(self):
        result = get_available_folders()
        assert "No topics found" in result

    def test_with_topics_lists_them(self, tmp_path):
        topic_dir = tmp_path / "papers" / "transformers"
        topic_dir.mkdir(parents=True)
        (topic_dir / "papers_info.json").write_text("{}")

        result = get_available_folders()
        assert "transformers" in result


class TestGetTopicPapers:
    def test_topic_with_papers_returns_details(self, tmp_path):
        topic_dir = tmp_path / "papers" / "transformers"
        topic_dir.mkdir(parents=True)
        (topic_dir / "papers_info.json").write_text(
            json.dumps({"2401.12345v1": SAMPLE_PAPER_DICT}, indent=2)
        )

        result = get_topic_papers("transformers")
        assert "Attention Is All You Need" in result
        assert "Ashish Vaswani" in result
        assert "2401.12345v1" in result

    def test_topic_not_found_returns_message(self):
        result = get_topic_papers("nonexistent")
        assert "No papers found" in result

    def test_path_traversal_blocked(self):
        result = get_topic_papers("../../etc/passwd")
        assert "Invalid topic name" in result
