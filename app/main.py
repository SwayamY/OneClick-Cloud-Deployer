from fastapi import FastAPI
from app.endpoints.clone_repo import router as clone_router
from app.endpoints.validate_compose import router as validate_router

app = FastAPI(
    title="OneClick Cloud Deployer",
    version="0.1.0"
)

app.include_router(clone_router, prefix="/api")
app.include_router(validate_router, prefix="/api")
