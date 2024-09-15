import pydantic
import typing

T = typing.TypeVar('T')


class PageResponseModel(pydantic.BaseModel, typing.Generic[T]):
    total: int
    page: int
    results: typing.List[T]
