from models import User
from security import hash_password


USER_DATA = [
    User(**{"username": "user1", "password": hash_password("pass1")}),
    User(**{"username": "user2", "password": hash_password("pass2")}),
    User(**{"username": "user3", "password": hash_password("pass3")}),
]


def get_user_from_db(username: str) -> User | None:
    for user in USER_DATA:
        if user.username == username:
            return user
    return None

