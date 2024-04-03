from fastapi import FastAPI, Cookie, Response, Request
from models import UserLogin
import uuid


app = FastAPI()

users_db = [UserLogin(username="vasya", password="31maet"), UserLogin(username="masha", password="qwerty")]


def generate_token():
    return uuid.uuid4()


@app.post('/login')
async def login_user(user: UserLogin, response: Response):
    for us in users_db:
        if us.username == user.username and us.password == user.password:
            token = str(generate_token())
            us.token = str(token)
            response.set_cookie(key='session_token', value=token, httponly=True)
            return {'message': 'Login is successful'}
    return {'message': 'Invalid credentials'}


@app.get('/user')
async def get_user(request: Request):
    session_token = request.cookies.get('session_token')
    for user in users_db:
        if session_token is not None and user.token == session_token:
            return {'username': user.username}
    return {'message': 'Invalid session'}



