from fastapi import FastAPI
from app.api import tasks
from app.core.config import settings

app = FastAPI(title=f"{settings.PROJECT_NAME} Gateway")

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

@app.get("/")
async def root():
    return {"message": "Gateway Running", "project": settings.PROJECT_NAME}
