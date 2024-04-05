from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import UserLogin
from passlib.hash import pbkdf2_sha256
import jwt


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


ALGORITHM = 'HS256'
SECRET_KEY = '123456'
TOKEN_EXPIRE_TIME = 3

USER_DATA = [
    UserLogin(**{"username": "Egor", "password": pbkdf2_sha256.hash("egor1234")}),
    UserLogin(**{"username": "Vasya", "password": pbkdf2_sha256.hash("vasya1234")}),
]


def get_user(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None


def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_TIME)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Expire token',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        )


@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    for user in USER_DATA:
        if user.username == username and pbkdf2_sha256.verify(password, user.password):
            access_token = create_jwt_token(data={'sub': username})
            return {'access_token': access_token, 'token_type': 'bearer'}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid login or password',
        headers={'WWW-Authenticate': 'Bearer'}
    )


@app.get('/protected_resource')
async def get_protected_resource(current_user: str = Depends(get_user_from_token)):
    user = get_user(current_user)
    if user:
        return user
    return {'error': 'User is not founded'}
