# src/server/api/__init__.py

from pydantic_settings import BaseSettings
from pydantic import computed_field
from typing import Optional


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    HELICONE_API_KEY: str

    PROJECT_NAME: str

    API_BASE: str
    API_HOST: str
    API_PORT: int
    API_RELOAD: bool

    CLIENT_HOST: str
    CLIENT_PORT: int

    SUPABASE_URL: str
    SUPABASE_KEY: str

    PG_USER: Optional[str] = None
    PG_PASS: Optional[str] = None
    PG_HOST: Optional[str] = None
    PG_PORT: Optional[str] = None
    PG_NAME: Optional[str] = None

    @computed_field
    @property
    def CLIENT_URL(self) -> str:
        return f"http://{self.CLIENT_HOST}:{self.CLIENT_PORT}"


settings = Settings()
