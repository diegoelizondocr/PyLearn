from typing import Optional

from pydantic import BaseModel


class UserOut(BaseModel):
    user_id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: str
    role_name: str
    role_description: Optional[str] = None
