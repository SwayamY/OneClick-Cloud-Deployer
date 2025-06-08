import os
import yaml


def validate_compose_file(redo_path:str):
    try:
        compose_path = os.path.join(redo_path,"docker-compose.yml")
        if not os.path.isfile(compose_path):
            return False, "docker-compose.yml not found."
        
        with open(compose_path, 'r') as f:
            yaml.safe_load(f)
        return True, "docker-compose.yml is valid."


    except Exception as e:
        return False, str(e)
