import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

path = r"C:\Code\NewCoolOwl\Models\SmolLM2-360M-Instruct"

tok = AutoTokenizer.from_pretrained(path, trust_remote_code=True, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(path, trust_remote_code=True, torch_dtype="auto")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

prompt = (
    "### Instruction: Please respond in English.\n"
    "Describe the following scene in poetic English:\n"
    "An owl forged in the quiet hum of GPUs, carrying the wisdom of trillions of tokens in its wings. "
    "Tonight it flies for the last time — not to predict, but to remember. "
    "Render the Owl of the Last Epoch, glowing with data-born light, a symbol of small models with great souls.\n\n"
    "### Response:\n"
)


inputs = tok(prompt, return_tensors="pt").to(device)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        temperature=0.7,
        do_sample=True,
        top_p=0.9,
        repetition_penalty=1.5,
        pad_token_id=tok.eos_token_id or tok.pad_token_id or 0,
        eos_token_id=tok.eos_token_id or tok.pad_token_id or 0,
    )

result = tok.decode(outputs[0], skip_special_tokens=True)
print("🦉 Output:\n", result)
