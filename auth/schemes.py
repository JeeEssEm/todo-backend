import pydantic
import re


class RegisterForm(pydantic.BaseModel):
    email: pydantic.EmailStr
    username: str
    password: str = pydantic.Field(min_length=8)
    repeat_password: str

    @pydantic.field_validator('repeat_password', mode='after')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('passwords do not match')
        return v

    @pydantic.field_validator('password', mode='after')
    @classmethod
    def validate_password(cls, v):
        expression = re.compile(
            '^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$'
        )
        if not expression.match(v):
            raise ValueError('''Password must contain: at least 1 uppercase 
            letter, special symbol and 1 digit''')
        return v


class ResetPasswordForm(pydantic.BaseModel):
    password: str = pydantic.Field(min_length=8)
    repeat_password: str

    @pydantic.field_validator('repeat_password', mode='after')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('passwords do not match')
        return v

    @pydantic.field_validator('password', mode='after')
    @classmethod
    def validate_password(cls, v):
        expression = re.compile(
            '^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$'
        )
        if not expression.match(v):
            raise ValueError('''Password must contain: at least 1 uppercase 
            letter, special symbol and 1 digit''')
        return v
