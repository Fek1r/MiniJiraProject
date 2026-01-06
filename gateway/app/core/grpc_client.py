import grpc
import os
from app.grpc_generated import task_pb2, task_pb2_grpc

class GrpcClient:
    def __init__(self):
        # In Docker this will be "task_service:50051", locally "localhost:50051"
        self.target = os.getenv("GRPC_SERVER_HOST", "localhost:50051")
        self.channel = None
        self.stub = None

    async def connect(self):
        self.channel = grpc.aio.insecure_channel(self.target)
        self.stub = task_pb2_grpc.TaskServiceStub(self.channel)

    async def close(self):
        if self.channel:
            await self.channel.close()

grpc_client = GrpcClient()
