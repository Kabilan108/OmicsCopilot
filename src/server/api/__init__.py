# src/server/api/__init__.py

from pydantic_settings import BaseSettings
from pydantic import computed_field


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

    @computed_field
    @property
    def CLIENT_URL(self) -> str:
        return f"http://{self.CLIENT_HOST}:{self.CLIENT_PORT}"


settings = Settings()
