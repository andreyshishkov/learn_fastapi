from fastapi import FastAPI, status, HTTPException
from .models import User
from .db import USER_DATA, get_user_from_db


app = FastAPI()


@app.post('/reg_user')
async def reg_user(user: User):
    for u in USER_DATA:
        if u.username == user.username or u.email == user.email:
            raise HTTPException(
                status_code=422,
                detail='That user is already in db'
            )
    USER_DATA.append(user)
    return user


@app.get('/get_user')
async def get_user(username: str):
    user = get_user_from_db(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )
    return user


@app.delete('/delete_user/{username}')
async def delete_user(username: str):
    user = get_user_from_db(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )
    USER_DATA.remove(user)
    return {'message': 'Delete is successful'}
