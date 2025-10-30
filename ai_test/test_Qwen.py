# test_Qwen.py
import argparse
import os
import time
import torch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", type=str, required=True, help="Local path to model folder")
    parser.add_argument("--prompt", type=str, default="Describe the final light of Owlsoft in poetic English.")
    parser.add_argument("--max-new-tokens", type=int, default=120)
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--repetition-penalty", type=float, default=1.1)
    args = parser.parse_args()

    print(f"🔧 CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"🧠 GPU: {torch.cuda.get_device_name(0)}  |  VRAM: {round(torch.cuda.get_device_properties(0).total_memory/1024**3, 2)} GB")

    # 延後匯入，讓錯誤訊息更聚焦
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from auto_gptq import AutoGPTQForCausalLM

    model_dir = os.path.abspath(args.model_dir)
    if not os.path.isdir(model_dir):
        raise FileNotFoundError(f"Model dir not found: {model_dir}")

    # 嘗試以 Transformers 直接載入（多數 Qwen2.5 皆可）
    model = None
    tok = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

    try:
        # dtype 由 transformers 近期版本採用；舊版會忽略此參數
        model = AutoModelForCausalLM.from_pretrained(
            model_dir,
            trust_remote_code=True,
            device_map="auto",   # 自動放到 GPU/CPU
            dtype="auto"
        )
        backend = "transformers"
    except Exception as e:
        # 若是 GPTQ 專案，可能需要 AutoGPTQ；做一次降級嘗試
        print(f"⚠️ Transformers load failed: {e}\nTrying AutoGPTQ fallback…")
        try:
            model = AutoGPTQForCausalLM.from_quantized(
            model_dir,
            device="cuda:0" if torch.cuda.is_available() else "cpu",
            trust_remote_code=True,
            use_safetensors=True,
            quantize_config_file="quantization_config.json"  # 🔹 新版名稱
        )

            backend = "auto-gptq"
        except Exception as e2:
            raise RuntimeError(f"Failed to load model with both Transformers and AutoGPTQ.\n"
                               f"Install auto-gptq if this is a GPTQ/Int4 model: pip install auto-gptq\nError: {e2}")

    # 準備 Prompt（避免 “Answer:” 觸發早停，並加 English-only 指示）
    system = "### Instruction: Answer in natural, fluent English only."
    user = args.prompt.strip()
    prompt = f"{system}\n### Input:\n{user}\n\n### Response:\n"

    inputs = tok(prompt, return_tensors="pt").to(model.device)

    gen_kwargs = dict(
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        do_sample=True,
        top_p=args.top_p,
        repetition_penalty=args.repetition_penalty,
        pad_token_id=tok.eos_token_id or tok.pad_token_id or 0,
        eos_token_id=tok.eos_token_id or tok.pad_token_id or 0,
        min_new_tokens=20,   # 強制至少生成一些內容，避免空輸出
    )

    torch.set_grad_enabled(False)
    t0 = time.time()
    outputs = model.generate(**inputs, **gen_kwargs)
    dt = time.time() - t0

    text = tok.decode(outputs[0], skip_special_tokens=True)
    # 只取「### Response:」之後的內容
    if "### Response:" in text:
        text = text.split("### Response:", 1)[-1].strip()

    gen_tokens = outputs.shape[1] - inputs["input_ids"].shape[1]
    tok_per_s = gen_tokens / dt if dt > 0 else 0.0

    print("\n===== RESULT =====")
    print(text)
    print("\n===== STATS =====")
    print(f"Backend: {backend}")
    print(f"Generated tokens: {gen_tokens}")
    print(f"Time: {dt:.2f}s  |  Speed: {tok_per_s:.2f} tok/s")

if __name__ == "__main__":
    main()
