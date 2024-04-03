from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from models import CalcRequest, User, UserAgeRequest, FeedBack


app = FastAPI()
user_info = {'id': 2, 'name': 'John'}
users = [User(**user_info)]
feedback_db = []


def get_adult_status(age: int):
    return age >= 18


@app.get('/')
async def index():
    html = Path('index.html').read_text(encoding='utf-8')
    return HTMLResponse(html)


@app.get('/users')
async def users():
    return users


@app.post('/user_is_adult')
async def is_adult(user: UserAgeRequest):
    adult_status = get_adult_status(user.age)
    data = user.model_dump()
    data['is_adult'] = adult_status
    return data


@app.post('/calculate')
async def calculate(nums: CalcRequest):
    return {'message': nums.num1 + nums.num2}


@app.post('/feedback')
async def feedback(feedback_request: FeedBack):
    try:
        feedback_db.append(
            {'name': feedback_request.name, 'message': feedback_request.message}
        )
        return 'Success'
    except:
        return 'Oops! Some error, make another attempt'
