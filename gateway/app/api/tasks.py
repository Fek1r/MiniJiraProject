from fastapi import APIRouter, HTTPException, status
from app.grpc_generated import task_pb2
from app.core.grpc_client import grpc_client
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdateStatus

router = APIRouter()

@router.on_event("startup")
async def startup_event():
    await grpc_client.connect()

@router.on_event("shutdown")
async def shutdown_event():
    await grpc_client.close()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_in: TaskCreate):
    request = task_pb2.CreateTaskRequest(title=task_in.title, description=task_in.description)
    response = await grpc_client.stub.CreateTask(request)
    return TaskResponse(
        id=response.id,
        title=response.title,
        description=response.description,
        status=response.status
    )

@router.get("/", response_model=list[TaskResponse])
async def list_tasks(skip: int = 0, limit: int = 100):
    request = task_pb2.ListTasksRequest(skip=skip, limit=limit)
    response = await grpc_client.stub.ListTasks(request)
    return [
        TaskResponse(
            id=t.id,
            title=t.title,
            description=t.description,
            status=t.status
        ) for t in response.tasks
    ]

@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(task_id: int, status_in: TaskUpdateStatus):
    try:
        request = task_pb2.UpdateStatusRequest(id=task_id, status=status_in.status.value)
        response = await grpc_client.stub.UpdateStatus(request)
        return TaskResponse(
            id=response.id,
            title=response.title,
            description=response.description,
            status=response.status
        )
    except Exception as e:
        # Simplistic error handling
        raise HTTPException(status_code=404, detail="Task not found or error updating")

@router.get("/stats")
async def get_stats():
    request = task_pb2.Empty()
    response = await grpc_client.stub.GetStats(request)
    return {
        "total_tasks": response.total_tasks,
        "by_status": dict(response.by_status)
    }
