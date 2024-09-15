from auth.views import router as auth_router
from users.views import router as users_router
from tasks.views import router as tasks_router
from teams.views import router as teams_router
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from core.exceptions import errors_handler

app = fastapi.FastAPI(exception_handlers={
    fastapi.exceptions.RequestValidationError: errors_handler,
    ValueError: errors_handler
}, title='Тудушлёп API', version='0.1')
app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(users_router, prefix='/users', tags=['users'])
app.include_router(tasks_router, prefix='/tasks', tags=['tasks'])
app.include_router(teams_router, prefix='/teams', tags=['teams'])

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*']
)
