from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse


app = FastAPI()


@app.get('/')
async def index():
    return HTMLResponse('<p>Привет</p>')


@app.get('/headers')
async def get_headers(request: Request):
    user_agent = request.headers.get('User-agent')
    accept_language = request.headers.get('Accept-Language')

    if not user_agent or accept_language:
        raise HTTPException(status_code=400, detail='You have not requested headers')

    return {
        'user-agent': user_agent,
        'accept-language': accept_language,
    }
