from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Bitrix
    BITRIX_API_TOKEN: str
    BITRIX_BASE_URL: str

    # Telegram
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ADMIN_CHAT_ID: str

    # Avito
    AVITO_CLIENT_ID: str = ""
    AVITO_CLIENT_SECRET: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()