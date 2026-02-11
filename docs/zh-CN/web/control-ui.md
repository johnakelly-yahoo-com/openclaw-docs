---
summary: "Browser-based control UI for the Gateway (chat, nodes, config)"
read_when:
  - You want to operate the Gateway from a browser
  - You want Tailnet access without SSH tunnels
title: "Control UI"
---

# Control UI (browser)

The Control UI is a small **Vite + Lit** single-page app served by the Gateway:

- default: `http://<host>:18789/`
- optional prefix: set `gateway.controlUi.basePath` (e.g. `/openclaw`)

It speaks **directly to the Gateway WebSocket** on the same port.

## Quick open (local)

If the Gateway is running on the same computer, open:

- [http://127.0.0.1:18789/](http://127.0.0.1:18789/) (or [http://localhost:18789/](http://localhost:18789/))

If the page fails to load, start the Gateway first: `openclaw gateway`.

Auth is supplied during the WebSocket handshake via:

- `connect.params.auth.token`
- `connect.params.auth.password`
  The dashboard settings panel lets you store a token; passwords are not persisted.
  The onboarding wizard generates a gateway token by default, so paste it here on first connect.

## Device pairing (first connection)

When you connect to the Control UI from a new browser or device, the Gateway
requires a **one-time pairing approval** — even if you're on the same Tailnet
with `gateway.auth.allowTailscale: true`. This is a security measure to prevent
unauthorized access.

**What you'll see:** "disconnected (1008): pairing required"

**To approve the device:**

```bash
# List pending requests
openclaw devices list

# Approve by request ID
openclaw devices approve <requestId>
```

Once approved, the device is remembered and won't require re-approval unless
you revoke it with `openclaw devices revoke --device <id> --role <role>`. See
[Devices CLI](/cli/devices) for token rotation and revocation.

**Notes:**

- 1. 本地连接（`127.0.0.1`）会被自动批准。
- 2. 远程连接（LAN、Tailnet 等） 3. 需要显式批准。
- 4. 每个浏览器配置文件都会生成一个唯一的设备 ID，因此切换浏览器或

## 清除浏览器数据将需要重新配对。

- 5. 它目前可以做什么
- Stream tool calls + live tool output cards in Chat (agent events)
- 7. 在聊天中流式展示工具调用 + 实时工具输出卡片（代理事件） 8. 渠道：WhatsApp/Telegram/Discord/Slack + 插件渠道（Mattermost 等）
- 9. 状态 + 二维码登录 + 按渠道配置（`channels.status`、`web.login.*`、`config.patch`）
- 10. 实例：在线列表 + 刷新（`system-presence`）
- 11. 会话：列表 + 按会话的思考/详细模式覆盖（`sessions.list`、`sessions.patch`）
- 12. 定时任务：列出/添加/运行/启用/禁用 + 运行历史（`cron.*`）
- 13. 技能：状态、启用/禁用、安装、API 密钥更新（`skills.*`）
- 14. 节点：列表 + 能力（`node.list`）
- 15. 执行审批：编辑网关或节点允许列表 + 针对 `exec host=gateway/node` 询问策略（`exec.approvals.*`）
- 16. 配置：查看/编辑 `~/.openclaw/openclaw.json`（`config.get`、`config.set`）
- 17. 配置：应用 + 校验后重启（`config.apply`），并唤醒最近一次活跃的会话
- 18. 配置写入包含基于哈希的防护，以防止覆盖并发编辑
- 19. 配置架构 + 表单渲染（`config.schema`，包括插件和渠道架构）；仍然提供原始 JSON 编辑器
- 20. 调试：状态/健康/模型快照 + 事件日志 + 手动 RPC 调用（`status`、`health`、`models.list`）
- 21. 日志：网关文件日志的实时尾随，支持过滤/导出（`logs.tail`）

22. 更新：运行包/Git 更新 + 重启（`update.run`），并生成重启报告

- 23. 定时任务面板说明： 24. 对于隔离的任务，投递方式默认是公告摘要。
- 25. 如果你只想进行内部运行，可以切换为 none。

## 26. 当选择 announce 时，将显示渠道/目标字段。

- 27. 聊天行为
- 28. `chat.send` 是**非阻塞**的：它会立即确认并返回 `{ runId, status: "started" }`，响应通过 `chat` 事件流式传输。
- 29. 使用相同的 `idempotencyKey` 重新发送时，运行期间返回 `{ status: "in_flight" }`，完成后返回 `{ status: "ok" }`。
- 30. `chat.inject` 会向会话记录追加一条助手备注，并广播一个 `chat` 事件，仅用于 UI 更新（不运行代理、不投递到渠道）。
  - 31. 停止：
  - 32. 点击 **Stop**（调用 `chat.abort`）
  - 33. 输入 `/stop`（或 `stop|esc|abort|wait|exit|interrupt`）以进行带外中止

## 34. `chat.abort` 支持 `{ sessionKey }`（不需要 `runId`），用于中止该会话的所有活动运行

### 35. Tailnet 访问（推荐）

36. 集成的 Tailscale Serve（首选）

```bash
37. 将 Gateway 保持在回环地址，并让 Tailscale Serve 通过 HTTPS 进行代理：
```

38. openclaw gateway --tailscale serve

- 39. 打开：

40. `https://<magicdns>/`（或你配置的 `gateway.controlUi.basePath`） 41. 默认情况下，当 `gateway.auth.allowTailscale` 为 `true` 时，Serve 请求可以通过 Tailscale 身份标头（`tailscale-user-login`）进行认证。 42. OpenClaw 通过使用 `tailscale whois` 解析 `x-forwarded-for` 地址并与该标头匹配来验证身份，并且仅在请求通过回环地址且带有 Tailscale 的 `x-forwarded-*` 标头时才接受这些请求。

### 43. 如果你希望即使是 Serve 流量也需要令牌/密码，请设置 `gateway.auth.allowTailscale: false`（或强制 `gateway.auth.mode: "password"`）。

```bash
44. 绑定到 tailnet + 令牌
```

45. openclaw gateway --bind tailnet --token "$(openssl rand -hex 32)"

- 46. 然后打开：

47. `http://<tailscale-ip>:18789/`（或你配置的 `gateway.controlUi.basePath`）

## 48. 将令牌粘贴到 UI 设置中（作为 `connect.params.auth.token` 发送）。

49. 不安全的 HTTP By default,
    OpenClaw **blocks** Control UI connections without device identity.

**Recommended fix:** use HTTPS (Tailscale Serve) or open the UI locally:

- `https://<magicdns>/` (Serve)
- `http://127.0.0.1:18789/` (on the gateway host)

**Downgrade example (token-only over HTTP):**

```json5
{
  gateway: {
    controlUi: { allowInsecureAuth: true },
    bind: "tailnet",
    auth: { mode: "token", token: "replace-me" },
  },
}
```

This disables device identity + pairing for the Control UI (even on HTTPS). Use
only if you trust the network.

See [Tailscale](/gateway/tailscale) for HTTPS setup guidance.

## Building the UI

The Gateway serves static files from `dist/control-ui`. Build them with:

```bash
pnpm ui:build # auto-installs UI deps on first run
```

Optional absolute base (when you want fixed asset URLs):

```bash
OPENCLAW_CONTROL_UI_BASE_PATH=/openclaw/ pnpm ui:build
```

For local development (separate dev server):

```bash
pnpm ui:dev # auto-installs UI deps on first run
```

Then point the UI at your Gateway WS URL (e.g. `ws://127.0.0.1:18789`).

## Debugging/testing: dev server + remote Gateway

The Control UI is static files; the WebSocket target is configurable and can be
different from the HTTP origin. This is handy when you want the Vite dev server
locally but the Gateway runs elsewhere.

1. Start the UI dev server: `pnpm ui:dev`
2. Open a URL like:

```text
http://localhost:5173/?gatewayUrl=ws://<gateway-host>:18789
```

Optional one-time auth (if needed):

```text
http://localhost:5173/?gatewayUrl=wss://<gateway-host>:18789&token=<gateway-token>
```

Notes:

- `gatewayUrl` is stored in localStorage after load and removed from the URL.
- `token` is stored in localStorage; `password` is kept in memory only.
- When `gatewayUrl` is set, the UI does not fall back to config or environment credentials.
  Provide `token` (or `password`) explicitly. Missing explicit credentials is an error.
- Use `wss://` when the Gateway is behind TLS (Tailscale Serve, HTTPS proxy, etc.).
- `gatewayUrl` is only accepted in a top-level window (not embedded) to prevent clickjacking.
- For cross-origin dev setups (e.g. `pnpm ui:dev` to a remote Gateway), add the UI
  origin to `gateway.controlUi.allowedOrigins`.

Example:

```json5
{
  gateway: {
    controlUi: {
      allowedOrigins: ["http://localhost:5173"],
    },
  },
}
```

Remote access setup details: [Remote access](/gateway/remote).
