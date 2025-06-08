from app.models.api.github import GitHubToken
from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import StreamingResponse
from app.services.github_service import GitHubService
from app.core.auth import get_current_user, require_claim
from app.core.logging import logger
import io
from firebase_admin import auth as firebase_auth
from typing import Optional

router = APIRouter()
github_service = GitHubService()

@router.get("/auth-url")
async def get_github_auth_url():
    """Get GitHub OAuth URL for user authentication"""
    return {"url": await github_service.get_oauth_url()}

@router.post("/callback")
async def github_callback(code: str):
    """Handle GitHub OAuth callback and return access token"""
    access_token = await github_service.get_access_token(code)
    return {"access_token": access_token}

@router.get("/repositories")
async def get_repositories(
    search: Optional[str] = None,
    page: int = 1,
    per_page: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Get list of user's repositories with search and pagination"""
    return await github_service.get_user_repositories(
        current_user['github_access_token'],
        search_query=search,
        page=page,
        per_page=per_page
    )

@router.get("/repository/{owner}/{repo}/download")
async def download_repository(
    owner: str, 
    repo: str, 
    ref: str, 
    current_user: dict = Depends(get_current_user)
):
    """Download repository as zip file"""
    zip_data = await github_service.get_repository_zip(
        current_user['token'],
        owner,
        repo,
        ref
    )
    
    return StreamingResponse(
        io.BytesIO(zip_data),
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{owner}-{repo}-{ref}.zip"'
        }
    )


@router.post("/store-token")
async def store_github_token(
    token_data: GitHubToken,
    current_user: dict = Depends(get_current_user)
):
    """Store GitHub access token in Firebase custom claims"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User must be authenticated to store GitHub token"
        )
        
    logger.info(f"Storing GitHub token for user {current_user['uid']}")
    logger.info(f"Token data: {token_data}")
    try:
        # Set custom claims for the user - this is a sync operation
        firebase_auth.set_custom_user_claims(
            current_user["uid"],
            {"github_access_token": token_data.token}
        )
        return {"message": "GitHub token stored successfully"}
    except Exception as e:
        logger.error(f"Error storing GitHub token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store GitHub token: {str(e)}"
        ) 