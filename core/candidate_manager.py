import sqlite3
import re
from random import sample

DB_PATH = "data/user_input.db"

def get_candidates(input_text, limit=5):
    """根據輸入文字，從資料庫中搜尋相似句子當作候選"""
    if not input_text.strip():
        return []
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT sentence 
        FROM input_log 
        WHERE sentence LIKE ? AND phase='final'
        ORDER BY timestamp DESC LIMIT ?
    """, (f"%{input_text}%", limit))
    results = [row[0] for row in cur.fetchall()]
    conn.close()

    # 若找不到候選詞，就用 AI 或 fallback 字詞填補
    if not results:
        base = ["你好", "謝謝", "好的", "對不起", "沒問題"]
        results = sample(base, k=min(limit, len(base)))

    return results
