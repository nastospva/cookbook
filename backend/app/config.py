from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    WEBAPP_URL: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


settings = Settings()