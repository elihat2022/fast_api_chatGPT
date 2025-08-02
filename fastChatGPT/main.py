from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()



app = FastAPI()

client = OpenAI(api_key=os.environ.get("OPEN_AI_KEY"))


class Body(BaseModel):
    message: str

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/chat")
async def chat(body: Body):
    response = client.responses.create(
    model="gpt-4.1",
    input=body.message
)
    return {"response": response.output_text}

