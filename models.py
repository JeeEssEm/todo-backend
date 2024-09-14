import sqlalchemy.orm


class Base(sqlalchemy.orm.DeclarativeBase):
    pass


from teams.models import *
from users.models import *
from tasks.models import *
