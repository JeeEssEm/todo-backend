from passlib.context import CryptContext
from config import (SECRET_KEY, REFRESH_TOKEN_EXPIRES,
                    ACCESS_TOKEN_EXPIRES)
import datetime as dt
import jwt

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
ALGORITHM = 'HS256'


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(pwd, hashed_pwd):
    return pwd_context.verify(pwd, hashed_pwd)


def generate_token(user_id, exp, token_type):
    return jwt.encode({
        'id': user_id,
        'type': token_type,
        'exp': exp
    }, algorithm=ALGORITHM, key=SECRET_KEY)


def create_tokens(user_id):
    access_token = generate_token(
        user_id,
        dt.datetime.utcnow() + dt.timedelta(minutes=ACCESS_TOKEN_EXPIRES),
        'access'
    )
    refresh_token = generate_token(
        user_id,
        dt.datetime.utcnow() + dt.timedelta(days=REFRESH_TOKEN_EXPIRES),
        'refresh'
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def decode_token(token):
    return jwt.decode(
        token, algorithms=[ALGORITHM],
        key=SECRET_KEY
    )


def is_valid_token(token, user):
    try:
        decode_token(token)
        date = user.token_date_valid
        if date is not None and date < dt.datetime.utcnow():
            return False
        return True
    except Exception:
        return False
