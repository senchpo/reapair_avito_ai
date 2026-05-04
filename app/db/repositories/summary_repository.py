from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import Lead

class SummaryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_summary(self, lead_id: str) -> str:
        result = await self.session.execute(
            select(Lead.summary).where(Lead.id == lead_id)
        )
        summary = result.scalar_one_or_none()
        return summary or ""

    async def save_summary(self, lead_id: str, summary: str):
        result = await self.session.execute(
            select(Lead).where(Lead.id == lead_id)
        )
        lead = result.scalar_one_or_none()
        if lead:
            lead.summary = summary
            await self.session.commit()