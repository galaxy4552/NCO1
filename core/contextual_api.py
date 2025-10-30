# contextual_api.py
import requests

def ask_llm(prompt, context="", model="local"):
    if model == "local":
        payload = {
            "prompt": context + prompt,
            "max_new_tokens": 200,
            "temperature": 0.7
        }
        r = requests.post("http://127.0.0.1:5000/api/v1/chat", json=payload)
        data = r.json()
        return data["results"][0]["text"]
    else:
        raise ValueError("目前只支援 local Qwen")
