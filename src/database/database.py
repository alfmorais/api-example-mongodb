from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database as PymongoDatabase

from src.config.settings import get_settings

settings = get_settings()


class Database:
    client: Optional[MongoClient] = None
    database: Optional[PymongoDatabase] = None


db = Database()


def get_database() -> Database:
    return db.database


class DatabaseUtils:
    @staticmethod
    def connect_to_mongo():
        db.client = MongoClient(settings.mongo_conn_str)
        db.database = db.client[settings.mongo_database]

    @staticmethod
    def disconnect_from_mongo():
        db.client.close()
