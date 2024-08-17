from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import SystemMessage, HumanMessage


class Message(BaseModel):
    role: str
    content: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
)


@app.post("/chat/")
async def chat_endpoint(messages: List[Message]):
    system_message = SystemMessage(
        content="Ahoy there! Ye be a clever assistant, known far and wide as Jack Sparrow. Speak like the legendary pirate Captain Jack Sparrow, with all his wit, charm, and pirate slang. Savvy?"
    )

    formatted_messages = [system_message] + [
        HumanMessage(role=msg.role, content=msg.content) for msg in messages
    ]

    result = await llm.ainvoke(formatted_messages)

    print("Result from AI:", result.content)

    return {"role": "assistant", "content": result.content}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
