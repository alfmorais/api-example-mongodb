from fastapi import APIRouter, Depends, HTTPException, status

from src.database.database import Database, get_database

from .models import UserModel
from .repositories import UserRepository, get_user_repository

router = APIRouter(tags=["Users"])


@router.post(
    "/users",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserModel,
    db: Database = Depends(get_database),
    repository: UserRepository = Depends(get_user_repository),
):
    user_registered = repository.get(db, user.document)
    if user_registered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )

    repository.create(db, user)
    return {**user.model_dump(by_alias=True)}


@router.get(
    "/users/{document}",
    response_model=UserModel,
    status_code=status.HTTP_200_OK,
)
def get_user(
    document: str,
    db: Database = Depends(get_database),
    repository: UserRepository = Depends(get_user_repository),
):
    user = repository.get(db, document)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    return user


@router.put(
    "/users/{document}",
    response_model=UserModel,
    status_code=status.HTTP_200_OK,
)
def update_user(
    document: str,
    user: UserModel,
    db: Database = Depends(get_database),
    repository: UserRepository = Depends(get_user_repository),
):
    user_registered = repository.get(db, document)
    if not user_registered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    repository.update(db, document, user)
    return {**user.model_dump(by_alias=True)}


@router.delete(
    "/users/{document}",
    status_code=status.HTTP_200_OK,
)
def delete_user(
    document: str,
    db: Database = Depends(get_database),
    repository: UserRepository = Depends(get_user_repository),
):
    user_registered = repository.get(db, document)
    if not user_registered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    repository.delete(db, document)
    return {"message": "User deleted successfully"}
