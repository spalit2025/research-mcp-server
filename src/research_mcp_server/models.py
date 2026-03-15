"""Data models for academic papers."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Paper:
    """Represents an academic paper with metadata."""

    paper_id: str
    title: str
    authors: list[str]
    summary: str
    pdf_url: str
    published: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization (excludes paper_id)."""
        data = asdict(self)
        del data["paper_id"]
        return data

    @classmethod
    def from_dict(cls, paper_id: str, data: dict[str, Any]) -> "Paper":
        """Create a Paper from a dictionary and paper ID."""
        return cls(
            paper_id=paper_id,
            title=data["title"],
            authors=data["authors"],
            summary=data["summary"],
            pdf_url=data["pdf_url"],
            published=data["published"],
        )
