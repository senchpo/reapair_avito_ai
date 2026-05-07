from services.bitrix.bitrix_client import Bitrix24Client

class BitrixService:
    def __init__(self):
        self.client = Bitrix24Client()

    async def create_lead(self, phone: str, name: str, description: str = ""):
        data = {
            "TITLE": f"Lead from Avito webhook - {name}",
            "NAME": name,
            "PHONE": [{"VALUE": phone, "VALUE_TYPE": "WORK"}],
            "COMMENTS": description,
            "STATUS_ID": "NEW"
        }
        result = await self.client.add_lead(data)
        return result

    async def get_lead(self, lead_id: int):
        return await self.client.get_lead(lead_id)

    async def update_lead_status(self, lead_id: int, status_id: str):
        data = {"STATUS_ID": status_id}
        return await self.client.update_lead(lead_id, data)