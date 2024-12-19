from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator
from validate_docbr import CPF


class UserModel(BaseModel):
    document: str
    first_name: str
    last_name: str
    email: EmailStr
    birthdate: str

    @field_validator("document")
    def validate_document(cls, document: str) -> str:
        validator = CPF()
        masked_document = validator.mask(document)

        if not validator.validate(masked_document):
            error = "Document invalid"
            raise ValueError(error)

        return document

    @field_validator("birthdate")
    def validate_birthdate(cls, birthdate: str) -> str:
        try:
            datetime.strptime(birthdate, "%Y-%m-%d")
        except ValueError:
            error = "Field 'birthdate' must be 'YYYY-MM-DD' format."
            raise ValueError(error)

        return birthdate

    class ConfigDict:
        extra = "allow"
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "document": str,
                "first_name": str,
                "last_name": str,
                "email": str,
                "birthdate": str,
            }
        }
