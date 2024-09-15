from models import Base
import sqlalchemy
import enum


class TaskStatus(enum.Enum):
    planning = 'planning'
    running = 'running'
    done = 'done'
    archived = 'archived'
    cancelled = 'cancelled'


class TaskImportance(enum.IntEnum):
    regular = 1
    important = 2
    extremely_important = 3


class Task(Base):
    __tablename__ = 'Task'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           index=True, autoincrement=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text)
    status = sqlalchemy.Column(sqlalchemy.Enum(TaskStatus), nullable=False)
    importance = sqlalchemy.Column(sqlalchemy.Enum(TaskImportance),
                                   nullable=False)
    reminder = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)

    attendant_id = sqlalchemy.Column(sqlalchemy.Integer,
                                     sqlalchemy.ForeignKey('User.id'),
                                     nullable=True)
    team_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('Team.id'),
                                nullable=True)
    xp = sqlalchemy.Column(sqlalchemy.Integer, default=10)
    team = sqlalchemy.orm.relationship('Team', back_populates='tasks')
    attendant = sqlalchemy.orm.relationship('User', back_populates='tasks')
