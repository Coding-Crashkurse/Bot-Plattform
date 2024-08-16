from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List, TYPE_CHECKING

# Use TYPE_CHECKING to avoid circular imports during runtime
if TYPE_CHECKING:
    from app.schemas import BotSummary


# Schema for Login Data
class Login(BaseModel):
    email: EmailStr
    password: str


# Schema for Token Response
class Token(BaseModel):
    access_token: str
    token_type: str


# Schema for Token Data
class TokenData(BaseModel):
    email: Optional[str] = None


# Base User Schema
class UserBase(BaseModel):
    email: str


# User Creation Schema
class UserCreate(UserBase):
    password: str


# Detailed User Schema
class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    bots: Optional[List["BotSummary"]] = []  # Forward reference to BotSummary
    group: Optional["GroupSummary"] = None  # Forward reference to GroupSummary

    model_config = {"from_attributes": True}


# Base Group Schema
class GroupBase(BaseModel):
    name: str


# Group Creation Schema
class GroupCreate(GroupBase):
    pass


# Group Summary Schema
class GroupSummary(GroupBase):
    id: int


# Group Detail Schema (with users and bots)
class GroupDetail(GroupBase):
    id: int
    users: List[User] = []
    bots: List["BotSummary"] = []

    model_config = {"from_attributes": True}


# Main Group Schema
class Group(GroupBase):
    id: int
    users: List[User] = []
    bots: List["BotSummary"] = []

    model_config = {"from_attributes": True}


# Base Bot Schema
class BotBase(BaseModel):
    name: str
    description: str
    image: str = "default.png"
    url: HttpUrl  # Validates that the URL is well-formed


# Bot Creation Schema
class BotCreate(BotBase):
    pass


# Bot Summary Schema
class BotSummary(BotBase):
    id: int


# Bot Detail Schema (with groups)
class BotDetail(BotBase):
    id: int
    groups: List[GroupSummary] = []

    model_config = {"from_attributes": True}


# Main Bot Schema
class Bot(BotBase):
    id: int
    groups: List[GroupSummary] = []

    model_config = {"from_attributes": True}


class UserEmailIdSchema(BaseModel):
    email: str
    id: int

    model_config = {"from_attributes": True}


class BotIdNameSchema(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
