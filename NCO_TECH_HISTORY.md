## 🔧 NCO 1.0 實際觀測結果

⚙️ NCO 1.0 採用 Flask 架構，  
雖然技術上仍屬於同步請求、沒有真正的流式理解，  
但它成功完成了五個端點的資料通路串接：

輸入監聽 → Flask 伺服器 → 本地 LLM → 候選顯示 → 使用者回饋。

這個版本的 AI 並不「懂」使用者，  
它只是「能接收並回傳」——  
所有候選結果仍是模型的假回覆（Flask 架構過慢）。

然而，這個版本第一次實現了五個模組的完整通路：
- 鍵盤監聽  
- Flask 伺服器  
- 本地模型橋接  
- 候選詞顯示層  
- 學習開關（Learning ON/OFF）

> 這使它成為台灣第一個能實際完成  
> **AI → 輸入法 → 學習 閉環** 的原型系統。

這使後續版本能以同一資料管線擴展

NewCoolOwl/
├── core/                             ← 🧠 核心功能層：輸入、選字、學習、記錄
│   ├── __init__.py
│   ├── //input_core.py                  # 處理鍵盤輸入主流程
│   ├── //ai_predictor.py                # 調用 LLM（TAIDE / SmolLM / Qwen）
│   ├── learn_sqlite.py                # 使用者語料學習與資料庫操作
│   ├── //log_manager.py                 # 操作日誌、錯誤記錄
│   ├── //ui_shell.py                    # 簡易前端介面／浮動視窗邏輯
│   ├── auto_adapt.py                  # 自適應候選詞排序
│   ├── contextual_api.py              # 與模型的上下文 API 橋接
│   ├── input_listener.py              # 鍵盤輸入監聽核心
│   ├── input_listener_combined.py     # 結合真核心
│   ├── input_to_taide.py              # 將輸入轉為模型輸入格式
│   └── uiautomation_listener.py       # 監控 Windows IME 狀態與焦點
│
├── tools/
│   ├── check_records.py               ← 查看資料（通用查詢）
│   ├── phase_stats.py                 ← 統計 early / final 比例
│   ├── app_records.py                 ← 篩選特定 App 的紀錄
│   ├── analyze_pairs.py               ← Early / Final 成對分析 (語流對照)
│   ├── check_input_log.py
│   └── check_uiautomation_env.py    
│   
├── samples/                           ← 範例與測試資料
│
├── models/                            ← 📦 模型資料夾（使用者自備）
│   └── README.txt                     # 說明如何放入 LLM 模型（例如 TAIDE / Qwen）
│
├── scripts/                           ← 💻 自動化腳本
│   ├── setup_env.sh                   # 初始化虛擬環境（Linux / Mac）
│   └── download_models.sh             # 自動下載模型腳本
│
├── config/                            ← ⚙️ 設定檔
│   ├── default.json                   # 系統預設設定
│   └── user_settings.json             # 使用者個人設定
│
├── ai_test/                           ← 🤖 模型測試模組
│   ├── test_Qwen.py
│   ├── test_smollm2.py
│   └── test_taide_api.py
│
├── main.test.py                       ← 測試主入口（整合核心模組）
│
├── requirements.txt                   ← Python 套件依賴
│
├── README.md                          ← 專案說明文件
│
└── .private/
      ├── MindMap.cs                         ← 架構導圖與系統備忘（內部文件）
      └── MindMap.DevDiary.cs                ← 開發日誌與實驗記錄

NewCoolOwl1(NCO1)

Keyboard Hook
   ↓
Input Watcher
   ↓
TAIDE API Bridge
   ↓
感知層 Perception Layer 
   ↓
候選層 Candidate Layer
   ↓
認知層 Cognition Layer
   ↓
UI Render / Popup


🦉 NewCoolOwl 版本沿革
🪶 0.1 — 概念原型期（2025/10/25）

副標題：本地化的第一聲啼鳴

開始構思「新酷鷹（NewCoolOwl）」名稱。

明確確立主題：「AI 輔助的中文輸入法外掛」。

目標：讓輸入法能本地運作、不依賴雲端、可理解語境。

確立願景：「尊重語言主權、創造屬於台灣的智慧輸入法」。

⚙️ 0.2 — 架構成形期（2025/10/26-10/28）

副標題：環境重建與骨架誕生

成功建立專案結構：core/, models/, tests/, README.md。

設定 Python 環境、安裝 text-generation-webui。

初次測試模型（TAIDE-LX-7B-Chat-4bit）。

建立本地執行的第一個 Python 入口檔 (input_listener_combined.py)。

能夠偵測輸入、回傳模型候選詞。

🧩 0.3 — 授權與倫理期（2025/10/29）

副標題：License + Ethics 立法階段

寫入 LICENSE-ETHICS.txt，組合 Apache 2.0 + 人格語言倫理條款。

🚀 1.0 — MVP 完成期（2025/10/29）

副標題：學習開關（Learning Button）誕生

實現 最小可行版本（MVP）。

Flask 為核心，模型透過 REST API 回傳候選詞。

介面能顯示「候選詞 UI」。

新增 學習開關（Learning ON/OFF），代表：

ON：學習使用者選擇；

OFF：不記錄、不改變模型。

NCO 1.0 定義為「開源教育範例」，教人理解 LLM + 輸入法整合的可能性。