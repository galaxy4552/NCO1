"""
🦉 NewCoolOwl: UIAutomation 環境診斷工具
用途：
- 檢查 UIAutomationCore.dll 是否存在與可載入
- 檢查 COM 初始化狀態
- 檢查 Python 與作業系統架構是否相容
"""

import os
import platform
import ctypes
import pythoncom

print("=== 🧠 NewCoolOwl UIAutomation 環境診斷 ===\n")

# ------------------------------------------------------------
# 1️⃣ 系統版本
# ------------------------------------------------------------
print("[系統版本]")
print(f"Windows: {platform.system()} {platform.release()} ({platform.version()})")
print(f"架構: {platform.machine()}")
print()

# ------------------------------------------------------------
# 2️⃣ Python 架構
# ------------------------------------------------------------
print("[Python 環境]")
print(f"Python 版本: {platform.python_version()}")
print(f"Python 架構: {platform.architecture()[0]}")
print()

# ------------------------------------------------------------
# 3️⃣ 檢查 UIAutomationCore.dll 是否存在
# ------------------------------------------------------------
dll_path = r"C:\Windows\System32\UIAutomationCore.dll"
print("[UIAutomationCore.dll 檢查]")
if os.path.exists(dll_path):
    size = os.path.getsize(dll_path)
    print(f"✅ 找到 {dll_path} ({size} bytes)")
else:
    print(f"❌ 沒有找到 {dll_path}")
print()

# ------------------------------------------------------------
# 4️⃣ 嘗試載入 DLL
# ------------------------------------------------------------
print("[DLL 載入測試]")
try:
    ctypes.windll.LoadLibrary(dll_path)
    print("✅ DLL 成功載入")
except Exception as e:
    print("❌ 載入失敗:", e)
print()

# ------------------------------------------------------------
# 5️⃣ 測試 COM 初始化
# ------------------------------------------------------------
print("[COM 初始化測試]")
try:
    pythoncom.CoInitialize()
    print("✅ COM 初始化成功")
    pythoncom.CoUninitialize()
except Exception as e:
    print("❌ COM 初始化失敗:", e)
print()

# ------------------------------------------------------------
# 6️⃣ 嘗試匯入 uiautomation 並抓焦點
# ------------------------------------------------------------
print("[uiautomation 模組測試]")
try:
    import uiautomation as auto
    with auto.UIAutomationInitializerInThread():
        ctrl = auto.GetFocusedControl()
        print(f"✅ 成功載入 uiautomation，焦點控制項：{ctrl.Name or ctrl.ControlTypeName}")
except Exception as e:
    print("❌ 無法使用 uiautomation:", e)

print("\n=== 測試完成 ===")
