from sqlalchemy.orm import Session
from app.models.bot import Bot, Group
from app.models.user import User
from app.schemas import BotCreate, GroupCreate, BotSummary


def get_bot(db: Session, bot_id: int):
    return db.query(Bot).filter(Bot.id == bot_id).first()


def get_bots(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Bot).offset(skip).limit(limit).all()


def get_bot_by_name(db: Session, name: str):
    return db.query(Bot).filter(Bot.name == name).first()


def create_bot(db: Session, bot: BotCreate):
    db_bot = Bot(
        name=bot.name, description=bot.description, image=bot.image or "default.png"
    )
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot


def assign_user_to_group(db: Session, user_id: int, group_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    group = db.query(Group).filter(Group.id == group_id).first()
    if user and group:
        group.users.append(user)
        db.commit()
    return group


def assign_bot_to_group(db: Session, bot_id: int, group_id: int) -> Group:
    bot = db.query(Bot).filter(Bot.id == bot_id).first()
    group = db.query(Group).filter(Group.id == group_id).first()

    if not bot or not group:
        return None

    if bot not in group.bots:
        group.bots.append(bot)
        db.commit()
        db.refresh(group)

    # Konvertiere die Daten in ein Pydantic-Modell
    return Group(
        id=group.id,
        name=group.name,
        users=group.users,
        bots=[BotSummary(id=bot.id, name=bot.name) for bot in group.bots],
    )


def get_users_in_group(db: Session, group_id: int):
    group = db.query(Group).filter(Group.id == group_id).first()
    return group.users if group else None


def get_group_by_name(db: Session, name: str):
    return db.query(Group).filter(Group.name == name).first()


def create_group(db: Session, group: GroupCreate):
    db_group = Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_groups(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Group).offset(skip).limit(limit).all()


def get_group(db: Session, group_id: int):
    return db.query(Group).filter(Group.id == group_id).first()


def get_bots_in_group(db: Session, group_id: int):
    group = db.query(Group).filter(Group.id == group_id).first()
    return group.bots if group else None


def assign_bot_to_group(db: Session, bot_id: int, group_id: int) -> Group:
    bot = db.query(Bot).filter(Bot.id == bot_id).first()
    group = db.query(Group).filter(Group.id == group_id).first()

    if not bot or not group:
        return None

    if bot not in group.bots:
        group.bots.append(bot)

        # Associate the bot with all users in the group
        for user in group.users:
            if bot not in user.bots:
                user.bots.append(bot)

        db.commit()
        db.refresh(group)

    return group
