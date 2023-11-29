# src/server/api/app.py

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from api.routes import datasets, auth
from api import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(auth.router)
app.include_router(datasets.router)


@app.get("/")
async def read_root():
    """Root endpoint."""
    return {"message": "Welcome to the OmicsCopilot API!"}
