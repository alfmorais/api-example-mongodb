from fastapi import APIRouter, Depends, status

from src.config.settings import get_settings
from src.database.database import Database, get_database

from .models import HealthCheck

router = APIRouter(tags=["Probes"])

settings = get_settings()


@router.get(
    "/health",
    response_model=HealthCheck,
    status_code=status.HTTP_200_OK,
)
def health_checks(db: Database = Depends(get_database)):
    data = HealthCheck(status="health").model_dump()
    _collection = db[settings.mongo_database].health_checks
    _collection.insert_one(data)
    return data
