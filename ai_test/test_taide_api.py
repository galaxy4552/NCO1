# file: test_taide_api.py
import os
import json
import requests

# 依啟動日誌調這個埠號：常見為 5000 或 7860
BASE_URL = os.getenv("TAIDE_API_BASE", "http://127.0.0.1:5000/v1")
MODEL = os.getenv("TAIDE_MODEL", "TAIDE-LX-7B-Chat-4bit")

def chat_once(system_msg: str, user_msg: str, max_tokens: int = 64):
    url = f"{BASE_URL}/chat/completions"
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user",   "content": user_msg}
        ],
        "max_tokens": max_tokens,
        # 需要可自行加入：temperature、top_p、stop、frequency_penalty...
    }
    r = requests.post(url, json=payload, timeout=20)
    r.raise_for_status()
    data = r.json()
    # 取文字與用量
    content = data["choices"][0]["message"]["content"]
    usage   = data.get("usage", {})
    return content, usage

if __name__ == "__main__":
    try:
        text, usage = chat_once(
            system_msg="你是台灣中文助手，請以繁體中文回答。",
            user_msg="你好，台灣！"
        )
        print("=== 回覆 ===")
        print(text)
        if usage:
            print("\n=== 用量 ===")
            print(json.dumps(usage, ensure_ascii=False, indent=2))
    except requests.ConnectionError as e:
        print("❌ 連不上 API：請確認 WebUI 有用 --api 啟動，且埠號正確。")
        print(e)
    except requests.HTTPError as e:
        print("❌ HTTP 錯誤：可能路徑不對（/v1/chat/completions），或 payload 不合。")
        print(e.response.status_code, e.response.text)
    except Exception as e:
        print("❌ 其他錯誤：")
        print(repr(e))
        
#想改埠號或模型名，也可暫時用環境變數：
#set TAIDE_API_BASE=http://127.0.0.1:7860/v1
#set TAIDE_MODEL=TAIDE-LX-7B-Chat-4bit