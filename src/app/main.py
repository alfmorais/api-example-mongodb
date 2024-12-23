from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.probes.views import router as probes_router
from src.app.users.views import router as users_router
from src.database.database import DatabaseUtils


@asynccontextmanager
async def lifespan(app: FastAPI):
    DatabaseUtils.connect_to_mongo()
    yield
    DatabaseUtils.disconnect_from_mongo()


app = FastAPI(lifespan=lifespan)
app.include_router(users_router, prefix="/api/v1")
app.include_router(probes_router)
