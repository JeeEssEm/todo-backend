import sqlalchemy
from .models import Task, TaskStatus, TaskImportance
from teams.models import UsersTeams
import datetime as dt
from pagination.pagination import paginate
from .utils import task_scheme_converter


class TaskCRUD:
    @staticmethod
    async def get_personal_tasks(session: sqlalchemy.orm.Session, user_id: int,
                                 page: int, limit: int):
        q = session.query(Task).filter(Task.team_id == None).filter(  # noqa
            Task.attendant_id == user_id
        ).filter(
            Task.status != TaskStatus.archived
        )
        if limit:
            q = q.limit(limit)
        return await paginate(page, q, task_scheme_converter, limit)

    @staticmethod
    async def get_task_by_id(session: sqlalchemy.orm.Session, task_id: int):
        return session.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    async def check_user_can_see(session: sqlalchemy.orm.Session, user_id: int,
                                 task_id: int):
        task = await TaskCRUD.get_task_by_id(session, task_id)
        if task is None:
            return False
        if task.attendant_id == user_id:
            return True

        q = session.query(UsersTeams).filter(
            UsersTeams.c.team_id == task.team_id).filter(
            UsersTeams.c.user_id == user_id
        ).first()
        return q is not None

    @staticmethod
    async def create_task(
            session: sqlalchemy.orm.Session,
            title: str, description: str, reminder: dt.datetime,
            task_status: TaskStatus, task_importance: TaskImportance,
            user_id: int, team_id: int = None, xp: int = 10):
        task = Task(
            title=title, description=description, reminder=reminder,
            status=task_status, importance=task_importance,
            attendant_id=user_id, team_id=team_id, xp=xp
        )
        session.add(task)
        session.commit()

    @staticmethod
    async def get_paginated_personal_tasks(
            session: sqlalchemy.orm.Session, user_id: int,
            page: int, limit: int,
            status: TaskStatus = None,
            importance: TaskImportance = None
    ):
        q = session.query(Task).filter(Task.attendant_id == user_id).filter(
            Task.team_id == None  # noqa
        )
        if status:
            q = q.filter(Task.status == status)
        else:
            q = q.filter(Task.status != TaskStatus.archived)
        if importance:
            q = q.filter(Task.importance == importance)

        return await paginate(page, q, task_scheme_converter, limit)
