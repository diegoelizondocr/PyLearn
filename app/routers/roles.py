from fastapi import APIRouter, Depends
from typing import List
from app.database import get_db
from app.services.role_service import RoleService
from app.models.schemas import RoleOut

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("", response_model=List[RoleOut])
def list_roles(conn=Depends(get_db)):
    service = RoleService(conn)
    return service.list_roles()