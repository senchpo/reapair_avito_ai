from sqlalchemy.ext.asyncio import AsyncSession
from db.models.message import Message

class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, conversation_id: int, sender: str, content: str) -> Message:
        message = Message(
            conversation_id=conversation_id,
            sender=sender,
            content=content,
        )
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_all_by_conversation(self, conversation_id: int):
        result = await self.session.execute(
            select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp)
        )
        return result.scalars().all()