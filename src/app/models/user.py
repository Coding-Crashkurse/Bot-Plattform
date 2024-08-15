from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Verknüpfungstabelle für die Many-to-Many-Beziehung zwischen User und Bot
user_bot_association = Table(
    "user_bot_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("bot_id", Integer, ForeignKey("bots.id"), primary_key=True),
    extend_existing=True,  # Dies erlaubt es SQLAlchemy, eine existierende Tabelle zu erweitern
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", back_populates="users")

    # Many-to-Many Beziehung zu Bots
    bots = relationship("Bot", secondary=user_bot_association, back_populates="users")
