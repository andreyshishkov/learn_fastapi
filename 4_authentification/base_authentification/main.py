from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import User


app = FastAPI()
security = HTTPBasic()


user_db = [User(username='user1', password='123'), User(username='user2', password='456')]


def get_user(username: str):
    for user in user_db:
        if user.username == username:
            return user
    return None


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user(credentials.username)
    if not user or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid credentials',
            headers={'WWW-Authenticate': 'Basic'}
        )
    return user


@app.get('/login')
async def login(user: User = Depends(authenticate_user)):
    return {'message': 'You are welcome!'}
