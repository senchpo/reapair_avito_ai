from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models.conversation import Conversation
from typing import Optional
from db.models.conversation import ConversationState
from services.conversation.state_machine import ConversationStateMachine

class ConversationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_avito_chat_id(self, avito_chat_id: str) -> Optional[Conversation]:
        result = await self.session.execute(
            select(Conversation).where(Conversation.avito_chat_id == avito_chat_id)
        )
        return result.scalars().first()

    async def create(self, avito_chat_id: str) -> Conversation:
        conv = Conversation(avito_chat_id=avito_chat_id)
        self.session.add(conv)
        await self.session.commit()
        await self.session.refresh(conv)
        return conv

    async def update_owner(self, conversation: Conversation, owner: str):
        conversation.owner = owner
        await self.session.commit()
    async def update_state(self, conversation: Conversation, new_state: ConversationState):
        sm = ConversationStateMachine(conversation.state)
        try:
            sm.transition(new_state)
            conversation.state = sm.current_state
            await self.session.commit()
            return conversation
        except ValueError as e:
            raise ValueError(f"State update error: {str(e)}")