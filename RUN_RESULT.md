# RUN_RESULT

| 字段 | 值 |
| --- | --- |
| 真实 OpenRouter 运行 | 否 |
| 离线契约验证 | 通过（2026-08-12） |
| 验证模型占位名 | `test/model` |
| 真实请求耗时 | — |
| 未运行原因 | 未读取或配置 OpenRouter 凭据，且没有获准进行付费或外部 API 调用 |

## 验证范围

在一次性的 `git archive` 副本中，以内存桩替代 `requests` 和 `python-dotenv`，验证了：

- 缺少 API key 或模型名时返回退出码 2，且不发起请求；
- OpenRouter URL、Bearer 头、模型、消息、`max_tokens` 与超时参数符合契约；
- 成功响应会生成预期的 `output/result.json`；
- HTTP 429 与畸形成功响应均返回退出码 1；
- `main.py` 通过 Python 语法编译检查。

验证结束后已移除一次性副本。桩响应与耗时不代表真实 OpenRouter 模型、账户额度或网络可用性。
