from core.db import get_db
from users.crud import UserCRUD
import fastapi
import core.security
from core.responses import Response
from . import schemes
from users.utils import get_current_user
from typing import Annotated
from sqlalchemy.orm import Session
from users.models import User

router = fastapi.APIRouter()


@router.post('/login')
async def login(
    response: fastapi.Response,
    form_data: Annotated[
        fastapi.security.OAuth2PasswordRequestForm,
        fastapi.Depends()],
        db: Session = fastapi.Depends(get_db)
):
    username = form_data.username
    password = form_data.password
    user = await UserCRUD.get_user_by_username_or_email(db, username)

    if user is None or not core.security.verify_password(
        password, user.password
    ):

        raise fastapi.exceptions.HTTPException(
            fastapi.status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect password or login'
        )
    tokens = core.security.create_tokens(user.id)
    response.set_cookie(key='refresh_token',
                        value=tokens['refresh_token'], httponly=True)

    return {
        'access_token': tokens['access_token'],
        'token_type': 'bearer'
    }


@router.post('/update_token')
async def update_token(request: fastapi.Request, response: fastapi.Response,
                       db: Session = fastapi.Depends(get_db)):
    refresh_token = request.cookies.get('refresh_token')

    try:
        token = core.security.decode_token(refresh_token)
        if token.get('type') != 'refresh':
            raise Exception('Invalid token')
        current_user = await get_current_user(refresh_token, db)
        tokens = core.security.create_tokens(current_user.id)
        response.headers['Authorization'] = f'Bearer {tokens["access_token"]}'
        return {
            'access_token': tokens['access_token'],
            'token_type': 'bearer'
        }
    except Exception:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token or token expired'
        )


@router.post(
    '/register'
)
async def register(
        form: Annotated[schemes.RegisterForm, fastapi.Form()],
        db: Session = fastapi.Depends(get_db)):

    if await UserCRUD.check_email_username_available(db, form.email,
                                                     form.username):
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail='User already exists!'
        )

    await UserCRUD.create_user(db, form.email, form.username, form.password)

    return Response(detail='User created successfully!')


@router.post('/reset-password')
async def reset_password(
    current_user: Annotated[User, fastapi.Depends(get_current_user)],
    db: Annotated[Session, fastapi.Depends(get_db)],
    form: Annotated[schemes.ResetPasswordForm, fastapi.Depends()]
):
    await UserCRUD.change_password(db, form.password, current_user)

    return Response(detail='Password changed successfully!')
