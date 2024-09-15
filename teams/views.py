import fastapi
from typing import Annotated
from users.models import User
from users.utils import get_current_user
from tasks.models import TaskImportance, TaskStatus
from .crud import TeamCRUD
from core.db import get_db
from core.responses import Response
from sqlalchemy.orm import Session
from .utils import generate_invite_link, decode_invite_link

router = fastapi.APIRouter()


@router.post('/')
async def create_team(
        title: str,
        db: Annotated[Session, fastapi.Depends(get_db)],
        current_user: Annotated[User, fastapi.Depends(get_current_user)]
):
    await TeamCRUD.create_team(db, current_user, title)
    return Response(message='Team created successfully!')


@router.put('/{team_id:int}')
async def edit_team(
        team_id: int,
        title: str,
        db: Annotated[Session, fastapi.Depends(get_db)],
        current_user: Annotated[User, fastapi.Depends(get_current_user)]
):
    if TeamCRUD.check_admin_in_team(db, team_id, current_user.id):
        await TeamCRUD.edit_team_title(db, team_id, title)
        return Response(message='Title changed successfully!')

    raise fastapi.exceptions.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail='Not enough rights!'
    )


@router.get('/{team_id:int}/tasks')
async def get_team_tasks(
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        db: Annotated[Session, fastapi.Depends(get_db)],
        team_id: int,
        page: int,
        limit: int = 10,
        status: TaskStatus = None,
        importance: TaskImportance = None,
        attendant_id: int = None
):
    if TeamCRUD.check_user_in_team(db, current_user.id, team_id):
        tasks = await TeamCRUD.get_paginated_tasks(db, team_id, page, limit,
                                                   status, importance,
                                                   attendant_id)
        return Response(tasks=tasks)

    raise fastapi.exceptions.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail='You are not a member of this team!'
    )


@router.get('/')
async def get_mine_teams(
    current_user: Annotated[User, fastapi.Depends(get_current_user)]
):
    return Response(current_user.teams)


@router.get('/invite-link/{team_id:int}')
async def create_invite_link(
        team_id: int,
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        db: Annotated[Session, fastapi.Depends(get_db)],
        request: fastapi.requests.Request
):
    if await TeamCRUD.check_admin_in_team(db, team_id, current_user.id):
        link = await generate_invite_link(team_id)
        url = str(request.url).split('/teams/')[0] + f'/teams/join?link={link}'
        return Response(url)
    raise fastapi.exceptions.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail='Not enough rights!'
    )


@router.get('/join')
async def join_team(
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        db: Annotated[Session, fastapi.Depends(get_db)],
        link: str
):
    try:
        data = await decode_invite_link(link)
        await TeamCRUD.add_user_to_team(db, data.get('team_id'), current_user.id)
        return Response(message='User successfully joined the team!')

    except Exception:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Oops, something went wrong...'
        )


@router.get('/{team_id:int}/members')
async def get_team_members(
    team_id: int,
    page: int,
    limit: int,
    db: Annotated[Session, fastapi.Depends(get_db)],
    current_user: Annotated[User, fastapi.Depends(get_current_user)],
):
    if await TeamCRUD.check_user_in_team(db, current_user.id, team_id):
        members = await TeamCRUD.get_paginated_members(db, team_id, page, limit)
        return Response(members)

    raise fastapi.exceptions.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail='Not enough rights!'
    )


@router.post('/{team_id:int}/kick/{user_id:int}')
async def kick_user(
        team_id: int,
        user_id: int,
        db: Annotated[Session, fastapi.Depends(get_db)],
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
):
    if await TeamCRUD.check_admin_in_team(db, team_id, current_user.id):
        await TeamCRUD.kick_user(db, team_id, user_id)
        return Response(message='User kicked')

    raise fastapi.exceptions.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail='Not enough rights!'
    )


@router.post('/{team_id:int}/make-admin/{user_id:int}')
async def make_admin(
        db: Annotated[Session, fastapi.Depends(get_db)],
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        team_id: int,
        user_id: int
):
    team = await TeamCRUD.get_team_by_id(db, team_id)
    if team is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail='Team not found'
        )
    if team.owner_id == current_user.id:
        await TeamCRUD.make_admin(db, team_id, user_id)
        return Response(message='User is admin now')

    raise fastapi.exceptions.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail='Not enough rights!'
    )


@router.post('/{team_id:int}/make-member/{user_id:int}')
async def make_member(
        db: Annotated[Session, fastapi.Depends(get_db)],
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        team_id: int,
        user_id: int
):
    team = await TeamCRUD.get_team_by_id(db, team_id)
    if team is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail='Team not found'
        )
    if team.owner_id == current_user.id:
        await TeamCRUD.make_member(db, team_id, user_id)
        return Response(message='User is member now')

    raise fastapi.exceptions.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail='Not enough rights!'
    )


@router.post('/{team_id:int}/make-owner/{user_id:int}')
async def make_owner(
        db: Annotated[Session, fastapi.Depends(get_db)],
        current_user: Annotated[User, fastapi.Depends(get_current_user)],
        team_id: int,
        user_id: int
):
    team = await TeamCRUD.get_team_by_id(db, team_id)
    if team is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail='Team not found'
        )
    if team.owner_id == current_user.id:
        await TeamCRUD.make_owner(db, team_id, user_id)
        return Response(message='User is owner now')

    raise fastapi.exceptions.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail='Not enough rights!'
    )
