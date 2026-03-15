"""Shared test fixtures for the research MCP server."""

import json

import pytest

from research_mcp_server.models import Paper
from research_mcp_server.storage import PaperStorage

SAMPLE_PAPER = Paper(
    paper_id="2401.12345v1",
    title="Attention Is All You Need",
    authors=["Ashish Vaswani", "Noam Shazeer"],
    summary="We propose a new simple network architecture, the Transformer.",
    pdf_url="https://arxiv.org/pdf/2401.12345v1",
    published="2024-01-15",
)

SAMPLE_PAPER_DICT = {
    "title": "Attention Is All You Need",
    "authors": ["Ashish Vaswani", "Noam Shazeer"],
    "summary": "We propose a new simple network architecture, the Transformer.",
    "pdf_url": "https://arxiv.org/pdf/2401.12345v1",
    "published": "2024-01-15",
}


@pytest.fixture
def storage(tmp_path):
    """PaperStorage backed by a temporary directory."""
    return PaperStorage(base_dir=str(tmp_path / "papers"))


@pytest.fixture
def populated_storage(storage):
    """Storage with one topic directory containing a sample paper."""
    from pathlib import Path

    topic_dir = Path(storage.base_dir) / "transformers"
    topic_dir.mkdir(parents=True)
    papers_file = topic_dir / "papers_info.json"
    papers_file.write_text(json.dumps({"2401.12345v1": SAMPLE_PAPER_DICT}, indent=2))
    return storage


@pytest.fixture
def sample_paper():
    return SAMPLE_PAPER


@pytest.fixture
def sample_paper_dict():
    return SAMPLE_PAPER_DICT
