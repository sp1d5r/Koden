from typing import List, Dict, Optional
import aiohttp
import base64
import os
from fastapi import HTTPException
from app.core.config import settings
from app.core.logging import logger
from firebase_admin import auth
from urllib.parse import urlparse, parse_qs

class GitHubService:
    def __init__(self):
        self.base_url = "https://api.github.com"

    async def get_user_repositories(
            self, 
            github_access_token: str,
            search_query: Optional[str] = None,
            page: int = 1,
            per_page: int = 10
        ) -> Dict:
        """Get list of user's repositories using GitHub access token with search and pagination"""
        if not github_access_token:
            raise HTTPException(status_code=401, detail="No GitHub access token found")

        try:
            async with aiohttp.ClientSession() as session:
                if search_query:
                    # First get the username
                    username = await self._get_username(github_access_token)
                    
                    # Use GitHub's search API for searching repositories
                    async with session.get(
                        f"{self.base_url}/search/repositories",
                        headers={
                            "Authorization": f"token {github_access_token}",
                            "Accept": "application/vnd.github.v3+json"
                        },
                        params={
                            "q": f"user:{username} {search_query} in:name,description",
                            "page": page,
                            "per_page": per_page,
                            "sort": "updated",
                            "order": "desc"
                        }
                    ) as response:
                        if response.status != 200:
                            error_data = await response.json()
                            logger.error(f"GitHub search error: {error_data}")
                            raise HTTPException(
                                status_code=response.status,
                                detail=f"GitHub search failed: {error_data.get('message', 'Unknown error')}"
                            )
                        
                        search_result = await response.json()
                        repositories = search_result.get("items", [])
                        total_count = search_result.get("total_count", 0)
                else:
                    # Use regular repositories API for listing all repositories
                    async with session.get(
                        f"{self.base_url}/user/repos",
                        headers={
                            "Authorization": f"token {github_access_token}",
                            "Accept": "application/vnd.github.v3+json"
                        },
                        params={
                            "page": page,
                            "per_page": per_page,
                            "sort": "updated",
                            "direction": "desc"
                        }
                    ) as response:
                        if response.status != 200:
                            raise HTTPException(status_code=400, detail="Failed to fetch repositories")

                        repositories = await response.json()
                        
                        # Get total count from Link header
                        link_header = response.headers.get("Link", "")
                        total_count = 0
                        if link_header:
                            for link in link_header.split(","):
                                if 'rel="last"' in link:
                                    url = link.split(";")[0].strip("<>")
                                    parsed_url = urlparse(url)
                                    query_params = parse_qs(parsed_url.query)
                                    last_page = int(query_params.get("page", ["1"])[0])
                                    total_count = last_page * per_page

                # Extract relevant fields only
                trimmed_repos = [
                    {
                        "name": repo["name"],
                        "html_url": repo["html_url"],
                        "description": repo["description"],
                        "language": repo["language"],
                        "stargazers_count": repo["stargazers_count"],
                        "forks_count": repo["forks_count"],
                        "updated_at": repo["updated_at"]
                    }
                    for repo in repositories
                ]

                return {
                    "repositories": trimmed_repos,
                    "total_count": total_count,
                    "page": page,
                    "per_page": per_page,
                    "total_pages": (total_count + per_page - 1) // per_page if total_count > 0 else 1
                }
        except Exception as e:
            logger.error(f"Error fetching GitHub repos: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def _get_username(self, github_access_token: str) -> str:
        """Get GitHub username from access token"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/user",
                    headers={
                        "Authorization": f"token {github_access_token}",
                        "Accept": "application/vnd.github.v3+json"
                    }
                ) as response:
                    if response.status != 200:
                        raise HTTPException(status_code=400, detail="Failed to fetch user info")
                    user_data = await response.json()
                    return user_data["login"]
        except Exception as e:
            logger.error(f"Error fetching GitHub user: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

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