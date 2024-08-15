from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas import UserCreate
from app.core.security import get_password_hash
from sqlalchemy.orm import joinedload


def get_user(db: Session, user_id: int):
    user = (
        db.query(User)
        .options(joinedload(User.bots), joinedload(User.group))
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        return None

    return user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
