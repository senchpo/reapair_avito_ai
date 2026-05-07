# services/orchestrator/handlers/message_handler.py

from schemas.events import IncomingMessageEvent

class MessageHandler:
    async def handle(self, event: IncomingMessageEvent):
        # Заглушка бизнес-логики
        print(f"Handling message event: {event.message_id} in conversation {event.conversation_id}")