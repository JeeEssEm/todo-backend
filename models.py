import sqlalchemy.orm


class Base(sqlalchemy.orm.DeclarativeBase):
    pass


from teams.models import *  # noqa
from users.models import *  # noqa
from tasks.models import *  # noqa
