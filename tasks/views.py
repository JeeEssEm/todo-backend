import json
import fastapi
from users.utils import get_current_user
from typing import Annotated
from users.models import User
from tasks.crud import TaskCRUD
from tasks.models import TaskStatus, TaskImportance
from core.responses import Response
from sqlalchemy.orm import Session
from core.db import get_db
from .schemes import TaskScheme, TaskForm
from users.schemes import UserScheme
from teams.crud import TeamCRUD
from .utils import task_json_converter

router = fastapi.APIRouter()


@router.get('/index')
async def index(
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        db: Annotated[Session, fastapi.Depends(get_db)]
):
    tasks = {'teams': current_user.teams,
             'personal': (await TaskCRUD.get_personal_tasks(
                 db, current_user.id, 1, 3)).results,
             'analytics': []}
    return Response(teams=tasks)


@router.get('/groups')
async def groups(
        current_user: Annotated[User, fastapi.Depends(get_current_user)]
):
    tasks = {team.title: team.tasks[:3] for team in current_user.teams}
    return Response(tasks=tasks)


@router.get('/{task_id:int}')
async def get_task(
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        db: Annotated[Session, fastapi.Depends(get_db)],
        task_id: int):
    if await TaskCRUD.check_user_can_see(db, current_user.id, task_id):
        task = await TaskCRUD.get_task_by_id(db, task_id)
        date = None
        if task.reminder is not None:
            date = task.reminder.timestamp()
        attendant = task.attendant

        return Response(task=TaskScheme(
            title=task.title,
            description=task.description,
            task_importance=task.importance,
            task_status=task.status,
            reminder=date,
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
        form: Annotated[TaskForm, fastapi.Form()],
        team_id: int = None):
    attendant_id = None
    xp = 10
    if team_id is not None:
        if not (await TeamCRUD.check_admin_in_team(
                db, team_id, current_user.id)):
            raise fastapi.exceptions.HTTPException(
                status_code=fastapi.status.HTTP_403_FORBIDDEN,
                detail='Not enough rights!'
            )
        else:
            xp = form.xp
            attendant_id = form.attendant_id
    else:
        attendant_id = current_user.id

    await TaskCRUD.create_task(
        db, title=form.title, description=form.description,
        reminder=form.reminder, task_status=form.task_status,
        task_importance=form.task_importance, user_id=attendant_id,
        team_id=team_id, xp=xp
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
            task.xp = form.xp or task.xp
            task.attendant_id = form.attendant_id or task.attendant_id

    task.title = form.title or task.title
    task.description = form.description or task.description
    task.status = form.task_status or task.status
    task.importance = form.task_importance or task.importance
    task.reminder = form.reminder or task.reminder
    db.add(task)
    db.commit()
    return Response(message='Task edited')


@router.delete('/{task_id:int}')
async def delete_task(
        task_id: int,
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        db: Annotated[Session, fastapi.Depends(get_db)]
):
    task = await TaskCRUD.get_task_by_id(db, task_id)
    if task is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )
    if task.team_id is None and task.attendant_id == current_user.id:
        task.delete()
        db.commit()
        return Response(message='Task deleted successfully')
    if TeamCRUD.check_admin_in_team(db, task.team_id, current_user.id):
        task.delete()
        db.commit()
        return Response(message='Task deleted successfully')

    raise fastapi.exceptions.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail='Not enough rights!'
    )


@router.get('')
async def get_personal_tasks(
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        db: Annotated[Session, fastapi.Depends(get_db)],
        page: int,
        limit: int = 10,
        status: TaskStatus = None,
        importance: TaskImportance = None,
        ):
    tasks = await TaskCRUD.get_paginated_personal_tasks(
        db, current_user.id, page, limit, status=status, importance=importance
    )

    return Response(tasks=tasks)


@router.get('/export')
async def export_data(
    current_user: Annotated[User, fastapi.Depends(get_current_user)],
    db: Annotated[Session, fastapi.Depends(get_db)],
    team_id: int = None
):
    if team_id:
        if not await TeamCRUD.check_admin_in_team(db, team_id, current_user.id):
            raise fastapi.exceptions.HTTPException(
                status_code=fastapi.status.HTTP_403_FORBIDDEN,
                detail='Not enough rights!'
            )
    tasks = await TaskCRUD.get_all_tasks(db, current_user.id, team_id)
    return [await task_json_converter(task) for task in tasks]


@router.post('/import')
async def import_data(
    current_user: Annotated[User, fastapi.Depends(get_current_user)],
    db: Annotated[Session, fastapi.Depends(get_db)],
    data: fastapi.UploadFile,
    team_id: int = None
):
    if team_id:
        if not await TeamCRUD.check_admin_in_team(db, team_id, current_user.id):
            raise fastapi.exceptions.HTTPException(
                status_code=fastapi.status.HTTP_403_FORBIDDEN,
                detail='Not enough rights!'
            )
    try:
        await TaskCRUD.load_tasks_from_json(
            db, current_user.id,
            json.loads((await data.read()).decode()),
            team_id
        )
        return Response(message='Tasks loaded successfully!')
    except Exception:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Oops, something went wrong... The data in the downloaded '
                   'file may be corrupted. '
        )
