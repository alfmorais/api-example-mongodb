import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)
    mongo_conn_str: str = os.environ["MONGO_CONN_STR"]
    mongo_database: str = os.environ["MONGO_DATABASE"]
    mongo_initdb_root_username: str = os.environ["MONGO_INITDB_ROOT_USERNAME"]
    mongo_initdb_root_password: str = os.environ["MONGO_INITDB_ROOT_PASSWORD"]
    mongo_db: str = os.environ["MONGO_DB"]
    mongo_host: str = os.environ["MONGO_HOST"]
    mongo_username: str = os.environ["MONGO_USERNAME"]
    mongo_password: str = os.environ["MONGO_PASSWORD"]


lru_settings = Settings()


@lru_cache
def get_settings() -> Settings:
    return lru_settings
