from repositories.connector import get_connection
from models.player import Player


class PlayerRepository:
    def get_all_players(self) -> list[Player]:
        query = '''
            SELECT
                id, account_id, match_id, hero_id, kills, deaths,
                assistances, is_radiant, rating_change
            FROM players
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return [Player(*row) for row in cur.fetchall()]

    def get_player_by_id(self, player_id: int) -> Player:
        query = '''
            SELECT
                id, account_id, match_id, hero_id, kills, deaths,
                assistances, is_radiant, rating_change
            FROM players
            WHERE id = %s
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (player_id,))
                row = cur.fetchone()
                if row:
                    return Player(*row)
                return None

    def add_player(self, player: Player) -> int:
        query = '''
            INSERT INTO players (
                account_id, match_id, hero_id, kills, deaths,
                assistances, is_radiant, rating_change
            )
            VALUES (
                %(account_id)s, %(match_id)s, %(hero_id)s,
                %(kills)s, %(deaths)s, %(assistances)s, %(is_radiant)s,
                %(rating_change)s
            )
            RETURNING id
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    {
                        'account_id': player.account_id,
                        'match_id': player.match_id,
                        'hero_id': player.hero_id,
                        'kills': player.kills,
                        'deaths': player.deaths,
                        'assistances': player.assistances,
                        'is_radiant': player.is_radiant,
                        'rating_change': player.rating_change
                    }
                )
                player_id = cur.fetchone()[0]
                conn.commit()
                return player_id

    def delete_player(self, player_id: int) -> bool:
        query = 'DELETE FROM players WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (player_id,))
                if cur.rowcount > 0:
                    conn.commit()
                    return True
                return False
