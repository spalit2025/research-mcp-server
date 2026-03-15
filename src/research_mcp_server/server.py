"""MCP server for arXiv paper search and research management."""

import json
import logging
import urllib.error

import arxiv
from mcp.server.fastmcp import FastMCP

from .models import Paper
from .storage import PaperStorage

logger = logging.getLogger(__name__)

mcp = FastMCP("research")
storage = PaperStorage()


@mcp.tool()
def search_papers(topic: str, max_results: int = 5) -> list[str]:
    """
    Search for papers on arXiv based on a topic and store their information.

    Args:
        topic: The topic to search for
        max_results: Maximum number of results to retrieve (default: 5, max: 50)

    Returns:
        List of paper IDs found in the search
    """
    topic = topic.strip()
    if not topic:
        return ["Error: Topic cannot be empty."]

    max_results = max(1, min(max_results, 50))

    try:
        storage.validate_topic_path(topic)
    except ValueError:
        return ["Error: Invalid topic name."]

    client = arxiv.Client()
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    try:
        results = client.results(search)
        papers: dict[str, Paper] = {}
        paper_ids: list[str] = []

        for result in results:
            paper_id = result.get_short_id()
            paper_ids.append(paper_id)
            papers[paper_id] = Paper(
                paper_id=paper_id,
                title=result.title,
                authors=[author.name for author in result.authors],
                summary=result.summary,
                pdf_url=str(result.pdf_url),
                published=str(result.published.date()),
            )
    except (urllib.error.URLError, ConnectionError) as e:
        logger.error("arXiv API unreachable: %s", e, exc_info=True)
        return ["Error: arXiv API is currently unavailable. Please try again later."]
    except arxiv.HTTPError as e:
        logger.error("arXiv API HTTP error (status %d): %s", e.status, e)
        return [f"Error: arXiv API returned an error (HTTP {e.status})."]

    try:
        file_path = storage.save_papers(topic, papers)
        logger.info("Saved %d papers to %s", len(papers), file_path)
    except OSError as e:
        logger.error("Failed to save papers: %s", e)
        return ["Error: Failed to save search results to disk."]

    return paper_ids


@mcp.tool()
def extract_info(paper_id: str) -> str:
    """
    Search for information about a specific paper across all topic directories.

    Args:
        paper_id: The ID of the paper to look for

    Returns:
        JSON string with paper information if found, error message if not found
    """
    paper_id = paper_id.strip()
    if not paper_id:
        return "Error: Paper ID cannot be empty."

    paper_data = storage.find_paper(paper_id)
    if paper_data is None:
        return f"No saved information found for paper '{paper_id}'."

    return json.dumps(paper_data, indent=2)


@mcp.resource("papers://folders")
def get_available_folders() -> str:
    """List all available topic folders in the papers directory."""
    topics = storage.list_topics()

    content = "# Available Topics\n\n"
    if topics:
        for topic in topics:
            content += f"- {topic}\n"
        content += "\nUse papers://<topic_name> to access papers in a specific topic.\n"
    else:
        content += "No topics found. Use the search_papers tool to get started.\n"

    return content


@mcp.resource("papers://{topic}")
def get_topic_papers(topic: str) -> str:
    """
    Get detailed information about papers on a specific topic.

    Args:
        topic: The research topic to retrieve papers for
    """
    try:
        papers_data = storage.load_papers(topic)
    except ValueError:
        return (
            f"# Error: Invalid topic name\n\n"
            f"The topic '{topic}' contains invalid characters."
        )

    if not papers_data:
        return (
            f"# No papers found for topic: {topic}\n\n"
            f"Try searching for papers on this topic first."
        )

    content = f"# Papers on {topic.replace('_', ' ').title()}\n\n"
    content += f"Total papers: {len(papers_data)}\n\n"

    for paper_id, paper_info in papers_data.items():
        content += f"## {paper_info['title']}\n"
        content += f"- **Paper ID**: {paper_id}\n"
        content += f"- **Authors**: {', '.join(paper_info['authors'])}\n"
        content += f"- **Published**: {paper_info['published']}\n"
        pdf = paper_info["pdf_url"]
        content += f"- **PDF URL**: [{pdf}]({pdf})\n\n"
        content += f"### Summary\n{paper_info['summary'][:500]}...\n\n"
        content += "---\n\n"

    return content


@mcp.prompt()
def generate_search_prompt(topic: str, num_papers: int = 5) -> str:
    """Generate a prompt for systematic academic paper research on a specific topic."""
    return (
        f"Search for {num_papers} academic papers about "
        f"'{topic}' using the search_papers tool.\n\n"
        f"Follow these instructions:\n"
        f"1. First, search for papers using "
        f"search_papers(topic='{topic}', max_results={num_papers})\n"
        f"2. For each paper found, extract and organize:\n"
        f"   - Paper title\n"
        f"   - Authors\n"
        f"   - Publication date\n"
        f"   - Brief summary of the key findings\n"
        f"   - Main contributions or innovations\n"
        f"   - Methodologies used\n"
        f"   - Relevance to the topic '{topic}'\n\n"
        f"3. Provide a comprehensive summary that includes:\n"
        f"   - Overview of the current state of research in '{topic}'\n"
        f"   - Common themes and trends across the papers\n"
        f"   - Key research gaps or areas for future investigation\n"
        f"   - Most impactful or influential papers in this area\n\n"
        f"4. Organize your findings in a clear, structured format "
        f"with headings and bullet points."
    )


def main() -> None:
    """Run the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
