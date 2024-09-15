from sqlalchemy.orm import Session
from core.security import get_password_hash
from models import User
from tasks.models import Task, TaskStatus
import sqlalchemy
import datetime as dt


class UserCRUD:
    @staticmethod
    async def get_user_by_id(session: Session, user_id: int):
        return session.query(User).filter(User.id == user_id).first()

    @staticmethod
    async def create_user(session: Session, email: str, username: str,
                          password: str):
        user = User(email=email, username=username,
                    password=get_password_hash(password))
        session.add(user)
        session.commit()

    @staticmethod
    async def get_user_by_username(session: Session, username: str):
        return session.query(User).filter(User.username == username).first()

    @staticmethod
    async def get_user_by_email(session: Session, email: str):
        return session.query(User).filter(User.email == email).first()

    @staticmethod
    async def get_user_by_username_or_email(session: Session, data: str):
        return session.query(User).filter(sqlalchemy.or_(
            User.email == data, User.username == data
        )).first()

    @staticmethod
    async def check_email_username_available(session: Session, email: str,
                                             username: str):
        return session.query(User).filter(sqlalchemy.or_(
            User.username == username, User.email == email)
        ).first()

    @staticmethod
    async def change_password(session: Session, password: str, user):
        user.password = get_password_hash(password)
        user.token_date_valid = dt.datetime.utcnow()
        session.add(user)
        session.commit()

    @staticmethod
    async def get_user_xp(session: Session, user_id: int, team_id: int = None):
        q = session.query(sqlalchemy.sql.func.sum(Task.xp)).filter(
            Task.attendant_id == user_id  # noqa
        ).filter(Task.status == TaskStatus.done)
        if team_id:
            q = q.filter(Task.team_id == team_id)
        res = q.scalar()

        if not res:
            res = 0
        return res

    @staticmethod
    async def get_user_image_path(session: Session, user_id: int):
        return (await UserCRUD.get_user_by_id(session, user_id)).image
