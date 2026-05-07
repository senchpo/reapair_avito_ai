from sqlalchemy import (
    Column, Integer, String, DateTime, Enum, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from db.models import Base

class MessageSender(str, enum.Enum):
    AI = "AI"
    HUMAN = "HUMAN"
    SYSTEM = "SYSTEM"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    sender = Column(Enum(MessageSender), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    conversation = relationship("Conversation", back_populates="messages")