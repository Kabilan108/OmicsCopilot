# src/server/api/routes/auth.py

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from schema.auth import User, NewUser, AuthResponse
from db import supabase


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=AuthResponse)
async def register(user: NewUser):
    """Register a new user."""

    try:
        response = supabase.auth.sign_up(user.model_dump())
    except Exception as E:
        raise HTTPException(status_code=400, detail=f"Error registering user: {E}")

    return {
        "message": "User registered successfully.",
        "user_id": response.user.id,
        "jwt": response.session.access_token,
    }


@router.post("/login", response_model=AuthResponse)
async def login(user: User):
    """Login a user."""

    try:
        response = supabase.auth.sign_in_with_password(user.model_dump())
    except Exception as E:
        raise HTTPException(status_code=400, detail=f"Error logging in user: {E}")

    return {
        "message": "User logged in successfully.",
        "user_id": response.user.id,
        "jwt": response.session.access_token,
    }


@router.get("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    """Logout a user."""

    try:
        supabase.auth.sign_out(token)
    except Exception as E:
        raise HTTPException(status_code=400, detail=f"Error logging out user: {E}")

    return {"message": "User logged out successfully."}
