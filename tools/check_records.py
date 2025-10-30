import sqlite3

conn = sqlite3.connect("data/user_input.db")
cur = conn.cursor()

print("總筆數：", cur.execute("SELECT COUNT(*) FROM input_log").fetchone()[0])
print("\n📋 欄位：")
for row in cur.execute("PRAGMA table_info(input_log)"):
    print(" ", row)
