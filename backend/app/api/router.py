from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from .routes.users.users import router as users_router
from .routes.analyse.analyse import router as analyse_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(analyse_router, prefix="/analyse", tags=["analyse"])