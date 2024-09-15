import fastapi
from typing import Annotated
from users.models import User
from users.utils import get_current_user
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
        limit: int = 10
):
    if TeamCRUD.check_user_in_team(db, current_user.id, team_id):
        tasks = await TeamCRUD.get_paginated_tasks(db, team_id, page, limit)
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

# TODO: kick user
# TODO: get team users
# TODO: make admin
# TODO: remove admin
# TODO: make owner
