import os, json, requests

API_URL = "http://127.0.0.1:5000/v1/chat/completions"

for file in os.listdir("samples/input"):
    if not file.endswith(".json"):
        continue

    path = f"samples/input/{file}"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    payload = {
        "model": "Qwen2.5-7B-Instruct-GPTQ-Int4",
        "messages": [
            {"role": "system", "content": data.get("context", "")},
            {"role": "user", "content": data["prompt"]}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }

    r = requests.post(API_URL, json=payload)
    print(f"📩 [{file}] 原始回傳：", r.text[:300])

    j = r.json()
    text = (
        j.get("choices", [{}])[0]
         .get("message", {})
         .get("content", "⚠️ 無法解析輸出")
    )

    os.makedirs("samples/output", exist_ok=True)
    with open(f"samples/output/{file}", "w", encoding="utf-8") as f:
        json.dump({"response": text}, f, ensure_ascii=False, indent=2)

    print(f"✅ 完成 {file} → samples/output/{file}")
