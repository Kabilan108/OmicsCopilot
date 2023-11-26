# src/client/app/settings.py

from pydantic_settings import BaseSettings as BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    HELICONE_API_KEY: str


settings = Settings()
