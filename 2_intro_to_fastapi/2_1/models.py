from pydantic import BaseModel


class CalcRequest(BaseModel):
    num1: int
    num2: int


class User(BaseModel):
    id: int
    name: str


class UserAgeRequest(BaseModel):
    name: str
    age: int


class FeedBack(BaseModel):
    name: str
    message: str

