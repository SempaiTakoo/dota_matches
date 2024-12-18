from repositories.connector import get_connection
from models.item import Item


class ItemRepository:
    def get_all_items(self) -> list[Item]:
        query = 'SELECT id, name FROM items'
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return [Item(*row) for row in cur.fetchall()]

    def add_item(self, name: str) -> int:
        query = 'INSERT INTO items (name) VALUES (%s) RETURNING id'
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (name,))
                item_id = cur.fetchone()[0]
                conn.commit()
                return item_id

    def delete_item(self, item_id: int) -> None:
        query = 'DELETE FROM items WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (item_id,))
                conn.commit()

    def update_item(self, item_id: int, new_name: str) -> bool:
        query = 'UPDATE items SET name = %s WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (new_name, item_id))
                updated_rows = cur.rowcount
                conn.commit()
                return updated_rows > 0
