"""File-based storage for academic paper metadata."""

import json
import logging
from pathlib import Path
from typing import Any

from .models import Paper

logger = logging.getLogger(__name__)


class PaperStorage:
    """Manages paper metadata storage organized by topic directories."""

    def __init__(self, base_dir: str = "papers") -> None:
        self.base_dir = Path(base_dir)

    def validate_topic_path(self, topic: str) -> Path:
        """Validate a topic name and return the safe directory path.

        Raises:
            ValueError: If the topic name would escape the base directory.
        """
        topic_dir = topic.lower().replace(" ", "_")
        path = self.base_dir / topic_dir
        resolved = path.resolve()
        if not str(resolved).startswith(str(self.base_dir.resolve())):
            raise ValueError(f"Invalid topic name: {topic}")
        return path

    def save_papers(self, topic: str, papers: dict[str, Paper]) -> Path:
        """Save papers to a topic directory, merging with any existing data.

        Returns:
            Path to the saved JSON file.
        """
        path = self.validate_topic_path(topic)
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / "papers_info.json"

        existing = self._load_json(file_path)
        for paper_id, paper in papers.items():
            existing[paper_id] = paper.to_dict()

        with open(file_path, "w") as f:
            json.dump(existing, f, indent=2)

        return file_path

    def load_papers(self, topic: str) -> dict[str, Any]:
        """Load all papers for a given topic.

        Returns:
            Dictionary mapping paper IDs to paper metadata.

        Raises:
            ValueError: If the topic name is invalid (path traversal).
        """
        path = self.validate_topic_path(topic)
        file_path = path / "papers_info.json"
        if not file_path.exists():
            return {}
        return self._load_json(file_path)

    def find_paper(self, paper_id: str) -> dict[str, Any] | None:
        """Find a paper by ID across all topic directories.

        Returns:
            Paper metadata dictionary if found, None otherwise.
        """
        if not self.base_dir.exists():
            return None

        for topic_dir in self.base_dir.iterdir():
            if not topic_dir.is_dir() or topic_dir.is_symlink():
                continue
            file_path = topic_dir / "papers_info.json"
            if file_path.is_file():
                data = self._load_json(file_path)
                if paper_id in data:
                    return data[paper_id]
        return None

    def list_topics(self) -> list[str]:
        """List all topic folders that contain paper data.

        Returns:
            Sorted list of topic directory names.
        """
        if not self.base_dir.exists():
            return []

        topics = []
        for topic_dir in self.base_dir.iterdir():
            if topic_dir.is_dir() and not topic_dir.is_symlink():
                if (topic_dir / "papers_info.json").exists():
                    topics.append(topic_dir.name)
        return sorted(topics)

    def _load_json(self, file_path: Path) -> dict[str, Any]:
        """Load a JSON file, returning an empty dict on error."""
        try:
            with open(file_path) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning("Failed to read %s: %s", file_path, e)
            return {}
