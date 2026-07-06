from .db import get_connection

def has_user_reacted(user_id: int, message_id: int) -> bool:
    with get_connection() as conn:
        cursor=conn.execute(
            'SELECT 1 FROM reaction_log WHERE user_id = ? AND message_id = ?',
            (user_id, message_id)
        )
        return cursor.fetchone() is not None

def add_reaction(user_id: int, target_id: int, message_id: int, guild_id: int) -> None:
    with get_connection() as conn:
        conn.execute('INSERT INTO reaction_log (user_id, target_id, message_id, guild_id) VALUES (?, ?, ?, ?)',
                     (user_id, target_id, message_id, guild_id)
                     )

def increment_candle_count(user_id: int) -> int:
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO candle_counts (user_id, count) VALUES (?, 1)'
            'ON CONFLICT(user_id) DO UPDATE SET count = count + 1',
            (user_id,)
        )
        cursor = conn.execute('SELECT count FROM candle_counts WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        return row[0] if row else 0

def get_candle_count(user_id: int) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            'SELECT count FROM candle_counts WHERE user_id = ?',
            (user_id,)
        )
        row = cursor.fetchone()
        return row[0] if row else 0

def get_total_users_count() -> int:
    with get_connection() as conn:
        cursor=conn.execute('SELECT COUNT(*) FROM candle_counts')
        return cursor.fetchone()[0]

def get_top_candlers(page: int=1, per_page: int=5):
    offset=(page-1)*per_page
    with get_connection() as conn:
        cursor=conn.execute(
            'SELECT user_id, count FROM candle_counts ORDER BY count DESC LIMIT ? OFFSET ?',
            (per_page, offset)
        )
        return cursor.fetchall()