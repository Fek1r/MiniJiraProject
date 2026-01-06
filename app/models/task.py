import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class TaskStatus(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.new, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
