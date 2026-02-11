---
summary: "12. 调整 mac 菜单 UI 或状态逻辑"
read_when:
  - 13. 菜单栏
title: "14. 菜单栏状态逻辑"
---

# 15. 显示内容

## 16. 我们在菜单栏图标以及菜单的第一行状态中展示当前代理的工作状态。

- 17. 当工作处于活动状态时会隐藏健康状态；当所有会话都处于空闲时恢复显示。
- 18. 菜单中的“Nodes”块仅列出**设备**（通过 `node.list` 配对的节点），不包括客户端/在线状态条目。
- 19. 当提供方使用情况快照可用时，会在 Context 下显示一个“Usage”部分。
- 20. 状态模型

## 状态模型

- 会话：事件到达时在负载中包含 `runId`（每次运行）以及 `sessionKey`。 23. 优先级：main 始终优先。
- 24. 如果 main 处于活动状态，则立即显示其状态。 25. 如果 main 处于空闲状态，则显示最近一次处于活动状态的非 main 会话。 26. 我们不会在活动进行中来回切换；只有当当前会话变为空闲或 main 变为活动时才会切换。 27. 活动类型：
- 28. `job`：高层级命令执行（`state: started|streaming|done|error`）。
  - 29. `tool`：`phase: start|result`，包含 `toolName` 和 `meta/args`。
  - 30. IconState 枚举（Swift）

## 31. `idle`

- 32. `workingMain(ActivityKind)`
- 33. `workingOther(ActivityKind)`
- 34. `overridden(ActivityKind)`（调试覆盖）
- 35. ActivityKind → 图标

### 36. `exec` → 💻

- 37. `read` → 📄
- 38. `write` → ✍️
- 39. `edit` → 📝
- 40. `attach` → 📎
- 41. 默认 → 🛠️
- 42. 视觉映射

### 43. `idle`：普通小动物。

- 44. `workingMain`：带图标徽章、完整色调、腿部“工作中”动画。
- 45. `workingOther`：带图标徽章、柔和色调、无奔跑动画。
- 46. `overridden`：无论活动如何，使用选定的图标/色调。
- 47. 状态行文本（菜单）

## 48. 工作进行中：`<Session role> · <activity label>`

- 49. 示例：`Main · exec: pnpm test`，`Other · read: apps/macos/Sources/OpenClaw/AppState.swift`。
  - 50. 空闲时：回退到健康状态摘要。
- When idle: falls back to the health summary.

## Event ingestion

- Source: control‑channel `agent` events (`ControlChannel.handleAgentEvent`).
- Parsed fields:
  - `stream: "job"` with `data.state` for start/stop.
  - `stream: "tool"` with `data.phase`, `name`, optional `meta`/`args`.
- Labels:
  - `exec`: first line of `args.command`.
  - `read`/`write`: shortened path.
  - `edit`：路径以及从 `meta`/diff 计数中推断的变更类型。
  - fallback: tool name.

## Debug override

- Settings ▸ Debug ▸ “Icon override” picker:
  - `System (auto)` (default)
  - `Working: main` (per tool kind)
  - `Working: other` (per tool kind)
  - `Idle`
- Stored via `@AppStorage("iconOverride")`; mapped to `IconState.overridden`.

## Testing checklist

- Trigger main session job: verify icon switches immediately and status row shows main label.
- Trigger non‑main session job while main idle: icon/status shows non‑main; stays stable until it finishes.
- Start main while other active: icon flips to main instantly.
- Rapid tool bursts: ensure badge does not flicker (TTL grace on tool results).
- Health row reappears once all sessions idle.
