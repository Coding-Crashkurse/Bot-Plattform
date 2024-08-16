from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud import bot as crud_bot
from app import schemas
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Bot, status_code=status.HTTP_201_CREATED)
def create_bot(
    bot: schemas.BotCreate,
    db: Session = Depends(get_db),
):
    existing_bot = crud_bot.get_bot_by_name(db=db, name=bot.name)
    if existing_bot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A bot with this name already exists.",
        )

    return crud_bot.create_bot(db=db, bot=bot)


@router.get("/", response_model=List[schemas.Bot])
def read_bots(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    bots = crud_bot.get_bots(db, skip=skip, limit=limit)
    return bots


@router.get("/{bot_id}", response_model=schemas.Bot)
def read_bot(bot_id: int, db: Session = Depends(get_db)):
    bot = crud_bot.get_bot(db=db, bot_id=bot_id)
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot


@router.put("/{bot_id}", response_model=schemas.Bot)
def update_bot(bot_id: int, bot: schemas.BotCreate, db: Session = Depends(get_db)):
    db_bot = crud_bot.get_bot(db=db, bot_id=bot_id)
    if db_bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")

    db_bot.name = bot.name
    db_bot.description = bot.description
    db_bot.image = (
        bot.image or db_bot.image
    )  # Preserve the existing image if not provided
    db_bot.url = str(bot.url)  # Convert HttpUrl to string

    db.commit()
    db.refresh(db_bot)
    return db_bot


@router.delete("/{bot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bot(bot_id: int, db: Session = Depends(get_db)):
    bot = crud_bot.get_bot(db=db, bot_id=bot_id)
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    db.delete(bot)
    db.commit()
    return {"message": "Bot deleted successfully"}
