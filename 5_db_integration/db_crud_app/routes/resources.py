from fastapi import APIRouter

from models.models import CreateToDoRequest, UpdateToDoRequest, ToDo
from db import create_todo, get_todo, update_todo, delete_todo


to_dos = APIRouter(prefix='/todos')


@to_dos.post('/', response_model=ToDo)
async def create(todo: CreateToDoRequest):
    result = await create_todo(todo)
    return result


@to_dos.get('/{todo_id}', response_model=ToDo)
async def read(todo_id: int):
    result = await get_todo(todo_id)
    return result


@to_dos.put('/{todo_id}', response_model=ToDo)
async def update(todo_id: int, todo: UpdateToDoRequest):
    result = await update_todo(todo_id, todo)
    return result


@to_dos.delete('/{todo_id}', response_model=dict)
async def delete(todo_id: int):
    await delete_todo(todo_id)
    return {'message': 'Delete is successful'}
