from fastapi import FastAPI
from routes.login import auth
from routes.resources import resource


app = FastAPI()
app.include_router(auth)
app.include_router(resource)
