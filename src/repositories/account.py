from models.account import Account

from repositories.connector import get_connection


class AccountRepository:
    def get_all_accounts(self) -> list[Account]:
        query = '''
            SELECT id, nickname, rating
            FROM accounts
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return [Account(*row) for row in cur.fetchall()]

    def get_account_by_id(self, account_id: int) -> Account | None:
        query = '''
            SELECT id, nickname, rating
            FROM accounts
            WHERE id = %s
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (account_id,))
                account =  cur.fetchone()

                if not account:
                    Exception(f'Аккаунт с id {account_id} не найден.')

                return Account(*account)

    def add_account(self, nickname: str, rating: int) -> int:
        query = '''
            INSERT INTO accounts (nickname, rating)
            VALUES (%(nickname)s, %(rating)s)
            RETURNING id
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, {'nickname': nickname, 'rating': rating})
                new_id = cur.fetchone()[0]
                conn.commit()
                return new_id

    def update_account(self, account_id: int, nickname: str, rating: int) -> None:
        query = '''
            UPDATE accounts
            SET nickname = %(nickname)s, rating = %(rating)s
            WHERE id = %(account_id)s
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, {
                    'account_id': account_id,
                    'nickname': nickname,
                    'rating': rating
                })
                conn.commit()

    def delete_account(self, account_id: int) -> None:
        query = '''
            DELETE FROM accounts
            WHERE id = %s
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (account_id,))
                conn.commit()
