import logging
from fastapi import APIRouter, HTTPException, Depends, Path, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.bot import Bot
import httpx

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/{bot_id}", response_model=dict)
async def proxy_chat_request(
    bot_id: int = Path(..., description="The ID of the bot to route the request to"),
    messages=Body(..., description="The list of messages to send to the bot's URL"),
    db: Session = Depends(get_db),
):
    logger.info(f"Received request for bot_id: {bot_id}")
    logger.info(f"Messages received: {messages}")

    bot = db.query(Bot).filter(Bot.id == bot_id).first()

    if not bot:
        logger.error(f"Bot with id {bot_id} not found.")
        raise HTTPException(status_code=404, detail="Bot not found")

    if not bot.url:
        logger.error(f"Bot with id {bot_id} does not have a URL configured.")
        raise HTTPException(
            status_code=400, detail="Bot does not have a URL configured"
        )

    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"Sending messages to bot URL: {bot.url}")
            response = await client.post(bot.url, json=messages)
            response.raise_for_status()

            response_data = response.json()
            logger.info(f"Response received: {response_data}")
            return response_data  # Return a single dictionary

        except httpx.RequestError as exc:
            logger.error(f"Error communicating with the bot: {exc}")
            raise HTTPException(
                status_code=500, detail=f"Error communicating with the bot: {str(exc)}"
            )
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"HTTP error: {exc.response.status_code} - {exc.response.text}"
            )
            raise HTTPException(
                status_code=exc.response.status_code, detail=exc.response.text
            )
