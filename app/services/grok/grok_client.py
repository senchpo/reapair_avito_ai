import httpx
from core.config import settings

class GrokClient:
    def __init__(self):
        self.base_url = settings.grok_api_base_url  # настройте в config
        self.api_key = settings.grok_api_key       # настройте
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=15.0)

    async def send_prompt(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        json_body = {"prompt": prompt}
        response = await self.client.post("generate", headers=headers, json=json_body)
        response.raise_for_status()
        data = response.json()
        return data.get("text", "")

    async def close(self):
        await self.client.aclose()