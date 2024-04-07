from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import jwt
from datetime import datetime, timedelta

from security.pwd_crypt import verify_password
from models.models import User, AuthUser, Role
from db.db import get_user
from config import EXPIRATION_TIME_MINUTES, SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def authenticate_user(username: str, password: str) -> User | None:
    db_user = get_user(username)
    if db_user is None or not verify_password(password, db_user.password):
        return None
    return db_user


def get_exp() -> datetime:
    return datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME_MINUTES)


def create_jwt_token(user:  User) -> str:
    data = {
        'sub': user.username,
        'role': user.role.name,
        'exp': get_exp(),
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_auth_user_from_token(token: str = Depends(oauth2_scheme)) -> AuthUser:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return AuthUser(username=payload.get('sub'), role=Role[payload.get('role')])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Expired token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
