from fastapi import FastAPI, status
from .models import User
from app import db


app = FastAPI()


@app.post('/create_user', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    response_user = db.create_user(user)
    return response_user


@app.get('/get_user/{username}', response_model=User, status_code=status.HTTP_200_OK)
async def get_user(username: str):
    return db.get_user(username)


@app.delete('/delete_user/{username}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(username: str):
    db.delete_user(username)
