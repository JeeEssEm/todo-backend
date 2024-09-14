from models import Base
import sqlalchemy
import enum


class TaskStatus(enum.Enum):
    planning = 'planning'
    running = 'running'
    done = 'done'
    archived = 'archived'


class TaskImportance(enum.IntEnum):
    regular = 1
    important = 2
    extremely_important = 3


TasksTeams = sqlalchemy.Table(
    'TasksTeams',
    Base.metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True,
                      index=True, autoincrement=True, nullable=False),
    sqlalchemy.Column('task_id',
                      sqlalchemy.Integer, sqlalchemy.ForeignKey('Task.id')),
    sqlalchemy.Column('team_id',
                      sqlalchemy.Integer, sqlalchemy.ForeignKey('Team.id')),
)


class Task(Base):
    __tablename__ = 'Task'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           index=True, autoincrement=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text)
    status = sqlalchemy.Column(sqlalchemy.Enum, nullable=False)
    importance = sqlalchemy.Column(sqlalchemy.Enum, nullable=False)
    reminder = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)

    attendant_id = sqlalchemy.Column(sqlalchemy.Integer,
                                     sqlalchemy.ForeignKey('User.id'),
                                     nullable=True)
    attendant = sqlalchemy.orm.relationship('User')
