from repositories.connector import get_connection
from models.player_items import PlayerItem
from models.item import Item
from models.player import Player


class PlayerItemsRepository:
    def get_all_player_items(self):
        query = "SELECT * FROM player_items;"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return [PlayerItem(*row) for row in cur.fetchall()]

    def get_items_by_player(self, player_id):
        query = "SELECT item_id FROM player_items WHERE player_id = %s;"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (player_id,))
                return [PlayerItem(*row) for row in cur.fetchall()]

    def add_item_to_player(self, player_id, item_id):
        query = "INSERT INTO player_items (player_id, item_id) VALUES (%s, %s);"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (player_id, item_id))
                conn.commit()

    def delete_items_by_player(self, player_id):
        query = "DELETE FROM player_items WHERE player_id = %s;"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (player_id,))
                conn.commit()
