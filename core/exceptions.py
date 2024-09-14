import fastapi


async def errors_handler(request, exception):
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=exception.errors()[0]['msg']
    )
