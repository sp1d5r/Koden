from fastapi import FastAPI
from app.api.routes import router
from app.core.logging import logger

app = FastAPI(title="Koden Backend", version="0.1.0")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Koden Backend")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Koden Backend")

app.include_router(router, prefix="/api") 