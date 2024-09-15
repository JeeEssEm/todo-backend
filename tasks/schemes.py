import pydantic
from .models import TaskImportance, TaskStatus
import datetime as dt
from typing import Optional


class TaskScheme(pydantic.BaseModel):
    title: str
    description: Optional[str] = None
    task_status: TaskStatus
    task_importance: TaskImportance
    reminder: Optional[dt.datetime] = None
