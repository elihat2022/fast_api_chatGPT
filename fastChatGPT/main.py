from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPEN_AI_KEY"))

class SearchQuery(BaseModel):
    query: str
   
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/web_search", operation_id="web_search")
async def web_search_endpoint(body: SearchQuery ):
    try:
        response = client.responses.create(
        tools=[
        {
            "type": "mcp",
            "server_label": "web_search",
            "server_url": "http://0.0.0.0:8000/mcp/",
            "require_approval": "never",
        },
    ],

        model="gpt-4.1",  # Cambiado de gpt-4.1 a gpt-4 que es más estable
        input=f"Search for information about: {body.query}")
        
        # Verificar si hay contenido en la respuesta
        content = response.output_text
        
        return {"response": content}
    except Exception as e:
        return {"error": str(e), "response": None}


if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor FastAPI en http://0.0.0.0:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
