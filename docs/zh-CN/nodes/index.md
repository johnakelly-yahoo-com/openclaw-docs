---
summary: "Nodes: pairing, capabilities, permissions, and CLI helpers for canvas/camera/screen/system"
read_when:
  - 1. 将 iOS/Android 节点与网关配对
  - 2. 使用节点的画布/相机为代理提供上下文
  - 3. 添加新的节点命令或 CLI 辅助工具
title: "4. 节点"
---

# 5. 节点

6. **节点（node）** 是一种伴随设备（macOS/iOS/Android/无界面），它使用 `role: "node"` 连接到网关的 **WebSocket**（与操作员使用相同的端口），并通过 `node.invoke` 暴露一个命令接口（例如 `canvas.*`、`camera.*`、`system.*`）。 7. 协议详情：[Gateway protocol](/gateway/protocol)。

8. 旧版传输方式：[Bridge protocol](/gateway/bridge-protocol)（TCP JSONL；已弃用/在当前节点中移除）。

9. macOS 也可以以 **node mode** 运行：菜单栏应用连接到网关的 WS 服务器，并将其本地的画布/相机命令作为一个节点暴露（因此 `openclaw nodes …` 可以针对这台 Mac 工作）。

10. 说明：

- 11. 节点是 **外设**，不是网关。 12. 它们不运行网关服务。
- 13. Telegram/WhatsApp 等消息会到达 **网关**，而不是节点。
- 14. 故障排查手册：[/nodes/troubleshooting](/nodes/troubleshooting)

## 15. 配对与状态

16. **WS 节点使用设备配对。** 节点在 `connect` 期间提供设备身份；网关会为 `role: node` 创建一个设备配对请求。 17. 通过 devices CLI（或 UI）进行批准。

18. 快速 CLI：

```bash
19. openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
```

20. 说明：

- 21. 当设备配对角色包含 `node` 时，`nodes status` 会将该节点标记为 **paired**。
- 22. `node.pair.*`（CLI：`openclaw nodes pending/approve/reject`）是一个独立的、由网关拥有的节点配对存储；它**不会**限制 WS 的 `connect` 握手。

## 23. 远程节点主机（system.run）

24. 当你的网关运行在一台机器上，而你希望命令在另一台机器上执行时，请使用 **节点主机**。 25. 模型仍然与 **网关** 通信；当选择 `host=node` 时，网关会将 `exec` 调用转发给 **节点主机**。

### 26. 运行位置说明

- 27. **网关主机**：接收消息、运行模型、路由工具调用。
- 28. **节点主机**：在节点机器上执行 `system.run`/`system.which`。
- 29. **审批**：在节点主机上通过 `~/.openclaw/exec-approvals.json` 强制执行。

### 30. 启动节点主机（前台）

31. 在节点机器上：

```bash
32. openclaw node run --host <gateway-host> --port 18789 --display-name "Build Node"
```

### 33. 通过 SSH 隧道连接远程网关（回环绑定）

34. 如果网关绑定到回环地址（`gateway.bind=loopback`，本地模式下的默认值），远程节点主机将无法直接连接。 35. 创建一个 SSH 隧道，并让节点主机指向隧道的本地端。

36. 示例（节点主机 -> 网关主机）：

```bash
37. # 终端 A（保持运行）：将本地 18790 转发到网关 127.0.0.1:18789
ssh -N -L 18790:127.0.0.1:18789 user@gateway-host

# 终端 B：导出网关令牌并通过隧道连接
export OPENCLAW_GATEWAY_TOKEN="<gateway-token>"
openclaw node run --host 127.0.0.1 --port 18790 --display-name "Build Node"
```

38. 说明：

- 39. 该令牌是网关配置中的 `gateway.auth.token`（位于网关主机的 `~/.openclaw/openclaw.json`）。
- 40. `openclaw node run` 会读取 `OPENCLAW_GATEWAY_TOKEN` 用于认证。

### 41. 启动节点主机（服务）

```bash
42. openclaw node install --host <gateway-host> --port 18789 --display-name "Build Node"
openclaw node restart
```

### 43. 配对与命名

44. 在网关主机上：

```bash
45. openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes list
```

46. 命名选项：

- 47. 在 `openclaw node run` / `openclaw node install` 上使用 `--display-name`（会持久化到节点上的 `~/.openclaw/node.json`）。
- 48. `openclaw nodes rename --node <id|name|ip> --name "Build Node"`（网关级覆盖）。

### 49. 将命令加入允许列表

50. 执行审批是 **按节点主机** 生效的。 Add allowlist entries from the gateway:

```bash
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/uname"
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/sw_vers"
```

Approvals live on the node host at `~/.openclaw/exec-approvals.json`.

### Point exec at the node

Configure defaults (gateway config):

```bash
openclaw config set tools.exec.host node
openclaw config set tools.exec.security allowlist
openclaw config set tools.exec.node "<id-or-name>"
```

Or per session:

```
/exec host=node security=allowlist node=<id-or-name>
```

Once set, any `exec` call with `host=node` runs on the node host (subject to the
node allowlist/approvals).

Related:

- [Node host CLI](/cli/node)
- [Exec tool](/tools/exec)
- [Exec approvals](/tools/exec-approvals)

## Invoking commands

Low-level (raw RPC):

```bash
openclaw nodes invoke --node <idOrNameOrIp> --command canvas.eval --params '{"javaScript":"location.href"}'
```

Higher-level helpers exist for the common “give the agent a MEDIA attachment” workflows.

## Screenshots (canvas snapshots)

If the node is showing the Canvas (WebView), `canvas.snapshot` returns `{ format, base64 }`.

CLI helper (writes to a temp file and prints `MEDIA:<path>`):

```bash
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format png
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format jpg --max-width 1200 --quality 0.9
```

### Canvas controls

```bash
openclaw nodes canvas present --node <idOrNameOrIp> --target https://example.com
openclaw nodes canvas hide --node <idOrNameOrIp>
openclaw nodes canvas navigate https://example.com --node <idOrNameOrIp>
openclaw nodes canvas eval --node <idOrNameOrIp> --js "document.title"
```

Notes:

- `canvas present` accepts URLs or local file paths (`--target`), plus optional `--x/--y/--width/--height` for positioning.
- `canvas eval` accepts inline JS (`--js`) or a positional arg.

### A2UI (Canvas)

```bash
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --text "Hello"
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --jsonl ./payload.jsonl
openclaw nodes canvas a2ui reset --node <idOrNameOrIp>
```

Notes:

- Only A2UI v0.8 JSONL is supported (v0.9/createSurface is rejected).

## Photos + videos (node camera)

Photos (`jpg`):

```bash
openclaw nodes camera list --node <idOrNameOrIp>
openclaw nodes camera snap --node <idOrNameOrIp>            # default: both facings (2 MEDIA lines)
openclaw nodes camera snap --node <idOrNameOrIp> --facing front
```

Video clips (`mp4`):

```bash
openclaw nodes camera clip --node <idOrNameOrIp> --duration 10s
openclaw nodes camera clip --node <idOrNameOrIp> --duration 3000 --no-audio
```

Notes:

- The node must be **foregrounded** for `canvas.*` and `camera.*` (background calls return `NODE_BACKGROUND_UNAVAILABLE`).
- Clip duration is clamped (currently `<= 60s`) to avoid oversized base64 payloads.
- Android will prompt for `CAMERA`/`RECORD_AUDIO` permissions when possible; denied permissions fail with `*_PERMISSION_REQUIRED`.

## Screen recordings (nodes)

Nodes expose `screen.record` (mp4). Example:

```bash
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10 --no-audio
```

Notes:

- `screen.record` requires the node app to be foregrounded.
- Android will show the system screen-capture prompt before recording.
- Screen recordings are clamped to `<= 60s`.
- `--no-audio` disables microphone capture (supported on iOS/Android; macOS uses system capture audio).
- Use `--screen <index>` to select a display when multiple screens are available.

## Location (nodes)

Nodes expose `location.get` when Location is enabled in settings.

CLI helper:

```bash
openclaw nodes location get --node <idOrNameOrIp>
openclaw nodes location get --node <idOrNameOrIp> --accuracy precise --max-age 15000 --location-timeout 10000
```

Notes:

- Location is **off by default**.
- “Always” requires system permission; background fetch is best-effort.
- The response includes lat/lon, accuracy (meters), and timestamp.

## SMS (Android nodes)

Android nodes can expose `sms.send` when the user grants **SMS** permission and the device supports telephony.

Low-level invoke:

```bash
openclaw nodes invoke --node <idOrNameOrIp> --command sms.send --params '{"to":"+15555550123","message":"Hello from OpenClaw"}'
```

Notes:

- The permission prompt must be accepted on the Android device before the capability is advertised.
- Wi-Fi-only devices without telephony will not advertise `sms.send`.

## System commands (node host / mac node)

The macOS node exposes `system.run`, `system.notify`, and `system.execApprovals.get/set`.
The headless node host exposes `system.run`, `system.which`, and `system.execApprovals.get/set`.

Examples:

```bash
openclaw nodes run --node <idOrNameOrIp> -- echo "Hello from mac node"
openclaw nodes notify --node <idOrNameOrIp> --title "Ping" --body "Gateway ready"
```

Notes:

- `system.run` returns stdout/stderr/exit code in the payload.
- `system.notify` respects notification permission state on the macOS app.
- `system.run` supports `--cwd`, `--env KEY=VAL`, `--command-timeout`, and `--needs-screen-recording`.
- `system.notify` supports `--priority <passive|active|timeSensitive>` and `--delivery <system|overlay|auto>`.
- macOS nodes drop `PATH` overrides; headless node hosts only accept `PATH` when it prepends the node host PATH.
- On macOS node mode, `system.run` is gated by exec approvals in the macOS app (Settings → Exec approvals).
  Ask/allowlist/full behave the same as the headless node host; denied prompts return `SYSTEM_RUN_DENIED`.
- On headless node host, `system.run` is gated by exec approvals (`~/.openclaw/exec-approvals.json`).

## Exec node binding

When multiple nodes are available, you can bind exec to a specific node.
This sets the default node for `exec host=node` (and can be overridden per agent).

Global default:

```bash
openclaw config set tools.exec.node "node-id-or-name"
```

Per-agent override:

```bash
openclaw config get agents.list
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"
```

Unset to allow any node:

```bash
openclaw config unset tools.exec.node
openclaw config unset agents.list[0].tools.exec.node
```

## Permissions map

Nodes may include a `permissions` map in `node.list` / `node.describe`, keyed by permission name (e.g. `screenRecording`, `accessibility`) with boolean values (`true` = granted).

## Headless node host (cross-platform)

OpenClaw can run a **headless node host** (no UI) that connects to the Gateway
WebSocket and exposes `system.run` / `system.which`. This is useful on Linux/Windows
or for running a minimal node alongside a server.

Start it:

```bash
openclaw node run --host <gateway-host> --port 18789
```

Notes:

- Pairing is still required (the Gateway will show a node approval prompt).
- The node host stores its node id, token, display name, and gateway connection info in `~/.openclaw/node.json`.
- Exec approvals are enforced locally via `~/.openclaw/exec-approvals.json`
  (see [Exec approvals](/tools/exec-approvals)).
- On macOS, the headless node host prefers the companion app exec host when reachable and falls
  back to local execution if the app is unavailable. Set `OPENCLAW_NODE_EXEC_HOST=app` to require
  the app, or `OPENCLAW_NODE_EXEC_FALLBACK=0` to disable fallback.
- 1. 当 Gateway WS 使用 TLS 时添加 `--tls` / `--tls-fingerprint`。

## 2. Mac 节点模式

- 3. macOS 菜单栏应用作为一个节点连接到 Gateway WS 服务器（因此 `openclaw nodes …` 可以针对这台 Mac 使用）。
- 4. 在远程模式下，应用会为 Gateway 端口打开一个 SSH 隧道，并连接到 `localhost`。
