import fastapi
from typing import Annotated
import models
from .crud import UserCRUD
from .utils import get_current_user, save_image, remove_file
from core.responses import Response
from sqlalchemy.orm import Session
from core.db import get_db
from .schemes import UserScheme
from config import STATIC_PATH

router = fastapi.APIRouter()


@router.get('/whoami')
async def whoami(
        current_user: Annotated[models.User,
                                fastapi.Depends(get_current_user)]):
    return Response(user=current_user)


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


@router.get('/{user_id:int}/xp')
async def get_user_xp(user_id: int,
                      db: Annotated[Session, fastapi.Depends(get_db)],
                      team_id: int = None):
    xp = await UserCRUD.get_user_xp(db, user_id, team_id)
    return Response(xp=xp)


@router.get('/media/{user_id:int}')
async def get_user_image(
        db: Annotated[Session, fastapi.Depends(get_db)],
        user_id: int):
    path = await UserCRUD.get_user_image_path(db, user_id)

    if path:
        path = STATIC_PATH / 'images' / path
        return fastapi.responses.FileResponse(path, media_type='image/webp')
    raise fastapi.exceptions.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail='User does not has image'
    )


@router.post('/media')
async def load_user_image(
    current_user: Annotated[models.User, fastapi.Depends(get_current_user)],
    db: Annotated[Session, fastapi.Depends(get_db)],
    image: fastapi.UploadFile
):
    filename = await save_image(image)
    current_user.image = filename

    db.add(current_user)
    db.commit()
    return Response(message='User image added successfully')


@router.delete('/media')
async def remove_user_image(
        current_user: Annotated[models.User, fastapi.Depends(get_current_user)],
        db: Annotated[Session, fastapi.Depends(get_db)]
):
    await remove_file(
        STATIC_PATH / 'images' / current_user.image
    )
    current_user.image = None
    db.add(current_user)
    db.commit()
    return Response(message='User image deleted')
