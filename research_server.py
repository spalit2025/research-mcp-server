import arxiv
import json
import os
from typing import List

# Try importing FastMCP, fallback to basic MCP if not available
try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("research")
    use_fastmcp = True
except ImportError:
    # Alternative: Use basic MCP server setup
    try:
        from mcp.server import Server
        from mcp.types import Tool, TextContent
        import asyncio
        
        server = Server("research")
        use_fastmcp = False
    except ImportError:
        # If MCP is not available, create a standalone version
        print("MCP not found. Creating standalone functions.")
        use_fastmcp = None

PAPER_DIR = "papers"

def search_papers(topic: str, max_results: int = 5) -> List[str]:
    """
    Search for papers on arXiv based on a topic and store their information.
    
    Args:
        topic: The topic to search for
        max_results: Maximum number of results to retrieve (default: 5)
    
    Returns:
        List of paper IDs found in the search
    """
    # Use arxiv to find the papers
    client = arxiv.Client()
    
    # Search for the most relevant articles matching the queried topic
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    papers = client.results(search)
    
    # Create directory for this topic
    path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, "papers_info.json")
    
    # Try to load existing papers info
    try:
        with open(file_path, "r") as json_file:
            papers_info = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        papers_info = {}
    
    # Process each paper and add to papers_info
    paper_ids: List[str] = []
    for paper in papers:
        short_id = paper.get_short_id()
        paper_ids.append(short_id)
        paper_info = {
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "summary": paper.summary,
            "pdf_url": paper.pdf_url,
            "published": str(paper.published.date()),
        }
        papers_info[short_id] = paper_info
    
    # Save updated papers_info to json file
    with open(file_path, "w") as json_file:
        json.dump(papers_info, json_file, indent=2)
    
    print(f"Results are saved in: {file_path}")
    return paper_ids

def extract_info(paper_id: str) -> str:
    """
    Search for information about a specific paper across all topic directories.
    
    Args:
        paper_id: The ID of the paper to look for
    
    Returns:
        JSON string with paper information if found, or an error message if not found
    """
    # Create PAPER_DIR if it doesn't exist
    if not os.path.exists(PAPER_DIR):
        return f"Papers directory '{PAPER_DIR}' does not exist."
    
    for item in os.listdir(PAPER_DIR):
        item_path = os.path.join(PAPER_DIR, item)
        if os.path.isdir(item_path):
            file_path = os.path.join(item_path, "papers_info.json")
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as json_file:
                        papers_info = json.load(json_file)
                        if paper_id in papers_info:
                            return json.dumps(papers_info[paper_id], indent=2)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error reading {file_path}: {str(e)}")
                    continue
    
    return f"There's no saved information related to paper {paper_id}."

# Register tools based on available MCP implementation
if use_fastmcp:
    # Using FastMCP
    mcp.tool()(search_papers)
    mcp.tool()(extract_info)
elif use_fastmcp is False:
    # Using basic MCP server
    @server.list_tools()
    async def handle_list_tools():
        return [
            Tool(name="search_papers", description="Search for papers on arXiv"),
            Tool(name="extract_info", description="Extract information about a specific paper")
        ]
    
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict):
        if name == "search_papers":
            result = search_papers(**arguments)
            return [TextContent(type="text", text=str(result))]
        elif name == "extract_info":
            result = extract_info(**arguments)
            return [TextContent(type="text", text=result)]
        else:
            raise ValueError(f"Unknown tool: {name}")

if __name__ == "__main__":
    if use_fastmcp:
        mcp.run(transport='stdio')
    elif use_fastmcp is False:
        # Basic MCP server setup with stdio transport
        import asyncio
        import sys
        from mcp.server.stdio import stdio_server
        
        async def main():
            async with stdio_server() as (read_stream, write_stream):
                await server.run(
                    read_stream, 
                    write_stream, 
                    server.create_initialization_options()
                )
        
        asyncio.run(main())
    else:
        # Standalone mode for testing
        print("Running in standalone mode...")
        print("Testing search_papers:")
        results = search_papers("machine learning", 3)
        print(f"Found papers: {results}")
        
        if results:
            print(f"\nTesting extract_info for {results[0]}:")
            info = extract_info(results[0])
            print(info)