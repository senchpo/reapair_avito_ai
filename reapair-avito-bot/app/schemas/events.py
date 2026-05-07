# schemas/events.py

from pydantic import BaseModel
from typing import Optional

class IncomingMessageEvent(BaseModel):
    event_type: str = "avito_message"
    message_id: str
    conversation_id: str
    text: str
    # Добавьте другие поля по необходимости

class TakeoverEvent(BaseModel):
    event_type: str = "telegram_takeover"
    lead_id: str
    new_owner_id: str

class PauseAIEvent(BaseModel):
    event_type: str = "telegram_pause_ai"
    lead_id: str

class ResumeAIEvent(BaseModel):
    event_type: str = "telegram_resume_ai"
    lead_id: str