from fastapi import APIRouter, HTTPException # type: ignore 
from pydantic import BaseModel, HttpUrl # type: ignore
from app.utils.git_utils import clone_repo_from_github
from app.utils.compose_utils import validate_compose_file
from app.utils.gcp_utils import create_instance , get_instance_external_ip
#import os
import time

router = APIRouter()

class RepoInput(BaseModel):
    repo_url: HttpUrl

@router.post("/clone_repo")
def clone_repo(input: RepoInput):
    repo_url_str = str(input.repo_url)
    #1 cloning
    success, local_path_or_error = clone_repo_from_github(repo_url_str)
    if not success:
        raise HTTPException(status_code=400, detail=local_path_or_error)
    #2 Validation using yaml 
    try:
        validate_result = validate_compose_file(local_path_or_error)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail = f"cloned repo docker-compose.yml validation failed, {str(e)}"
        )
    
    try:
        gcp_response = create_instance(repo_url_str)
        vm_name = gcp_response["vm_name"]

        time.sleep(10)

        external_ip = get_instance_external_ip(vm_name)
    except Exception as e :
        raise HTTPException(
            status_code=500,
            detail=f"GCP Deployment failure: {str(e)}"
        )
    

    return {"status": "cloned",
            "local_path": local_path_or_error,
            "validation":validate_result ,
            "VM_Deployment": gcp_response,
            "VM_Name": vm_name,
            "External_IP": external_ip or "pending",
            "note": "It may take 1-2 mins  before  the app is live on this IP"}
