import httpx
from core.config import settings

class Bitrix24Client:
    def __init__(self):
        self.base_url = settings.bitrix_api_base_url
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=10.0)

    async def get_lead(self, lead_id: int):
        response = await self.client.get(f"crm.lead.get.json?id={lead_id}")
        response.raise_for_status()
        return response.json()

    async def add_lead(self, data: dict):
        response = await self.client.post("crm.lead.add.json", json={"fields": data})
        response.raise_for_status()
        return response.json()

    async def update_lead(self, lead_id: int, data: dict):
        response = await self.client.post("crm.lead.update.json", json={"id": lead_id, "fields": data})
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()