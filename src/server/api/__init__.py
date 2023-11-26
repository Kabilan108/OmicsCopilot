# src/server/api/__init__.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    HELICONE_API_KEY: str

    PROJECT_NAME: str

    API_BASE: str
    API_HOST: str
    API_PORT: int
    API_RELOAD: bool

    CLIENT_URL: str


settings = Settings()
