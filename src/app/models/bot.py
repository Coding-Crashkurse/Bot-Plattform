from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Verknüpfungstabelle für die Many-to-Many-Beziehung zwischen Bot und Group sowie Bot und User
bot_group_association = Table(
    "bot_group_association",
    Base.metadata,
    Column("bot_id", Integer, ForeignKey("bots.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
    extend_existing=True,  # Erlaubt SQLAlchemy, eine existierende Tabelle zu erweitern
)

user_bot_association = Table(
    "user_bot_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("bot_id", Integer, ForeignKey("bots.id"), primary_key=True),
    extend_existing=True,  # Erlaubt SQLAlchemy, eine existierende Tabelle zu erweitern
)


class Bot(Base):
    __tablename__ = "bots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    image = Column(
        String, default="default.png"
    )  # Standardbild, wenn kein Bild vorhanden ist
    url = Column(String, nullable=True)  # Add the URL field

    # Many-to-Many Beziehung zu Gruppen
    groups = relationship(
        "Group", secondary=bot_group_association, back_populates="bots"
    )

    # Many-to-Many Beziehung zu Benutzern
    users = relationship("User", secondary=user_bot_association, back_populates="bots")


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Many-to-Many Beziehung zu Bots
    bots = relationship("Bot", secondary=bot_group_association, back_populates="groups")

    # One-to-Many Beziehung zu Benutzern
    users = relationship("User", back_populates="group")
