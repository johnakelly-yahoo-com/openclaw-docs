---
summary: "8. OpenClaw CLI 参考，用于 `openclaw` 命令、子命令和选项"
read_when:
  - 添加或修改 CLI 命令或选项
  - 10. 为新的命令界面编写文档
title: "11. CLI 参考"
---

# CLI 参考

13. 本页面描述当前的 CLI 行为。 14. 如果命令发生变化，请更新此文档。

## 15. 命令页面

- 16. [`setup`](/cli/setup)
- 17. [`onboard`](/cli/onboard)
- 18. [`configure`](/cli/configure)
- 19. [`config`](/cli/config)
- 20. [`doctor`](/cli/doctor)
- [`dashboard`](/cli/dashboard)
- 22. [`reset`](/cli/reset)
- [`uninstall`](/cli/uninstall)
- 24. [`update`](/cli/update)
- 25. [`message`](/cli/message)
- 26. [`agent`](/cli/agent)
- 27. [`agents`](/cli/agents)
- 28. [`acp`](/cli/acp)
- 29. [`status`](/cli/status)
- 30. [`health`](/cli/health)
- 31. [`sessions`](/cli/sessions)
- 32. [`gateway`](/cli/gateway)
- 33. [`logs`](/cli/logs)
- 34. [`system`](/cli/system)
- 35. [`models`](/cli/models)
- 36. [`memory`](/cli/memory)
- 37. [`nodes`](/cli/nodes)
- 38. [`devices`](/cli/devices)
- 39. [`node`](/cli/node)
- 40. [`approvals`](/cli/approvals)
- 41. [`sandbox`](/cli/sandbox)
- 42. [`tui`](/cli/tui)
- 43. [`browser`](/cli/browser)
- 44. [`cron`](/cli/cron)
- 45. [`dns`](/cli/dns)
- 46. [`docs`](/cli/docs)
- 47. [`hooks`](/cli/hooks)
- 48. [`webhooks`](/cli/webhooks)
- 49. [`pairing`](/cli/pairing)
- 50. [`plugins`](/cli/plugins)（插件命令）
- [`channels`](/cli/channels)
- [`security`](/cli/security)
- [`skills`](/cli/skills)
- [`voicecall`](/cli/voicecall) (plugin; if installed)

## Global flags

- `--dev`: isolate state under `~/.openclaw-dev` and shift default ports.
- `--profile <name>`: isolate state under `~/.openclaw-<name>`.
- `--no-color`: disable ANSI colors.
- `--update`: shorthand for `openclaw update` (source installs only).
- `-V`, `--version`, `-v`: print version and exit.

## Output styling

- ANSI colors and progress indicators only render in TTY sessions.
- OSC-8 hyperlinks render as clickable links in supported terminals; otherwise we fall back to plain URLs.
- `--json` (and `--plain` where supported) disables styling for clean output.
- `--no-color` disables ANSI styling; `NO_COLOR=1` is also respected.
- Long-running commands show a progress indicator (OSC 9;4 when supported).

## Color palette

OpenClaw uses a lobster palette for CLI output.

- `accent` (#FF5A2D): headings, labels, primary highlights.
- `accentBright` (#FF7A3D): command names, emphasis.
- `accentDim` (#D14A22): secondary highlight text.
- `info` (#FF8A5B): informational values.
- `success` (#2FBF71): success states.
- `warn` (#FFB020)：警告、回退、需要注意。
- `error` (#E23D2D): errors, failures.
- `muted` (#8B7F77): de-emphasis, metadata.

Palette source of truth: `src/terminal/palette.ts` (aka “lobster seam”).

## Command tree

```
openclaw [--dev] [--profile <name>] <command>
  setup
  onboard
  configure
  config
    get
    set
    unset
  doctor
  security
    audit
  reset
  uninstall
  update
  channels
    list
    status
    logs
    add
    remove
    login
    logout
  skills
    list
    info
    check
  plugins
    list
    info
    install
    enable
    disable
    doctor
  memory
    status
    index
    search
  message
  agent
  agents
    list
    add
    delete
  acp
  status
  health
  sessions
  gateway
    call
    health
    status
    probe
    discover
    install
    uninstall
    start
    stop
    restart
    run
  logs
  system
    event
    heartbeat last|enable|disable
    presence
  models
    list
    status
    set
    set-image
    aliases list|add|remove
    fallbacks list|add|remove|clear
    image-fallbacks list|add|remove|clear
    scan
    auth add|setup-token|paste-token
    auth order get|set|clear
  sandbox
    list
    recreate
    explain
  cron
    status
    list
    add
    edit
    rm
    enable
    disable
    runs
    run
  nodes
  devices
  node
    run
    status
    install
    uninstall
    start
    stop
    restart
  approvals
    get
    set
    allowlist add|remove
  browser
    status
    start
    stop
    reset-profile
    tabs
    open
    focus
    close
    profiles
    create-profile
    delete-profile
    screenshot
    snapshot
    navigate
    resize
    click
    type
    press
    hover
    drag
    select
    upload
    fill
    dialog
    wait
    evaluate
    console
    pdf
  hooks
    list
    info
    check
    enable
    disable
    install
    update
  webhooks
    gmail setup|run
  pairing
    list
    approve
  docs
  dns
    setup
  tui
```

Note: plugins can add additional top-level commands (for example `openclaw voicecall`).

## Security

- `openclaw security audit` — audit config + local state for common security foot-guns.
- `openclaw security audit --deep` — best-effort live Gateway probe.
- `openclaw security audit --fix` — tighten safe defaults and chmod state/config.

## Plugins

Manage extensions and their config:

- `openclaw plugins list` — discover plugins (use `--json` for machine output).
- `openclaw plugins info <id>` — show details for a plugin.
- `openclaw plugins install <path|.tgz|npm-spec>` — install a plugin (or add a plugin path to `plugins.load.paths`).
- `openclaw plugins enable <id>` / `disable <id>` — toggle `plugins.entries.<id>.enabled`.
- `openclaw plugins doctor` — report plugin load errors.

Most plugin changes require a gateway restart. See [/plugin](/tools/plugin).

## Memory

Vector search over `MEMORY.md` + `memory/*.md`:

- `openclaw memory status` — show index stats.
- `openclaw memory index` — reindex memory files.
- `openclaw memory search "<query>"` — semantic search over memory.

## Chat slash commands

1. 聊天消息支持 `/...` 命令（文本和原生）。 2. 参见 [/tools/slash-commands](/tools/slash-commands)。

3. 亮点：

- 4. `/status` 用于快速诊断。
- 5. `/config` 用于持久化配置更改。
- 6. `/debug` 用于仅在运行时生效的配置覆盖（内存中，不写入磁盘；需要 `commands.debug: true`）。

## 7. 设置与引导

### 8. `setup`

9. 初始化配置和工作区。

10. 选项：

- 11. `--workspace <dir>`：代理工作区路径（默认 `~/.openclaw/workspace`）。
- 12. `--wizard`：运行引导向导。
- 13. `--non-interactive`：在无提示的情况下运行向导。
- 14. `--mode <local|remote>`：向导模式。
- 15. `--remote-url <url>`：远程 Gateway URL。
- 16. `--remote-token <token>`：远程 Gateway 令牌。

17. 当存在任何向导标志时，向导将自动运行（`--non-interactive`、`--mode`、`--remote-url`、`--remote-token`）。

### 18. `onboard`

19. 用于设置网关、工作区和技能的交互式向导。

20. 选项：

- 21. `--workspace <dir>`
- `--reset`（在向导前重置配置 + 凭据 + 会话 + 工作区）
- `--non-interactive`
- 24. `--mode <local|remote>`
- 25. `--flow <quickstart|advanced|manual>`（manual 是 advanced 的别名）
- 26. `--auth-choice <setup-token|token|chutes|openai-codex|openai-api-key|openrouter-api-key|ai-gateway-api-key|moonshot-api-key|moonshot-api-key-cn|kimi-code-api-key|synthetic-api-key|venice-api-key|gemini-api-key|zai-api-key|apiKey|minimax-api|minimax-api-lightning|opencode-zen|skip>`
- `--token-provider <id>`（非交互式；与 `--auth-choice token` 一起使用）
- 28. `--token <token>`（非交互式；与 `--auth-choice token` 一起使用）
- `--token-profile-id <id>`（非交互式；默认：`<provider>:manual`）
- 30. `--token-expires-in <duration>`（非交互式；例如 `365d`、`12h`）
- `--anthropic-api-key <key>`
- 32. `--openai-api-key <key>`
- 33. `--openrouter-api-key <key>`
- 34. `--ai-gateway-api-key <key>`
- 35. `--moonshot-api-key <key>`
- 36. `--kimi-code-api-key <key>`
- 37. `--gemini-api-key <key>`
- 38. `--zai-api-key <key>`
- 39. `--minimax-api-key <key>`
- 40. `--opencode-zen-api-key <key>`
- 41. `--gateway-port <port>`
- 42. `--gateway-bind <loopback|lan|tailnet|auto|custom>`
- 43. `--gateway-auth <token|password>`
- 44. `--gateway-token <token>`
- 45. `--gateway-password <password>`
- 46. `--remote-url <url>`
- 47. `--remote-token <token>`
- 48. `--tailscale <off|serve|funnel>`
- 49. `--tailscale-reset-on-exit`
- 50. `--install-daemon`
- `--no-install-daemon` (alias: `--skip-daemon`)
- `--daemon-runtime <node|bun>`
- `--skip-channels`
- `--skip-skills`
- `--skip-health`
- `--skip-ui`
- `--node-manager <npm|pnpm|bun>` (pnpm recommended; bun not recommended for Gateway runtime)
- `--json`

### `configure`

Interactive configuration wizard (models, channels, skills, gateway).

### `config`

Non-interactive config helpers (get/set/unset). Running `openclaw config` with no
subcommand launches the wizard.

Subcommands:

- `config get <path>`：打印配置值（点/括号路径）。
- `config set <path> <value>`: set a value (JSON5 or raw string).
- `config unset <path>`: remove a value.

### `doctor`

Health checks + quick fixes (config + gateway + legacy services).

Options:

- `--no-workspace-suggestions`: disable workspace memory hints.
- `--yes`: accept defaults without prompting (headless).
- `--non-interactive`: skip prompts; apply safe migrations only.
- `--deep`: scan system services for extra gateway installs.

## Channel helpers

### `channels`

Manage chat channel accounts (WhatsApp/Telegram/Discord/Google Chat/Slack/Mattermost (plugin)/Signal/iMessage/MS Teams).

Subcommands:

- `channels list`: show configured channels and auth profiles.
- `channels status`: check gateway reachability and channel health (`--probe` runs extra checks; use `openclaw health` or `openclaw status --deep` for gateway health probes).
- Tip: `channels status` prints warnings with suggested fixes when it can detect common misconfigurations (then points you to `openclaw doctor`).
- `channels logs`: show recent channel logs from the gateway log file.
- `channels add`: wizard-style setup when no flags are passed; flags switch to non-interactive mode.
- `channels remove`: disable by default; pass `--delete` to remove config entries without prompts.
- `channels login`: interactive channel login (WhatsApp Web only).
- `channels logout`: log out of a channel session (if supported).

Common options:

- `--channel <name>`: `whatsapp|telegram|discord|googlechat|slack|mattermost|signal|imessage|msteams`
- `--account <id>`: channel account id (default `default`)
- `--name <label>`: display name for the account

`channels login` options:

- `--channel <channel>` (default `whatsapp`; supports `whatsapp`/`web`)
- `--account <id>`
- `--verbose`

`channels logout` options:

- `--channel <channel>` (default `whatsapp`)
- `--account <id>`

`channels list` options:

- `--no-usage`: skip model provider usage/quota snapshots (OAuth/API-backed only).
- `--json`: output JSON (includes usage unless `--no-usage` is set).

`channels logs` options:

- `--channel <name|all>`（默认 `all`）
- `--lines <n>`（默认 `200`）
- `--json`

更多详情：[/concepts/oauth](/concepts/oauth)

示例：

```bash
openclaw channels add --channel telegram --account alerts --name "Alerts Bot" --token $TELEGRAM_BOT_TOKEN
openclaw channels add --channel discord --account work --name "Work Bot" --token $DISCORD_BOT_TOKEN
openclaw channels remove --channel discord --account work --delete
openclaw channels status --probe
openclaw status --deep
```

### `skills`

列出并检查可用技能及其就绪状态信息。

子命令：

- `skills list`：列出技能（无子命令时的默认行为）。
- `skills info <name>`：显示单个技能的详细信息。
- `skills check`：已就绪与缺失依赖的汇总。

选项：

- `--eligible`：仅显示已就绪的技能。
- `--json`：以 JSON 输出（无样式）。
- `-v`、`--verbose`：包含缺失依赖的详细信息。

提示：使用 `npx clawhub` 搜索、安装并同步技能。

### `pairing`

跨渠道批准私信配对请求。

子命令：

- `pairing list <channel> [--json]`
- `pairing approve <channel> <code> [--notify]`

### `webhooks gmail`

Gmail Pub/Sub 钩子设置与运行器。 参见 [/automation/gmail-pubsub](/automation/gmail-pubsub)。

子命令：

- `webhooks gmail setup`（需要 `--account <email>`；支持 `--project`、`--topic`、`--subscription`、`--label`、`--hook-url`、`--hook-token`、`--push-token`、`--bind`、`--port`、`--path`、`--include-body`、`--max-bytes`、`--renew-minutes`、`--tailscale`、`--tailscale-path`、`--tailscale-target`、`--push-endpoint`、`--json`）
- `webhooks gmail run`（对相同标志的运行时覆盖）

### `dns setup`

广域发现 DNS 助手（CoreDNS + Tailscale）。 参见 [/gateway/discovery](/gateway/discovery)。

选项：

- `--apply`：安装/更新 CoreDNS 配置（需要 sudo；仅 macOS）。

## 消息传递 + 代理

### `message`

统一的外发消息与频道操作。

参见：[/cli/message](/cli/message)

子命令：

- `message send|poll|react|reactions|read|edit|delete|pin|unpin|pins|permissions|search|timeout|kick|ban`
- `message thread <create|list|reply>`
- `message emoji <list|upload>`
- `message sticker <send|upload>`
- `message role <info|add|remove>`
- `message channel <info|list>`
- `message member info`
- `message voice status`
- `message event <list|create>`

示例：

- `openclaw message send --target +15555550123 --message "Hi"`
- `openclaw message poll --channel discord --target channel:123 --poll-question "Snack?" --poll-option Pizza --poll-option Sushi`

### `agent`

通过网关运行一次 agent 轮次（或使用 `--local` 内嵌）。

必需：

- `--message <text>`

选项：

- `--to <dest>`（用于会话密钥和可选投递）
- `--session-id <id>`
- `--thinking <off|minimal|low|medium|high|xhigh>`（仅 GPT-5.2 + Codex 模型）
- `--verbose <on|full|off>`
- `--channel <whatsapp|telegram|discord|slack|mattermost|signal|imessage|msteams>`
- `--local`
- `--deliver`
- `--json`
- `--timeout <seconds>`

### `agents`

管理隔离的 agents（工作区 + 认证 + 路由）。

#### `agents list`

列出已配置的 agents。

选项：

- `--json`
- `--bindings`

#### `agents add [name]`

添加一个新的隔离 agent。 除非传递标志（或 `--non-interactive`），否则将运行引导式向导；在非交互模式下需要 `--workspace`。

选项：

- `--workspace <dir>`
- `--model <id>`
- `--agent-dir <dir>`
- `--bind <channel[:accountId]>`（可重复）
- `--non-interactive`
- `--json`

绑定规范使用 `channel[:accountId]`。 当 WhatsApp 省略 `accountId` 时，将使用默认账户 ID。

#### `agents delete <id>`

删除一个 agent，并清理其工作区和状态。

选项：

- `--force`
- `--json`

### `acp`

运行将 IDE 连接到 Gateway 的 ACP 桥接器。

有关完整选项和示例，请参见 [`acp`](/cli/acp)。

### `status`

显示已链接会话的健康状况和最近的接收方。

选项：

- `--json`
- `--all`（完整诊断；只读，可粘贴）
- `--deep`（探测各渠道）
- `--usage`（显示模型提供方的使用量/配额）
- 1. `--timeout <ms>`
- 2. `--verbose`
- 3. `--debug`（`--verbose` 的别名）

4. 说明：

- 5. 概览在可用时包含 Gateway + 节点主机服务状态。

### 6. 使用量跟踪

7. 当 OAuth/API 凭据可用时，OpenClaw 可以展示提供方的使用量/配额。

8. 展示位置：

- 9. `/status`（在可用时增加一行简短的提供方使用量信息）
- 10. `openclaw status --usage`（打印完整的提供方明细）
- 11. macOS 菜单栏（Context 下的 Usage 区域）

12. 说明：

- 数据直接来自提供方的用量端点（非估算）。
- 14. 提供方：Anthropic、GitHub Copilot、OpenAI Codex OAuth，以及在启用相应提供方插件时的 Gemini CLI/Antigravity。
- 15. 如果不存在匹配的凭据，则隐藏使用量。
- 16. 详情：参见 [Usage tracking](/concepts/usage-tracking)。

### 17. `health`

18. 从正在运行的 Gateway 获取健康状态。

19. 选项：

- 20. `--json`
- 21. `--timeout <ms>`
- 22. `--verbose`

### 23. `sessions`

24. 列出已存储的会话。

25. 选项：

- 26. `--json`
- 27. `--verbose`
- 28. `--store <path>`
- 29. `--active <minutes>`

## 30. 重置 / 卸载

### 31. `reset`

32. 重置本地配置/状态（保留 CLI 已安装）。

33. 选项：

- 34. `--scope <config|config+creds+sessions|full>`
- 35. `--yes`
- 36. `--non-interactive`
- 37. `--dry-run`

38. 说明：

- 39. `--non-interactive` 需要同时指定 `--scope` 和 `--yes`。

### 40. `uninstall`

41. 卸载网关服务和本地数据（CLI 仍然保留）。

42. 选项：

- 43. `--service`
- 44. `--state`
- 45. `--workspace`
- 46. `--app`
- 47. `--all`
- 48. `--yes`
- 49. `--non-interactive`
- 50. `--dry-run`

Notes:

- `--non-interactive` requires `--yes` and explicit scopes (or `--all`).

## Gateway

### `gateway`

Run the WebSocket Gateway.

Options:

- `--port <port>`
- `--bind <loopback|tailnet|lan|auto|custom>`
- `--token <token>`
- `--auth <token|password>`
- `--password <password>`
- `--tailscale <off|serve|funnel>`
- `--tailscale-reset-on-exit`
- `--allow-unconfigured`
- `--dev`
- `--reset` (reset dev config + credentials + sessions + workspace)
- `--force` (kill existing listener on port)
- `--verbose`
- `--claude-cli-logs`
- `--ws-log <auto|full|compact>`
- `--compact` (alias for `--ws-log compact`)
- `--raw-stream`
- `--raw-stream-path <path>`

### `gateway service`

Manage the Gateway service (launchd/systemd/schtasks).

Subcommands:

- `gateway status` (probes the Gateway RPC by default)
- `gateway install` (service install)
- `gateway uninstall`
- `gateway start`
- `gateway stop`
- `gateway restart`

说明：

- `gateway status` probes the Gateway RPC by default using the service’s resolved port/config (override with `--url/--token/--password`).
- `gateway status` supports `--no-probe`, `--deep`, and `--json` for scripting.
- `gateway status` also surfaces legacy or extra gateway services when it can detect them (`--deep` adds system-level scans). Profile-named OpenClaw services are treated as first-class and aren't flagged as "extra".
- `gateway status` prints which config path the CLI uses vs which config the service likely uses (service env), plus the resolved probe target URL.
- `gateway install|uninstall|start|stop|restart` support `--json` for scripting (default output stays human-friendly).
- `gateway install` defaults to Node runtime; bun is **not recommended** (WhatsApp/Telegram bugs).
- `gateway install` options: `--port`, `--runtime`, `--token`, `--force`, `--json`.

### `logs`

Tail Gateway file logs via RPC.

Notes:

- TTY sessions render a colorized, structured view; non-TTY falls back to plain text.
- `--json` 输出按行分隔的 JSON（每行一个日志事件）。

Examples:

```bash
openclaw logs --follow
openclaw logs --limit 200
openclaw logs --plain
openclaw logs --json
openclaw logs --no-color
```

### `gateway <subcommand>`

Gateway CLI helpers (use `--url`, `--token`, `--password`, `--timeout`, `--expect-final` for RPC subcommands).
当你传入 `--url` 时，CLI 不会自动应用配置或环境凭据。
请显式包含 `--token` 或 `--password`。 缺少显式凭据将被视为错误。

子命令：

- `gateway call <method> [--params <json>]`
- `gateway health`
- `gateway status`
- `gateway probe`
- `gateway discover`
- `gateway install|uninstall|start|stop|restart`
- `gateway run`

常见 RPC：

- `config.apply`（校验 + 写入配置 + 重启 + 唤醒）
- `config.patch`（合并部分更新 + 重启 + 唤醒）
- `update.run`（运行更新 + 重启 + 唤醒）

提示：当直接调用 `config.set`/`config.apply`/`config.patch` 时，如果配置已存在，请从
`config.get` 传入 `baseHash`。

## 模型

有关回退行为和扫描策略，请参见 [/concepts/models](/concepts/models)。

首选的 Anthropic 认证（setup-token）：

```bash
claude setup-token
openclaw models auth setup-token --provider anthropic
openclaw models status
```

### `models`（根）

`openclaw models` 是 `models status` 的别名。

根选项：

- `--status-json`（`models status --json` 的别名）
- `--status-plain`（`models status --plain` 的别名）

### `models list`

选项：

- `--all`
- `--local`
- `--provider <name>`
- `--json`
- `--plain`

### `models status`

选项：

- `--json`
- `--plain`
- `--check`（退出码：1=过期/缺失，2=即将过期）
- `--probe`（对已配置的认证配置文件进行实时探测）
- `--probe-provider <name>`
- `--probe-profile <id>`（可重复或使用逗号分隔）
- `--probe-timeout <ms>`
- `--probe-concurrency <n>`
- `--probe-max-tokens <n>`

始终包含认证概览以及认证存储中各配置文件的 OAuth 过期状态。
`--probe` 会运行实时请求（可能消耗令牌并触发速率限制）。

### `models set <model>`

设置 `agents.defaults.model.primary`。

### `models set-image <model>`

设置 `agents.defaults.imageModel.primary`。

### `models aliases list|add|remove`

Options:

- `list`: `--json`, `--plain`
- `add <alias> <model>`
- `remove <alias>`

### `models fallbacks list|add|remove|clear`

Options:

- `list`: `--json`, `--plain`
- `add <model>`
- `remove <model>`
- `clear`

### `models image-fallbacks list|add|remove|clear`

Options:

- `list`: `--json`, `--plain`
- `add <model>`
- `remove <model>`
- `clear`

### `models scan`

Options:

- `--min-params <b>`
- `--max-age-days <days>`
- `--provider <name>`
- `--max-candidates <n>`
- `--timeout <ms>`
- `--concurrency <n>`
- `--no-probe`
- `--yes`
- `--no-input`
- `--set-default`
- `--set-image`
- `--json`

### `models auth add|setup-token|paste-token`

Options:

- `add`: interactive auth helper
- `setup-token`: `--provider <name>` (default `anthropic`), `--yes`
- `paste-token`: `--provider <name>`, `--profile-id <id>`, `--expires-in <duration>`

### `models auth order get|set|clear`

Options:

- `get`: `--provider <name>`, `--agent <id>`, `--json`
- `set`: `--provider <name>`, `--agent <id>`, `<profileIds...>`
- `clear`: `--provider <name>`, `--agent <id>`

## System

### `system event`

Enqueue a system event and optionally trigger a heartbeat (Gateway RPC).

Required:

- `--text <text>`

Options:

- `--mode <now|next-heartbeat>`
- `--json`
- `--url`, `--token`, `--timeout`, `--expect-final`

### `system heartbeat last|enable|disable`

1. 心跳控制（Gateway RPC）。

2. 选项：

- 3. `--json`
- 4. `--url`、`--token`、`--timeout`、`--expect-final`

### 5. `system presence`

6. 列出系统在线状态条目（Gateway RPC）。

7. 选项：

- 8. `--json`
- 9. `--url`、`--token`、`--timeout`、`--expect-final`

## 10. Cron

11. 管理计划任务（Gateway RPC）。 12. 参见 [/automation/cron-jobs](/automation/cron-jobs)。

13. 子命令：

- 14. `cron status [--json]`
- 15. `cron list [--all] [--json]`（默认表格输出；使用 `--json` 获取原始数据）
- 16. `cron add`（别名：`create`；需要 `--name` 且在 `--at` | `--every` | `--cron` 中**恰好一个**，并且在 `--system-event` | `--message` 中**恰好一个**负载）
- 17. `cron edit <id>`（修补字段）
- 18. `cron rm <id>`（别名：`remove`、`delete`）
- 19. `cron enable <id>`
- 20. `cron disable <id>`
- 21. `cron runs --id <id> [--limit <n>]`
- 22. `cron run <id> [--force]`

23. 所有 `cron` 命令都支持 `--url`、`--token`、`--timeout`、`--expect-final`。

## 24. Node 主机

25. `node` 运行一个**无界面 Node 主机**或将其作为后台服务进行管理。 参见
    [`openclaw node`](/cli/node)。

27. 子命令：

- 28. `node run --host <gateway-host> --port 18789`
- 29. `node status`
- 30. `node install [--host <gateway-host>] [--port <port>] [--tls] [--tls-fingerprint <sha256>] [--node-id <id>] [--display-name <name>] [--runtime <node|bun>] [--force]`
- 31. `node uninstall`
- 32. `node stop`
- 33. `node restart`

## 节点

`nodes` 与网关通信并以已配对的节点为目标。 36. 参见 [/nodes](/nodes)。

37. 通用选项：

- 38. `--url`、`--token`、`--timeout`、`--json`

39. 子命令：

- 40. `nodes status [--connected] [--last-connected <duration>]`
- 41. `nodes describe --node <id|name|ip>`
- 42. `nodes list [--connected] [--last-connected <duration>]`
- 43. `nodes pending`
- 44. `nodes approve <requestId>`
- 45. `nodes reject <requestId>`
- 46. `nodes rename --node <id|name|ip> --name <displayName>`
- 47. `nodes invoke --node <id|name|ip> --command <command> [--params <json>] [--invoke-timeout <ms>] [--idempotency-key <key>]`
- 48. `nodes run --node <id|name|ip> [--cwd <path>] [--env KEY=VAL] [--command-timeout <ms>] [--needs-screen-recording] [--invoke-timeout <ms>] <command...>`（Mac 节点或无界面 Node 主机）
- 49. `nodes notify --node <id|name|ip> [--title <text>] [--body <text>] [--sound <name>] [--priority <passive|active|timeSensitive>] [--delivery <system|overlay|auto>] [--invoke-timeout <ms>]`（仅限 Mac）

50. 摄像头：

- `nodes camera list --node <id|name|ip>`
- `nodes camera snap --node <id|name|ip> [--facing front|back|both] [--device-id <id>] [--max-width <px>] [--quality <0-1>] [--delay-ms <ms>] [--invoke-timeout <ms>]`
- `nodes camera clip --node <id|name|ip> [--facing front|back] [--device-id <id>] [--duration <ms|10s|1m>] [--no-audio] [--invoke-timeout <ms>]`

Canvas + screen:

- `nodes canvas snapshot --node <id|name|ip> [--format png|jpg|jpeg] [--max-width <px>] [--quality <0-1>] [--invoke-timeout <ms>]`
- `nodes canvas present --node <id|name|ip> [--target <urlOrPath>] [--x <px>] [--y <px>] [--width <px>] [--height <px>] [--invoke-timeout <ms>]`
- `nodes canvas hide --node <id|name|ip> [--invoke-timeout <ms>]`
- `nodes canvas navigate <url> --node <id|name|ip> [--invoke-timeout <ms>]`
- `nodes canvas eval [<js>] --node <id|name|ip> [--js <code>] [--invoke-timeout <ms>]`
- `nodes canvas a2ui push --node <id|name|ip> (--jsonl <path> | --text <text>) [--invoke-timeout <ms>]`
- `nodes canvas a2ui reset --node <id|name|ip> [--invoke-timeout <ms>]`
- `nodes screen record --node <id|name|ip> [--screen <index>] [--duration <ms|10s>] [--fps <n>] [--no-audio] [--out <path>] [--invoke-timeout <ms>]`

Location:

- `nodes location get --node <id|name|ip> [--max-age <ms>] [--accuracy <coarse|balanced|precise>] [--location-timeout <ms>] [--invoke-timeout <ms>]`

## Browser

Browser control CLI (dedicated Chrome/Brave/Edge/Chromium). See [`openclaw browser`](/cli/browser) and the [Browser tool](/tools/browser).

Common options:

- `--url`, `--token`, `--timeout`, `--json`
- `--browser-profile <name>`

Manage:

- `browser status`
- `browser start`
- `browser stop`
- `browser reset-profile`
- `browser tabs`
- `browser open <url>`
- `browser focus <targetId>`
- `browser close [targetId]`
- `browser profiles`
- `browser create-profile --name <name> [--color <hex>] [--cdp-url <url>]`
- `browser delete-profile --name <name>`

Inspect:

- `browser screenshot [targetId] [--full-page] [--ref <ref>] [--element <selector>] [--type png|jpeg]`
- `browser snapshot [--format aria|ai] [--target-id <id>] [--limit <n>] [--interactive] [--compact] [--depth <n>] [--selector <sel>] [--out <path>]`

Actions:

- `browser navigate <url> [--target-id <id>]`
- `browser resize <width> <height> [--target-id <id>]`
- `browser click <ref> [--double] [--button <left|right|middle>] [--modifiers <csv>] [--target-id <id>]`
- `browser type <ref> <text> [--submit] [--slowly] [--target-id <id>]`
- `browser press <key> [--target-id <id>]`
- `browser hover <ref> [--target-id <id>]`
- `browser drag <startRef> <endRef> [--target-id <id>]`
- `browser select <ref> <values...> [--target-id <id>]`
- `browser upload <paths...> [--ref <ref>] [--input-ref <ref>] [--element <selector>] [--target-id <id>] [--timeout-ms <ms>]`
- `browser fill [--fields <json>] [--fields-file <path>] [--target-id <id>]`
- `browser dialog --accept|--dismiss [--prompt <text>] [--target-id <id>] [--timeout-ms <ms>]`
- `browser wait [--time <ms>] [--text <value>] [--text-gone <value>] [--target-id <id>]`
- `browser evaluate --fn <code> [--ref <ref>] [--target-id <id>]`
- `browser console [--level <error|warn|info>] [--target-id <id>]`
- `browser pdf [--target-id <id>]`

## Docs search

### `docs [query...]`

Search the live docs index.

## TUI

### `tui`

Open the terminal UI connected to the Gateway.

Options:

- `--url <url>`
- `--token <token>`
- `--password <password>`
- `--session <key>`
- `--deliver`
- `--thinking <level>`
- `--message <text>`
- `--timeout-ms <ms>` (defaults to `agents.defaults.timeoutSeconds`)
- `--history-limit <n>`
