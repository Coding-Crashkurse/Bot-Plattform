from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import List
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import logging

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware


# Define the request model using Pydantic
class Message(BaseModel):
    role: str
    content: str


# Initialize the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the OpenAI Chat model using LangChain
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
)


@app.post("/chat/")
async def chat_endpoint(messages: List[Message]):
    # Debug: Print the incoming payload
    print(f"Received messages: {messages}")

    # Convert the incoming messages into the format expected by ChatOpenAI
    formatted_messages = [(msg.role, msg.content) for msg in messages]

    # Invoke the model and get the result
    result = await llm.ainvoke(formatted_messages)

    # Log the result
    print("Result from AI:", result.content)

    # Return the response as a dictionary
    return {"role": "assistant", "content": result.content}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=4000)
