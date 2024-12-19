import pytest
from pydantic import ValidationError

from src.app.users.models import UserModel


class TestModels:
    @pytest.mark.parametrize(
        "payload,expected_error",
        [
            (
                {
                    "first_name": "Rosa",
                    "last_name": "Aline Assunção",
                    "email": "rosa_assuncao@testemail.com.br",
                    "birthdate": "1993-01-04",
                },
                "ValidationError",
            ),
            (
                {
                    "document": "40279818980",
                    "last_name": "Aline Assunção",
                    "email": "rosa_assuncao@testemail.com.br",
                    "birthdate": "1993-01-04",
                },
                "ValidationError",
            ),
            (
                {
                    "document": "40279818980",
                    "first_name": "Rosa",
                    "email": "rosa_assuncao@testemail.com.br",
                    "birthdate": "1993-01-04",
                },
                "ValidationError",
            ),
            (
                {
                    "document": "40279818980",
                    "first_name": "Rosa",
                    "last_name": "Aline Assunção",
                    "birthdate": "1993-01-04",
                },
                "ValidationError",
            ),
            (
                {
                    "document": "40279818980",
                    "first_name": "Rosa",
                    "last_name": "Aline Assunção",
                    "email": "rosa_assuncao@testemail.com.br",
                },
                "ValidationError",
            ),
        ],
    )
    def test_user_models_validate(self, payload, expected_error):
        with pytest.raises(ValidationError) as error:
            UserModel(**payload)

        assert error.typename == expected_error

    def test_user_models_document_invalid(self):
        payload = {
            "document": "40279818989",
            "first_name": "Rosa",
            "last_name": "Aline Assunção",
            "email": "rosa_assuncao@testemail.com.br",
            "birthdate": "1993-01-04",
        }

        with pytest.raises(ValueError) as error:
            UserModel(**payload)

        expected_error = "Value error, Document invalid"

        assert error.typename == "ValidationError"
        assert error.value.errors()[0]["msg"] == expected_error

    def test_user_models_birthdate_invalid(self):
        payload = {
            "document": "40279818980",
            "first_name": "Rosa",
            "last_name": "Aline Assunção",
            "email": "rosa_assuncao@testemail.com.br",
            "birthdate": "01-04-1992",
        }

        with pytest.raises(ValueError) as error:
            UserModel(**payload)

        expected_error = (
            "Value error, Field 'birthdate' must be 'YYYY-MM-DD' format."
        )

        assert error.typename == "ValidationError"
        assert error.value.errors()[0]["msg"] == expected_error
