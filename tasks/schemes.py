import pydantic
from .models import TaskImportance, TaskStatus
import datetime as dt
from typing import Optional, Any


class TaskScheme(pydantic.BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    task_status: TaskStatus
    task_importance: TaskImportance
    reminder: Optional[dt.datetime] = None
    attendant: Optional[Any] = None
    xp: Optional[int] = None


class TaskForm(pydantic.BaseModel):
    title: Optional[str]
    description: Optional[str] = None
    task_status: Optional[TaskStatus] = TaskStatus.planning
    task_importance: Optional[TaskImportance] = TaskImportance.regular
    reminder: Optional[dt.datetime] = None
    attendant_id: Optional[int] = None
    xp: Optional[int] = None


class TaskFormEditable(pydantic.BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    task_status: Optional[TaskStatus] = TaskStatus.planning
    task_importance: Optional[TaskImportance] = TaskImportance.regular
    reminder: Optional[dt.datetime] = None
    attendant_id: Optional[int] = None
    xp: Optional[int] = None
