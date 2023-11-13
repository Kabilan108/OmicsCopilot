# src/server/main.py

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

from server.routes import dataqc
from server import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CLIENT_URL, settings.QDRANT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(dataqc.router)


@app.get("/")
async def read_root():
    """Root endpoint."""
    return {"message": "Welcome to the OmicsCopilot API!"}


if __name__ == "__main__":
    if __name__ == "__main__":
        uvicorn.run(
            "server.main:app",
            host=settings.API_HOST,
            port=settings.API_PORT,
            reload=True,
        )
