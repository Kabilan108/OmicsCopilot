# src/client/app/settings.py

from pydantic_settings import BaseSettings as BaseSettings
from rich.logging import RichHandler
import streamlit as st
import logging

from schema.auth import Session

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)


def get_user() -> Session:
    """Get the user ID from the session state."""
    return st.session_state.get("session", None)


def set_user(user_id: str, token: str):
    """Set the user ID in the session state."""
    st.session_state["session"] = Session(user_id=user_id, jwt=token)


def clear_user():
    """Clear the user ID from the session state."""
    st.session_state["session"] = None


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    HELICONE_API_KEY: str

    API_BASE: str

    def get_endpoint(self, endpoint: str) -> str:
        """Get the full URL for an API endpoint."""
        return f"{self.API_BASE}/{endpoint}"


settings = Settings()
