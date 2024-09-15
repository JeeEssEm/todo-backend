import fastapi
from users.utils import get_current_user
from typing import Annotated
from users.models import User
from tasks.crud import TaskCRUD
from core.responses import Response
from sqlalchemy.orm import Session
from core.db import get_db
from .schemes import TaskScheme, TaskForm
from users.schemes import UserScheme
from teams.crud import TeamCRUD

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


@router.get('/{task_id:int}')
async def get_task(
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        db: Annotated[Session, fastapi.Depends(get_db)],
        task_id: int):
    if await TaskCRUD.check_user_can_see(db, current_user.id, task_id):
        task = await TaskCRUD.get_task_by_id(db, task_id)
        attendant = task.attendant
        return Response(task=TaskScheme(
            title=task.title,
            description=task.description,
            task_importance=task.importance,
            task_status=task.status,
            reminder=task.reminder,
            attendant=UserScheme(
                username=attendant.username,
                email=attendant.email,
                id=attendant.id
            )
        ))

    raise fastapi.exceptions.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail='Not enough rights!'
    )


@router.post('/create_task')
async def create_task(
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        db: Annotated[Session, fastapi.Depends(get_db)],
        form: Annotated[TaskForm, fastapi.Depends()],
        team_id: int = None):
    attendant_id = None
    if team_id is not None:
        if not (await TeamCRUD.check_admin_in_team(
                db, team_id, current_user.id)):
            # TODO: different configs in teams
            raise fastapi.exceptions.HTTPException(
                status_code=fastapi.status.HTTP_403_FORBIDDEN,
                detail='Not enough rights!'
            )
        else:
            attendant_id = form.attendant_id
    else:
        attendant_id = current_user.id

    await TaskCRUD.create_task(
        db, title=form.title, description=form.description,
        reminder=form.reminder, task_status=form.task_status,
        task_importance=form.task_importance, user_id=attendant_id,
        team_id=team_id
    )
    return Response(message='Task created successfully!')


@router.put('/{task_id:int}')
async def edit_task(
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        db: Annotated[Session, fastapi.Depends(get_db)],
        form: Annotated[TaskForm, fastapi.Depends()],
        task_id: int):
    task = await TaskCRUD.get_task_by_id(db, task_id)
    if task.team_id is not None:
        if not (await TeamCRUD.check_admin_in_team(
                db, task.team_id, current_user.id)):
            raise fastapi.exceptions.HTTPException(
                status_code=fastapi.status.HTTP_403_FORBIDDEN,
                detail='Not enough rights!'
            )
        else:
            task.attendant_id = form.attendant_id or task.attendant_id

    task.title = form.title or task.title
    task.description = form.description or task.description
    task.status = form.task_status or task.status
    task.importance = form.task_importance or task.importance
    task.reminder = form.reminder or task.reminder
    db.add(task)
    db.commit()
    return Response(message='Task edited')


@router.get('')
async def get_personal_tasks(
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        db: Annotated[Session, fastapi.Depends(get_db)],
        page: int,
        limit: int = 10
        ):
    tasks = await TaskCRUD.get_personal_tasks(db, current_user.id, page, limit)
    return Response(tasks=tasks)


@router.post('/attend/{task_id}')
async def attend_to_task():
    # TODO: ?
    ...
