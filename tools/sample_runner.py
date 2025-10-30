import os, json, requests

API_URL = "http://127.0.0.1:7860/api/v1/chat"

for file in os.listdir("samples/input"):
    if not file.endswith(".json"):
        continue

    path = f"samples/input/{file}"
    if os.path.getsize(path) == 0:
        print(f"⚠️ 跳過空檔：{file}")
        continue

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"⚠️ JSON 格式錯誤：{file}")
        continue

    payload = {
        "prompt": f"{data['context']}\n{data['prompt']}",
        "max_new_tokens": 200,
        "temperature": 0.7
    }

    r = requests.post(API_URL, json=payload)
    print("📩 原始回傳：", r.text)
    text = r.json()["results"][0]["text"]

    out = {
        "model": "Qwen2.5-7B-Instruct-GPTQ-Int4",
        "response": text
    }

    os.makedirs("samples/output", exist_ok=True)
    with open(f"samples/output/{file}", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"✅ 完成 {file} → samples/output/{file}")
