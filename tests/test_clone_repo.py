from fastapi.testclient import TestClient # type: ignore 
from app.main import app
import os

client = TestClient(app)

def test_clone_repo_valid():
    response = client.post("/api/clone_repo", json={"repo_url": "https://github.com/octocat/Hello-World.git"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "cloned"
    assert "local_path" in data

    # Cleanup cloned repo folder after test (optional)
    import shutil
    shutil.rmtree(data["local_path"], ignore_errors=True)

def test_clone_repo_invalid_url():
    response = client.post("/api/clone_repo", json={"repo_url": "not-a-valid-url"})
    assert response.status_code == 422  # Pydantic validation error

def test_validate_compose_valid(tmp_path):
    # Setup: create a dummy valid docker-compose.yml file
    compose_dir = tmp_path / "repo"
    compose_dir.mkdir()
    compose_file = compose_dir / "docker-compose.yml"
    compose_file.write_text("""
version: '3'
services:
  web:
    image: nginx
    ports:
      - "80:80"
""")

    response = client.post("/api/validate_compose", json={"local_path": str(compose_dir)})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "valid"

def test_validate_compose_missing_file(tmp_path):
    # Setup: directory with no docker-compose.yml
    empty_dir = tmp_path / "empty_repo"
    empty_dir.mkdir()

    response = client.post("/api/validate_compose", json={"local_path": str(empty_dir)})
    assert response.status_code == 400
    data = response.json()
    assert "not found" in data["detail"]

def test_validate_compose_invalid_yaml(tmp_path):
    # Setup: directory with invalid docker-compose.yml content
    bad_dir = tmp_path / "bad_repo"
    bad_dir.mkdir()
    bad_file = bad_dir / "docker-compose.yml"
    bad_file.write_text("invalid: [unbalanced brackets")

    response = client.post("/api/validate_compose", json={"local_path": str(bad_dir)})
    assert response.status_code == 400
    data = response.json()
    assert "mapping values" in data["detail"] or "expected" in data["detail"]
