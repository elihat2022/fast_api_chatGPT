from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from tavily import TavilyClient
from typing import Dict, List
import os




load_dotenv()


# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# Initialize Tavily client
tavily_client = TavilyClient(api_key=os.environ.get('TVLY'))

# Define all your MCP tools here
# For example, if you have a filesystem tool, you can define it like this:
filesystem = MCPServerStdio(
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-filesystem",
            f"{os.environ.get('FILESYSTEM_PATH')}"
        ]
    )




# Agent configuration using pydantic_ai
agent = Agent(
    'google-gla:gemini-2.5-flash',
    system_prompt=("Today is " + datetime.now().strftime("%Y-%m-%d") + ". "
        
        """
        - Perform at least two distinct searches per request using different, relevant questions to ensure comprehensive context is gathered before writing code.
        - Do not fabricate field names, parameter values, or request formats.
        
        """
        "Available tools: web_search, filesystem"
        "Use filesystem to write, read, or update data and files."
        "If user asks for saving/writing files, create a folder named 'files' in the root directory and save the files there."      

    ),
    toolsets=[filesystem, 
    ], # Define the toolsets available to the agent
    instructions="if user asks for saving/writing files create a folder named 'files' in the root directory and save the files there."
)


# Define agent tool
@agent.tool_plain(name="web_search")
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

