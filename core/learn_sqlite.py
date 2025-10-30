import sqlite3

def init_db():
    conn = sqlite3.connect("data/user_input.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS input_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT,
            sentence TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
