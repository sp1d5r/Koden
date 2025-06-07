from fastapi import APIRouter, HTTPException, Response, Depends
from fastapi.responses import StreamingResponse
from app.services.github_service import GitHubService
from app.core.auth import get_current_user
from typing import List, Dict
import io

router = APIRouter()
github_service = GitHubService()

@router.get("/github/auth-url")
async def get_github_auth_url():
    """Get GitHub OAuth URL for user authentication"""
    return {"url": await github_service.get_oauth_url()}

@router.post("/github/callback")
async def github_callback(code: str):
    """Handle GitHub OAuth callback and return access token"""
    access_token = await github_service.get_access_token(code)
    return {"access_token": access_token}

@router.get("/github/repositories")
async def get_repositories(current_user: dict = Depends(get_current_user)):
    """Get list of user's repositories"""
    return await github_service.get_user_repositories(current_user['token'])

@router.get("/github/repository/{owner}/{repo}/download")
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