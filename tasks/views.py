import fastapi
from users.utils import get_current_user
from typing import Annotated
from users.models import User
from tasks.crud import TaskCRUD
from core.responses import Response
from sqlalchemy.orm import Session
from core.db import get_db

router = fastapi.APIRouter()


@router.get('/index')
async def index(
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        db: Annotated[Session, fastapi.Depends(get_db)]
):
    tasks = {team.title: team.tasks[:3] for team in current_user.teams}
    tasks['personal'] = await TaskCRUD.get_personal_tasks(db,
                                                          current_user.id, 3)
    return Response(teams=tasks)
