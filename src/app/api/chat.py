from fastapi import APIRouter, HTTPException, Depends, Path, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.bot import Bot
import httpx
from pydantic import BaseModel
from typing import Union


class SimpleMessage(BaseModel):
    """Pydantic model focusing only on the content field."""

    content: Union[str, list[Union[str, dict]]]
    """The string contents of the message."""

    class Config:
        extra = "allow"  # Allows additional fields if needed


router = APIRouter()


@router.post("/{bot_id}", response_model=list[SimpleMessage])
async def proxy_chat_request(
    bot_id: int = Path(..., description="The ID of the bot to route the request to"),
    messages: list[SimpleMessage] = Body(
        ..., description="The list of messages to send to the bot's URL"
    ),
    db: Session = Depends(get_db),
):
    bot = db.query(Bot).filter(Bot.id == bot_id).first()

    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    if not bot.url:
        raise HTTPException(
            status_code=400, detail="Bot does not have a URL configured"
        )

    async with httpx.AsyncClient() as client:
        try:
            # Send the list of messages to the bot's URL
            response = await client.post(
                bot.url, json=[message.model_dump() for message in messages]
            )
            response.raise_for_status()

            # Parse and return the response as a list of BaseMessage objects
            response_data = response.json()
            return [SimpleMessage(**msg) for msg in response_data]

        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=500, detail=f"Error communicating with the bot: {str(exc)}"
            )
