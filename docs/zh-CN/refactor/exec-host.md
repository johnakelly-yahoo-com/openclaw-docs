---
summary: "50. 重构计划：exec 主机路由、节点批准以及无头运行器。"
read_when:
  - Designing exec host routing or exec approvals
  - Implementing node runner + UI IPC
  - Adding exec host security modes and slash commands
title: "Exec Host Refactor"
---

# Exec host refactor plan

## Goals

- Add `exec.host` + `exec.security` to route execution across **sandbox**, **gateway**, and **node**.
- Keep defaults **safe**: no cross-host execution unless explicitly enabled.
- Split execution into a **headless runner service** with optional UI (macOS app) via local IPC.
- Provide **per-agent** policy, allowlist, ask mode, and node binding.
- Support **ask modes** that work _with_ or _without_ allowlists.
- Cross-platform: Unix socket + token auth (macOS/Linux/Windows parity).

## Non-goals

- No legacy allowlist migration or legacy schema support.
- No PTY/streaming for node exec (aggregated output only).
- No new network layer beyond the existing Bridge + Gateway.

## Decisions (locked)

- **Config keys:** `exec.host` + `exec.security` (per-agent override allowed).
- **Elevation:** keep `/elevated` as an alias for gateway full access.
- **Ask default:** `on-miss`.
- **Approvals store:** `~/.openclaw/exec-approvals.json` (JSON, no legacy migration).
- **Runner:** headless system service; UI app hosts a Unix socket for approvals.
- **Node identity:** use existing `nodeId`.
- **Socket auth:** Unix socket + token (cross-platform); split later if needed.
- **Node host state:** `~/.openclaw/node.json` (node id + pairing token).
- **macOS exec host:** run `system.run` inside the macOS app; node host service forwards requests over local IPC.
- **No XPC helper:** stick to Unix socket + token + peer checks.

## Key concepts

### Host

- `sandbox`: Docker exec (current behavior).
- `gateway`: exec on gateway host.
- `node`: exec on node runner via Bridge (`system.run`).

### Security mode

- `deny`: always block.
- `allowlist`: allow only matches.
- `full`: allow everything (equivalent to elevated).

### Ask mode

- `off`: never ask.
- `on-miss`: ask only when allowlist does not match.
- `always`: ask every time.

Ask is **independent** of allowlist; allowlist can be used with `always` or `on-miss`.

### Policy resolution (per exec)

1. Resolve `exec.host` (tool param → agent override → global default).
2. Resolve `exec.security` and `exec.ask` (same precedence).
3. If host is `sandbox`, proceed with local sandbox exec.
4. If host is `gateway` or `node`, apply security + ask policy on that host.

## Default safety

- Default `exec.host = sandbox`.
- Default `exec.security = deny` for `gateway` and `node`.
- Default `exec.ask = on-miss` (only relevant if security allows).
- 1. 如果未设置节点绑定，**agent 可以定位到任何节点**，但前提是策略允许。

## 2. 配置面

### 3. 工具参数

- 4. `exec.host`（可选）：`sandbox | gateway | node`。
- 5. `exec.security`（可选）：`deny | allowlist | full`。
- 6. `exec.ask`（可选）：`off | on-miss | always`。
- `exec.node` (optional): node id/name to use when `host=node`.

### Config keys (global)

- 9. `tools.exec.host`
- 10. `tools.exec.security`
- 11. `tools.exec.ask`
- 12. `tools.exec.node`（默认节点绑定）

### 13. 配置键（每个 agent）

- 14. `agents.list[].tools.exec.host`
- 15. `agents.list[].tools.exec.security`
- 16. `agents.list[].tools.exec.ask`
- 17. `agents.list[].tools.exec.node`

### 18. 别名

- 19. `/elevated on` = 为 agent 会话设置 `tools.exec.host=gateway`、`tools.exec.security=full`。
- 20. `/elevated off` = 为 agent 会话恢复之前的 exec 设置。

## 21. 审批存储（JSON）

22. 路径：`~/.openclaw/exec-approvals.json`

23. 目的：

- 24. 针对**执行主机**（gateway 或 node runner）的本地策略 + 允许列表。
- 25. 在没有 UI 可用时的询问回退机制。
- 26. UI 客户端的 IPC 凭据。

27. 建议的 schema（v1）：

```json
28. {
  "version": 1,
  "socket": {
    "path": "~/.openclaw/exec-approvals.sock",
    "token": "base64-opaque-token"
  },
  "defaults": {
    "security": "deny",
    "ask": "on-miss",
    "askFallback": "deny"
  },
  "agents": {
    "agent-id-1": {
      "security": "allowlist",
      "ask": "on-miss",
      "allowlist": [
        {
          "pattern": "~/Projects/**/bin/rg",
          "lastUsedAt": 0,
          "lastUsedCommand": "rg -n TODO",
          "lastResolvedPath": "/Users/user/Projects/.../bin/rg"
        }
      ]
    }
  }
}
```

29. 说明：

- 30. 不支持旧版 allowlist 格式。
- 31. `askFallback` 仅在需要 `ask` 且无法连接任何 UI 时适用。
- 32. 文件权限：`0600`。

## 33. Runner 服务（无头）

### 34. 角色

- 35. 在本地强制执行 `exec.security` + `exec.ask`。
- 36. 执行系统命令并返回输出。
- 37. 为 exec 生命周期发送 Bridge 事件（可选但推荐）。

### 38. 服务生命周期

- 39. macOS 上使用 Launchd/daemon；Linux/Windows 上使用系统服务。
- 40. 审批 JSON 仅存在于执行主机本地。
- 41. UI 托管本地 Unix socket；runner 按需连接。

## 42. UI 集成（macOS 应用）

### 43. IPC

- 44. Unix socket 位于 `~/.openclaw/exec-approvals.sock`（0600）。
- 45. Token 存储在 `exec-approvals.json` 中（0600）。
- 46. 对等检查：仅允许同一 UID。
- 47. 质询/响应：nonce + HMAC(token, request-hash)，用于防止重放。
- 48. 短 TTL（例如 10 秒）+ 最大负载 + 速率限制。

### 49. 询问流程（macOS 应用 exec 主机）

1. 50. 节点服务从 gateway 接收 `system.run`。
2. 1. Node 服务连接到本地 socket 并发送 prompt/exec 请求。
3. 2. App 校验对端 + token + HMAC + TTL，如有需要则显示对话框。
4. 3. App 在 UI 上下文中执行命令并返回输出。
5. 4. Node 服务将输出返回给网关。

5) 如果 UI 缺失：

- 6. 应用 `askFallback`（`deny|allowlist|full`）。

### 7. 架构图（SCI）

```
8. Agent -> Gateway -> Bridge -> Node Service（TS）
                         |  IPC（UDS + token + HMAC + TTL）
                         v
                     Mac App（UI + TCC + system.run）
```

## 9. Node 身份 + 绑定

- 10. 使用来自 Bridge 配对的现有 `nodeId`。
- 11. 绑定模型：
  - 12. `tools.exec.node` 将 agent 限制到特定的 node。
  - 13. 若未设置，agent 可选择任意 node（策略仍会强制默认值）。
- Node selection resolution:
  - 15. `nodeId` 精确匹配
  - 16. `displayName`（标准化）
  - 17. `remoteIp`
  - 18. `nodeId` 前缀（>= 6 个字符）

## 19. 事件机制

### 20. 谁能看到事件

- 21. 系统事件是**按会话**的，并在下一次提示时展示给 agent。
- 22. 存储在网关的内存队列中（`enqueueSystemEvent`）。

### 23. 事件文本

- 24. `Exec started (node=<id>, id=<runId>)`
- 25. `Exec finished (node=<id>, id=<runId>, code=<code>)` + 可选的输出尾部
- 26. `Exec denied (node=<id>, id=<runId>, <reason>)`

### 27. 传输

28. 方案 A（推荐）：

- 29. Runner 通过 Bridge 发送 `event` 帧 `exec.started` / `exec.finished`。
- 30. 网关的 `handleBridgeEvent` 将其映射为 `enqueueSystemEvent`。

31. 方案 B：

- 32. 网关的 `exec` 工具直接处理生命周期（仅限同步）。

## 33. Exec 流程

### 34. 沙箱主机

- 35. 现有的 `exec` 行为（Docker，或在未沙箱时使用宿主机）。
- 36. 仅在非沙箱模式下支持 PTY。

### 37. 网关主机

- 38. 网关进程在其自身机器上执行。
- 39. 强制执行本地 `exec-approvals.json`（security/ask/allowlist）。

### 40. Node 主机

- 41. 网关通过 `system.run` 调用 `node.invoke`。
- 42. Runner 强制执行本地审批。
- 43. Runner 返回聚合后的 stdout/stderr。
- 44. 可选的 Bridge 事件用于开始/完成/拒绝。

## 45. 输出上限

- 46. 将 stdout+stderr 的合并输出限制为 **200k**；事件中保留 **20k** 的尾部。
- 47. 使用清晰的后缀进行截断（例如，`"…` 48. （truncated）"）。

## 49. 斜杠命令

- 50. `/exec host=<sandbox|gateway|node> security=<deny|allowlist|full> ask=<off|on-miss|always> node=<id>`
- Per-agent, per-session overrides; non-persistent unless saved via config.
- `/elevated on|off|ask|full` remains a shortcut for `host=gateway security=full` (with `full` skipping approvals).

## Cross-platform story

- The runner service is the portable execution target.
- UI is optional; if missing, `askFallback` applies.
- Windows/Linux support the same approvals JSON + socket protocol.

## Implementation phases

### Phase 1: config + exec routing

- Add config schema for `exec.host`, `exec.security`, `exec.ask`, `exec.node`.
- Update tool plumbing to respect `exec.host`.
- Add `/exec` slash command and keep `/elevated` alias.

### Phase 2: approvals store + gateway enforcement

- Implement `exec-approvals.json` reader/writer.
- Enforce allowlist + ask modes for `gateway` host.
- Add output caps.

### Phase 3: node runner enforcement

- Update node runner to enforce allowlist + ask.
- Add Unix socket prompt bridge to macOS app UI.
- Wire `askFallback`.

### Phase 4: events

- Add node → gateway Bridge events for exec lifecycle.
- Map to `enqueueSystemEvent` for agent prompts.

### Phase 5: UI polish

- Mac app: allowlist editor, per-agent switcher, ask policy UI.
- Node binding controls (optional).

## Testing plan

- Unit tests: allowlist matching (glob + case-insensitive).
- Unit tests: policy resolution precedence (tool param → agent override → global).
- Integration tests: node runner deny/allow/ask flows.
- Bridge event tests: node event → system event routing.

## Open risks

- UI unavailability: ensure `askFallback` is respected.
- Long-running commands: rely on timeout + output caps.
- Multi-node ambiguity: error unless node binding or explicit node param.

## Related docs

- [Exec tool](/tools/exec)
- [Exec approvals](/tools/exec-approvals)
- [Nodes](/nodes)
- [Elevated mode](/tools/elevated)
