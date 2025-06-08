from fastapi.testclient import TestClient # type: ignore 
from app.main import app
import tempfile
import os
import shutil

client = TestClient(app)

def create_temp_compose_dir(valid=True):
    tmp_dir = tempfile.mkdtemp()
    compose_path = os.path.join(tmp_dir,"docker-compose.yml")
    with open(compose_path,"w") as f:
        if valid:
            f.write("""\
                    version: '3'\n
                    services:\n
                        app:\n
                            image: nginx
                    """)
        else:
            f.write("version: '3'\nservices:\n app:\n image:[broken]") #malformed
    return tmp_dir

def test_validate_compose_valid():
    temp_dir = create_temp_compose_dir(valid=True)
    response = client.post("/api/validate_compose", json={"local_path":temp_dir})
    print("RESPONSE JSON:", response.json())
    shutil.rmtree(temp_dir)
    assert response.status_code == 200
    assert response.json()["status"] == "valid"

def test_validate_compose_invalid():
    temp_dir = create_temp_compose_dir(valid=False)
    response = client.post("./api/validate_compose", json={"local_path":temp_dir})
    shutil.rmtree(temp_dir)
    assert response.status_code == 400
    assert "could not" in response.json()["detail"].lower() or "yaml" in response.json()["detail"].lower()

def test_validate_compose_missing_file():
    temp_dir = tempfile.mkdtemp()
    response = client.post("./api/validate_compose", json={"local_path": temp_dir})
    shutil.rmtree(temp_dir)
    assert response.status_code == 400
    assert "not found" in  response.json()["detail"].lower()