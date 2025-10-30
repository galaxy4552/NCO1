import time, threading, requests, json

BUF = []
LAST_TS = time.time()
PAUSE_MS = 0.35
API_URL = "http://127.0.0.1:5001/v1/completions"

def call_taide(text: str, phase: str = "early"):
    payload = {
        "model": "NewCoolOwl-Local",
        "prompt": f"[{phase.upper()}] 使用者輸入：{text}\nAI回覆："
    }
    try:
        r = requests.post(API_URL, json=payload, timeout=30)
        data = r.json()
        result = data.get("choices", [{}])[0].get("text", "").strip()
        print(f"[TAIDE] ({phase}) → {result}")
        return result
    except Exception as e:
        print(f"[ERR][TAIDE {phase}] {e}")
        return ""

# --------------------------------------------------------
# 測試區（僅限直接執行本檔時使用，不會被 import 觸發）
# --------------------------------------------------------
if __name__ == "__main__":
    import keyboard

    def on_key(e):
        global LAST_TS
        if e.event_type != 'down':
            return
        k = e.name
        if len(k) == 1: BUF.append(k)
        elif k == 'space': BUF.append(' ')
        elif k in ('enter', 'tab'): BUF.clear()
        elif k == 'backspace' and BUF: BUF.pop()
        LAST_TS = time.time()

    def watcher():
        while True:
            time.sleep(0.05)
            if time.time() - LAST_TS > PAUSE_MS and BUF:
                text = ''.join(BUF).strip()
                if text:
                    print(f"[TRIGGER] '{text}'")
                    threading.Thread(target=call_taide, args=(text,), daemon=True).start()
                BUF.clear()

    keyboard.hook(on_key)
    threading.Thread(target=watcher, daemon=True).start()
    keyboard.wait()
