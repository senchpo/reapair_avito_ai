# services/router/message_router.py

from typing import Union
from schemas.events import IncomingMessageEvent, TakeoverEvent, PauseAIEvent, ResumeAIEvent
from services.orchestrator.orchestrator import Orchestrator

class MessageRouter:
    def __init__(self):
        self.orchestrator = Orchestrator()

    async def route(self, event: Union[IncomingMessageEvent, TakeoverEvent, PauseAIEvent, ResumeAIEvent]):
        event_type = getattr(event, "event_type", None)

        if event_type == "avito_message":
            await self.orchestrator.handle_message(event)
        elif event_type == "telegram_takeover":
            await self.orchestrator.handle_takeover(event)
        elif event_type == "telegram_pause_ai":
            await self.orchestrator.handle_pause_ai(event)
        elif event_type == "telegram_resume_ai":
            await self.orchestrator.handle_resume_ai(event)
        else:
            raise ValueError(f"Unknown event type: {event_type}")