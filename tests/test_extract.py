"""Tests for the extract_info MCP tool."""

import json
from unittest.mock import patch

import pytest

from research_mcp_server.server import extract_info
from research_mcp_server.storage import PaperStorage

from .conftest import SAMPLE_PAPER_DICT


@pytest.fixture(autouse=True)
def mock_storage(tmp_path):
    """Replace global storage with tmp_path-based storage for all tests."""
    test_storage = PaperStorage(base_dir=str(tmp_path / "papers"))
    with patch("research_mcp_server.server.storage", test_storage):
        yield test_storage


def _create_topic_with_paper(tmp_path, topic="transformers", paper_id="2401.12345v1"):
    """Helper to create a topic directory with a sample paper."""
    topic_dir = tmp_path / "papers" / topic
    topic_dir.mkdir(parents=True, exist_ok=True)
    papers_file = topic_dir / "papers_info.json"
    papers_file.write_text(json.dumps({paper_id: SAMPLE_PAPER_DICT}, indent=2))


class TestExtractInfo:
    def test_found_paper_returns_json(self, tmp_path):
        _create_topic_with_paper(tmp_path)
        result = extract_info("2401.12345v1")
        data = json.loads(result)
        assert data["title"] == "Attention Is All You Need"

    def test_found_in_second_topic_dir(self, tmp_path):
        # Create an empty topic first, then one with the paper
        empty_dir = tmp_path / "papers" / "aaa_empty"
        empty_dir.mkdir(parents=True)
        (empty_dir / "papers_info.json").write_text("{}")
        _create_topic_with_paper(tmp_path, topic="zzz_transformers")

        result = extract_info("2401.12345v1")
        data = json.loads(result)
        assert data["title"] == "Attention Is All You Need"

    def test_not_found_returns_message(self, tmp_path):
        _create_topic_with_paper(tmp_path)
        result = extract_info("9999.99999v1")
        assert "No saved information" in result

    def test_empty_paper_id_returns_error(self):
        result = extract_info("")
        assert "cannot be empty" in result

    def test_whitespace_paper_id_returns_error(self):
        result = extract_info("   ")
        assert "cannot be empty" in result

    def test_corrupt_json_skipped_gracefully(self, tmp_path):
        topic_dir = tmp_path / "papers" / "corrupt_topic"
        topic_dir.mkdir(parents=True)
        (topic_dir / "papers_info.json").write_text("not json{{{")

        result = extract_info("2401.12345v1")
        assert "No saved information" in result
