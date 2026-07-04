import sqlite3
import os

DB_PATH=os.path.join(os.path.dirname((os.path.dirname(__file__))), 'bot.db')

def get_connection():
    conn=sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA journal_mode=WAL')
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute(
            # ===== Таблицы для свечей =====
            '''
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

        # ===== Таблицы для игры в слова =====

        conn.execute('''
        CREATE TABLE IF NOT EXISTS game_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            current_letter TEXT,
            total_words_used INTEGER DEFAULT 0,
            last_player_id INTEGER
            )    
        ''')

        conn.execute('''
                    INSERT OR IGNORE INTO game_state (id, current_letter, total_words_used, last_player_id)
                    VALUES (1, NULL, 0, NULL)
                ''')
        conn.execute('''
                    CREATE TABLE IF NOT EXISTS used_words (
                        word TEXT PRIMARY KEY
                    )
                ''')

        conn.execute('''
                    CREATE TABLE IF NOT EXISTS player_stats (
                        user_id INTEGER PRIMARY KEY,
                        words_count INTEGER DEFAULT 0,
                        letter_counts TEXT DEFAULT '{}',
                        hints_used INTEGER DEFAULT 0
                    )
                ''')

        cursor = conn.execute("PRAGMA table_info(player_stats)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'hints_used' not in columns:
            conn.execute('ALTER TABLE player_stats ADD COLUMN hints_used INTEGER DEFAULT 0')
            print("✅ Обновлена таблица player_stats: добавлена колонка hints_used")
