import sqlite3
from datetime import datetime

DB_PATH = "data/user_input.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("🦉 檢查資料庫內容：input_log\n")

# 顯示欄位結構
cursor.execute("PRAGMA table_info(input_log)")
print("📋 欄位結構：")
for row in cursor.fetchall():
    print("  ", row)
print("\n")

# 顯示最近 10 筆紀錄
cursor.execute("SELECT id, app_name, sentence, phase, timestamp FROM input_log ORDER BY id DESC LIMIT 10")
rows = cursor.fetchall()

if not rows:
    print("⚠️ 沒有資料（可能程式還沒寫入）")
else:
    print("📄 最近 10 筆紀錄：\n")
    for r in rows:
        print(f"[{r[0]}] ({r[4]}) {r[3]} | {r[1]} → {r[2]}")

conn.close()
