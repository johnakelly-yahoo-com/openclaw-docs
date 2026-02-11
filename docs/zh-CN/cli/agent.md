---
summary: "CLI reference for `openclaw agent` (send one agent turn via the Gateway)"
read_when:
  - 你希望从脚本中运行一次 agent 回合（可选择投递回复）
title: "agent"
---

# `openclaw agent`

通过 Gateway 运行一次 agent 回合（嵌入式使用 `--local`）。
Use `--agent <id>` to target a configured agent directly.

相关：

- Agent 发送工具：[Agent send](/tools/agent-send)

## 示例

```bash
openclaw agent --to +15555550123 --message "status update" --deliver
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
```
