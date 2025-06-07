from fastapi import APIRouter, Depends, HTTPException, status
from app.core.auth import get_current_user
from firebase_admin import auth
from pydantic import BaseModel

router = APIRouter()

class GitHubToken(BaseModel):
    token: str

@router.post("/store-github-token")
async def store_github_token(
    token_data: GitHubToken,
    current_user: dict = Depends(get_current_user)
):
    """Store GitHub access token in Firebase custom claims"""
    try:
        # Set custom claims for the user
        await auth.set_custom_user_claims(
            current_user["uid"],
            {"github_access_token": token_data.token}
        )
        return {"message": "GitHub token stored successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store GitHub token: {str(e)}"
        ) 