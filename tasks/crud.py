import sqlalchemy
from .models import Task, TaskStatus


class TaskCRUD:
    @staticmethod
    async def get_personal_tasks(session: sqlalchemy.orm.Session, user_id: int,
                                 limit: int = None):
        q = session.query(Task).filter(Task.team_id == None).filter(
            Task.attendant_id == user_id
        ).filter(
            Task.status != TaskStatus.archived
        )
        if limit:
            q = q.limit(limit)
        return q.all()
