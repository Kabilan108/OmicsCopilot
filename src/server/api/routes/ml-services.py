# src/server/api/routes/ml-services.py

from fastapi import APIRouter, Depends, HTTPException

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager


router = APIRouter(
    prefix="/ml-services",
    tags=["ml-services"],
    responses={404: {"description": "Not found"}},
)
