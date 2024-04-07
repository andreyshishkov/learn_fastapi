from pydantic import BaseModel
from enum import Enum
from typing import Optional


class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'


class User(BaseModel):
    username: str
    password: str
    role: Role


class AuthUser(BaseModel):
    username: str
    role: Role


class AuthRequest(BaseModel):
    username: str
    password: str
