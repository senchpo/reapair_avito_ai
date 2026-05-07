# services/bitrix/integration.py

from typing import Optional

class BitrixClient:
    def __init__(self, api_token: str, base_url: str):
        self.api_token = api_token
        self.base_url = base_url

    def create_lead(self, phone: str, data: dict) -> Optional[str]:
        """
        Создает новый лид в Bitrix.
        Возвращает id лида или None.
        """
        # Пример запроса к API Bitrix, заглушка
        # Реализовать реальный запрос через requests или aiohttp
        print(f"Создаем лид с телефоном {phone} и данными {data}")
        lead_id = "12345"  # заглушка
        return lead_id

    def update_lead(self, lead_id: str, data: dict) -> bool:
        """
        Обновляет существующий лид.
        """
        print(f"Обновляем лид {lead_id} с данными {data}")
        return True

    def change_responsible(self, lead_id: str, user_id: str) -> bool:
        """
        Меняет ответственного за лид.
        """
        print(f"Меняем ответственного для лида {lead_id} на пользователя {user_id}")
        return True