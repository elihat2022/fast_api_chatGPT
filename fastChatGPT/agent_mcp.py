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




# pinecone = MCPServerStdio(
#     command="npx",
#     args=[
#         "-y",
#         "@pinecone-database/mcp"
#     ],
#     env={
#         "PINECONE_API_KEY": os.environ.get("PINECONE_API_KEY")
#     }
# )


# Agent configuration using pydantic_ai
agent = Agent(
    'google-gla:gemini-2.5-flash',
    system_prompt=("Today is " + datetime.now().strftime("%Y-%m-%d") + ". "
        "You are a helpful assistant that can search the web and interact with Pinecone's MCP server. "
        
        "When the user asks for  Pinecone-related tasks or code, use the `pinecone` MCP server and its tools (e.g., `search_docs`, `create-index-for-model`, `upsert-records`, `search-records`). "
        """
        - When generating code related to Pinecone, always use the `pinecone` MCP and the `search_docs` tool.
        - Perform at least two distinct searches per request using different, relevant questions to ensure comprehensive context is gathered before writing code.
        - If an error occurs while executing Pinecone-related code, invoke the `pinecone` MCP and the `search_docs` tool to search for guidance on the specific error.
        - Verify and use the correct syntax for the latest stable version of the Pinecone SDK.
        - Prefer official code snippets and examples from Pinecone documentation over generated or assumed values.
        - Do not fabricate field names, parameter values, or request formats.
        - When providing installation instructions, use `pip install pinecone` (not deprecated packages like `pinecone-client`).
        """
        "Available tools: web_search, filesystem, pinecone"
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

