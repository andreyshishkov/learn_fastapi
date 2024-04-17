from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models import User


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={'error': str(exc)}
    )


@app.post('/user')
async def get_user(user: User):
    return user
