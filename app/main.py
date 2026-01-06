from fastapi import FastAPI
from app.core.config import settings

from app.api import tasks

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

@app.get("/")
async def root():
    return {"message": "Hello World", "project": settings.PROJECT_NAME}
