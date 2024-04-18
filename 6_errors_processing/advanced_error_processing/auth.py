from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from exceptions import UserNotFoundException, InvalidUserDataException
from models import User
from security import verify_password, hash_password
from db import get_user_from_db, USER_DATA


router = APIRouter()
security = HTTPBasic()


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or not verify_password(credentials.password, user.password):
        raise UserNotFoundException()
    return user


@router.get('/login_user')
async def login(user: User = Depends(authenticate_user)):
    return {'message': 'You are success'}


@router.post('/reg_user')
async def reg_user(user_data: User):
    if len(user_data.password) < 5 or len(user_data.username) < 5:
        raise InvalidUserDataException()
    USER_DATA.append(User(username=user_data.username, password=hash_password(user_data.password)))
    return {'message': 'Success'}
