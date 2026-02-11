---
summary: "24. 直接运行 `openclaw agent` CLI（可选投递）"
read_when:
  - 25. 添加或修改代理 CLI 入口点
title: "Agent Send"
---

# `openclaw agent`（直接运行 agent）

28. `openclaw agent` 运行单个代理回合，无需入站聊天消息。
29. 默认情况下它**通过 Gateway** 运行；添加 `--local` 以强制使用当前机器上的嵌入式运行时。

## 30. 行为

- 31. 必需：`--message <text>`
- 32. 会话选择：
  - 33. `--to <dest>` 派生会话键（群组/频道目标保持隔离；直接聊天会折叠为 `main`），**或**
  - 34. `--session-id <id>` 通过 id 重用现有会话，**或**
  - 35. `--agent <id>` 直接指向已配置的代理（使用该代理的 `main` 会话键）
- 36. 运行与正常入站回复相同的嵌入式代理运行时。
- 37. 思考/详细标志会持久化到会话存储中。
- 38. 输出：
  - 默认：打印回复文本（以及 `MEDIA:<url>` 行）
  - 40. `--json`：打印结构化负载 + 元数据
- 41. 可选地使用 `--deliver` + `--channel` 将回复投递回频道（目标格式与 `openclaw message --target` 匹配）。
- 42. 使用 `--reply-channel`/`--reply-to`/`--reply-account` 在不更改会话的情况下覆盖投递设置。

43. 如果 Gateway 无法访问，CLI 会**回退**到嵌入式本地运行。

## 44. 示例

```bash
45. openclaw agent --to +15555550123 --message "status update"
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --to +15555550123 --message "Trace logs" --verbose on --json
openclaw agent --to +15555550123 --message "Summon reply" --deliver
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
```

## 46. 标志

- 47. `--local`：本地运行（需要在 shell 中配置模型提供商 API 密钥）
- 48. `--deliver`：将回复发送到选定的频道
- 49. `--channel`：投递频道（`whatsapp|telegram|discord|googlechat|slack|signal|imessage`，默认：`whatsapp`）
- 50. `--reply-to`：投递目标覆盖
- `--reply-channel`：投递渠道覆盖
- `--reply-account`：投递账号 ID 覆盖
- `--thinking <off|minimal|low|medium|high|xhigh>`：持久化思考级别（仅限 GPT-5.2 + Codex 模型）
- `--verbose <on|full|off>`：持久化详细程度级别
- `--timeout <seconds>`：覆盖 agent 超时时间
- `--json`：输出结构化 JSON
