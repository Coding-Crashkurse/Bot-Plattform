from fastapi import APIRouter, HTTPException, Depends, Path, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.bot import Bot
import httpx

router = APIRouter()


@router.post("/{bot_id}")
async def proxy_chat_request(
    bot_id: int = Path(..., description="The ID of the bot to route the request to"),
    payload: dict = Body(..., description="The payload to send to the bot's URL"),
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
            response = await client.post(bot.url, json=payload)
            response.raise_for_status()
            return response.json()

        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=500, detail=f"Error communicating with the bot: {str(exc)}"
            )
