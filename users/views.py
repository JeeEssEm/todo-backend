import fastapi
from typing import Annotated
import models
from .crud import UserCRUD
from .utils import get_current_user
from core.responses import Response
from sqlalchemy.orm import Session
from core.db import get_db
from .schemes import UserScheme

router = fastapi.APIRouter()


@router.get('/whoami')
async def whoami(current_user: Annotated[models.User,
                                         fastapi.Depends(get_current_user)]):
    return Response(
        current_user
    )


@router.get('/{user_id:int}')
async def get_user(
        user_id: int,
        db: Annotated[Session, fastapi.Depends(get_db)]
):
    user = await UserCRUD.get_user_by_id(db, user_id)
    if not user:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail='User does not exist'
        )
    return Response(user=UserScheme(
        username=user.username,
        email=user.email,
        id=user.id
    ))


@router.get('/image/{user_id:int}')
async def get_user_image():
    ...


@router.post('/load_image')
async def load_user_image():
    ...
