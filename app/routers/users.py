from fastapi import APIRouter, Depends, status
from typing import List
from app.database import get_db
from app.services.user_service import UserService
from app.models.schemas import UserOut, UserCreate, UserUpdateActive

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(conn=Depends(get_db)) -> UserService:
    return UserService(conn)


@router.get("", response_model=List[UserOut])
def list_users(service: UserService = Depends(get_user_service)):
    return service.list_users()


@router.get("/{username}", response_model=UserOut)
def get_user(username: str, service: UserService = Depends(get_user_service)):
    return service.get_user(username)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(user)


@router.patch("/{username}/active")
def update_user_active(
    username: str,
    body: UserUpdateActive,
    service: UserService = Depends(get_user_service),
):
    return service.update_active(username, body.is_active)


@router.delete("/{username}")
def delete_user(username: str, service: UserService = Depends(get_user_service)):
    return service.delete_user(username)
