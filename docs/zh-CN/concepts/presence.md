---
summary: "How OpenClaw presence entries are produced, merged, and displayed"
read_when:
  - Debugging the Instances tab
  - Investigating duplicate or stale instance rows
  - Changing gateway WS connect or system-event beacons
title: "Presence"
---

# Presence

OpenClaw “presence” is a lightweight, best‑effort view of:

- the **Gateway** itself, and
- **clients connected to the Gateway** (mac app, WebChat, CLI, etc.)

Presence is used primarily to render the macOS app’s **Instances** tab and to
provide quick operator visibility.

## Presence fields (what shows up)

Presence entries are structured objects with fields like:

- `instanceId` (optional but strongly recommended): stable client identity (usually `connect.client.instanceId`)
- `host`: human‑friendly host name
- `ip`: best‑effort IP address
- `version`: client version string
- `deviceFamily` / `modelIdentifier`: hardware hints
- `mode`: `ui`, `webchat`, `cli`, `backend`, `probe`, `test`, `node`, ...
- `lastInputSeconds`: “seconds since last user input” (if known)
- `reason`: `self`, `connect`, `node-connected`, `periodic`, ...
- `ts`: last update timestamp (ms since epoch)

## Producers (where presence comes from)

Presence entries are produced by multiple sources and **merged**.

### 1. Gateway self entry

The Gateway always seeds a “self” entry at startup so UIs show the gateway host
even before any clients connect.

### 2. WebSocket connect

Every WS client begins with a `connect` request. On successful handshake the
Gateway upserts a presence entry for that connection.

#### 1. 为什么一次性的 CLI 命令不会显示

2. CLI 通常用于短暂的一次性命令连接。 3. 为了避免刷屏
   Instances 列表，`client.mode === "cli"` **不会** 被转换为 presence 条目。

### 4. 3. `system-event` 信标

5. 客户端可以通过 `system-event` 方法发送更丰富的周期性信标。 6. mac
   应用使用它来上报主机名、IP 以及 `lastInputSeconds`。

### 7. 4. Node 连接（角色：node）

8. 当一个 node 通过 Gateway WebSocket 以 `role: node` 连接时，Gateway 会为该 node 执行 presence 条目的 upsert（流程与其他 WS 客户端相同）。

## 9. 合并 + 去重规则（为什么 `instanceId` 很重要）

10. Presence 条目存储在一个单一的内存 Map 中：

- 11. 条目以 **presence key** 作为键。
- 12. 最佳的 key 是稳定的 `instanceId`（来自 `connect.client.instanceId`），可在重启后保持不变。
- 13. Key 不区分大小写。

15. 如果客户端在没有稳定 `instanceId` 的情况下重新连接，可能会显示为一条**重复**记录。

## 15. TTL 与有界大小

16. Presence 被刻意设计为短暂存在：

- 17. **TTL：** 超过 5 分钟的条目会被清理
- 16. **最大条目数：** 200（最旧的优先丢弃）

17. 这可以保持列表新鲜，并避免内存无限增长。

## 20. 远程 / 隧道注意事项（回环 IP）

21. 当客户端通过 SSH 隧道 / 本地端口转发连接时，Gateway 可能会将远端地址视为 `127.0.0.1`。 22. 为了避免覆盖客户端自行上报的有效 IP，会忽略回环的远端地址。

## 23. 使用方

### 24. macOS Instances 标签页

25. macOS 应用会渲染 `system-presence` 的输出，并根据最近一次更新的时间应用一个小的状态指示器（Active/Idle/Stale）。

## 26. 调试提示

- 27. 要查看原始列表，请对 Gateway 调用 `system-presence`。
- 28. 如果你看到重复项：
  - 29. 确认客户端在握手时发送了稳定的 `client.instanceId`
  - 30. 确认周期性信标使用的是相同的 `instanceId`
  - 31. 检查是否由连接派生的条目缺少 `instanceId`（这种情况下出现重复是预期的）
