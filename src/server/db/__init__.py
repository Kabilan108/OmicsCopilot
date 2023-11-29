# src/server/db/__init__.py

from supabase import create_client, Client
from pathlib import Path

from api import settings


MODULE_PATH = Path(__file__).parent
DB_PATH = MODULE_PATH / "omicscopilot.db"

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
