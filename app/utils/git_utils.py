import os
import subprocess
import tempfile
from urllib.parse import urlparse

def clone_repo_from_github(repo_url: str):
    try:
        parsed = urlparse(repo_url)
        repo_name = os.path.splitext(os.path.basename(parsed.path))[0]
        clone_dir = tempfile.mkdtemp(prefix="repo_")
        repo_path = os.path.join(clone_dir, repo_name)
        
        result = subprocess.run(
            ["git", "clone", repo_url, repo_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            return False, result.stderr.strip()
        return True, repo_path
    except Exception as e:
        return False, str(e)
