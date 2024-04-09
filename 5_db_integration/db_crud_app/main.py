from fastapi import FastAPI
from contextlib import asynccontextmanager

from db import database
from routes.resources import to_dos


@asynccontextmanager
async def lifespan(application: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(to_dos)
