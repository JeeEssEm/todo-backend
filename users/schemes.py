import pydantic


class UserScheme(pydantic.BaseModel):
    username: str
    id: int
    email: str
