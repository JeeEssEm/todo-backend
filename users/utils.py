import fastapi
from typing import Annotated
import core.security
from .crud import UserCRUD
from sqlalchemy.orm import Session
from core.db import get_db
from .schemes import UserScheme

oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl='auth/login')


async def get_current_user(
        token: Annotated[str, fastapi.Depends(oauth2_scheme)],
        db: Annotated[Session, fastapi.Depends(get_db)]
):
    try:
        data = core.security.decode_token(token)
        user = UserCRUD.get_user_by_id(db, data.get('id'))

        if core.security.is_valid_token(token, user):
            return user
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
