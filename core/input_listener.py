import time, threading, keyboard

BUF = []
LAST_TS = time.time()
PAUSE_MS = 0.35  # 使用者停頓多久才觸發（秒）

def on_key(e):
    global LAST_TS
    if e.event_type != 'down': 
        return
    k = e.name
    if len(k) == 1: BUF.append(k)
    elif k == 'space': BUF.append(' ')
    elif k in ('enter', 'tab'): BUF.clear()  # 結束一段輸入就清空
    elif k == 'backspace' and BUF: BUF.pop()
    LAST_TS = time.time()

def watcher():
    while True:
        time.sleep(0.05)
        if time.time() - LAST_TS > PAUSE_MS and BUF:
            text = ''.join(BUF).strip()
            if text:
                print(f"[TRIGGER] '{text}'")  # 之後這裡呼叫 API
            # 不清空，讓連續輸入也能累積；若想每次觸發都清空，就開這行：
            # BUF.clear()
            
keyboard.hook(on_key)
threading.Thread(target=watcher, daemon=True).start()
keyboard.wait()  # 阻塞主執行緒
