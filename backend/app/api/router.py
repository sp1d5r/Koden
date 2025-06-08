from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.api.routes.users.users import router as users_router
from app.api.routes.repos.repos import router as repos_router
from app.api.auth import router as auth_router
from app.api.github import router as github_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(repos_router, prefix="/repos", tags=["repos"])
router.include_router(github_router, prefix="/github", tags=["github"])