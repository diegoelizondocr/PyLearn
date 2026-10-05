from fastapi import APIRouter, Depends
from typing import List
from app.database import get_db
from app.services.role_service import RoleService
from app.models.schemas import RoleOut

router = APIRouter(prefix="/roles", tags=["Roles"])


def get_role_service(conn=Depends(get_db)) -> RoleService:
    return RoleService(conn)


@router.get("", response_model=List[RoleOut])
def list_roles(service: RoleService = Depends(get_role_service)):
    return service.list_roles()
