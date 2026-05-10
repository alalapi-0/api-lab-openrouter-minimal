# LEARNING — api-lab-openrouter-minimal

> 这份文件回答：「我跑完这个仓库，应该真的学到什么？」
> README 负责"怎么跑"，本文件负责"为什么跑、跑完该看什么、自己有没有真懂"。

## 你跑完应该能回答的问题

1. 什么是「网关型」LLM 服务？OpenRouter 这种"中间层"和直接调 OpenAI / Anthropic 有什么区别？
2. 为什么我只改一行 `OPENROUTER_MODEL`，底层就能切到完全不同的厂商（OpenAI、Anthropic、DeepSeek……）？
3. `base_url`、`api_key`、`model` 在一次 LLM 调用里各自承担什么职责？
4. OpenAI-compatible 是 OpenAI 的"专利"还是"事实标准"？

## 实操验证清单（务必动手）

### 阶段 A — 环境就绪
- [ ] `cp .env.example .env`
- [ ] `pip install -r requirements.txt`
- [ ] 在 OpenRouter 控制台拿到一个 `sk-or-v1-...`，填进 `.env` 的 `OPENROUTER_API_KEY`
- [ ] 在 OpenRouter 模型市场挑一个**便宜**的模型名（如 `openai/gpt-4o-mini`），填进 `OPENROUTER_MODEL`

### 阶段 B — 跑通最小调用
- [ ] `python3 main.py`
- [ ] 看到「[成功] 模型返回内容」并打印中文回答
- [ ] `cat output/result.json` 看完整结构化结果（注意 `model` 字段）

### 阶段 C — 关键观察（不做这步等于没学）
- [ ] **替换模型不替换代码**：把 `OPENROUTER_MODEL` 换成另一家厂商的模型名（如 `anthropic/claude-3.5-haiku`），**不改任何 .py**，再跑一次 → 你应该看到回答风格变化但代码完全没动
- [ ] **观察请求形状**：如果你装了 `mitmproxy` 或类似抓包工具，看 OpenRouter 收到的请求和它转发给底层厂商的请求差别（不强制，但有助理解"网关"职责）
- [ ] **故意写错 model 名**：比如 `OPENROUTER_MODEL=this/does-not-exist`，再跑 → 应该看到 HTTP 404 / model not found 的清晰报错（验证脚本"不会瞎重试"）
- [ ] **故意写错 key**：在 key 后面加几个字符 → 应该看到 HTTP 401，而不是程序崩溃

## 自检题（不查文档自己答一遍）

1. 如果 OpenRouter 是个"网关"，为什么我还是要跟它要钱（购买 credits）？它跟底层厂商之间是怎么结算的？
2. 同一个 prompt，分别用 `OPENROUTER_MODEL=openai/gpt-4o-mini` 和 `openai/gpt-4o`，回答会有差别吗？哪些差别是模型本身的，哪些是 OpenRouter 加的？
3. 如果我有自己的 OpenAI key，**不**通过 OpenRouter，能直接跑通这份 `main.py` 吗？需要怎么改？（提示：只改 `.env` 三个变量）
4. 如果我把 `OPENROUTER_BASE_URL` 改成一个不存在的域名，超时会发生在 30 秒之内吗？为什么？

## 与其它仓库的连接

| 关系 | 仓库 | 为什么去看 |
| --- | --- | --- |
| **同协议、不同供应商** | `api-lab-openai-compatible-minimal` | 同一份代码，把 `AI_BASE_URL` 指向 OpenRouter / DeepSeek / LM Studio 都能跑——这就是"OpenAI-compatible 是协议"的最直接证据 |
| **不同协议** | `api-lab-anthropic-minimal` | 走 Anthropic 原生协议，请求/响应字段完全不同。回头你会更深刻地理解"OpenRouter 帮你抹平了什么" |
| **不同协议** | `api-lab-gemini-minimal` | Google 的第三套协议；OpenRouter 把它也包成了 `chat/completions` |
| **下一步进阶** | `api-lab-tool-calling-minimal` | 在 OpenAI-compatible 基础上加"工具调用意图"，是 Agent 的雏形 |

## 你应该感受到的"啊哈"瞬间

- 当你只改 `.env` 不改 `.py`，回答风格从一家变到另一家——**这就是"协议抽象"在帮你省掉适配代码**。
- 当你看到 OpenRouter 返回的 `model` 字段，发现里面包含厂商前缀（如 `openai/`、`anthropic/`）——**这就是"网关"的小心机**。
