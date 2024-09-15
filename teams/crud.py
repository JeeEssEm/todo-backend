import sqlalchemy
from users.models import User
from teams.models import UsersTeams, Team, Rights
from pagination.pagination import paginate
from tasks.models import Task, TaskStatus
from tasks.utils import task_scheme_converter
from users.utils import user_scheme_converter


class TeamCRUD:
    @staticmethod
    async def create_team(session: sqlalchemy.orm.Session, owner: User,
                          title: str):
        team = Team(title=title, owner_id=owner.id)
        session.add(team)
        session.commit()
        session.refresh(team)
        q = UsersTeams.insert().values(
            user_id=owner.id, team_id=team.id, rights=Rights.admin
        )
        session.execute(q)
        session.commit()

    @staticmethod
    async def check_user_in_team(session: sqlalchemy.orm.Session,
                                 user_id: int, team_id: int):
        return session.query(UsersTeams).filter(
            UsersTeams.c.user_id == user_id
        ).filter(UsersTeams.c.team_id == team_id).count() != 0

    @staticmethod
    async def get_paginated_tasks(session: sqlalchemy.orm.Session, team_id: int,
                                  page: int, limit: int):
        q = session.query(Task).filter(Task.team_id == team_id).filter(
            Task.status != TaskStatus.archived
        )
        return await paginate(
            page, q, task_scheme_converter, limit
        )

    @staticmethod
    async def check_admin_in_team(session: sqlalchemy.orm.Session, team_id: int,
                                  user_id: int):
        user = session.query(UsersTeams).filter(
            UsersTeams.c.user_id == user_id
        ).filter(UsersTeams.c.team_id == team_id).first()
        return (user is not None) and (user.rights == Rights.admin)

    @staticmethod
    async def get_team_by_id(session: sqlalchemy.orm.Session, team_id: int):
        return session.query(Team).filter(Team.id == team_id).first()

    @staticmethod
    async def edit_team_title(session: sqlalchemy.orm.Session, team_id: int,
                              title: str):
        team = TeamCRUD.get_team_by_id(session, team_id)
        team.title = title
        session.add(team)
        session.commit()

    @staticmethod
    async def add_user_to_team(session: sqlalchemy.orm.Session, team_id: int,
                               user_id: int):
        q = UsersTeams.insert().values(
            user_id=user_id, team_id=team_id, rights=Rights.member
        )
        session.execute(q)
        session.commit()

    @staticmethod
    async def get_paginated_members(session: sqlalchemy.orm.Session,
                                    team_id: int, page: int, limit: int):
        q = session.query(UsersTeams, User).filter(
            UsersTeams.c.team_id == team_id
        ).filter(User.id == UsersTeams.c.user_id)
        return await paginate(page, q, user_scheme_converter, limit)

    @staticmethod
    async def kick_user(session: sqlalchemy.orm.Session, team_id: int,
                        user_id: int):
        q = UsersTeams.delete().where(
            UsersTeams.c.team_id == team_id
        ).where(UsersTeams.c.user_id == user_id)
        session.execute(q)
        session.commit()

    @staticmethod
    async def make_admin(session: sqlalchemy.orm.Session, team_id: int,
                         user_id: int):
        q = UsersTeams.update().where(
            UsersTeams.c.team_id == team_id
        ).where(UsersTeams.c.user_id == user_id).values(rights=Rights.admin)
        session.execute(q)
        session.commit()

    @staticmethod
    async def make_member(session: sqlalchemy.orm.Session, team_id: int,
                          user_id: int):
        q = UsersTeams.update().where(
            UsersTeams.c.team_id == team_id
        ).where(UsersTeams.c.user_id == user_id).values(rights=Rights.member)
        session.execute(q)
        session.commit()

    @staticmethod
    async def make_owner(session: sqlalchemy.orm.Session, team_id: int,
                         user_id: int):
        team = await TeamCRUD.get_team_by_id(session, team_id)
        team.owner_id = user_id
        session.add(team)
        session.commit()
