from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
from tavily import TavilyClient
from typing import List, Dict
import os
from fastChatGPT.agent import agent

# Load environment variables
load_dotenv()

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# Initialize Tavily client
tavily_client = TavilyClient(api_key=os.environ.get('TVLY'))


@agent.tool_plain
def web_search(query: str) -> List[Dict]:
    """
    Perform a web search using the Tavily API.

    Args:
        query: The search query string to look up on the web.

    Returns:
        A list of search results from the Tavily API, where each result is a dictionary.
    """
    print(f"Received query: {query}")
    try:
        response = tavily_client.search(query)
        results = response.get("results", [])
        print(f"✅ Found {len(results)} search results")
        return results
    except Exception as e:
        print(f"Error during web search: {e}")
        # En lugar de ModelRetry, retorna un error descriptivo
        return [{"error": f"Search failed: {str(e)}"}]

# Define a Pydantic model for the search query
class SearchQuery(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastChatGPT web search API!"}

@app.post("/web_search")
async def web_search_endpoint(body: SearchQuery):
    """
    Endpoint to perform a web search using the Tavily API.
    """
    print(f"Received search query: {body.query}")
    
    try:
        enhanced_prompt = f"Please search the web for information about: {body.query}, return the concise and helpful results."
        result = await agent.run(user_prompt=enhanced_prompt)
        print(f"Agent output: {result.output}")
        return {"response": result.output}
    except Exception as e:
        print(f"Error in agent run: {e}")
        return {"response": f"Error: {str(e)}"}


if __name__ == "__main__":
    import uvicorn
    print("FastApi is running at http://0.0.0.0:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)