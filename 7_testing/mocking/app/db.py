from fastapi import HTTPException, status
from .models import User


USER_DB: dict[str, User] = {}


def check_user_in_db(user: User) -> bool:
    for db_user in USER_DB.values():
        if user.name == db_user.name or user.email == db_user.email:
            return True
    return False


def create_user(user: User) -> User:
    if check_user_in_db(user):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Name or email are already taken',
        )
    USER_DB[user.name] = user
    return user


def get_user(username: str) -> User | None:
    if username not in USER_DB.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User is not found'
        )
    return USER_DB.get(username)


def delete_user(username: str) -> None:
    if username not in USER_DB.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User is not found'
        )
    del USER_DB[username]
