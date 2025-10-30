import sqlite3
conn = sqlite3.connect("data/user_input.db")
cur = conn.cursor()
print("📋 資料表列表：")
for t in cur.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print("  ", t)
print("\n📄 前 5 筆資料：")
for row in cur.execute("SELECT * FROM input_log ORDER BY id DESC LIMIT 5"):
    print(row)
conn.close()
