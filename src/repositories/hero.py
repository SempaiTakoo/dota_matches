from repositories.connector import get_connection

from models.hero import Hero


class HeroRepository:
    def get_all_heroes(self) -> list[Hero]:
        query = 'SELECT id, name FROM heroes'
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return [Hero(*row) for row in cur.fetchall()]

    def get_hero_by_id(self, hero_id: int) -> Hero | None:
        query = 'SELECT id, name FROM heroes WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (hero_id,))
                row = cur.fetchone()
                return Hero(*row) if row else None

    def add_hero(self, name: str) -> int:
        query = 'INSERT INTO heroes (name) VALUES (%s) RETURNING id'
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (name,))
                hero_id = cur.fetchone()[0]
                conn.commit()
                return hero_id

    def update_hero(self, hero_id: int, name: str) -> bool:
        query = 'UPDATE heroes SET name = %s WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (name, hero_id))
                updated_rows = cur.rowcount
                conn.commit()
                return updated_rows > 0

    def delete_hero(self, hero_id: int) -> bool:
        query = 'DELETE FROM heroes WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (hero_id,))
                deleted_rows = cur.rowcount
                conn.commit()
                return deleted_rows > 0
