from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.utils.git_utils import clone_repo_from_github

router = APIRouter()

class RepoInput(BaseModel):
    repo_url: HttpUrl

@router.post("/clone_repo")
def clone_repo(input: RepoInput):
    success, local_path_or_error = clone_repo_from_github(input.repo_url)
    if not success:
        raise HTTPException(status_code=400, detail=local_path_or_error)
    return {"status": "cloned", "local_path": local_path_or_error}
