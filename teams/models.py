from models import Base
import sqlalchemy
import enum


class Rights(enum.Enum):
    admin = 'admin'
    member = 'member'


UsersTeams = sqlalchemy.Table(
    'UsersTeams',
    Base.metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True,
                      index=True, autoincrement=True, nullable=False),
    sqlalchemy.Column('user_id',
                      sqlalchemy.Integer, sqlalchemy.ForeignKey('User.id')),
    sqlalchemy.Column('team_id',
                      sqlalchemy.Integer, sqlalchemy.ForeignKey('Team.id')),
    sqlalchemy.Column('rights', sqlalchemy.Enum(Rights))
)


class Team(Base):
    __tablename__ = 'Team'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           index=True, autoincrement=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    owner_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('User.id'))

    owner = sqlalchemy.orm.relationship('User')
    members = sqlalchemy.orm.relationship('User', secondary=UsersTeams,
                                          back_populates='teams')
    tasks = sqlalchemy.orm.relationship('Task')
