from enum import Enum
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import Lead

class Ownership(str, Enum):
    AI = "AI"
    HUMAN = "HUMAN"

class OwnershipManager:
    """
    Управляет переключением ownership между AI и HUMAN.
    При HUMAN — AI не отвечает.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_ownership(self, lead_id: str) -> Ownership:
        result = await self.session.execute(
            select(Lead.ownership).where(Lead.id == lead_id)
        )
        ownership = result.scalar_one_or_none()
        return Ownership(ownership) if ownership else Ownership.AI

    async def set_ownership(self, lead_id: str, ownership: Ownership, user_id: Optional[str] = None):
        result = await self.session.execute(
            select(Lead).where(Lead.id == lead_id)
        )
        lead = result.scalar_one_or_none()
        if lead:
            lead.ownership = ownership.value
            if user_id:
                lead.assigned_user_id = user_id
            await self.session.commit()

    async def is_ai_active(self, lead_id: str) -> bool:
        ownership = await self.get_ownership(lead_id)
        return ownership == Ownership.AI

    async def take_over(self, lead_id: str, user_id: str):
        """Менеджер берет лид себе"""
        await self.set_ownership(lead_id, Ownership.HUMAN, user_id)

    async def return_to_ai(self, lead_id: str):
        """Возврат к AI"""
        await self.set_ownership(lead_id, Ownership.AI)