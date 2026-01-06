import asyncio
import grpc
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.grpc_generated import task_pb2, task_pb2_grpc
from app.services.task import TaskService
from app.schemas.task import TaskCreate, TaskUpdateStatus

class TaskServiceServicer(task_pb2_grpc.TaskServiceServicer):
    async def get_db(self):
        async with AsyncSessionLocal() as session:
            yield session

    async def CreateTask(self, request, context):
        async for session in self.get_db():
            service = TaskService(session)
            task_in = TaskCreate(title=request.title, description=request.description)
            task = await service.create_task(task_in)
            return task_pb2.TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description or "",
                status=task.status.value
            )

    async def ListTasks(self, request, context):
        async for session in self.get_db():
            service = TaskService(session)
            tasks = await service.get_tasks(skip=request.skip, limit=request.limit)
            return task_pb2.ListTasksResponse(
                tasks=[task_pb2.TaskResponse(
                    id=t.id,
                    title=t.title,
                    description=t.description or "",
                    status=t.status.value
                ) for t in tasks]
            )

    async def UpdateStatus(self, request, context):
        async for session in self.get_db():
            service = TaskService(session)
            status_in = TaskUpdateStatus(status=request.status)
            task = await service.update_status(request.id, status_in)
            if not task:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Task not found")
                return task_pb2.TaskResponse()
            return task_pb2.TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description or "",
                status=task.status.value
            )

    async def GetStats(self, request, context):
        async for session in self.get_db():
            service = TaskService(session)
            # Reusing get_tasks for stats for now
            tasks = await service.get_tasks(limit=1000)
            stats = {
                "new": len([t for t in tasks if t.status == "new"]),
                "in_progress": len([t for t in tasks if t.status == "in_progress"]),
                "done": len([t for t in tasks if t.status == "done"]),
            }
            return task_pb2.StatsResponse(
                total_tasks=len(tasks),
                by_status=stats
            )

async def serve():
    server = grpc.aio.server()
    task_pb2_grpc.add_TaskServiceServicer_to_server(TaskServiceServicer(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    print(f"Starting gRPC server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
