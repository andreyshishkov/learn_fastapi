from fastapi import APIRouter, Depends, HTTPException, status
from models.models import AuthUser, Role
from security.security import get_auth_user_from_token


resource = APIRouter()


@resource.get('/admin')
async def get_admin_data(auth_user: AuthUser = Depends(get_auth_user_from_token)) -> dict:
    if auth_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized',
        )
    return {'message': f'Hi, {auth_user.username}'}


@resource.get('/user')
async def get_user_data(auth_user: AuthUser = Depends(get_auth_user_from_token)) -> dict:
    if auth_user.role not in (Role.ADMIN, Role.USER):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized'
        )
    return {'message': 'user data'}


@resource.get('/info')
async def get_info(auth_user: AuthUser = Depends(get_auth_user_from_token)) -> dict:
    return {'message': 'Common data'}
