from src.app.users.models import UserModel
from src.app.users.repositories import UserRepository, get_user_repository


class TestRepositories:
    _repository = get_user_repository()
    _payload = UserModel(**{
        "document": "40279818980",
        "first_name": "Rosa",
        "last_name": "Aline Assunção",
        "email": "rosa_assuncao@testemail.com.br",
        "birthdate": "1993-01-04",
    })

    def test_create_user_success(self, database):
        user_id = self._repository.create(database, self._payload)

        assert isinstance(user_id, str)

    def test_get_user_not_found(self, database):
        user = self._repository.get(database, "79721947008")

        assert user is None

    def test_get_user_success(self, database):
        self._repository.create(database, self._payload)

        user = self._repository.get(database, "40279818980")

        assert user.document == self._payload.document
        assert user.first_name == self._payload.first_name
        assert user.last_name == self._payload.last_name
        assert user.email == self._payload.email
        assert user.birthdate == self._payload.birthdate

    def test_update_user_success(self, database):
        self._repository.create(database, self._payload)

        user_updated = UserModel(**{
            "document": "40279818980",
            "first_name": "Aline",
            "last_name": "Assunção",
            "email": "aline@gmail.com.br",
            "birthdate": "1993-01-04",
        })

        user_has_been_updated = self._repository.update(
            database,
            self._payload.document,
            user_updated,
        )

        user = self._repository.get(database, "40279818980")

        assert user.document == user_updated.document
        assert user.first_name == user_updated.first_name
        assert user.last_name == user_updated.last_name
        assert user.email == user_updated.email
        assert user.birthdate == user_updated.birthdate
        assert user_has_been_updated is True

    def test_delete_user_success(self, database):
        self._repository.create(database, self._payload)

        user_has_been_deleted = self._repository.delete(
            database,
            self._payload.document,
        )

        assert user_has_been_deleted is True

    def test_get_user_repository_success(self, database):
        assert isinstance(self._repository, UserRepository)
