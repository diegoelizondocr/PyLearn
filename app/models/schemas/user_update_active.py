from pydantic import BaseModel


class UserUpdateActive(BaseModel):
    is_active: bool
