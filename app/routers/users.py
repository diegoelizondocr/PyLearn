from fastapi import APIRouter, Depends, status
from typing import List
from app.database import get_db
from app.services.user_service import UserService
from app.models.schemas import UserOut, UserCreate, UserUpdateActive

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserOut])
def list_users(conn=Depends(get_db)):
    service = UserService(conn)
    return service.list_users()


@router.get("/{username}", response_model=UserOut)
def get_user(username: str, conn=Depends(get_db)):
    service = UserService(conn)
    return service.get_user(username)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, conn=Depends(get_db)):
    service = UserService(conn)
    return service.create_user(user)


@router.patch("/{username}/active")
def update_user_active(username: str, body: UserUpdateActive, conn=Depends(get_db)):
    service = UserService(conn)
    return service.update_active(username, body.is_active)


@router.delete("/{username}")
def delete_user(username: str, conn=Depends(get_db)):
    service = UserService(conn)
    return service.delete_user(username)