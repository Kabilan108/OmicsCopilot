# src/runpod-worker/src/settings.py

from pydantic_settings import BaseSettings

from pathlib import Path


class Settings(BaseSettings):
    MODEL_PATH: Path

    EMBEDDING_MODEL: str
    ONNX_EMBEDDING_MODEL: Path


settings = Settings()
