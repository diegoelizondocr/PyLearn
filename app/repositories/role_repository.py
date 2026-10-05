from typing import List
from app.models.schemas import RoleOut


class RoleRepository:

    def __init__(self, conn):
        self.conn = conn

    def get_all(self) -> List[RoleOut]:
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT role_id, role_name, description
                FROM Roles
                ORDER BY role_id
            """)
            rows = cursor.fetchall()
            return [
                RoleOut(role_id=r[0], role_name=r[1], description=r[2])
                for r in rows
            ]