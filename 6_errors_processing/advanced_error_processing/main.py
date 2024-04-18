from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime

from auth import router
from exception_model import ErrorResponseModel
from exceptions import UserNotFoundException, InvalidUserDataException


app = FastAPI()
app.include_router(router)


async def user_not_found(request: Request, exc: ErrorResponseModel):
    start = datetime.utcnow()
    return JSONResponse(
        status_code=exc.status_code,
        content={'Error': exc.detail, 'status_code': exc.status_code},
        headers={'X-ErrorHandleTime': str(datetime.utcnow() - start)}
    )


app.add_exception_handler(UserNotFoundException, user_not_found)
app.add_exception_handler(InvalidUserDataException, user_not_found)
