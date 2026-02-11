---
summary: "Gateway 服务的运行手册、生命周期和运维"
read_when:
  - 运行或调试 gateway 进程
title: "Gateway Runbook"
---

# Gateway 服务运行手册

最后更新：2025-12-09

## 它是什么

- 始终运行的进程，拥有单一的 Baileys/Telegram 连接以及控制/事件平面。
- 替代旧版的 `gateway` 命令。 CLI entry point: `openclaw gateway`.
- 持续运行直到被停止；发生致命错误时以非零状态退出，以便由监督器重启。

## 如何运行（本地）

```bash
openclaw gateway --port 18789
# 获取完整的 debug/trace 日志输出到 stdio：
openclaw gateway --port 18789 --verbose
# 如果端口被占用，先终止监听者再启动：
openclaw gateway --force
# 开发循环（TS 变更自动重载）：
pnpm gateway:watch
```

- Config hot reload watches `~/.openclaw/openclaw.json` (or `OPENCLAW_CONFIG_PATH`).
  - 默认模式：`gateway.reload.mode="hybrid"`（安全变更热应用，关键变更重启）。
  - Hot reload uses in-process restart via **SIGUSR1** when needed.
  - 可通过 `gateway.reload.mode="off"` 禁用。
- Binds WebSocket control plane to `127.0.0.1:<port>` (default 18789).
- 同一端口还提供 HTTP（控制 UI、hooks、A2UI）。 单端口复用。
  - OpenAI Chat Completions（HTTP）：[`/v1/chat/completions`](/gateway/openai-http-api)。
  - OpenResponses（HTTP）：[`/v1/responses`](/gateway/openresponses-http-api)。
  - Tools Invoke（HTTP）：[`/tools/invoke`](/gateway/tools-invoke-http-api)。
- 默认在 `canvasHost.port`（默认 `18793`）上启动 Canvas 文件服务器，从 `~/.openclaw/workspace/canvas` 提供 `http://<gateway-host>:18793/__openclaw__/canvas/`。 可通过 `canvasHost.enabled=false` 或 `OPENCLAW_SKIP_CANVAS_HOST=1` 禁用。
- 日志输出到 stdout；使用 launchd/systemd 保持其运行并进行日志轮转。
- 排障时传递 `--verbose`，可将日志文件中的调试日志（握手、请求/响应、事件）镜像输出到 stdio。
- `--force` 使用 `lsof` 查找所选端口上的监听者，发送 SIGTERM，记录被终止的进程，然后启动 gateway（如果缺少 `lsof` 则快速失败）。
- 如果在监督器下运行（launchd/systemd/mac 应用子进程模式），停止/重启通常会发送 **SIGTERM**；旧版本可能将其表现为 `pnpm` `ELIFECYCLE` 退出码 **143**（SIGTERM），这是正常关停而非崩溃。
- **SIGUSR1** 在获得授权时触发进程内重启（gateway 工具/配置 应用/更新，或启用 `commands.restart` 进行手动重启）。
- 默认需要 Gateway 认证：设置 `gateway.auth.token`（或 `OPENCLAW_GATEWAY_TOKEN`）或 `gateway.auth.password`。 客户端必须发送 `connect.params.auth.token/password`，除非使用 Tailscale Serve 身份。
- 向导现在默认会生成一个 token，即使是在回环地址上。
- 端口优先级：`--port` > `OPENCLAW_GATEWAY_PORT` > `gateway.port` > 默认 `18789`。

## 远程访问

- 优先使用 Tailscale/VPN；否则使用 SSH 隧道：

  ```bash
  ssh -N -L 18789:127.0.0.1:18789 user@host
  ```

- 客户端随后通过隧道连接到 `ws://127.0.0.1:18789`。

- If a token is configured, clients must include it in `connect.params.auth.token` even over the tunnel.

## Multiple gateways (same host)

通常不需要：一个 Gateway 可以服务多个消息通道和代理。 仅在需要冗余或严格隔离时使用多个 Gateway（例如：救援机器人）。

在隔离状态和配置并使用唯一端口的情况下是受支持的。 完整指南：[Multiple gateways](/gateway/multiple-gateways)。

服务名称与配置文件相关：

- macOS：`bot.molt.<profile>`（旧版 `com.openclaw.*` 可能仍然存在）
- Linux: `openclaw-gateway-<profile>.service`
- Windows：`OpenClaw Gateway (<profile>)`

安装元数据嵌入在服务配置中：

- `OPENCLAW_SERVICE_MARKER=openclaw`
- `OPENCLAW_SERVICE_KIND=gateway`
- `OPENCLAW_SERVICE_VERSION=<version>`

救援机器人模式：保持第二个 Gateway 隔离，使用其自己的 profile、状态目录、工作区，以及基础端口间隔。 Full guide: [Rescue-bot guide](/gateway/multiple-gateways#rescue-bot-guide).

### Dev profile (`--dev`)

Fast path: run a fully-isolated dev instance (config/state/workspace) without touching your primary setup.

```bash
openclaw --dev setup
openclaw --dev gateway --allow-unconfigured
# then target the dev instance:
openclaw --dev status
openclaw --dev health
```

Defaults (can be overridden via env/flags/config):

- `OPENCLAW_STATE_DIR=~/.openclaw-dev`
- `OPENCLAW_CONFIG_PATH=~/.openclaw-dev/openclaw.json`
- `OPENCLAW_GATEWAY_PORT=19001` (Gateway WS + HTTP)
- browser control service port = `19003` (derived: `gateway.port+2`, loopback only)
- `canvasHost.port=19005` (derived: `gateway.port+4`)
- `agents.defaults.workspace` default becomes `~/.openclaw/workspace-dev` when you run `setup`/`onboard` under `--dev`.

Derived ports (rules of thumb):

- Base port = `gateway.port` (or `OPENCLAW_GATEWAY_PORT` / `--port`)
- browser control service port = base + 2 (loopback only)
- `canvasHost.port = base + 4` (or `OPENCLAW_CANVAS_HOST_PORT` / config override)
- Browser profile CDP ports auto-allocate from `browser.controlPort + 9 .. + 108` (persisted per profile).

Checklist per instance:

- unique `gateway.port`
- unique `OPENCLAW_CONFIG_PATH`
- unique `OPENCLAW_STATE_DIR`
- unique `agents.defaults.workspace`
- separate WhatsApp numbers (if using WA)

Service install per profile:

```bash
openclaw --profile main gateway install
openclaw --profile rescue gateway install
```

Example:

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json OPENCLAW_STATE_DIR=~/.openclaw-a openclaw gateway --port 19001
OPENCLAW_CONFIG_PATH=~/.openclaw/b.json OPENCLAW_STATE_DIR=~/.openclaw-b openclaw gateway --port 19002
```

## Protocol (operator view)

- Full docs: [Gateway protocol](/gateway/protocol) and [Bridge protocol (legacy)](/gateway/bridge-protocol).
- Mandatory first frame from client: `req {type:"req", id, method:"connect", params:{minProtocol,maxProtocol,client:{id,displayName?,version,platform,deviceFamily?,modelIdentifier?,mode,instanceId?}, caps, auth?, locale?, userAgent? } }`.
- Gateway replies `res {type:"res", id, ok:true, payload:hello-ok }` (or `ok:false` with an error, then closes).
- After handshake:
  - Requests: `{type:"req", id, method, params}` → `{type:"res", id, ok, payload|error}`
  - Events: `{type:"event", event, payload, seq?, stateVersion?}`
- Structured presence entries: `{host, ip, version, platform?, deviceFamily?, modelIdentifier?, mode, lastInputSeconds?, ts, reason?, tags?[], instanceId? }` (for WS clients, `instanceId` comes from `connect.client.instanceId`).
- `agent` responses are two-stage: first `res` ack `{runId,status:"accepted"}`, then a final `res` `{runId,status:"ok"|"error",summary}` after the run finishes; streamed output arrives as `event:"agent"`.

## Methods (initial set)

- `health` — full health snapshot (same shape as `openclaw health --json`).
- `status` — short summary.
- `system-presence` — current presence list.
- `system-event` — post a presence/system note (structured).
- `send` — send a message via the active channel(s).
- `agent` — run an agent turn (streams events back on same connection).
- `node.list` — list paired + currently-connected nodes (includes `caps`, `deviceFamily`, `modelIdentifier`, `paired`, `connected`, and advertised `commands`).
- `node.describe` — describe a node (capabilities + supported `node.invoke` commands; works for paired nodes and for currently-connected unpaired nodes).
- `node.invoke` — invoke a command on a node (e.g. `canvas.*`, `camera.*`).
- `node.pair.*` — pairing lifecycle (`request`, `list`, `approve`, `reject`, `verify`).

See also: [Presence](/concepts/presence) for how presence is produced/deduped and why a stable `client.instanceId` matters.

## Events

- `agent` — streamed tool/output events from the agent run (seq-tagged).
- `presence` — 推送给所有已连接客户端的在线状态更新（包含 stateVersion 的增量）。
- `tick` — periodic keepalive/no-op to confirm liveness.
- `shutdown` — Gateway 正在退出；负载包含 `reason` 以及可选的 `restartExpectedMs`。 Clients should reconnect.

## WebChat 集成

- WebChat is a native SwiftUI UI that talks directly to the Gateway WebSocket for history, sends, abort, and events.
- 远程使用通过同一条 SSH/Tailscale 隧道；如果配置了 gateway token，客户端会在 `connect` 时附带它。
- macOS app connects via a single WS (shared connection); it hydrates presence from the initial snapshot and listens for `presence` events to update the UI.

## Typing and validation

- 服务器使用 AJV，根据协议定义生成的 JSON Schema 校验每一个入站帧。
- Clients (TS/Swift) consume generated types (TS directly; Swift via the repo’s generator).
- Protocol definitions are the source of truth; regenerate schema/models with:
  - `pnpm protocol:gen`
  - `pnpm protocol:gen:swift`

## 连接快照

- `hello-ok` 包含一个 `snapshot`，其中有 `presence`、`health`、`stateVersion` 和 `uptimeMs`，以及 `policy {maxPayload,maxBufferedBytes,tickIntervalMs}`，以便客户端无需额外请求即可立即渲染。
- `health`/`system-presence` 仍可用于手动刷新，但在连接时并非必需。

## 错误码（res.error 结构）

- 错误使用 `{ code, message, details?, retryable?, retryAfterMs?
  }`。 }\`.
- `NOT_LINKED` — WhatsApp 未通过身份验证。
  - `AGENT_TIMEOUT` — 代理未在配置的截止时间内响应。
  - `INVALID_REQUEST` — schema/参数校验失败。
  - `UNAVAILABLE` — Gateway 正在关闭或某个依赖不可用。
  - 保活行为

## 会定期发送 `tick` 事件（或 WS ping/pong），以便客户端在无流量时也能知道 Gateway 仍然存活。

- 发送/代理的确认仍然是独立的响应；不要将发送确认混用到 tick 中。
- 重放 / 缺口

## 事件不会被重放。

- 客户端检测到序列缺口时，应在继续之前刷新（`health` + `system-presence`）。 WebChat 和 macOS 客户端现在会在出现缺口时自动刷新。 WebChat and macOS clients now auto-refresh on gap.

## 使用 launchd 保持服务存活：

- Program：`openclaw` 的路径
  - Program: path to `openclaw`
  - KeepAlive：true
  - KeepAlive: true
  - 发生故障时，launchd 会重启；致命的错误配置应持续退出，以便运维人员注意到。
- LaunchAgents 是按用户的，并且需要已登录的会话；对于无头设置，请使用自定义的 LaunchDaemon（未随附）。
- `openclaw gateway install` 会写入 `~/Library/LaunchAgents/bot.molt.gateway.plist`
  （或 `bot.molt.<profile>
  .plist`；旧的 `com.openclaw.*` 会被清理）。
  - `openclaw doctor` 会审计 LaunchAgent 配置，并可将其更新为当前默认值。Gateway 服务管理（CLI）
  - 使用 Gateway CLI 进行 install/start/stop/restart/status：

openclaw gateway status
openclaw gateway install
openclaw gateway stop
openclaw gateway restart
openclaw logs --follow
----------------------

注意：

```bash
`gateway status` 默认通过服务解析得到的端口/配置来探测 Gateway RPC（可使用 `--url` 覆盖）。
```

Notes:

- `gateway status` probes the Gateway RPC by default using the service’s resolved port/config (override with `--url`).
- `gateway status --deep` adds system-level scans (LaunchDaemons/system units).
- `gateway status --no-probe` 跳过 RPC 探测（在网络不可用时很有用）。
- `gateway status --json` 对脚本而言是稳定的。
- `gateway status` 将 **监督器运行时**（launchd/systemd 是否运行）与 **RPC 可达性**（WS 连接 + status RPC）分开报告。
- `gateway status` prints config path + probe target to avoid “localhost vs LAN bind” confusion and profile mismatches.
- `gateway status` 在服务看似运行但端口关闭时，包含最近一条网关错误日志。
- `logs` tails the Gateway file log via RPC (no manual `tail`/`grep` needed).
- If other gateway-like services are detected, the CLI warns unless they are OpenClaw profile services.
  我们仍然建议 **每台机器一个网关** 适用于大多数场景；如需冗余或救援机器人，请使用隔离的配置文件/端口。 参见 [Multiple gateways](/gateway/multiple-gateways)。
  - Cleanup: `openclaw gateway uninstall` (current service) and `openclaw doctor` (legacy migrations).
- `gateway install` 在已安装时是无操作；如需重新安装（配置文件/环境/路径更改），请使用 `openclaw gateway install --force`。

捆绑的 mac 应用：

- OpenClaw.app can bundle a Node-based gateway relay and install a per-user LaunchAgent labeled
  `bot.molt.gateway` (or `bot.molt.<profile>; 旧版 `com.openclaw.\*\` 标签仍可干净卸载）。
- 要干净停止，请使用 `openclaw gateway stop`（或 `launchctl bootout gui/$UID/bot.molt.gateway`）。
- 要重启，请使用 `openclaw gateway restart`（或 `launchctl kickstart -k gui/$UID/bot.molt.gateway`）。
  - `launchctl` only works if the LaunchAgent is installed; otherwise use `openclaw gateway install` first.
  - 在运行命名配置文件时，将标签替换为 \`bot.molt.<profile>\`\` when running a named profile.

## 监督（systemd 用户单元）

OpenClaw installs a **systemd user service** by default on Linux/WSL2. 我们
建议单用户机器使用用户服务（环境更简单，按用户配置）。
多用户或常开服务器请使用 **系统服务**（无需 lingering，共享监督）。

`openclaw gateway install` 会写入用户单元。 `openclaw doctor` 会审计该
单元，并可将其更新为当前推荐的默认值。

创建 `~/.config/systemd/user/openclaw-gateway[-<profile>].service`：

```
[Unit]
Description=OpenClaw Gateway (profile: <profile>, v<version>)
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/openclaw gateway --port 18789
Restart=always
RestartSec=5
Environment=OPENCLAW_GATEWAY_TOKEN=
WorkingDirectory=/home/youruser

[Install]
WantedBy=default.target
```

Enable lingering (required so the user service survives logout/idle):

```
sudo loginctl enable-linger youruser
```

引导流程会在 Linux/WSL2 上运行此命令（可能会提示 sudo；写入 `/var/lib/systemd/linger`）。
Then enable the service:

```
systemctl --user enable --now openclaw-gateway[-<profile>].service
```

**替代方案（系统服务）**——对于常开或多用户服务器，可以安装 systemd **系统** 单元而非用户单元（无需 lingering）。
创建 `/etc/systemd/system/openclaw-gateway[-<profile>].service`（复制上述单元，
将 `WantedBy=multi-user.target`，并设置 `User=` + `WorkingDirectory=`），然后：

```
sudo systemctl daemon-reload
sudo systemctl enable --now openclaw-gateway[-<profile>].service
```

## Windows（WSL2）

Windows 安装应使用 **WSL2** 并遵循上述 Linux systemd 部分。

## 运行检查

- 存活性：打开 WS 并发送 `req:connect` → 期望收到带有 `payload.type="hello-ok"`（含快照）的 `res`。
- 就绪性：调用 `health` → 期望 `ok: true`，并在适用时在 `linkChannel` 中有已链接的通道。
- 调试：订阅 `tick` 和 `presence` 事件；确保 `status` 显示已链接/认证时长；presence 条目显示 Gateway 主机和已连接客户端。

## 安全保证

- 默认假设每台主机一个 Gateway；如果运行多个配置文件，请隔离端口/状态并指向正确的实例。
- 不回退到直接的 Baileys 连接；如果 Gateway 停机，发送会快速失败。
- 非连接的首帧或格式错误的 JSON 会被拒绝并关闭套接字。
- 优雅关闭：在关闭前发出 `shutdown` 事件；客户端必须处理关闭并重连。

## CLI 辅助工具

- `openclaw gateway health|status` — 通过 Gateway WS 请求健康/状态。
- `openclaw message send --target <num> --message "hi" [--media ...]` — 通过 Gateway 发送（对 WhatsApp 是幂等的）。
- `openclaw agent --message "hi" --to <num>` — run an agent turn (waits for final by default).
- `openclaw gateway call <method> --params '{"k":"v"}'` — raw method invoker for debugging.
- `openclaw gateway stop|restart` — stop/restart the supervised gateway service (launchd/systemd).
- Gateway helper subcommands assume a running gateway on `--url`; they no longer auto-spawn one.

## Migration guidance

- Retire uses of `openclaw gateway` and the legacy TCP control port.
- Update clients to speak the WS protocol with mandatory connect and structured presence.
