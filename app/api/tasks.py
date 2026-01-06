from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdateStatus
from app.services.task import TaskService

router = APIRouter()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_in: TaskCreate, db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.create_task(task_in)

@router.get("/", response_model=list[TaskResponse])
async def list_tasks(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.get_tasks(skip, limit)

@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(task_id: int, status_in: TaskUpdateStatus, db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    task = await service.update_status(task_id, status_in)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    # Simple mock stats for now, can be expanded strictly if needed
    service = TaskService(db)
    tasks = await service.get_tasks(limit=1000)
    return {
        "total_tasks": len(tasks),
        "by_status": {
            "new": len([t for t in tasks if t.status == "new"]),
            "in_progress": len([t for t in tasks if t.status == "in_progress"]),
            "done": len([t for t in tasks if t.status == "done"]),
        }
    }
