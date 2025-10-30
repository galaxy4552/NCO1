# NewCoolOwl/server.py
from flask import Flask, request, jsonify
import time, random

app = Flask(__name__)

@app.route("/v1/completions", methods=["POST"])
def completions():
    """
    模擬本地 AI API（或轉發到 text-generation-webui）
    """
    data = request.get_json(force=True)
    prompt = data.get("prompt", "")
    model = data.get("model", "mock-model")
    phase = "early" if "[EARLY" in prompt else "final"

    # ✨ 這裡可以改成轉發到 text-generation-webui 的 7860 API
    # resp = requests.post("http://127.0.0.1:7860/api/v1/generate", json=data)
    # return jsonify(resp.json())

    # 現階段先用模擬回覆
    replies = [
        "好的～", "了解！", "沒問題。", "我明白你的意思。", "可以的。"
    ]
    reply_text = random.choice(replies)
    print(f"[Server] ({phase}) 收到: {prompt[:20]}... → 回覆: {reply_text}")
    # time.sleep(0.5)
    return jsonify({
        "choices": [{"text": reply_text}],
        "model": model
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
