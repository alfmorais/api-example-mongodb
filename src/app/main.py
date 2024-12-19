from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.users.views import router
from src.database.database import DatabaseUtils


@asynccontextmanager
async def lifespan(app: FastAPI):
    DatabaseUtils.connect_to_mongo()
    yield
    DatabaseUtils.disconnect_from_mongo()


app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/api/v1")
