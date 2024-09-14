import sqlalchemy.orm
import sqlalchemy
from models import Base
from teams.models import UsersTeams


class User(Base):
    __tablename__ = 'User'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           index=True, autoincrement=True, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    teams = sqlalchemy.orm.relationship('Team', secondary=UsersTeams,
                                        back_populates='users')
