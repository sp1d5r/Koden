from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router
from app.api.github import router as github_router
from app.api.auth import router as auth_router
from app.core.logging import logger

app = FastAPI(title="Koden Backend", version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Koden Backend")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Koden Backend")

app.include_router(router, prefix="/api")
app.include_router(github_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth") 