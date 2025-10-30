import sqlite3

conn = sqlite3.connect("data/user_input.db")
cur = conn.cursor()

for phase, count in cur.execute("SELECT phase, COUNT(*) FROM input_log GROUP BY phase"):
    print(f"{phase}：{count} 筆")
