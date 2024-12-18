from repositories.connector import get_connection

from models.match import Match


class MatchRepository:
    def get_all_matches(self) -> list[Match]:
        query = '''
            SELECT
                id, start_time, duration, radiant_win, radiant_kills, dire_kills
            FROM matches
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return [Match(*row) for row in cur.fetchall()]

    def add_match(self, match: Match) -> int:
        print(f'match: {match}')
        query = '''
            INSERT INTO matches (
                start_time, duration, radiant_win, radiant_kills, dire_kills
            )
            VALUES (
                %(start_time)s, %(duration)s, %(radiant_win)s,
                %(radiant_kills)s, %(dire_kills)s
            )
            RETURNING id
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    {
                        'start_time': match.start_time,
                        'duration': match.duration,
                        'radiant_win': match.radiant_win,
                        'radiant_kills': match.radiant_kills,
                        'dire_kills': match.dire_kills
                    }
                )
                match_id = cur.fetchone()[0]
                conn.commit()
                return match_id

    def update_match(self, match_id: int, updated_match: Match) -> None:
        query = '''
            UPDATE matches
            SET
                start_time = %(start_time)s,
                duration = %(duration)s,
                radiant_win = %(radiant_win)s,
                radiant_kills = %(radiant_kills)s,
                dire_kills = %(dire_kills)s
            WHERE id = %(id)s
        '''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    {
                        'id': match_id,
                        'start_time': updated_match.start_time,
                        'duration': updated_match.duration,
                        'radiant_win': updated_match.radiant_win,
                        'radiant_kills': updated_match.radiant_kills,
                        'dire_kills': updated_match.dire_kills
                    }
                )
                conn.commit()

    def delete_match(self, match_id: int) -> None:
        query = 'DELETE FROM matches WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (match_id,))
                conn.commit()
