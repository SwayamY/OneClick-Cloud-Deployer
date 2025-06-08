from fastapi import APIRouter, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from app.utils.compose_utils import validate_compose_file
import os

router = APIRouter()

class ComposeInput(BaseModel):
    local_path: str


@router.post("/validate_compose")
def validate_compose(input: ComposeInput):
    docker_compose_path = os.path.join(input.local_path, "docker-compose.yml")
    print(f"[DEBUG] Reading docker-compose.yml from: {docker_compose_path}")
    print(f"[DEBUG] Validating docker-compose.yml file in: {input.local_path}")
    if not os.path.exists(docker_compose_path):
        raise HTTPException(status_code=400, detail="docker-compose.yml is not found in the given path.")
    # with open(docker_compose_path, 'r', encoding='utf-8') as f:  #for debug can open this check docker-compose.yml
    #     content = f.read()
    #     print(f"[DEBUG] docker-compose.yml content:\n{content}")
    valid, message = validate_compose_file(input.local_path)
    if not valid:
        raise HTTPException(status_code=400,detail=message)
    return {"status":"valid","message":message}
