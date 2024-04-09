from databases import Database
from fastapi import HTTPException

from config import Config, load_config
from models.models import ToDo, CreateToDoRequest, UpdateToDoRequest


config: Config = load_config()
database = Database(config.db_url)


async def create_todo(todo_request: CreateToDoRequest) -> ToDo:
    query = """
    INSERT INTO todo_list (title, description, completed)
    VALUES (:title, :description, :completed) 
    RETURNING id; 
    """
    values = {'title': todo_request.title, 'description': todo_request.description, 'completed': False}
    try:
        todo_id = await database.execute(query=query, values=values)
        return ToDo(**todo_request.model_dump(), id=todo_id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Fail to create todo')


async def get_todo(todo_id: int) -> ToDo:
    query = """
    SELECT * FROM todo_list WHERE id=:todo_id;
    """
    values = {'todo_id': todo_id}
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception:
        raise HTTPException(status_code=500, detail='Fail to fetch from database')
    if result:
        return ToDo(
            title=result['title'],
            description=result['description'],
            completed=result['completed'],
            id=result['id'],
        )
    else:
        raise HTTPException(
            status_code=404,
            detail='ToDo is not found'
        )


async def update_todo(todo_id: int, todo: UpdateToDoRequest):
    query = """
    UPDATE todo_list
    SET title=:title, description=:description, completed=:completed
    WHERE id=:todo_id
    RETURNING id;
    """
    values = {
        'title': todo.title,
        'description': todo.description,
        'completed': todo.completed,
        'todo_id': todo_id,
    }

    try:
        result = await database.execute(query=query, values=values)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Fail to update',
        )

    if result:
        return ToDo(**todo.model_dump(), id=todo_id)
    else:
        raise HTTPException(
            status_code=404,
            detail='ToDo not found',
        )


async def delete_todo(todo_id: int) -> bool:
    query = """
    DELETE
    FROM todo_list
    WHERE id=:todo_id;
    RETURNING id;
    """
    values = {
        'todo_id': todo_id,
    }
    try:
        result = await database.execute(query=query, values=values)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Fail to delete',
        )
    if result:
        return True
    else:
        raise HTTPException(
            status_code=404,
            detail='Todo not found'
        )
