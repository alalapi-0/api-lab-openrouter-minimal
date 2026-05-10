# api-lab-openrouter-minimal

> 最小化体验：用 OpenRouter 调用一次聊天模型。

## 它在做什么

OpenRouter 是一个聚合多家 LLM 服务商的网关，提供 **OpenAI-compatible** 的 `/chat/completions` 接口。
本仓库做且只做一件事：

1. 从 `.env` 读取 `OPENROUTER_API_KEY` / `OPENROUTER_BASE_URL` / `OPENROUTER_MODEL`
2. 用 `requests` 发起一次 POST 到 `{base_url}/chat/completions`
3. 把返回的文本打印出来，并写入 `output/result.json`

## 为什么这样设计

- **不写死 API Key**：所有密钥从环境变量读，`.env` 已在 `.gitignore` 中。
- **不写死模型名**：`OPENROUTER_MODEL` 必须由你填，避免我编造你账户里不存在的模型名。
- **只发一次请求 + max_tokens=80**：避免在你试错时浪费额度。
- **不重试**：失败就停下，由你看错误信息。

## 运行步骤

```bash
cd api-lab-openrouter-minimal
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# 编辑 .env：
#   OPENROUTER_API_KEY=sk-or-v1-...
#   OPENROUTER_MODEL=openai/gpt-4o-mini   （示例，请用你账户可用的）

python3 main.py
cat output/result.json
```

## 常见报错

| 终端打印 | 可能原因 | 怎么处理 |
| --- | --- | --- |
| `未在 .env 中检测到 OPENROUTER_API_KEY` | `.env` 没创建或 key 没填 | `cp .env.example .env` 后填 key |
| `HTTP 401` | API Key 无效或写错 | 去 OpenRouter 后台重新生成 key |
| `HTTP 402` / 余额不足 | OpenRouter 账户没余额 | 去 OpenRouter 充值或换模型 |
| `HTTP 404` model not found | 模型名写错了 | 在 OpenRouter 模型市场找一个你账户可用的模型名 |
| `HTTP 429` | 限流 | 等几秒再试，不要循环重试 |
| `请求超时（30s）` | 网络不通或被墙 | 检查网络 / 代理，不要反复重试 |

## .env.example

```
OPENROUTER_API_KEY=填入你的OpenRouter API Key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=请填入你账户可用的模型名
```

## 输出位置

成功后：

- 终端打印模型回答与耗时
- `output/result.json`：完整结构化结果（**不提交到 git**）

## 不会做的事

- 不会自动重试
- 不会打印 API Key
- 不会下载额外模型
- 不会把 `.env` 提交到 git
