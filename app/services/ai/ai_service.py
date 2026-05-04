# services/ai/ai_service.py

from enum import Enum
from typing import Optional

class Ownership(str, Enum):
    AI = "AI"
    HUMAN = "HUMAN"

class Stage(str, Enum):
    NEW = "NEW"
    QUALIFYING = "QUALIFYING"
    HOT = "HOT"
    TRANSFERRED = "TRANSFERRED"
    HUMAN_ACTIVE = "HUMAN_ACTIVE"

class AIContext:
    def __init__(
        self,
        stage: Stage,
        has_phone: bool,
        has_photo: bool,
        summary: Optional[str],
        ownership: Ownership,
    ):
        self.stage = stage
        self.has_phone = has_phone
        self.has_photo = has_photo
        self.summary = summary or ""
        self.ownership = ownership


class AIService:
    def __init__(self):
        # Здесь может быть инициализация модели AI, API и т.п.
        pass

    async def generate_response(self, user_message: str, context: AIContext) -> str:
        # Если ownership HUMAN — AI не отвечает
        if context.ownership == Ownership.HUMAN:
            return ""  # AI должен молчать, ответственность у человека

        # Формируем контекст для генерации
        prompt_parts = [
            f"Stage: {context.stage}",
            f"Has phone: {'yes' if context.has_phone else 'no'}",
            f"Has photo: {'yes' if context.has_photo else 'no'}",
            f"Summary: {context.summary}",
            f"Ownership: {context.ownership}",
            f"User message: {user_message}",
        ]
        prompt = "\n".join(prompt_parts)

        # Заглушка генерации — в реальном варианте тут будет вызов ML-модели или API
        response = self.simple_rule_based_response(user_message, context)

        return response

    def simple_rule_based_response(self, user_message: str, context: AIContext) -> str:
        """
        Простой пример генерации ответа на основе ключей в сообщении и стадии.
        Это заглушка, позже заменить на полноценный AI-модуль.
        """
        if context.stage == Stage.NEW and not context.has_phone:
            return "Здравствуйте! Можете, пожалуйста, оставить ваш номер телефона?"

        if "цена" in user_message.lower():
            return "Стоимость товара составляет 10 000 рублей."

        if context.stage == Stage.QUALIFYING and context.has_phone:
            return "Спасибо за предоставленный номер. Мы скоро с вами свяжемся."

        return "Спасибо за сообщение! Чем могу помочь?"
