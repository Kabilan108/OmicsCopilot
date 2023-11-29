# src/runpod-worker/src/settings.py

from pydantic_settings import BaseSettings
from pydantic import Field

from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    MODEL_PATH: Path

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    ONNX_EMBEDDING_MODEL: Optional[Path] = Field(None, env="ONNX_EMBEDDING_MODEL")


settings = Settings()
