import sqlite3

# 建立資料庫檔案（不存在會自動建立）
conn = sqlite3.connect("memory.db")
cursor = conn.cursor()

# 建立表格（如果不存在）
cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    vector BLOB
)
""")

print("✅ 資料庫與表格建立完成")

conn.close()
