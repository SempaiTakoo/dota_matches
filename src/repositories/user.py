from repositories.connector import get_connection

from models.user import User


class UserRepository:
    def get_all_users(self) -> list[User]:
        query = '''
            SELECT id, username, account_id, role, password_hash
            FROM users
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return [User(*row) for row in cur.fetchall()]

    def get_user_by_id(self, user_id: int) -> User | None:
        query = '''
            SELECT id, username, account_id, role, password_hash
            FROM users
            WHERE id = %s
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id,))
                user =  cur.fetchone()

                if not user:
                    return False

                return User(*user)

    def get_user_by_username(self, username: str) -> User | bool:
        query = '''
            SELECT id, username, account_id, role, password_hash
            FROM users
            WHERE username = %s
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (username,))
                user = cur.fetchone()

                if not user:
                    return False

                return User(*user)

    def add_user(self, user: User) -> int:
        query = '''
            INSERT INTO users (username, account_id, role, password_hash)
            VALUES (%(username)s, %(account_id)s, %(role)s, %(password_hash)s)
            RETURNING id
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    {
                        'username': user.username,
                        'account_id': user.account_id,
                        'role': user.role,
                        'password_hash': user.password_hash
                    }
                )
                new_id = cur.fetchone()[0]
                conn.commit()
                return new_id

    def update_user(self, user_id: int, username: str, role: str) -> None:
        query = '''
            UPDATE users
            SET
                username = %(username)s,
                role = %(role)s
            WHERE id = %(user_id)s
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    {
                        'user_id': user_id,
                        'username': username,
                        'role': role,
                    }
                )
                conn.commit()

    def delete_user(self, user_id: int) -> None:
        query = '''
            DELETE FROM users
            WHERE id = %s
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id,))
                conn.commit()
