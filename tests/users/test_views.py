from fastapi import status

from src.app.users.models import UserModel
from src.app.users.repositories import get_user_repository


class TestViews:
    _payload = UserModel(**{
        "document": "40279818980",
        "first_name": "Rosa",
        "last_name": "Aline Assunção",
        "email": "rosa_assuncao@testemail.com.br",
        "birthdate": "1993-01-04",
    })
    _repository = get_user_repository()

    def test_create_user_registered(self, client, database):
        self._repository.create(database, self._payload)

        response = client.post(
            "/api/v1/users",
            json=self._payload.model_dump(by_alias=True),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "User already registered"

    def test_create_user_success(self, client, database):
        response = client.post(
            "/api/v1/users",
            json=self._payload.model_dump(by_alias=True),
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == self._payload.model_dump(by_alias=True)

    def test_get_user_not_found(self, client, database):
        response = client.get("/api/v1/users/40279818980")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "User not found"

    def test_get_user_success(self, client, database):
        self._repository.create(database, self._payload)

        response = client.get("/api/v1/users/40279818980")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self._payload.model_dump(by_alias=True)

    def test_update_user_not_found(self, client, database):
        user_updated = UserModel(**{
            "document": "40279818980",
            "first_name": "Joaquim",
            "last_name": "Morais",
            "email": "aline@gmail.com.br",
            "birthdate": "1990-01-04",
        })

        response = client.put(
            "/api/v1/users/35388077012",
            json=user_updated.model_dump(by_alias=True),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_user_success(self, client, database):
        self._repository.create(
            database,
            UserModel(**{
                "document": "35388077012",
                "first_name": "Joaquim",
                "last_name": "Lamonico",
                "email": "aline@gmail.com.br",
                "birthdate": "1990-01-04",
            }),
        )
        user_updated = UserModel(**{
            "document": "40279818980",
            "first_name": "Joaquim",
            "last_name": "Morais",
            "email": "aline@gmail.com.br",
            "birthdate": "1990-01-04",
        })

        response = client.put(
            "/api/v1/users/35388077012",
            json=user_updated.model_dump(by_alias=True),
        )
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_json["document"] == user_updated.document
        assert response_json["first_name"] == user_updated.first_name
        assert response_json["last_name"] == user_updated.last_name
        assert response_json["email"] == user_updated.email
        assert response_json["birthdate"] == user_updated.birthdate

    def test_delete_user_not_found(self, client, database):
        response = client.delete("/api/v1/users/40279818980")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "User not found"

    def test_delete_user_success(self, client, database):
        self._repository.create(database, self._payload)

        response = client.delete("/api/v1/users/40279818980")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "User deleted successfully"
