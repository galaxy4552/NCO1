# auto_adapt.py
import json

def load_profile():
    with open("user_profile.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_context(mode="chat"):
    p = load_profile()
    return f"你是 {p['name']}。現在進入「{mode}」模式：{p['modes'][mode]}\n"

if __name__ == "__main__":
    print(get_context("work"))


# 使用範例：
# context = get_context("work")
# reply = ask_llm("幫我整理今日代辦", context=context)
