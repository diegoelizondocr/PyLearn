from typing import Optional

from pydantic import BaseModel


class RoleOut(BaseModel):
    role_id: int
    role_name: str
    description: Optional[str] = None
