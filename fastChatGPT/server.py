
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
from typing import List, Dict
import os


load_dotenv()


mcp = FastMCP("web_search", host="0.0.0.0", port=8000)
tavily_client = TavilyClient(api_key=os.environ.get('TVLY'))

@mcp.tool()
def web_search(query: str) -> List[Dict]:
    """
    Use this tool to perform a web search using the Tavily API.
    Args:
        query (str): The search query object containing the query string.
    Returns:
        List[Dict]: A list of search results from the Tavily API.
    """
    print(f"Received query: {query}")
    try:
        
        response = tavily_client.search(query)
        print(f"Search results: {response['results']}")
        return response['results']

    except Exception as e:
        print(f"Error during web search: {e}")

if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport="streamable-http")