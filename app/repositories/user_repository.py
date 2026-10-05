from typing import List, Optional
import oracledb
from app.models.schemas import UserOut, UserCreate


class UserRepository:

    def __init__(self, conn):
        self.conn = conn

    def get_all(self) -> List[UserOut]:
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT u.user_id, u.username, u.email, u.full_name,
                       u.is_active, r.role_name, r.description
                FROM Users u
                JOIN Roles r ON u.role_id = r.role_id
                ORDER BY u.user_id
            """)
            columns = [c[0].lower() for c in cursor.description]
            return [UserOut(**dict(zip(columns, row))) for row in cursor.fetchall()]

    def get_by_username(self, username: str) -> Optional[UserOut]:
        with self.conn.cursor() as cursor:
            out_cursor = self.conn.cursor()
            cursor.callproc("get_user_with_role", [username, out_cursor])

            row = out_cursor.fetchone()
            if not row:
                out_cursor.close()
                return None

            columns = [c[0].lower() for c in out_cursor.description]
            out_cursor.close()
            return UserOut(**dict(zip(columns, row)))

    def create(self, user: UserCreate) -> int:
        with self.conn.cursor() as cursor:
            user_id_var = cursor.var(oracledb.NUMBER)
            cursor.callproc("create_user", [
                user.username,
                user.email,
                user.full_name,
                user.role_name.upper(),
                user_id_var
            ])
            return int(user_id_var.getvalue())

    def update_active(self, username: str, is_active: bool) -> int:
        with self.conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Users
                SET is_active = :active
                WHERE username = :username
            """, active='Y' if is_active else 'N', username=username)
            self.conn.commit()
            return cursor.rowcount

    def delete(self, username: str) -> int:
        with self.conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM Users WHERE username = :username",
                username=username
            )
            self.conn.commit()
            return cursor.rowcount