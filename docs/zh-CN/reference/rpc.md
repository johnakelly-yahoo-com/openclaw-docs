---
summary: "RPC adapters for external CLIs (signal-cli, legacy imsg) and gateway patterns"
read_when:
  - Adding or changing external CLI integrations
  - Debugging RPC adapters (signal-cli, imsg)
title: "RPC Adapters"
---

# RPC adapters

OpenClaw integrates external CLIs via JSON-RPC. Two patterns are used today.

## Pattern A: HTTP daemon (signal-cli)

- `signal-cli` runs as a daemon with JSON-RPC over HTTP.
- Event stream is SSE (`/api/v1/events`).
- Health probe: `/api/v1/check`.
- OpenClaw owns lifecycle when `channels.signal.autoStart=true`.

See [Signal](/channels/signal) for setup and endpoints.

## Pattern B: stdio child process (legacy: imsg)

> **Note:** For new iMessage setups, use [BlueBubbles](/channels/bluebubbles) instead.

- OpenClaw spawns `imsg rpc` as a child process (legacy iMessage integration).
- JSON-RPC is line-delimited over stdin/stdout (one JSON object per line).
- No TCP port, no daemon required.

Core methods used:

- 1. `watch.subscribe` → 通知（`method: "message"`）
- 2. `watch.unsubscribe`
- 3. `send`
- 4. `chats.list`（探测/诊断）

5. 有关传统设置和寻址（优先使用 `chat_id`），请参阅 [iMessage](/channels/imessage)。

## 6. 适配器指南

- 7. Gateway 拥有该进程（启动/停止与提供方生命周期绑定）。
- 8. 保持 RPC 客户端具备弹性：设置超时，在进程退出时重启。
- Prefer stable IDs (e.g., `chat_id`) over display strings.
