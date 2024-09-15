from config import SECRET_KEY
import jwt
ALGORITHM = 'HS256'


async def generate_invite_link(team_id: int):
    return jwt.encode({
        'team_id': team_id
    }, key=SECRET_KEY, algorithm=ALGORITHM)


async def decode_invite_link(token: str):
    return jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
