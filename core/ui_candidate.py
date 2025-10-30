# core/ui_candidate.py
import tkinter as tk
import threading
import keyboard
import time
import pyautogui

class CandidateUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#1e1e1e")
        self.root.geometry("+800+400")  # 讓它固定開在螢幕中央
        self.root.wm_attributes("-alpha", 0.92)
        print("[DEBUG] 候選浮窗初始化成功")


        self.label = tk.Label(
            self.root,
            text="🦉 NewCoolOwl 候選詞啟動中...",
            font=("Microsoft JhengHei", 12),
            fg="white",
            bg="#1e1e1e",
            justify="left"
        )
        self.label.pack(padx=10, pady=6)

        self.candidates = []
        self.current_index = 0
        self.last_update = time.time()

        # 啟動監聽執行緒
        threading.Thread(target=self._update_loop, daemon=True).start()
        threading.Thread(target=self._keyboard_listener, daemon=True).start()

    # -----------------------------------------------------
    # 顯示候選詞
    # -----------------------------------------------------
    def show_candidates(self, items):
        if not items:
            self.hide()
            return
        self.candidates = items
        self._refresh_display()

    def _refresh_display(self):
        display = []
        for i, word in enumerate(self.candidates):
            if i == self.current_index:
                display.append(f"👉 [{i+1}] {word}")
            else:
                display.append(f"   [{i+1}] {word}")
        self.label.config(text="💡 候選詞：\n" + "\n".join(display))
        self.root.deiconify()
        self.last_update = time.time()

    # -----------------------------------------------------
    # 鍵盤事件
    # -----------------------------------------------------
    def _keyboard_listener(self):
        while True:
            try:
                if not self.candidates:
                    time.sleep(0.2)
                    continue

                # 數字鍵選取
                for i in range(len(self.candidates)):
                    if keyboard.is_pressed(str(i+1)):
                        self._select_candidate(i)
                        time.sleep(0.3)

                # 方向鍵移動
                if keyboard.is_pressed("up"):
                    self.current_index = (self.current_index - 1) % len(self.candidates)
                    self._refresh_display()
                    time.sleep(0.2)
                elif keyboard.is_pressed("down"):
                    self.current_index = (self.current_index + 1) % len(self.candidates)
                    self._refresh_display()
                    time.sleep(0.2)

                # Enter 選取
                if keyboard.is_pressed("enter"):
                    self._select_candidate(self.current_index)
                    time.sleep(0.3)

                time.sleep(0.05)
            except:
                pass

    # -----------------------------------------------------
    # 選取候選詞
    # -----------------------------------------------------
    def _select_candidate(self, index):
        if 0 <= index < len(self.candidates):
            choice = self.candidates[index]
            print(f"✅ 已選擇：{choice}")
            self.show_text(f"✅ 選擇：{choice}")
            # TODO: 可在這裡加入 pyperclip.copy(choice) + keyboard.send('ctrl+v')

    # -----------------------------------------------------
    # 顯示自訂文字
    # -----------------------------------------------------
    def show_text(self, text):
        self.label.config(text=text)
        self.root.deiconify()

    def hide(self):
        self.root.withdraw()

    # -----------------------------------------------------
    # 自動隱藏
    # -----------------------------------------------------
    def _update_loop(self):
        while True:
            try:
                if time.time() - self.last_update > 10:
                    self.hide()
                self.root.update_idletasks()
                self.root.update()
                time.sleep(0.05)
            except tk.TclError:
                break
    # -----------------------------------------------------
    # 滑鼠事件和顯示
    # -----------------------------------------------------

    def _refresh_display(self):
        display = []
        for i, word in enumerate(self.candidates):
            prefix = "👉" if i == self.current_index else "  "
            display.append(f"{prefix} [{i+1}] {word}")
        self.label.config(text="💡 候選詞：\n" + "\n".join(display))

        # 🖱️ 更新浮窗位置（移進方法內）
        import pyautogui
        x, y = pyautogui.position()
        offset_x, offset_y = 20, 20  # 浮窗相對滑鼠位置偏移
        self.root.geometry(f"+{x + offset_x}+{y + offset_y}")
