# services/lead/qualifier.py

from enum import Enum
from typing import Optional

class LeadQuality(str, Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"

class LeadQualifier:
    """
    Логика классификации лида на hot, warm, cold. 
    Здесь простой пример на основе наличия телефона и активности.
    """

    def qualify(
        self,
        has_phone: bool,
        conversation_stage: str,
        message_count: Optional[int] = 0
    ) -> LeadQuality:
        if has_phone and conversation_stage in {"HOT", "TRANSFERRED", "HUMAN_ACTIVE"}:
            return LeadQuality.HOT
        elif message_count and message_count > 3:
            return LeadQuality.WARM
        else:
            return LeadQuality.COLD