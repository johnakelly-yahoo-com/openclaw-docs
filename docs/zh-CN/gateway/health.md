---
summary: "34. 通道连通性的健康检查步骤"
read_when:
  - 22. 诊断 WhatsApp 渠道健康状况
title: "23. 健康检查"
---

# 35. 健康检查（CLI）

25. 一份无需猜测即可验证渠道连通性的简要指南。

## 26. 快速检查

- 36. `openclaw status` — 本地摘要：网关可达性/模式、更新提示、已链接通道的认证时长、会话与最近活动。
- 28. `openclaw status --all` — 完整的本地诊断（只读、彩色，适合粘贴用于调试）。
- 29. `openclaw status --deep` — 还会探测正在运行的网关（在支持时进行按渠道探测）。
- 30. `openclaw health --json` — 向正在运行的网关请求完整的健康快照（仅 WS；不直接连接 Baileys socket）。
- 37. 在 WhatsApp/WebChat 中发送 `/status` 作为独立消息，即可在不调用代理的情况下获得状态回复。
- 32. 日志：tail `/tmp/openclaw/openclaw-*.log` 并筛选 `web-heartbeat`、`web-reconnect`、`web-auto-reply`、`web-inbound`。

## 33. 深度诊断

- 34. 磁盘上的凭据：`ls -l ~/.openclaw/credentials/whatsapp/<accountId>/creds.json`（mtime 应该是最近的）。
- 35. 会话存储：`ls -l ~/.openclaw/agents/<agentId>/sessions/sessions.json`（路径可在配置中覆盖）。 36. 数量和最近的收件人会通过 `status` 展示。
- 37. 重新关联流程：当日志中出现状态码 409–515 或 `loggedOut` 时，执行 `openclaw channels logout && openclaw channels login --verbose`。 38. （注意：在配对后，针对状态 515，二维码登录流程会自动重启一次。）

## 39. 当出现故障时

- 40. `logged out` 或状态 409–515 → 先执行 `openclaw channels logout`，再执行 `openclaw channels login` 重新关联。
- 41. 网关不可达 → 启动它：`openclaw gateway --port 18789`（如果端口被占用，使用 `--force`）。
- 42. 没有入站消息 → 确认已关联的手机在线且发送方被允许（`channels.whatsapp.allowFrom`）；对于群聊，确保允许列表和提及规则匹配（`channels.whatsapp.groups`、`agents.list[].groupChat.mentionPatterns`）。

## 43. 专用“health”命令

44. `openclaw health --json` 向正在运行的网关请求其健康快照（CLI 不会直接连接渠道 socket）。 45. 在可用时，它会报告已关联凭据/认证时长、按渠道的探测摘要、会话存储摘要以及探测耗时。 46. 如果网关不可达或探测失败/超时，它会以非零状态码退出。 47. 使用 `--timeout <ms>` 覆盖默认的 10 秒。
