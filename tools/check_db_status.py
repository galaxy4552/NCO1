import os
import sqlite3
import subprocess

# ---------------------------
# 資料庫路徑
# ---------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "user_input.db")
IGNORE_PATH = os.path.join(BASE_DIR, ".gitignore")

print("🦉 檢查資料庫狀態啟動中...", flush=True)

# ---------------------------
# 檢查檔案是否存在
# ---------------------------
if not os.path.exists(DB_PATH):
    print(f"⚠️ 找不到資料庫：{DB_PATH}")
    print("➡️ 嘗試建立新的 SQLite 資料庫...")
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS input_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT,
            sentence TEXT,
            phase TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("✅ 已建立新的資料庫 user_input.db\n")
else:
    print(f"✅ 資料庫存在：{DB_PATH}\n")

# ---------------------------
# 嘗試讀取資料
# ---------------------------
try:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        count = cur.execute("SELECT COUNT(*) FROM input_log").fetchone()[0]
    except sqlite3.OperationalError:
        print("⚠️ 找不到資料表 input_log，這看起來像是新資料庫。")
        count = 0

    if count == 0:
        print("⚠️ 目前資料庫是空的，先跑 listener 收集語料。")
    else:
        print(f"📊 資料筆數：{count}")
        print("\n📄 最近 5 筆資料：")
    for row in cur.execute("SELECT * FROM input_log ORDER BY id DESC LIMIT 5"):
        print(" ", row)
    conn.close()
except Exception as e:
    print("⚠️ 無法讀取資料庫內容：", e)

# ---------------------------
# 檢查 .gitignore 狀態
# ---------------------------
# 檢查 .gitignore 狀態（可選）
try:
    import subprocess, os
    subprocess.run(["git","rev-parse","--is-inside-work-tree"], check=True,
                   capture_output=True)
# ... 原本的 check-ignore 邏輯 ...
except Exception:
    print("⚙️ 未偵測到 git 環境，略過 gitignore 檢查。")

print("\n🦉 完成檢查。")
