from pydantic import BaseModel
class GitHubToken(BaseModel):
    token: str