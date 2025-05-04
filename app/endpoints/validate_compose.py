from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.compose_utils import validate_compose_file

router = APIRouter()

class ComposeInput(BaseModel):
    local_path: str


@router.post("/validate_compose")
def validate_compose(input: ComposeInput):
    valid, message = validate_compose_file(input.local_path)
    if not valid:
        raise HTTPException(status_code=400,detail=message)
    return {"status":"valid","message":message}
