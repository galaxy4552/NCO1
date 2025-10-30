import os
import time
import threading
import sqlite3
import tkinter as tk
import pyautogui
import uiautomation as auto
import pythoncom
from core.input_to_taide import call_taide

print("🦉 NewCoolOwl：Tkinter 浮窗 + SQLite 紀錄版 啟動（Ctrl+C 結束）\n")

# =========================================================
# 🧱 1️⃣ 初始化資料庫
# =========================================================
DB_PATH = os.path.join("data", "user_input.db")
os.makedirs("data", exist_ok=True)

def init_db():
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

def log_to_db(app_name, sentence, phase):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO input_log (app_name, sentence, phase) VALUES (?, ?, ?)",
                (app_name, sentence.strip(), phase),
            )
            conn.commit()
        print(f"💾 已記錄：{sentence.strip()} ({phase})")
    except Exception as e:
        print("⚠️ 資料庫寫入錯誤：", e)

init_db()

# =========================================================
# 💡 2️⃣ Tkinter 候選詞顯示
# =========================================================
class CandidatePopup:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.label = tk.Label(
            self.root,
            text="💡 候選詞初始化中...",
            bg="white",
            fg="black",
            justify="left",
            font=("Microsoft JhengHei", 10),
            padx=10,
            pady=5
        )
        self.label.pack()
        self.candidates = []
        self.current_index = 0
        self.update_position()
        self.root.after(100, self._loop)

    def update_candidates(self, candidates):
        self.candidates = candidates
        self.current_index = 0
        self._refresh_display()

    def _refresh_display(self):
        display = []
        for i, word in enumerate(self.candidates):
            prefix = "👉" if i == self.current_index else "  "
            display.append(f"{prefix} [{i+1}] {word}")
        text = "💡 候選詞：\n" + "\n".join(display) if display else "（暫無候選詞）"
        self.label.config(text=text)
        self.update_position()

    def update_position(self):
        x, y = pyautogui.position()
        offset_x, offset_y = 20, 20
        self.root.geometry(f"+{x + offset_x}+{y + offset_y}")

    def _loop(self):
        self.update_position()
        self.root.after(200, self._loop)

    def run(self):
        self.root.mainloop()

def monitor_loop():
    pythoncom.CoInitialize()  # 🧩 初始化 COM 環境，修正 WinError -2147221008
    SCAN_INTERVAL = 0.5
    last_text = ""

    while True:
        try:
            ctrl = auto.GetFocusedControl()
            if not ctrl:
                time.sleep(SCAN_INTERVAL)
                continue

            text = ""
            try:
                pattern = getattr(ctrl, "GetValuePattern", None)
                if pattern:
                    vp = pattern()
                    text = vp.Value
                else:
                    text = getattr(ctrl, "Name", "")
            except Exception:
                pass

            if text and text.strip() != last_text:
                last_text = text.strip()
                app_name = getattr(ctrl, "Name", "Unknown")
                print(f"[DEBUG] 偵測文字：{last_text}")
                log_to_db(app_name, last_text, "early")

                ai_reply = call_taide(last_text, "early")
                print(f"[TAIDE 回覆] → {ai_reply}")

                candidates = ai_reply.split()[:5]
                # 🧠 在 Tkinter 主執行緒中更新候選詞
                popup.root.after(0, popup.update_candidates, candidates)

            time.sleep(SCAN_INTERVAL)

        except KeyboardInterrupt:
            print("\n🦉 停止監聽。")
            break
        except Exception as e:
            print("[錯誤]", e)
            time.sleep(SCAN_INTERVAL)

popup = CandidatePopup()
threading.Thread(target=monitor_loop, daemon=True).start()  # 開新執行緒跑監聽
popup.root.mainloop()  # 主執行緒跑 UI

SCAN_INTERVAL = 0.5
last_text = ""