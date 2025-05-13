from sqlalchemy.orm import declarative_base
from typing import Optional
from sqlalchemy.orm import relationship  # Add this import at the top
from typing import List  # Add this for the Deck model
from pydantic import BaseModel, ConfigDict
from sqlalchemy import ForeignKey  # Add this at the top with other SQLAlchemy imports
from sqlalchemy import Boolean, Column, Float, Integer, String, select
Base = declarative_base()

class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    isAdmin = Column(Boolean, default=False)

# Pydantic models for API input/output
class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    password: str
    isAdmin: bool = False
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[float] = None
    isAdmin: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)

############################################################

class CrewModel(Base):
    __tablename__ = "crew"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Pydantic models for API input/output
class Crew(BaseModel):
    id: Optional[int] = None
    name: str
    model_config = ConfigDict(from_attributes=True)

class CrewUpdate(BaseModel):
    name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


#################################################################
class TaskModel(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Pydantic models for API input/output
class Task(BaseModel):
    id: Optional[int] = None
    name: str
    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


#################################################################
class TodoModel(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    priority = Column(String, index=True)
    active = Column(Boolean, default=False)
    color = Column(String, index=True)
    label = Column(String, index=True)
    repeat_daily = Column(Boolean, default=False)
    

# Pydantic models for API input/output
class Todo(BaseModel):
    id: Optional[int] = None
    name: str
    priority: str
    active: bool
    repeat_daily: bool
    label: str
    color: str
    model_config = ConfigDict(from_attributes=True)

class TodoUpdate(BaseModel):
    name: Optional[str] = ''
    priority: Optional[str] = ''
    active: Optional[bool] = False
    repeat_daily: Optional[bool] = False
    color: Optional[str] = ''
    label: Optional[str] = ''

    model_config = ConfigDict(from_attributes=True)

#################################################################

class FlashCardModel(Base):
    __tablename__ = "flashcard"
    id = Column(Integer, primary_key=True, index=True)
    front = Column(String, index=True)
    back = Column(String, index=True)
    isDone = Column(Boolean, index=True)
    deckId = Column(Integer, ForeignKey("deck.id", ondelete="CASCADE"))
    deck = relationship(
        "DeckModel",
        back_populates="flashcards",
        lazy="selectin"  # This ensures efficient loading
    )

class DeckModel(Base):
    __tablename__ = "deck"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    flashcards = relationship(
        "FlashCardModel",
        back_populates="deck",
        lazy="selectin",  # This ensures efficient loading
        cascade="all, delete-orphan"  # This ensures proper cleanup
    )

# Pydantic models for API
class FlashCardBase(BaseModel):
    front: str
    back: str
    isDone: bool
    model_config = ConfigDict(from_attributes=True)

class FlashCard(FlashCardBase):
    id: Optional[int] = None
    isDone: Optional[bool]  = False
    deckId: Optional[int] = None

class FlashCardCreate(FlashCardBase):
    pass

class FlashCardUpdate(BaseModel):
    front: Optional[str] = None
    back: Optional[str] = None
    isDone: Optional[bool]  = None
    deckId: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class DeckBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class Deck(DeckBase):
    id: Optional[int] = None
    flashcards: List[FlashCard] = []

class DeckCreate(DeckBase):
    flashcards: Optional[List[FlashCardCreate]] = None

class DeckUpdate(BaseModel):
    name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)