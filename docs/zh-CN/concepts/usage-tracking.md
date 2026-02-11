---
summary: "用量跟踪展示与凭据要求"
read_when:
  - 你正在接线提供方的用量/配额展示
  - 你需要解释用量跟踪行为或认证要求
title: "用量跟踪"
---

# 用量跟踪

## 它是什么

- 直接从提供方的用量端点拉取用量/配额。
- 不提供估算成本；仅使用提供方报告的时间窗口。

## 它显示在哪里

- `/status`（聊天中）：包含会话令牌 + 预估成本的表情符号丰富状态卡（仅 API key）。 在可用时，显示**当前模型提供方**的用量。
- `/usage off|tokens|full` in chats: per-response usage footer (OAuth shows tokens only).
- `/usage cost`（聊天中）：基于 OpenClaw 会话日志汇总的本地成本摘要。
- CLI：`openclaw status --usage` 打印完整的按提供方明细。
- CLI：`openclaw channels list` 在提供方配置旁打印相同的用量快照（使用 `--no-usage` 可跳过）。
- macOS 菜单栏：Context 下的“Usage”部分（仅在可用时）。

## 提供方 + 凭据

- **Anthropic（Claude）**：认证配置中的 OAuth 令牌。
- **GitHub Copilot**：认证配置中的 OAuth 令牌。
- **Gemini CLI**：认证配置中的 OAuth 令牌。
- **Antigravity**：认证配置中的 OAuth 令牌。
- **OpenAI Codex**：认证配置中的 OAuth 令牌（存在时使用 accountId）。
- **MiniMax**：API key（编码套餐密钥；`MINIMAX_CODE_PLAN_KEY` 或 `MINIMAX_API_KEY`）；使用 5 小时编码套餐窗口。
- **z.ai**: API key via env/config/auth store.

如果不存在匹配的 OAuth/API 凭据，则隐藏用量。
