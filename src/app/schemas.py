from pydantic import BaseModel, EmailStr
from typing import Optional


# Schema für Login-Daten
class Login(BaseModel):
    email: EmailStr
    password: str


# Schema für das zurückgegebene Token
class Token(BaseModel):
    access_token: str
    token_type: str


# Schema für zusätzliche Daten, die mit dem Token verwendet werden können
class TokenData(BaseModel):
    email: Optional[str] = None


# Schema für die Erstellung eines neuen Benutzers
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True


class BotBase(BaseModel):
    name: str
    description: Optional[str] = None
    image: Optional[str] = None


class BotCreate(BotBase):
    pass


class Bot(BotBase):
    id: int

    class Config:
        from_attributes = True


class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int

    class Config:
        from_attributes = True
