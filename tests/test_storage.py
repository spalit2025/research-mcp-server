"""Tests for PaperStorage."""

import json
from pathlib import Path

import pytest

from research_mcp_server.models import Paper


class TestPaperStorage:
    def test_save_and_load_roundtrip(self, storage, sample_paper):
        storage.save_papers("test topic", {sample_paper.paper_id: sample_paper})
        loaded = storage.load_papers("test topic")
        assert sample_paper.paper_id in loaded
        assert loaded[sample_paper.paper_id]["title"] == sample_paper.title
        assert loaded[sample_paper.paper_id]["authors"] == sample_paper.authors

    def test_validate_path_blocks_traversal(self, storage):
        with pytest.raises(ValueError, match="Invalid topic name"):
            storage.validate_topic_path("../../etc/passwd")

    def test_load_papers_returns_empty_for_missing_topic(self, storage):
        result = storage.load_papers("nonexistent")
        assert result == {}

    def test_save_papers_merges_with_existing(self, populated_storage):
        new_paper = Paper(
            paper_id="2401.99999v1",
            title="New Paper",
            authors=["Author"],
            summary="Summary",
            pdf_url="https://arxiv.org/pdf/2401.99999v1",
            published="2024-06-01",
        )
        populated_storage.save_papers("transformers", {new_paper.paper_id: new_paper})
        loaded = populated_storage.load_papers("transformers")
        assert len(loaded) == 2
        assert "2401.12345v1" in loaded
        assert "2401.99999v1" in loaded

    def test_load_json_handles_corrupt_file(self, storage):
        topic_dir = Path(storage.base_dir) / "corrupt"
        topic_dir.mkdir(parents=True)
        (topic_dir / "papers_info.json").write_text("not valid json{{{")
        result = storage.load_papers("corrupt")
        assert result == {}

    def test_find_paper_across_topics(self, populated_storage):
        result = populated_storage.find_paper("2401.12345v1")
        assert result is not None
        assert result["title"] == "Attention Is All You Need"

    def test_find_paper_returns_none_when_not_found(self, populated_storage):
        result = populated_storage.find_paper("9999.99999v1")
        assert result is None

    def test_list_topics(self, populated_storage):
        topics = populated_storage.list_topics()
        assert "transformers" in topics

    def test_list_topics_empty(self, storage):
        topics = storage.list_topics()
        assert topics == []

    def test_find_paper_skips_symlinks(self, storage, tmp_path):
        real_dir = tmp_path / "outside"
        real_dir.mkdir()
        (real_dir / "papers_info.json").write_text(
            json.dumps({"secret.paper": {"title": "Secret"}})
        )
        papers_dir = Path(storage.base_dir)
        papers_dir.mkdir(parents=True, exist_ok=True)
        symlink = papers_dir / "linked"
        symlink.symlink_to(real_dir)

        result = storage.find_paper("secret.paper")
        assert result is None
