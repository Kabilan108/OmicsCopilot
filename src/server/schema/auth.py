# src/server/api/schema/auth.py

from typing import Optional
from pydantic import BaseModel
import json


class User(BaseModel):
    email: str
    password: str


class NewUser(User):
    full_name: Optional[str] = None

    def model_dump(self, *args, **kwargs):
        return {
            "email": self.email,
            "password": self.password,
            "options": {"data": {"full_name": self.full_name or ""}},
        }

    def model_dump_json(self, *args, **kwargs) -> str:
        return json.dumps(self.model_dump(*args, **kwargs))


class AuthResponse(BaseModel):
    message: str
    user_id: str
    jwt: str
