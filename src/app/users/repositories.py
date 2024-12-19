from src.config.settings import get_settings
from src.database.database import Database

from .models import UserModel

settings = get_settings()


class UserRepository:
    def create(self, db: Database, user: UserModel) -> str:
        _user = user.model_dump(by_alias=True)
        result = db[settings.mongo_database].insert_one(_user)
        return str(result.inserted_id)

    def get(self, db: Database, document: str) -> UserModel:
        _filter = {"document": document}
        user = db[settings.mongo_database].find_one(_filter)
        if user:
            return UserModel(**user)

    def update(self, db: Database, document: str, user: UserModel) -> bool:
        result = db[settings.mongo_database].update_one(
            {"document": document},
            {"$set": user.model_dump(by_alias=True)},
        )
        return result.modified_count > 0

    def delete(self, db: Database, document: str) -> bool:
        _filter = {"document": document}
        result = db[settings.mongo_database].delete_one(_filter)
        return result.deleted_count > 0


def get_user_repository():
    return UserRepository()
