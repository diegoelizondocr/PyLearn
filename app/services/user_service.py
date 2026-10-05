from typing import List
from fastapi import HTTPException
from loguru import logger
import oracledb
from app.repositories.user_repository import UserRepository
from app.models.schemas import UserOut, UserCreate


class UserService:

    def __init__(self, conn):
        self.repo = UserRepository(conn)

    def list_users(self) -> List[UserOut]:
        return self.repo.get_all()

    def get_user(self, username: str) -> UserOut:
        logger.info(f"Buscando usuario: {username}")
        user = self.repo.get_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail=f"Usuario '{username}' no encontrado")
        return user

    def create_user(self, user: UserCreate) -> dict:
        try:
            user_id = self.repo.create(user)
            logger.info(f"Usuario creado: {user.username}")
            return {
                "message": "Usuario creado correctamente",
                "user_id": user_id,
                "username": user.username
            }
        except oracledb.Error as e:
            error_obj, = e.args
            if error_obj.code == 20001:
                raise HTTPException(status_code=400, detail=f"El rol '{user.role_name}' no existe")
            elif error_obj.code == 20002:
                raise HTTPException(status_code=400, detail="Username o email ya existe")
            raise HTTPException(status_code=500, detail=str(error_obj.message))

    def update_active(self, username: str, is_active: bool) -> dict:
        rows = self.repo.update_active(username, is_active)
        if rows == 0:
            raise HTTPException(status_code=404, detail=f"Usuario '{username}' no encontrado")
        logger.info(f"Usuario '{username}' actualizado")
        return {
            "message": f"Usuario '{username}' actualizado",
            "is_active": is_active
        }

    def delete_user(self, username: str) -> dict:
        rows = self.repo.delete(username)
        if rows == 0:
            raise HTTPException(status_code=404, detail=f"Usuario '{username}' no encontrado")
        logger.info(f"Usuario '{username}' eliminado")
        return {"message": f"Usuario '{username}' eliminado"}