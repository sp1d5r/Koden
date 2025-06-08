import os
import tempfile
import zipfile
from pathlib import Path
from typing import Optional
import aiohttp
import asyncio
from app.celery_app import celery_app
from app.core.logging import logger

@celery_app.task(name="download_github_repo")
def download_github_repo(owner: str, repo: str, ref: str, access_token: str, output_path: Optional[str] = None) -> str:
    """
    Download a GitHub repository and save it as a zip file.
    
    Args:
        owner: Repository owner
        repo: Repository name
        ref: Branch/tag/commit reference
        access_token: GitHub access token
        output_path: Optional path to save the zip file. If not provided, a temporary file will be created.
    
    Returns:
        str: Path to the downloaded zip file
    """
    try:
        # Create a temporary directory if no output path is provided
        if not output_path:
            temp_dir = tempfile.mkdtemp()
            output_path = os.path.join(temp_dir, f"{owner}-{repo}-{ref}.zip")
        
        # Run the async download in a sync context
        zip_data = asyncio.run(_download_repo_async(owner, repo, ref, access_token))
        
        # Save the zip data to file
        with open(output_path, 'wb') as f:
            f.write(zip_data)
        
        logger.info(f"Successfully downloaded repository {owner}/{repo}@{ref}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error downloading repository: {str(e)}")
        raise

async def _download_repo_async(owner: str, repo: str, ref: str, access_token: str) -> bytes:
    """Async helper function to download the repository zip"""
    url = f"https://api.github.com/repos/{owner}/{repo}/zipball/{ref}"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"Failed to download repository: {error_text}")
            return await response.read() 