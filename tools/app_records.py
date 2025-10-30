import sqlite3

APP_KEYWORD = "記事本"

conn = sqlite3.connect("data/user_input.db")
cur = conn.cursor()

for (sentence,) in cur.execute(f"SELECT sentence FROM input_log WHERE app_name LIKE '%{APP_KEYWORD}%' ORDER BY id DESC LIMIT 5"):
    print(sentence)
