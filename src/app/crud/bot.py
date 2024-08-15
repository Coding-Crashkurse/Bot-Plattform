from sqlalchemy.orm import Session
from app.models.bot import Bot, Group
from app.schemas import BotCreate


def get_bot(db: Session, bot_id: int):
    return db.query(Bot).filter(Bot.id == bot_id).first()


def get_bots(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Bot).offset(skip).limit(limit).all()


def create_bot(db: Session, bot: BotCreate):
    db_bot = Bot(
        name=bot.name, description=bot.description, image=bot.image or "default.png"
    )
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot


def assign_bot_to_group(db: Session, bot_id: int, group_id: int):
    bot = get_bot(db, bot_id)
    group = db.query(Group).filter(Group.id == group_id).first()
    if bot and group:
        group.bots.append(bot)
        db.commit()
    return bot


def get_group(db: Session, group_id: int):
    return db.query(Group).filter(Group.id == group_id).first()
