from sqlalchemy import (
    Column, Integer, String, DateTime, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from db.models import Base

class ConversationState(str, enum.Enum):
    NEW = "NEW"
    QUALIFYING = "QUALIFYING"
    HOT = "HOT"
    TRANSFERRED = "TRANSFERRED"
    HUMAN_ACTIVE = "HUMAN_ACTIVE"
    APPOINTMENT = "APPOINTMENT"
    CLOSED = "CLOSED"
    LOST = "LOST"


class OwnerType(str, enum.Enum):
    AI = "AI"
    HUMAN = "HUMAN"
    HYBRID = "HYBRID"


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    avito_chat_id = Column(String(64), unique=True, index=True, nullable=False)
    owner = Column(Enum(OwnerType), default=OwnerType.AI, nullable=False)
    state = Column(Enum(ConversationState), default=ConversationState.NEW, nullable=False)
    last_message_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete")