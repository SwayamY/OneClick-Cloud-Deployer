from fastapi import APIRouter, HTTPException # type: ignore 
from pydantic import BaseModel, HttpUrl # type: ignore
from app.utils.git_utils import clone_repo_from_github
from app.utils.compose_utils import validate_compose_file
import os

router = APIRouter()

class RepoInput(BaseModel):
    repo_url: HttpUrl

@router.post("/clone_repo")
def clone_repo(input: RepoInput):
    repo_url_str = str(input.repo_url)
    success, local_path_or_error = clone_repo_from_github(repo_url_str)
    if not success:
        raise HTTPException(status_code=400, detail=local_path_or_error)
    try:
        validate_result = validate_compose_file(local_path_or_error)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail = f"cloned repo docker-compose.yml validation failed, {str(e)}"
        )

    return {"status": "cloned", "local_path": local_path_or_error,"validation":validate_result}
