# services/orchestrator/orchestrator.py

from schemas.events import IncomingMessageEvent, TakeoverEvent, PauseAIEvent, ResumeAIEvent
from services.orchestrator.handlers.message_handler import MessageHandler
from services.orchestrator.handlers.takeover_handler import TakeoverHandler

class Orchestrator:
    def __init__(self):
        self.message_handler = MessageHandler()
        self.takeover_handler = TakeoverHandler()

    async def handle_message(self, event: IncomingMessageEvent):
        # Сейчас вызываем заглушку
        await self.message_handler.handle(event)

    async def handle_takeover(self, event: TakeoverEvent):
        await self.takeover_handler.handle_takeover(event)

    async def handle_pause_ai(self, event: PauseAIEvent):
        await self.takeover_handler.handle_pause_ai(event)

    async def handle_resume_ai(self, event: ResumeAIEvent):
        await self.takeover_handler.handle_resume_ai(event)