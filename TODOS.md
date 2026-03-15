# TODOs

## P1

### Semantic Scholar Integration
Add Semantic Scholar as a second paper source alongside arXiv. Requires an abstract
source interface in the storage layer, a new API client, and merged search results.
This is the key differentiator that elevates the project from a single-source demo
to a multi-source research tool.
- **Effort:** L
- **Depends on:** storage.py architecture (complete)

## P2

### Console Script Entry Point
Add `[project.scripts]` to `pyproject.toml` so users can run `research-mcp-server`
directly instead of locating and running the Python file.
- **Effort:** S
- **Depends on:** pyproject.toml (complete)

### Search History Resource
Add `papers://search-history` resource tracking what topics were searched and when.
Gives AI assistants memory of past research sessions across conversations.
- **Effort:** M
- **Depends on:** storage.py (complete)

### PyPI Publishing
Publish the package to PyPI so users can install with `pip install research-mcp-server`.
Requires PyPI account setup, unique package name verification, and a release workflow
in GitHub Actions.
- **Effort:** M
- **Depends on:** pyproject.toml + tests passing (complete)

## P3

### Compare Papers Tool
Add `compare_papers(id_a, id_b)` tool returning a side-by-side comparison of paper
metadata (authors, dates, topics, summaries).
- **Effort:** S
- **Depends on:** storage.py (complete)
