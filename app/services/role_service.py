from typing import List
from loguru import logger
from app.repositories.role_repository import RoleRepository
from app.models.schemas import RoleOut


class RoleService:

    def __init__(self, conn):
        self.repo = RoleRepository(conn)

    def list_roles(self) -> List[RoleOut]:
        logger.info("Listando roles")
        return self.repo.get_all()