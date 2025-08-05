from datetime import datetime
from fastapi import FastAPI, Form
from agent_mcp import agent
from pydantic import BaseModel
from typing import Annotated


app = FastAPI(title="FastAPI and MCP Integration",)

# Define a Pydantic model for the search query
class Query(BaseModel):
    query: str

# Define the root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FASTAPI and MCP Integration!"}

# Define your endpoints
@app.post("/agent")
async def agent_endpoint(body: Annotated[Query, Form()]):
    """
    Perform different tasks using the MCP agent.
    Args:
        body (Query): The performs the query object containing the query string.
    Returns:
        dict: A dictionary containing the response from the agent.
    """
    print(f"Received search query: {body.query}")
    async with agent:
        try:
            enhanced_prompt = f"Please search for information about: {body.query} or performs what the user needs, you have tools to help you, return the concise and helpful results. Today is {datetime.now().strftime('%Y-%m-%d')}. "+"if user asks for saving/writing files create a folder named 'files' in the root directory and save the files there."
            # Run the agent with the enhanced prompt
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