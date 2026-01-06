from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdateStatus

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task_in: TaskCreate) -> Task:
        db_task = Task(
            title=task_in.title,
            description=task_in.description,
            status=TaskStatus.new
        )
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def get_tasks(self, skip: int = 0, limit: int = 100) -> list[Task]:
        result = await self.db.execute(select(Task).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_task(self, task_id: int) -> Task | None:
        result = await self.db.execute(select(Task).filter(Task.id == task_id))
        return result.scalar_one_or_none()

    async def update_status(self, task_id: int, status_in: TaskUpdateStatus) -> Task | None:
        task = await self.get_task(task_id)
        if not task:
            return None
        task.status = status_in.status
        await self.db.commit()
        await self.db.refresh(task)
        return task
