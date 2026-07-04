from .db import get_connection
import json

def get_words_state():
    with get_connection() as conn:
        cursor=conn.execute('SELECT current_letter, total_words_used, last_player_id FROM game_state WHERE id = 1')
        row = cursor.fetchone()
        if row:
            return {
                'current_letter': row[0],
                'total_words_used': row[1],
                'last_player_id': row[2]
            }
        return None

def update_words_state(current_letter=None, total_words_used=None, last_player_id=None):
    with get_connection() as conn:
        if current_letter is not None:
            conn.execute('UPDATE game_state SET current_letter = ? WHERE id = 1', (current_letter,))
        if total_words_used is not None:
            conn.execute('UPDATE game_state SET total_words_used = ? WHERE id = 1', (total_words_used,))
        if last_player_id is not None:
            conn.execute('UPDATE game_state SET last_player_id = ? WHERE id = 1', (last_player_id,))

def is_word_used(word: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute('SELECT 1 FROM used_words WHERE word = ?', (word,))
        return cursor.fetchone() is not None

def add_used_word(word: str) -> None:
    with get_connection() as conn:
        conn.execute('INSERT OR IGNORE INTO used_words (word) VALUES (?)', (word,))

def update_words_player_stats(user_id: int, first_letter: str):
    with get_connection() as conn:
        cursor = conn.execute('''
            UPDATE player_stats 
            SET words_count = words_count + 1,
                letter_counts = json_set(letter_counts, '$.' || ?, 
                    COALESCE(json_extract(letter_counts, '$.' || ?), 0) + 1
                )
            WHERE user_id = ?
        ''', (first_letter, first_letter, user_id))

        if cursor.rowcount == 0:
            conn.execute('''
                INSERT INTO player_stats (user_id, words_count, letter_counts)
                VALUES (?, 1, json_object(?, 1))
            ''', (user_id, first_letter))

def get_words_player_stats(user_id: int):
    with get_connection() as conn:
        cursor = conn.execute(
            'SELECT words_count, letter_counts, hints_used FROM player_stats WHERE user_id = ?',
            (user_id,)
        )
        row = cursor.fetchone()
        if row:
            return {
                'words_count': row[0],
                'letter_counts': json.loads(row[1]) if row[1] else {},
                'hints_used': row[2] or 0
            }
        return None

def get_top_user():
    with get_connection() as conn:
        cursor = conn.execute('''
            SELECT user_id, words_count
            FROM player_stats
            ORDER BY words_count DESC
            LIMIT 1
        ''')
        row = cursor.fetchone()
        if row:
            return {
                'user_id': row[0],
                'words_count': row[1]
            }
        return None

def get_all_used_words() -> set:
    with get_connection() as conn:
        cursor = conn.execute('SELECT word FROM used_words')
        return {row[0] for row in cursor.fetchall()}

def increment_hints_used(user_id: int):
    with get_connection() as conn:
        conn.execute('''
            INSERT INTO player_stats (user_id, hints_used)
            VALUES (?, 1)
            ON CONFLICT(user_id) DO UPDATE SET hints_used = hints_used + 1
        ''', (user_id,))

def reset_word_game():
    with get_connection() as conn:
        conn.execute('DELETE FROM used_words')
        conn.execute('DELETE FROM player_stats')
        conn.execute('''
            UPDATE game_state 
            SET current_letter = NULL, 
                total_words_used = 0, 
                last_player_id = NULL 
            WHERE id = 1
        ''')