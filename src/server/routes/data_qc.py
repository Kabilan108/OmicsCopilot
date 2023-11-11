# src/server/routes/data_qc.py

from fastapi import APIRouter, Depends, HTTPException, status

from server import settings


router = APIRouter(
    prefix="/data_qc",
    tags=["data qc"],
    responses={404: {"description": "Not found"}},
)
