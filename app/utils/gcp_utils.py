import os 
import time
import json
import random
from google.oauth2 import service_account
from googleapiclient import discovery 
from dotenv import load_dotenv

load_dotenv()
CREDENTIALS_PATH= os.getenv("GCP_CREDENTIALS_PATH")
PROJECT_ID= os.getenv("GCP_PROJECT_ID")
ZONE= os.getenv("GCP_ZONE")
MACHINE_TYPE= os.getenv("GCP_MACHINE_TYPE")
IMAGE_FAMILY= os.getenv("GCP_IMAGE_FAMILY")
IMAGE_PROJECT= os.getenv("GCP_IMAGE_PROJECT")

credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
compute = discovery.build('compute','v1',credentials=credentials)

def generate_unique_vm_name(prefix="oneclick-vm"):
    suffix = random.randint(1000,9999)
    return f"{prefix}-{suffix}"

def create_instance(repo_url):
    vm_name = generate_unique_vm_name()
    print(f"[INFO] creatinng VM: {vm_name}")

    config ={
        "name": vm_name,
        "machineType": f"zones/{ZONE}/machineTypes/{MACHINE_TYPE}",
        "items": ["allow-external-8000"],
        "disks": [
            {
                "boot": True,
                "autoDelete": True,
                "initializeParams" : {
                    "sourceImage" : f"projects/{IMAGE_PROJECT}/global/images/family/{IMAGE_FAMILY}",
                },
            }
        ],
        "networkInterfaces": [
            {
                "network": "global/networks/default",
                "accessConfigs": [{"type": "ONE_TO_ONE_NAT","name":"External NAT"}],

            }
        ],
        "metadata": {
            "items": [
                {
                    "key": "startup-script",
                    "value": f"""#!/bin/bash
                    sudo apt update
                    sudo apt install -y git docker.io

                    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                    sudo chmod +x /usr/local/bin/docker-compose /usr/bin/docker-compose
                    
                    git clone {repo_url}
                    cd $(basename {repo_url} .git)
                    sudo docker-compose up --build -d
                    """
                }
            ]
        }
    }
    response = compute.instances().insert(
        project=PROJECT_ID,
        zone=ZONE,
        body=config
    ).execute()

    return {"vm_name": vm_name,"status": "creating", "operation": response["name"]}


def get_instance_external_ip(vm_name):
    result = compute.instances().get(
        project=PROJECT_ID,
        zone=ZONE,
        instance=vm_name
    ).execute()

    try:
        return result['networkInterfaces'][0]['accessConfigs'][0]['natIP']
    except Exception as e:
        print(f"External IP extraction failed exception: {str(e)}")
        return str(e)