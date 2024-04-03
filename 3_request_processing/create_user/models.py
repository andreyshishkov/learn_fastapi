from pydantic import BaseModel, EmailStr, PositiveInt


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: PositiveInt | None
    is_subscribed: bool | None


