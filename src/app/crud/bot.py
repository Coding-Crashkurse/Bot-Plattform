from sqlalchemy.orm import Session
from app.models.bot import Bot
from app.schemas import BotCreate


def get_bot(db: Session, bot_id: int):
    return db.query(Bot).filter(Bot.id == bot_id).first()


def get_bots(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Bot).offset(skip).limit(limit).all()


def create_bot(db: Session, bot: BotCreate):
    db_bot = Bot(name=bot.name, description=bot.description, owner_id=bot.owner_id)
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot
