from fastapi import APIRouter
from app.api.routes.users.users import router as users_router
from app.api.routes.repos.repos import router as repos_router
from app.api.github import router as github_router
from app.api.tasks import router as tasks_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(repos_router, prefix="/repos", tags=["repos"])
router.include_router(github_router, prefix="/github", tags=["github"])
router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])