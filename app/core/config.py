from pydantic import BaseSettings, Field, AnyUrl

class Settings(BaseSettings):
    app_name: str = "Avito AI Sales Agent"
    env: str = Field("dev", env="ENV")

    # Postgres
    postgres_dsn: AnyUrl = Field(..., env="POSTGRES_DSN")

    # Redis
    redis_dsn: str = Field(..., env="REDIS_DSN")

    # Bitrix24
    bitrix_webhook_url: AnyUrl = Field(..., env="BITRIX_WEBHOOK_URL")

    # Grok API
    grok_api_key: str = Field(..., env="GROK_API_KEY")
    grok_api_url: AnyUrl = Field("https://api.grok.com/v1", env="GROK_API_URL")

    # Telegram Bot
    telegram_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"