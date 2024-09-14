from auth.views import router as auth_router
from users.views import router as users_router
import fastapi
from core.exceptions import errors_handler

app = fastapi.FastAPI(exception_handlers={
    fastapi.exceptions.RequestValidationError: errors_handler,
    ValueError: errors_handler
})
app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(users_router, prefix='/users', tags=['users'])
