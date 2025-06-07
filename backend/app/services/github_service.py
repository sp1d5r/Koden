from typing import List, Dict, Optional
import aiohttp
import base64
import os
from fastapi import HTTPException
from app.core.config import settings
from firebase_admin import auth

class GitHubService:
    def __init__(self):
        self.base_url = "https://api.github.com"

    async def get_user_repositories(self, firebase_token: str) -> List[Dict]:
        """Get list of user's repositories using Firebase token"""
        try:
            # Verify Firebase token and get GitHub access token
            decoded_token = auth.verify_id_token(firebase_token)
            github_token = decoded_token.get('github_access_token')
            
            if not github_token:
                raise HTTPException(status_code=401, detail="No GitHub access token found")

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/user/repos",
                    headers={
                        "Authorization": f"token {github_token}",
                        "Accept": "application/vnd.github.v3+json"
                    }
                ) as response:
                    if response.status != 200:
                        raise HTTPException(status_code=400, detail="Failed to fetch repositories")
                    return await response.json()
        except auth.InvalidIdTokenError:
            raise HTTPException(status_code=401, detail="Invalid Firebase token")

    async def get_repository_zip(self, firebase_token: str, owner: str, repo: str, ref: str) -> bytes:
        """Download repository as zip file using Firebase token"""
        try:
            # Verify Firebase token and get GitHub access token
            decoded_token = auth.verify_id_token(firebase_token)
            github_token = decoded_token.get('github_access_token')
            
            if not github_token:
                raise HTTPException(status_code=401, detail="No GitHub access token found")

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/repos/{owner}/{repo}/zipball/{ref}",
                    headers={
                        "Authorization": f"token {github_token}",
                        "Accept": "application/vnd.github.v3+json"
                    }
                ) as response:
                    if response.status != 200:
                        raise HTTPException(status_code=400, detail="Failed to download repository")
                    return await response.read()
        except auth.InvalidIdTokenError:
            raise HTTPException(status_code=401, detail="Invalid Firebase token") 