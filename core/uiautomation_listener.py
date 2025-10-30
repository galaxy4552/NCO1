import keyboard, time, sqlite3, uiautomation as auto, re, requests
import pythoncom
pythoncom.CoInitialize()

DB_PATH = "data/user_input.db"
AI_API = "http://127.0.0.1:5001/ai_reply"
SENTENCE_END_CHARS = "。！？.!?\n"

# ---------------------------
# 初始化資料庫
# ---------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS input_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT,
            sentence TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log_to_db(app_name, sentence):
    if not sentence.strip():
        return
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO input_log (app_name, sentence) VALUES (?, ?)",
            (app_name, sentence.strip())
        )
        conn.commit()
    print(f"💾 已寫入：{sentence.strip()}")

def send_to_ai(sentence):
    try:
        res = requests.post(AI_API, json={"text": sentence})
        if res.ok:
            print(f"🤖 AI 回覆：{res.json().get('reply','')}")
    except Exception:
        pass

# ---------------------------
# 主監聽流程
# ---------------------------
init_db()

buffer = ""
last_time = time.time()

print("🦉 New Cool Owl 輸入監聽開始 (Ctrl+C 結束)\n")

def handle_key(event):
    global buffer, last_time

    if event.event_type != "down":
        return

    key = event.name
    now = time.time()

    # 字元輸入
    if len(key) == 1:
        buffer += key
    elif key == "space":
        buffer += " "
    elif key == "enter":
        commit_sentence()
        return

    # 若停頓超過 1.2 秒也判定一句
    if now - last_time > 1.2 and buffer.strip():
        commit_sentence()

    last_time = now

def commit_sentence():
    global buffer
    if not buffer.strip():
        return

    # 嘗試讀出目前焦點 app 名稱
    app_name = "Unknown"
    try:
        pythoncom.CoInitialize()  # 🔹 這行確保該 thread 初始化 COM
        with auto.UIAutomationInitializerInThread():
            ctrl = auto.GetFocusedControl()
            app_name = ctrl.Name or ctrl.ControlTypeName
    except Exception as e:
        print("⚠️ 無法取得焦點控制項：", e)
    finally:
        try:
            pythoncom.CoUninitialize()
        except:
            pass

    # 過濾出可讀中文（若有）
    if re.search(r'[\u4e00-\u9fff]', buffer):
        log_to_db(app_name, buffer)
        send_to_ai(buffer)
    else:
        print(f"[英數句] {buffer}")

    buffer = ""


keyboard.hook(handle_key)

try:
    keyboard.wait()
except KeyboardInterrupt:
    print("\n🦉 已停止監聽。")
