from typing import List, Dict
from openai import AsyncOpenAI

class SummaryEngine:
    """
    Автообновление summary после каждого сообщения.
    Summary хранится в БД и используется в AI промптах.
    """

    def __init__(self, openai_client: AsyncOpenAI, model: str = "gpt-4o-mini"):
        self.client = openai_client
        self.model = model

    async def update_summary(
        self,
        previous_summary: str,
        new_messages: List[Dict[str, str]]
    ) -> str:
        """
        Обновляет summary на основе предыдущего summary и новых сообщений.
        new_messages: [{"role": "user"/"assistant", "content": "..."}]
        """
        messages_text = "\n".join(
            f"{m['role']}: {m['content']}" for m in new_messages
        )

        prompt = f"""Ты — система резюмирования диалогов с лидом.
Обнови краткое summary диалога, сохранив ключевую информацию:
- Имя клиента
- Контактные данные
- Интересы и потребности
- Текущий этап воронки
- Важные детали

Предыдущее summary:
{previous_summary or "Нет предыдущего summary"}

Новые сообщения:
{messages_text}

Верни обновленное summary (сжато, до 500 символов):"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()