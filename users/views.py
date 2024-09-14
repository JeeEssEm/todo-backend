import fastapi
from typing import Annotated
import models
from .utils import get_current_user
from core.responses import Response


router = fastapi.APIRouter()


@router.get('/whoami')
def whoami(current_user: Annotated[models.User,
                                   fastapi.Depends(get_current_user)]):
    return Response(
        current_user
    )
