import sqlite3
import os

DB_PATH=os.path.join(os.path.dirname((os.path.dirname(__file__))), 'reactions.db')

def get_connection():
    conn=sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA journal_mode=WAL')
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS reaction_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            target_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL,
            guild_id INTEGER NOT NULL,
            UNIQUE(user_id, message_id)
            )
        ''')

        conn.execute('''
        CREATE TABLE IF NOT EXISTS candle_counts (
            user_id INTEGER PRIMARY KEY,
            count INTEGER DEFAULT 0
            )
        ''')