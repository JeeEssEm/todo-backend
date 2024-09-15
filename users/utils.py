import fastapi
from typing import Annotated
import core.security
from .crud import UserCRUD
from sqlalchemy.orm import Session
from core.db import get_db
from .schemes import UserScheme
import uuid
import os
from config import STATIC_PATH
import aiofiles

oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl='auth/login')


async def get_current_user(
        token: Annotated[str, fastapi.Depends(oauth2_scheme)],
        db: Annotated[Session, fastapi.Depends(get_db)]
):
    try:
        data = core.security.decode_token(token)
        user = await UserCRUD.get_user_by_id(db, data.get('id'))

        if core.security.is_valid_token(token, user):
            return user
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail='Token is not valid anymore'
        )
    except Exception:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail='Token expired!'
        )


async def is_authenticated(request: fastapi.Request):
    return request.headers.get('Authorization') is not None


async def user_scheme_converter(user_obj):
    user_obj = user_obj[-1]
    return UserScheme(
        username=user_obj.username,
        email=user_obj.email,
        id=user_obj.id
    )


async def generate_filename(path, ext):
    filename = str(uuid.uuid4()) + ext
    while os.path.exists(path / filename):
        filename = str(uuid.uuid4()) + ext
    return filename


async def save_image(image):
    path = STATIC_PATH / 'images'
    filename = await generate_filename(path, '.webp')
    path = path / filename
    await save_file(image, path)
    return filename


async def save_file(file, path):
    async with aiofiles.open(path, 'wb') as out:
        while content := await file.read(1024):
            await out.write(content)


async def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
