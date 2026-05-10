"""api-lab-openrouter-minimal

最小化地体验一次 OpenRouter 聊天 API 调用。
- 所有配置都从 .env 读取，绝不硬编码 API Key。
- 只发起一次请求，max_tokens 很小，避免浪费额度。
- 失败时打印清晰的中文提示，不重试。
"""

import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

PROMPT = "请用三句话解释什么是 API。"
TIMEOUT_SECONDS = 30
MAX_TOKENS = 80


def main() -> int:
    load_dotenv()

    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
    model = os.getenv("OPENROUTER_MODEL", "").strip()

    if not api_key:
        print("[错误] 未在 .env 中检测到 OPENROUTER_API_KEY。")
        print("       请先执行: cp .env.example .env，然后在 .env 中填入真实 key。")
        return 2
    if not model:
        print("[错误] 未在 .env 中检测到 OPENROUTER_MODEL。")
        print("       请在 .env 中填入你账户可用的模型名（例如 openai/gpt-4o-mini）。")
        return 2

    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": MAX_TOKENS,
    }

    print(f"[信息] endpoint = {url}")
    print(f"[信息] model    = {model}")
    print(f"[信息] prompt   = {PROMPT}")

    started = time.time()
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT_SECONDS)
    except requests.exceptions.Timeout:
        print(f"[失败] 请求超时（{TIMEOUT_SECONDS}s）。可能是网络或服务商限流。")
        return 1
    except requests.exceptions.RequestException as exc:
        print(f"[失败] 网络请求异常: {exc}")
        return 1
    elapsed = time.time() - started

    if resp.status_code != 200:
        print(f"[失败] HTTP {resp.status_code}")
        print(f"        响应片段: {resp.text[:300]}")
        print("        常见原因: API Key 无效 / 模型名错 / 余额不足 / 当前地区不可用。")
        return 1

    try:
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        print("[失败] 响应结构不符合 OpenAI-compatible /chat/completions 预期。")
        print(f"        原始响应片段: {resp.text[:300]}")
        return 1

    print()
    print("[成功] 模型返回内容：")
    print(content)
    print()
    print(f"[信息] 耗时 {elapsed:.2f}s")

    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(exist_ok=True)
    result = {
        "provider": "openrouter",
        "model": model,
        "base_url": base_url,
        "prompt": PROMPT,
        "elapsed_seconds": round(elapsed, 3),
        "content": content,
    }
    out_file = out_dir / "result.json"
    out_file.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[信息] 已写入 {out_file}（不会被 git 提交）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
