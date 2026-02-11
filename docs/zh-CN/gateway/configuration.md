---
summary: "All configuration options for ~/.openclaw/openclaw.json with examples"
read_when:
  - Adding or modifying config fields
title: "Configuration"
---

# Configuration 🔧

OpenClaw reads an optional **JSON5** config from `~/.openclaw/openclaw.json` (comments + trailing commas allowed).

If the file is missing, OpenClaw uses safe-ish defaults (embedded Pi agent + per-sender sessions + workspace `~/.openclaw/workspace`). You usually only need a config to:

- restrict who can trigger the bot (`channels.whatsapp.allowFrom`, `channels.telegram.allowFrom`, etc.)
- control group allowlists + mention behavior (`channels.whatsapp.groups`, `channels.telegram.groups`, `channels.discord.guilds`, `agents.list[].groupChat`)
- customize message prefixes (`messages`)
- set the agent's workspace (`agents.defaults.workspace` or `agents.list[].workspace`)
- tune the embedded agent defaults (`agents.defaults`) and session behavior (`session`)
- set per-agent identity (`agents.list[].identity`)

> **New to configuration?** Check out the [Configuration Examples](/gateway/configuration-examples) guide for complete examples with detailed explanations!

## Strict config validation

OpenClaw only accepts configurations that fully match the schema.
Unknown keys, malformed types, or invalid values cause the Gateway to **refuse to start** for safety.

When validation fails:

- The Gateway does not boot.
- Only diagnostic commands are allowed (for example: `openclaw doctor`, `openclaw logs`, `openclaw health`, `openclaw status`, `openclaw service`, `openclaw help`).
- Run `openclaw doctor` to see the exact issues.
- Run `openclaw doctor --fix` (or `--yes`) to apply migrations/repairs.

Doctor never writes changes unless you explicitly opt into `--fix`/`--yes`.

## Schema + UI hints

The Gateway exposes a JSON Schema representation of the config via `config.schema` for UI editors.
The Control UI renders a form from this schema, with a **Raw JSON** editor as an escape hatch.

Channel plugins and extensions can register schema + UI hints for their config, so channel settings
stay schema-driven across apps without hard-coded forms.

Hints (labels, grouping, sensitive fields) ship alongside the schema so clients can render
better forms without hard-coding config knowledge.

## Apply + restart (RPC)

Use `config.apply` to validate + write the full config and restart the Gateway in one step.
It writes a restart sentinel and pings the last active session after the Gateway comes back.

Warning: `config.apply` replaces the **entire config**. If you want to change only a few keys,
use `config.patch` or `openclaw config set`. Keep a backup of `~/.openclaw/openclaw.json`.

Params:

- `raw` (string) — JSON5 payload for the entire config
- `baseHash` (optional) — config hash from `config.get` (required when a config already exists)
- `sessionKey` (optional) — last active session key for the wake-up ping
- `note` (optional) — note to include in the restart sentinel
- `restartDelayMs` (optional) — delay before restart (default 2000)

Example (via `gateway call`):

```bash
openclaw gateway call config.get --params '{}' # capture payload.hash
openclaw gateway call config.apply --params '{
  "raw": "{\\n  agents: { defaults: { workspace: \\"~/.openclaw/workspace\\" } }\\n}\\n",
  "baseHash": "<hash-from-config.get>",
  "sessionKey": "agent:main:whatsapp:dm:+15555550123",
  "restartDelayMs": 1000
}'
```

## Partial updates (RPC)

Use `config.patch` to merge a partial update into the existing config without clobbering
unrelated keys. It applies JSON merge patch semantics:

- objects merge recursively
- `null` deletes a key
- arrays replace
  Like `config.apply`, it validates, writes the config, stores a restart sentinel, and schedules
  the Gateway restart (with an optional wake when `sessionKey` is provided).

Params:

- `raw` (string) — JSON5 payload containing just the keys to change
- `baseHash` (required) — config hash from `config.get`
- `sessionKey` (optional) — last active session key for the wake-up ping
- `note` (optional) — note to include in the restart sentinel
- `restartDelayMs` (optional) — delay before restart (default 2000)

Example:

```bash
openclaw gateway call config.get --params '{}' # capture payload.hash
openclaw gateway call config.patch --params '{
  "raw": "{\\n  channels: { telegram: { groups: { \\"*\\": { requireMention: false } } } }\\n}\\n",
  "baseHash": "<hash-from-config.get>",
  "sessionKey": "agent:main:whatsapp:dm:+15555550123",
  "restartDelayMs": 1000
}'
```

## Minimal config (recommended starting point)

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

Build the default image once with:

```bash
scripts/sandbox-setup.sh
```

## Self-chat mode (recommended for group control)

To prevent the bot from responding to WhatsApp @-mentions in groups (only respond to specific text triggers):

```json5
{
  agents: {
    defaults: { workspace: "~/.openclaw/workspace" },
    list: [
      {
        id: "main",
        groupChat: { mentionPatterns: ["@openclaw", "reisponde"] },
      },
    ],
  },
  channels: {
    whatsapp: {
      // Allowlist is DMs only; including your own number enables self-chat mode.
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
}
```

## Config Includes (`$include`)

Split your config into multiple files using the `$include` directive. This is useful for:

- Organizing large configs (e.g., per-client agent definitions)
- Sharing common settings across environments
- Keeping sensitive configs separate

### Basic usage

```json5
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789 },

  // Include a single file (replaces the key's value)
  agents: { $include: "./agents.json5" },

  // Include multiple files (deep-merged in order)
  broadcast: {
    $include: ["./clients/mueller.json5", "./clients/schmidt.json5"],
  },
}
```

```json5
// ~/.openclaw/agents.json5
{
  defaults: { sandbox: { mode: "all", scope: "session" } },
  list: [{ id: "main", workspace: "~/.openclaw/workspace" }],
}
```

### Merge behavior

- **Single file**: Replaces the object containing `$include`
- **Array of files**: Deep-merges files in order (later files override earlier ones)
- **With sibling keys**: Sibling keys are merged after includes (override included values)
- **Sibling keys + arrays/primitives**: Not supported (included content must be an object)

```json5
// Sibling keys override included values
{
  $include: "./base.json5", // { a: 1, b: 2 }
  b: 99, // Result: { a: 1, b: 99 }
}
```

### Nested includes

Included files can themselves contain `$include` directives (up to 10 levels deep):

```json5
// clients/mueller.json5
{
  agents: { $include: "./mueller/agents.json5" },
  broadcast: { $include: "./mueller/broadcast.json5" },
}
```

### Path resolution

- **Relative paths**: Resolved relative to the including file
- **Absolute paths**: Used as-is
- **Parent directories**: `../` references work as expected

```json5
{ "$include": "./sub/config.json5" }      // relative
{ "$include": "/etc/openclaw/base.json5" } // absolute
{ "$include": "../shared/common.json5" }   // parent dir
```

### Error handling

- **Missing file**: Clear error with resolved path
- **Parse error**: Shows which included file failed
- **Circular includes**: Detected and reported with include chain

### Example: Multi-client legal setup

```json5
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789, auth: { token: "secret" } },

  // Common agent defaults
  agents: {
    defaults: {
      sandbox: { mode: "all", scope: "session" },
    },
    // Merge agent lists from all clients
    list: { $include: ["./clients/mueller/agents.json5", "./clients/schmidt/agents.json5"] },
  },

  // Merge broadcast configs
  broadcast: {
    $include: ["./clients/mueller/broadcast.json5", "./clients/schmidt/broadcast.json5"],
  },

  channels: { whatsapp: { groupPolicy: "allowlist" } },
}
```

```json5
// ~/.openclaw/clients/mueller/agents.json5
[
  { id: "mueller-transcribe", workspace: "~/clients/mueller/transcribe" },
  { id: "mueller-docs", workspace: "~/clients/mueller/docs" },
]
```

```json5
// ~/.openclaw/clients/mueller/broadcast.json5
{
  "120363403215116621@g.us": ["mueller-transcribe", "mueller-docs"],
}
```

## Common options

### Env vars + `.env`

OpenClaw reads env vars from the parent process (shell, launchd/systemd, CI, etc.).

Additionally, it loads:

- `.env` from the current working directory (if present)
- a global fallback `.env` from `~/.openclaw/.env` (aka `$OPENCLAW_STATE_DIR/.env`)

Neither `.env` file overrides existing env vars.

You can also provide inline env vars in config. These are only applied if the
process env is missing the key (same non-overriding rule):

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
  },
}
```

See [/environment](/help/environment) for full precedence and sources.

### `env.shellEnv` (optional)

Opt-in convenience: if enabled and none of the expected keys are set yet, OpenClaw runs your login shell and imports only the missing expected keys (never overrides).
This effectively sources your shell profile.

```json5
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

Env var equivalent:

- `OPENCLAW_LOAD_SHELL_ENV=1`
- `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`

### Env var substitution in config

You can reference environment variables directly in any config string value using
`${VAR_NAME}` syntax. Variables are substituted at config load time, before validation.

```json5
{
  models: {
    providers: {
      "vercel-gateway": {
        apiKey: "${VERCEL_GATEWAY_API_KEY}",
      },
    },
  },
  gateway: {
    auth: {
      token: "${OPENCLAW_GATEWAY_TOKEN}",
    },
  },
}
```

**Rules:**

- Only uppercase env var names are matched: `[A-Z_][A-Z0-9_]*`
- Missing or empty env vars throw an error at config load
- Escape with `$${VAR}` to output a literal `${VAR}`
- Works with `$include` (included files also get substitution)

**Inline substitution:**

```json5
{
  models: {
    providers: {
      custom: {
        baseUrl: "${CUSTOM_API_BASE}/v1", // → "https://api.example.com/v1"
      },
    },
  },
}
```

### Auth storage (OAuth + API keys)

OpenClaw stores **per-agent** auth profiles (OAuth + API keys) in:

- `<agentDir>/auth-profiles.json` (default: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`)

See also: [/concepts/oauth](/concepts/oauth)

Legacy OAuth imports:

- `~/.openclaw/credentials/oauth.json` (or `$OPENCLAW_STATE_DIR/credentials/oauth.json`)

The embedded Pi agent maintains a runtime cache at:

- `<agentDir>/auth.json` (managed automatically; don’t edit manually)

Legacy agent dir (pre multi-agent):

- `~/.openclaw/agent/*` (migrated by `openclaw doctor` into `~/.openclaw/agents/<defaultAgentId>/agent/*`)

Overrides:

- OAuth dir (legacy import only): `OPENCLAW_OAUTH_DIR`
- Agent dir (default agent root override): `OPENCLAW_AGENT_DIR` (preferred), `PI_CODING_AGENT_DIR` (legacy)

On first use, OpenClaw imports `oauth.json` entries into `auth-profiles.json`.

### `auth`

Optional metadata for auth profiles. This does **not** store secrets; it maps
profile IDs to a provider + mode (and optional email) and defines the provider
rotation order used for failover.

```json5
{
  auth: {
    profiles: {
      "anthropic:me@example.com": { provider: "anthropic", mode: "oauth", email: "me@example.com" },
      "anthropic:work": { provider: "anthropic", mode: "api_key" },
    },
    order: {
      anthropic: ["anthropic:me@example.com", "anthropic:work"],
    },
  },
}
```

### `agents.list[].identity`

可选的按代理身份，用于默认值和用户体验。 这是由 macOS 入门引导助手写入的。

如果设置了，OpenClaw 会派生默认值（仅当你尚未显式设置时）：

- 从**活动代理**的 `identity.emoji` 派生 `messages.ackReaction`（回退为 👀）
- 从代理的 `identity.name`/`identity.emoji` 派生 `agents.list[].groupChat.mentionPatterns`（因此在 Telegram/Slack/Discord/Google Chat/iMessage/WhatsApp 的群组中“@Samantha”可用）
- `identity.avatar` 接受工作区相对的图片路径或远程 URL/data URL。 本地文件必须位于代理工作区内。

`identity.avatar` 接受：

- 工作区相对路径（必须保持在代理工作区内）
- `http(s)` URL
- `data:` URI

```json5
{
  agents: {
    list: [
      {
        id: "main",
        identity: {
          name: "Samantha",
          theme: "helpful sloth",
          emoji: "🦥",
          avatar: "avatars/samantha.png",
        },
      },
    ],
  },
}
```

### `wizard`

由 CLI 向导（`onboard`、`configure`、`doctor`）写入的元数据。

```json5
{
  wizard: {
    lastRunAt: "2026-01-01T00:00:00.000Z",
    lastRunVersion: "2026.1.4",
    lastRunCommit: "abc1234",
    lastRunCommand: "configure",
    lastRunMode: "local",
  },
}
```

### `logging`

- 默认日志文件：`/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- 如果你想要稳定的路径，将 `logging.file` 设为 `/tmp/openclaw/openclaw.log`。
- 控制台输出可以通过以下方式单独调节：
  - `logging.consoleLevel`（默认为 `info`，使用 `--verbose` 时提升为 `debug`）
  - `logging.consoleStyle`（`pretty` | `compact` | `json`）
- 工具摘要可以被脱敏以避免泄露机密：
  - `logging.redactSensitive`（`off` | `tools`，默认：`tools`）
  - `logging.redactPatterns`（正则字符串数组；会覆盖默认值）

```json5
{
  logging: {
    level: "info",
    file: "/tmp/openclaw/openclaw.log",
    consoleLevel: "info",
    consoleStyle: "pretty",
    redactSensitive: "tools",
    redactPatterns: [
      // Example: override defaults with your own rules.
      "\\bTOKEN\\b\\s*[=:]\\s*([\"']?)([^\\s\"']+)\\1",
      "/\\bsk-[A-Za-z0-9_-]{8,}\\b/gi",
    ],
  },
}
```

### `channels.whatsapp.dmPolicy`

控制 WhatsApp 私聊（DM）的处理方式：

- `"pairing"`（默认）：未知发送者会收到配对码；需要所有者批准
- `"allowlist"`：仅允许 `channels.whatsapp.allowFrom`（或已配对的允许存储）中的发送者
- `"open"`：允许所有入站私聊（**需要** `channels.whatsapp.allowFrom` 包含 `"*"`）
- `"disabled"`：忽略所有入站私聊

配对码在 1 小时后过期；机器人仅在创建新请求时发送配对码。 待处理的私聊配对请求默认限制为**每个频道 3 个**。

配对审批：

- `openclaw pairing list whatsapp`
- `openclaw pairing approve whatsapp <code>`

### `channels.whatsapp.allowFrom`

允许触发 WhatsApp 自动回复的 E.164 电话号码白名单（**仅限私聊**）。
如果为空且 `channels.whatsapp.dmPolicy="pairing"`，未知发送者将收到配对码。
对于群组，请使用 `channels.whatsapp.groupPolicy` + `channels.whatsapp.groupAllowFrom`。

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing", // pairing | allowlist | open | disabled
      allowFrom: ["+15555550123", "+447700900123"],
      textChunkLimit: 4000, // optional outbound chunk size (chars)
      chunkMode: "length", // optional chunking mode (length | newline)
      mediaMaxMb: 50, // optional inbound media cap (MB)
    },
  },
}
```

### `channels.whatsapp.sendReadReceipts`

控制是否将入站的 WhatsApp 消息标记为已读（蓝色对勾）。 默认值：`true`。

自聊模式即使启用也始终跳过已读回执。

按账号覆盖：`channels.whatsapp.accounts.<id>`.sendReadReceipts

```json5
{
  channels: {
    whatsapp: { sendReadReceipts: false },
  },
}
```

### `channels.whatsapp.accounts`（多账号）

在一个网关中运行多个 WhatsApp 账号：

```json5
{
  channels: {
    whatsapp: {
      accounts: {
        default: {}, // optional; keeps the default id stable
        personal: {},
        biz: {
          // Optional override. Default: ~/.openclaw/credentials/whatsapp/biz
          // authDir: "~/.openclaw/credentials/whatsapp/biz",
        },
      },
    },
  },
}
```

说明：

- 出站命令在存在 `default` 账号时默认使用该账号；否则使用第一个已配置的账号 id（按排序）。
- 遗留的单账号 Baileys 认证目录会通过 `openclaw doctor` 迁移到 `whatsapp/default`。

### `channels.telegram.accounts` / `channels.discord.accounts` / `channels.googlechat.accounts` / `channels.slack.accounts` / `channels.mattermost.accounts` / `channels.signal.accounts` / `channels.imessage.accounts`

在每个通道中运行多个账号（每个账号都有自己的 `accountId` 和可选的 `name`）：

```json5
{
  channels: {
    telegram: {
      accounts: {
        default: {
          name: "Primary bot",
          botToken: "123456:ABC...",
        },
        alerts: {
          name: "Alerts bot",
          botToken: "987654:XYZ...",
        },
      },
    },
  },
}
```

说明：

- 当省略 `accountId` 时使用 `default`（CLI + 路由）。
- 环境变量中的 token 仅适用于 **default** 账号。
- 基础通道设置（群组策略、提及门控等） 除非在账号级别覆盖，否则适用于所有账号。
- 使用 `bindings[].match.accountId` 将每个账号路由到不同的 agents.defaults。

### 群聊提及门控（`agents.list[].groupChat` + `messages.groupChat`）

群消息默认 **需要提及**（元数据提及或正则模式之一）。 适用于 WhatsApp、Telegram、Discord、Google Chat 和 iMessage 的群聊。

**提及类型：**

- **元数据提及**：平台原生的 @ 提及（例如 WhatsApp 的点击提及）。 在 WhatsApp 自聊模式下会被忽略（参见 `channels.whatsapp.allowFrom`）。
- **文本模式**：在 `agents.list[].groupChat.mentionPatterns` 中定义的正则模式。 无论是否为自聊模式，都会始终检查。
- 只有在能够进行提及检测时（原生提及或至少存在一个 `mentionPattern`）才会强制执行提及门控。

```json5
{
  messages: {
    groupChat: { historyLimit: 50 },
  },
  agents: {
    list: [{ id: "main", groupChat: { mentionPatterns: ["@openclaw", "openclaw"] } }],
  },
}
```

`messages.groupChat.historyLimit` 设置群历史上下文的全局默认值。 通道可以通过 `channels.<channel>``.historyLimit`（或多账号情况下的 `channels.<channel>``.accounts.*.historyLimit`）进行覆盖。 将其设置为 `0` 以禁用历史包装。

#### DM 历史限制

DM 会话使用由代理管理的基于会话的历史记录。 你可以限制每个 DM 会话中保留的用户轮次数：

```json5
{
  channels: {
    telegram: {
      dmHistoryLimit: 30, // limit DM sessions to 30 user turns
      dms: {
        "123456789": { historyLimit: 50 }, // per-user override (user ID)
      },
    },
  },
}
```

解析顺序：

1. 按 DM 覆盖：`channels.<provider>``.dms[userId].historyLimit`
2. 提供方默认值：`channels.<provider>``.dmHistoryLimit`
3. 无限制（保留全部历史）。

支持的提供方：`telegram`、`whatsapp`、`discord`、`slack`、`signal`、`imessage`、`msteams`。

按代理覆盖（一旦设置即优先生效，即使为 `[]`）：

```json5
{
  agents: {
    list: [
      { id: "work", groupChat: { mentionPatterns: ["@workbot", "\\+15555550123"] } },
      { id: "personal", groupChat: { mentionPatterns: ["@homebot", "\\+15555550999"] } },
    ],
  },
}
```

提及门控的默认值按通道设置（`channels.whatsapp.groups`、`channels.telegram.groups`、`channels.imessage.groups`、`channels.discord.guilds`）。 当设置了 `*.groups` 时，它也会作为群组白名单；包含 `"*"` 以允许所有群组。

若要 **仅** 响应特定文本触发（忽略原生 @ 提及）：

```json5
{
  channels: {
    whatsapp: {
      // Include your own number to enable self-chat mode (ignore native @-mentions).
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          // Only these text patterns will trigger responses
          mentionPatterns: ["reisponde", "@openclaw"],
        },
      },
    ],
  },
}
```

### 群组策略（按通道）

Use `channels.*.groupPolicy` to control whether group/room messages are accepted at all:

```json5
{
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
    telegram: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["tg:123456789", "@alice"],
    },
    signal: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
    imessage: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["chat_id:123"],
    },
    msteams: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["user@org.com"],
    },
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        GUILD_ID: {
          channels: { help: { allow: true } },
        },
      },
    },
    slack: {
      groupPolicy: "allowlist",
      channels: { "#general": { allow: true } },
    },
  },
}
```

说明：

- `"open"`: groups bypass allowlists; mention-gating still applies.
- `"disabled"`: block all group/room messages.
- `"allowlist"`: only allow groups/rooms that match the configured allowlist.
- `channels.defaults.groupPolicy` sets the default when a provider’s `groupPolicy` is unset.
- WhatsApp/Telegram/Signal/iMessage/Microsoft Teams use `groupAllowFrom` (fallback: explicit `allowFrom`).
- Discord/Slack use channel allowlists (`channels.discord.guilds.*.channels`, `channels.slack.channels`).
- Group DMs (Discord/Slack) are still controlled by `dm.groupEnabled` + `dm.groupChannels`.
- Default is `groupPolicy: "allowlist"` (unless overridden by `channels.defaults.groupPolicy`); if no allowlist is configured, group messages are blocked.

### Multi-agent routing (`agents.list` + `bindings`)

Run multiple isolated agents (separate workspace, `agentDir`, sessions) inside one Gateway.
Inbound messages are routed to an agent via bindings.

- `agents.list[]`: per-agent overrides.
  - `id`: stable agent id (required).
  - `default`: optional; when multiple are set, the first wins and a warning is logged.
    If none are set, the **first entry** in the list is the default agent.
  - `name`: display name for the agent.
  - `workspace`: default `~/.openclaw/workspace-<agentId>` (for `main`, falls back to `agents.defaults.workspace`).
  - `agentDir`: default `~/.openclaw/agents/<agentId>/agent`.
  - `model`: per-agent default model, overrides `agents.defaults.model` for that agent.
    - string form: `"provider/model"`, overrides only `agents.defaults.model.primary`
    - object form: `{ primary, fallbacks }` (fallbacks override `agents.defaults.model.fallbacks`; `[]` disables global fallbacks for that agent)
  - `identity`: per-agent name/theme/emoji (used for mention patterns + ack reactions).
  - `groupChat`: per-agent mention-gating (`mentionPatterns`).
  - `sandbox`: per-agent sandbox config (overrides `agents.defaults.sandbox`).
    - `mode`: `"off"` | `"non-main"` | `"all"`
    - `workspaceAccess`: `"none"` | `"ro"` | `"rw"`
    - `scope`: `"session"` | `"agent"` | `"shared"`
    - `workspaceRoot`: custom sandbox workspace root
    - `docker`: per-agent docker overrides (e.g. `image`, `network`, `env`, `setupCommand`, limits; ignored when `scope: "shared"`)
    - `browser`: per-agent sandboxed browser overrides (ignored when `scope: "shared"`)
    - `prune`: per-agent sandbox pruning overrides (ignored when `scope: "shared"`)
  - `subagents`: per-agent sub-agent defaults.
    - `allowAgents`: allowlist of agent ids for `sessions_spawn` from this agent (`["*"]` = allow any; default: only same agent)
  - `tools`: per-agent tool restrictions (applied before sandbox tool policy).
    - `profile`: base tool profile (applied before allow/deny)
    - `allow`: array of allowed tool names
    - `deny`: array of denied tool names (deny wins)
- `agents.defaults`: shared agent defaults (model, workspace, sandbox, etc.).
- `bindings[]`: routes inbound messages to an `agentId`.
  - `match.channel` (required)
  - `match.accountId` (optional; `*` = any account; omitted = default account)
  - `match.peer` (optional; `{ kind: direct|group|channel, id }`)
  - `match.guildId` / `match.teamId` (optional; channel-specific)

Deterministic match order:

1. `match.peer`
2. `match.guildId`
3. `match.teamId`
4. `match.accountId` (exact, no peer/guild/team)
5. `match.accountId: "*"` (channel-wide, no peer/guild/team)
6. default agent (`agents.list[].default`, else first list entry, else `"main"`)

Within each match tier, the first matching entry in `bindings` wins.

#### Per-agent access profiles (multi-agent)

Each agent can carry its own sandbox + tool policy. Use this to mix access
levels in one gateway:

- **Full access** (personal agent)
- **Read-only** tools + workspace
- **No filesystem access** (messaging/session tools only)

See [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools) for precedence and
additional examples.

Full access (no sandbox):

```json5
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: { mode: "off" },
      },
    ],
  },
}
```

Read-only tools + read-only workspace:

```json5
{
  agents: {
    list: [
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "ro",
        },
        tools: {
          allow: [
            "read",
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
          ],
          deny: ["write", "edit", "apply_patch", "exec", "process", "browser"],
        },
      },
    ],
  },
}
```

No filesystem access (messaging/session tools enabled):

```json5
{
  agents: {
    list: [
      {
        id: "public",
        workspace: "~/.openclaw/workspace-public",
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "none",
        },
        tools: {
          allow: [
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
            "whatsapp",
            "telegram",
            "slack",
            "discord",
            "gateway",
          ],
          deny: [
            "read",
            "write",
            "edit",
            "apply_patch",
            "exec",
            "process",
            "browser",
            "canvas",
            "nodes",
            "cron",
            "gateway",
            "image",
          ],
        },
      },
    ],
  },
}
```

Example: two WhatsApp accounts → two agents:

```json5
{
  agents: {
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
  channels: {
    whatsapp: {
      accounts: {
        personal: {},
        biz: {},
      },
    },
  },
}
```

### `tools.agentToAgent` (optional)

Agent-to-agent messaging is opt-in:

```json5
{
  tools: {
    agentToAgent: {
      enabled: false,
      allow: ["home", "work"],
    },
  },
}
```

### `messages.queue`

Controls how inbound messages behave when an agent run is already active.

```json5
{
  messages: {
    queue: {
      mode: "collect", // steer | followup | collect | steer-backlog (steer+backlog ok) | interrupt (queue=steer legacy)
      debounceMs: 1000,
      cap: 20,
      drop: "summarize", // old | new | summarize
      byChannel: {
        whatsapp: "collect",
        telegram: "collect",
        discord: "collect",
        imessage: "collect",
        webchat: "collect",
      },
    },
  },
}
```

### `messages.inbound`

Debounce rapid inbound messages from the **same sender** so multiple back-to-back
messages become a single agent turn. Debouncing is scoped per channel + conversation
and uses the most recent message for reply threading/IDs.

```json5
{
  messages: {
    inbound: {
      debounceMs: 2000, // 0 disables
      byChannel: {
        whatsapp: 5000,
        slack: 1500,
        discord: 1500,
      },
    },
  },
}
```

Notes:

- Debounce batches **text-only** messages; media/attachments flush immediately.
- Control commands (e.g. `/queue`, `/new`) bypass debouncing so they stay standalone.

### `commands` (chat command handling)

Controls how chat commands are enabled across connectors.

```json5
{
  commands: {
    native: "auto", // register native commands when supported (auto)
    text: true, // parse slash commands in chat messages
    bash: false, // allow ! (alias: /bash) (host-only; requires tools.elevated allowlists)
    bashForegroundMs: 2000, // bash foreground window (0 backgrounds immediately)
    config: false, // allow /config (writes to disk)
    debug: false, // allow /debug (runtime-only overrides)
    restart: false, // allow /restart + gateway restart tool
    useAccessGroups: true, // enforce access-group allowlists/policies for commands
  },
}
```

Notes:

- Text commands must be sent as a **standalone** message and use the leading `/` (no plain-text aliases).
- `commands.text: false` disables parsing chat messages for commands.
- `commands.native: "auto"` (default) turns on native commands for Discord/Telegram and leaves Slack off; unsupported channels stay text-only.
- Set `commands.native: true|false` to force all, or override per channel with `channels.discord.commands.native`, `channels.telegram.commands.native`, `channels.slack.commands.native` (bool or `"auto"`). `false` clears previously registered commands on Discord/Telegram at startup; Slack commands are managed in the Slack app.
- `channels.telegram.customCommands` adds extra Telegram bot menu entries. Names are normalized; conflicts with native commands are ignored.
- `commands.bash: true` enables `! <cmd>` to run host shell commands (`/bash <cmd>` also works as an alias). Requires `tools.elevated.enabled` and allowlisting the sender in `tools.elevated.allowFrom.<channel>`.
- `commands.bashForegroundMs` controls how long bash waits before backgrounding. While a bash job is running, new `! <cmd>` requests are rejected (one at a time).
- `commands.config: true` enables `/config` (reads/writes `openclaw.json`).
- `channels.<provider>.configWrites` gates config mutations initiated by that channel (default: true). This applies to `/config set|unset` plus provider-specific auto-migrations (Telegram supergroup ID changes, Slack channel ID changes).
- `commands.debug: true` enables `/debug` (runtime-only overrides).
- `commands.restart: true` 启用 `/restart` 以及网关工具的重启动作。
- `commands.useAccessGroups: false` allows commands to bypass access-group allowlists/policies.
- 斜杠命令和指令仅对**已授权的发送者**生效。 Authorization is derived from
  channel allowlists/pairing plus `commands.useAccessGroups`.

### `web` (WhatsApp web channel runtime)

WhatsApp 通过网关的 web 渠道运行（Baileys Web）。 当存在已链接的会话时，它会自动启动。
设置 `web.enabled: false` 可使其默认保持关闭。

```json5
{
  web: {
    enabled: true,
    heartbeatSeconds: 60,
    reconnect: {
      initialMs: 2000,
      maxMs: 120000,
      factor: 1.4,
      jitter: 0.2,
      maxAttempts: 0,
    },
  },
}
```

### `channels.telegram`（机器人传输）

只有当存在 `channels.telegram` 配置段时，OpenClaw 才会启动 Telegram。 The bot token is resolved from `channels.telegram.botToken` (or `channels.telegram.tokenFile`), with `TELEGRAM_BOT_TOKEN` as a fallback for the default account.
设置 `channels.telegram.enabled: false` 以禁用自动启动。
Multi-account support lives under `channels.telegram.accounts` (see the multi-account section above). 环境变量令牌仅适用于默认账户。
设置 `channels.telegram.configWrites: false` 以阻止 Telegram 发起的配置写入（包括超级群 ID 迁移以及 `/config set|unset`）。

````json5
```
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "your-bot-token",
      dmPolicy: "pairing", // pairing | allowlist | open | disabled
      allowFrom: ["tg:123456789"], // optional; "open" requires ["*"]
      groups: {
        "*": { requireMention: true },
        "-1001234567890": {
          allowFrom: ["@admin"],
          systemPrompt: "Keep answers brief.",
          topics: {
            "99": {
              requireMention: false,
              skills: ["search"],
              systemPrompt: "Stay on topic.",
            },
          },
        },
      },
      customCommands: [
        { command: "backup", description: "Git backup" },
        { command: "generate", description: "Create an image" },
      ],
      historyLimit: 50, // include last N group messages as context (0 disables)
      replyToMode: "first", // off | first | all
      linkPreview: true, // toggle outbound link previews
      streamMode: "partial", // off | partial | block (draft streaming; separate from block streaming)
      draftChunk: {
        // optional; only for streamMode=block
        minChars: 200,
        maxChars: 800,
        breakPreference: "paragraph", // paragraph | newline | sentence
      },
      actions: { reactions: true, sendMessage: true }, // tool action gates (false disables)
      reactionNotifications: "own", // off | own | all
      mediaMaxMb: 5,
      retry: {
        // outbound retry policy
        attempts: 3,
        minDelayMs: 400,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
      network: {
        // transport overrides
        autoSelectFamily: false,
      },
      proxy: "socks5://localhost:9050",
      webhookUrl: "https://example.com/telegram-webhook", // requires webhookSecret
      webhookSecret: "secret",
      webhookPath: "/telegram-webhook",
    },
  },
}
```
````

草稿流式传输说明：

- 使用 Telegram 的 `sendMessageDraft`（草稿气泡，而非真实消息）。
- 需要**私聊主题**（私信中的 message_thread_id；机器人已启用主题）。
- `/reasoning stream` 会将推理过程流式写入草稿，然后发送最终答案。
  重试策略的默认值和行为记录在 [Retry policy](/concepts/retry)。

### `channels.discord`（机器人传输）

通过设置机器人令牌和可选的门控来配置 Discord 机器人：
多账户支持位于 `channels.discord.accounts` 下（参见上方的多账户部分）。 环境变量令牌仅适用于默认账户。

````json5
```
{
  channels: {
    discord: {
      enabled: true,
      token: "your-bot-token",
      mediaMaxMb: 8, // clamp inbound media size
      allowBots: false, // allow bot-authored messages
      actions: {
        // tool action gates (false disables)
        reactions: true,
        stickers: true,
        polls: true,
        permissions: true,
        messages: true,
        threads: true,
        pins: true,
        search: true,
        memberInfo: true,
        roleInfo: true,
        roles: false,
        channelInfo: true,
        voiceStatus: true,
        events: true,
        moderation: false,
      },
      replyToMode: "off", // off | first | all
      dm: {
        enabled: true, // disable all DMs when false
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["1234567890", "steipete"], // optional DM allowlist ("open" requires ["*"])
        groupEnabled: false, // enable group DMs
        groupChannels: ["openclaw-dm"], // optional group DM allowlist
      },
      guilds: {
        "123456789012345678": {
          // guild id (preferred) or slug
          slug: "friends-of-openclaw",
          requireMention: false, // per-guild default
          reactionNotifications: "own", // off | own | all | allowlist
          users: ["987654321098765432"], // optional per-guild user allowlist
          channels: {
            general: { allow: true },
            help: {
              allow: true,
              requireMention: true,
              users: ["987654321098765432"],
              skills: ["docs"],
              systemPrompt: "Short answers only.",
            },
          },
        },
      },
      historyLimit: 20, // include last N guild messages as context
      textChunkLimit: 2000, // optional outbound text chunk size (chars)
      chunkMode: "length", // optional chunking mode (length | newline)
      maxLinesPerMessage: 17, // soft max lines per message (Discord UI clipping)
      retry: {
        // outbound retry policy
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}
```
````

只有当存在 `channels.discord` 配置段时，OpenClaw 才会启动 Discord。 令牌从 `channels.discord.token` 解析；默认账户在缺省时会回退到 `DISCORD_BOT_TOKEN`（除非 `channels.discord.enabled` 为 `false`）。 在为 cron/CLI 命令指定投递目标时，使用 `user:<id>`（私信）或 `channel:<id>`（服务器频道）；裸的数字 ID 含义不明确并会被拒绝。
服务器 slug 为小写，空格替换为 `-`；频道键使用已 slug 化的频道名（不带前导 `#`）。 为避免重命名歧义，优先使用服务器 id 作为键。
默认情况下会忽略由机器人自身发送的消息。 通过 `channels.discord.allowBots` 启用（仍会过滤自身消息以防止自回复循环）。
表情反应通知模式：

- `off`: no reaction events.
- `own`：机器人自身消息上的反应（默认）。
- `all`：所有消息上的所有反应。
- `allowlist`：来自 `guilds.<id>`
  .users`在所有消息上的反应（空列表将禁用）。
    出站文本按`channels.discord.textChunkLimit`（默认 2000）进行分块。 Set `channels.discord.chunkMode="newline"` to split on blank lines (paragraph boundaries) before length chunking. Discord 客户端可能会裁剪非常高的消息，因此即使少于 2000 个字符，`channels.discord.maxLinesPerMessage\`（默认 17）也会拆分很长的多行回复。
  重试策略的默认值和行为记录在 [Retry policy](/concepts/retry)。

### `channels.googlechat`（Chat API webhook）

Google Chat 通过 HTTP webhook 运行，并使用应用级认证（服务账号）。
多账户支持位于 `channels.googlechat.accounts` 下（参见上方的多账户部分）。 环境变量仅适用于默认账户。

````json5
```
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountFile: "/path/to/service-account.json",
      audienceType: "app-url", // app-url | project-number
      audience: "https://gateway.example.com/googlechat",
      webhookPath: "/googlechat",
      botUser: "users/1234567890", // optional; improves mention detection
      dm: {
        enabled: true,
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["users/1234567890"], // optional; "open" requires ["*"]
      },
      groupPolicy: "allowlist",
      groups: {
        "spaces/AAAA": { allow: true, requireMention: true },
      },
      actions: { reactions: true },
      typingIndicator: "message",
      mediaMaxMb: 20,
    },
  },
}
```
````

说明：

- Service account JSON can be inline (`serviceAccount`) or file-based (`serviceAccountFile`).
- Env fallbacks for the default account: `GOOGLE_CHAT_SERVICE_ACCOUNT` or `GOOGLE_CHAT_SERVICE_ACCOUNT_FILE`.
- `audienceType` + `audience` must match the Chat app’s webhook auth config.
- Use `spaces/<spaceId>` or `users/<userId|email>` when setting delivery targets.

### `channels.slack` (socket mode)

Slack runs in Socket Mode and requires both a bot token and app token:

```json5
{
  channels: {
    slack: {
      enabled: true,
      botToken: "xoxb-...",
      appToken: "xapp-...",
      dm: {
        enabled: true,
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["U123", "U456", "*"], // optional; "open" requires ["*"]
        groupEnabled: false,
        groupChannels: ["G123"],
      },
      channels: {
        C123: { allow: true, requireMention: true, allowBots: false },
        "#general": {
          allow: true,
          requireMention: true,
          allowBots: false,
          users: ["U123"],
          skills: ["docs"],
          systemPrompt: "Short answers only.",
        },
      },
      historyLimit: 50, // include last N channel/group messages as context (0 disables)
      allowBots: false,
      reactionNotifications: "own", // off | own | all | allowlist
      reactionAllowlist: ["U123"],
      replyToMode: "off", // off | first | all
      thread: {
        historyScope: "thread", // thread | channel
        inheritParent: false,
      },
      actions: {
        reactions: true,
        messages: true,
        pins: true,
        memberInfo: true,
        emojiList: true,
      },
      slashCommand: {
        enabled: true,
        name: "openclaw",
        sessionPrefix: "slack:slash",
        ephemeral: true,
      },
      textChunkLimit: 4000,
      chunkMode: "length",
      mediaMaxMb: 20,
    },
  },
}
```

Multi-account support lives under `channels.slack.accounts` (see the multi-account section above). Env tokens only apply to the default account.

OpenClaw starts Slack when the provider is enabled and both tokens are set (via config or `SLACK_BOT_TOKEN` + `SLACK_APP_TOKEN`). Use `user:<id>` (DM) or `channel:<id>` when specifying delivery targets for cron/CLI commands.
Set `channels.slack.configWrites: false` to block Slack-initiated config writes (including channel ID migrations and `/config set|unset`).

Bot-authored messages are ignored by default. Enable with `channels.slack.allowBots` or `channels.slack.channels.<id>.allowBots`.

Reaction notification modes:

- `off`: no reaction events.
- `own`: reactions on the bot's own messages (default).
- `all`: all reactions on all messages.
- `allowlist`: reactions from `channels.slack.reactionAllowlist` on all messages (empty list disables).

Thread session isolation:

- `channels.slack.thread.historyScope` controls whether thread history is per-thread (`thread`, default) or shared across the channel (`channel`).
- `channels.slack.thread.inheritParent` controls whether new thread sessions inherit the parent channel transcript (default: false).

Slack action groups (gate `slack` tool actions):

| Action group | Default | Notes                  |
| ------------ | ------- | ---------------------- |
| reactions    | enabled | React + list reactions |
| messages     | enabled | Read/send/edit/delete  |
| pins         | enabled | Pin/unpin/list         |
| memberInfo   | enabled | Member info            |
| emojiList    | enabled | Custom emoji list      |

### `channels.mattermost` (bot token)

Mattermost ships as a plugin and is not bundled with the core install.
Install it first: `openclaw plugins install @openclaw/mattermost` (or `./extensions/mattermost` from a git checkout).

Mattermost requires a bot token plus the base URL for your server:

```json5
{
  channels: {
    mattermost: {
      enabled: true,
      botToken: "mm-token",
      baseUrl: "https://chat.example.com",
      dmPolicy: "pairing",
      chatmode: "oncall", // oncall | onmessage | onchar
      oncharPrefixes: [">", "!"],
      textChunkLimit: 4000,
      chunkMode: "length",
    },
  },
}
```

OpenClaw starts Mattermost when the account is configured (bot token + base URL) and enabled. The token + base URL are resolved from `channels.mattermost.botToken` + `channels.mattermost.baseUrl` or `MATTERMOST_BOT_TOKEN` + `MATTERMOST_URL` for the default account (unless `channels.mattermost.enabled` is `false`).

Chat modes:

- `oncall` (default): respond to channel messages only when @mentioned.
- `onmessage`: respond to every channel message.
- `onchar`: respond when a message starts with a trigger prefix (`channels.mattermost.oncharPrefixes`, default `[">", "!"]`).

Access control:

- Default DMs: `channels.mattermost.dmPolicy="pairing"` (unknown senders get a pairing code).
- Public DMs: `channels.mattermost.dmPolicy="open"` plus `channels.mattermost.allowFrom=["*"]`.
- Groups: `channels.mattermost.groupPolicy="allowlist"` by default (mention-gated). Use `channels.mattermost.groupAllowFrom` to restrict senders.

Multi-account support lives under `channels.mattermost.accounts` (see the multi-account section above). Env vars only apply to the default account.
Use `channel:<id>` or `user:<id>` (or `@username`) when specifying delivery targets; bare ids are treated as channel ids.

### `channels.signal` (signal-cli)

Signal reactions can emit system events (shared reaction tooling):

```json5
{
  channels: {
    signal: {
      reactionNotifications: "own", // off | own | all | allowlist
      reactionAllowlist: ["+15551234567", "uuid:123e4567-e89b-12d3-a456-426614174000"],
      historyLimit: 50, // include last N group messages as context (0 disables)
    },
  },
}
```

Reaction notification modes:

- `off`: no reaction events.
- `own`: reactions on the bot's own messages (default).
- `all`: all reactions on all messages.
- `allowlist`: reactions from `channels.signal.reactionAllowlist` on all messages (empty list disables).

### `channels.imessage` (imsg CLI)

OpenClaw spawns `imsg rpc` (JSON-RPC over stdio). No daemon or port required.

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "imsg",
      dbPath: "~/Library/Messages/chat.db",
      remoteHost: "user@gateway-host", // SCP for remote attachments when using SSH wrapper
      dmPolicy: "pairing", // pairing | allowlist | open | disabled
      allowFrom: ["+15555550123", "user@example.com", "chat_id:123"],
      historyLimit: 50, // include last N group messages as context (0 disables)
      includeAttachments: false,
      mediaMaxMb: 16,
      service: "auto",
      region: "US",
    },
  },
}
```

Multi-account support lives under `channels.imessage.accounts` (see the multi-account section above).

Notes:

- Requires Full Disk Access to the Messages DB.
- The first send will prompt for Messages automation permission.
- Prefer `chat_id:<id>` targets. Use `imsg chats --limit 20` to list chats.
- `channels.imessage.cliPath` can point to a wrapper script (e.g. `ssh` to another Mac that runs `imsg rpc`); use SSH keys to avoid password prompts.
- For remote SSH wrappers, set `channels.imessage.remoteHost` to fetch attachments via SCP when `includeAttachments` is enabled.

Example wrapper:

```bash
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"
```

### `agents.defaults.workspace`

Sets the **single global workspace directory** used by the agent for file operations.

Default: `~/.openclaw/workspace`.

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

If `agents.defaults.sandbox` is enabled, non-main sessions can override this with their
own per-scope workspaces under `agents.defaults.sandbox.workspaceRoot`.

### `agents.defaults.repoRoot`

Optional repository root to show in the system prompt’s Runtime line. If unset, OpenClaw
tries to detect a `.git` directory by walking upward from the workspace (and current
working directory). The path must exist to be used.

```json5
{
  agents: { defaults: { repoRoot: "~/Projects/openclaw" } },
}
```

### `agents.defaults.skipBootstrap`

Disables automatic creation of the workspace bootstrap files (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, and `BOOTSTRAP.md`).

Use this for pre-seeded deployments where your workspace files come from a repo.

```json5
{
  agents: { defaults: { skipBootstrap: true } },
}
```

### `agents.defaults.bootstrapMaxChars`

Max characters of each workspace bootstrap file injected into the system prompt
before truncation. Default: `20000`.

当文件超过此限制时，OpenClaw 会记录一条警告，并注入一个带有标记的截断头/尾。

```json5
{
  agents: { defaults: { bootstrapMaxChars: 20000 } },
}
```

### `agents.defaults.userTimezone`

为 **系统提示上下文** 设置用户的时区（不用于消息信封中的时间戳）。 如果未设置，OpenClaw 会在运行时使用主机时区。

```json5
{
  agents: { defaults: { userTimezone: "America/Chicago" } },
}
```

### `agents.defaults.timeFormat`

控制系统提示中“当前日期与时间”部分显示的 **时间格式**。
默认值：`auto`（操作系统偏好）。

```json5
{
  agents: { defaults: { timeFormat: "auto" } }, // auto | 12 | 24
}
```

### `messages`

控制入站/出站前缀以及可选的确认（ack）反应。
有关队列、会话和流式上下文，请参阅 [Messages](/concepts/messages)。

```json5
{
  messages: {
    responsePrefix: "🦞", // or "auto"
    ackReaction: "👀",
    ackReactionScope: "group-mentions",
    removeAckAfterReply: false,
  },
}
```

`responsePrefix` 会应用于 **所有出站回复**（工具摘要、分块流式输出、最终回复），跨所有通道，除非已存在前缀。

可以按通道和按账号配置覆盖：

- `channels.<channel>``.responsePrefix`
- `channels.<channel>``.accounts.<id>``.responsePrefix`

解析顺序（越具体优先级越高）：

1. `channels.<channel>``.accounts.<id>``.responsePrefix`
2. `channels.<channel>``.responsePrefix`
3. `messages.responsePrefix`

语义：

- `undefined` 会继续向下一级传递。
- `""` 会显式禁用前缀并停止级联。
- `"auto"` 会为路由到的代理派生 `[{identity.name}]`。

覆盖适用于所有通道（包括扩展）以及每一种出站回复类型。

如果未设置 `messages.responsePrefix`，默认不应用任何前缀。 WhatsApp 自聊回复是例外：当设置时默认使用 `[{identity.name}]`，否则使用 `[openclaw]`，以便同一部手机上的对话保持可读。
将其设置为 `"auto"`，以便为路由到的代理派生 `[{identity.name}]`（在已设置时）。

#### 模板变量

`responsePrefix` 字符串可以包含会动态解析的模板变量：

| 变量                | 描述      | 示例                          |
| ----------------- | ------- | --------------------------- |
| `{model}`         | 简短模型名称  | `claude-opus-4-6`, `gpt-4o` |
| `{modelFull}`     | 完整模型标识符 | `anthropic/claude-opus-4-6` |
| `{provider}`      | 提供方名称   | `anthropic`, `openai`       |
| `{thinkingLevel}` | 当前思考级别  | `high`, `low`, `off`        |
| `{identity.name}` | 代理身份名称  | （与 `"auto"` 模式相同）           |

变量不区分大小写（`{MODEL}` = `{model}`）。 `{think}` 是 `{thinkingLevel}` 的别名。
未解析的变量将保持为字面文本。

```json5
{
  messages: {
    responsePrefix: "[{model} | think:{thinkingLevel}]",
  },
}
```

示例输出：`[claude-opus-4-6 | think:high] 这是我的回复...`

WhatsApp 入站前缀通过 `channels.whatsapp.messagePrefix` 配置（已弃用：
`messages.messagePrefix`）。 Default stays **unchanged**: `"[openclaw]"` when
`channels.whatsapp.allowFrom` is empty, otherwise `""` (no prefix). 当使用
`"[openclaw]"` 时，如果路由到的代理设置了 `identity.name`，OpenClaw 将改为使用 `[{identity.name}]`。

`ackReaction` sends a best-effort emoji reaction to acknowledge inbound messages
on channels that support reactions (Slack/Discord/Telegram/Google Chat). 默认使用当前活动代理的 `identity.emoji`（如果已设置），否则使用 `"👀"`。 将其设置为 `""` 以禁用。

`ackReactionScope` 控制反应触发的时机：

- `group-mentions` (default): only when a group/room requires mentions **and** the bot was mentioned
- `group-all`：所有群组/房间消息
- `direct`：仅直接消息
- `all`：所有消息

`removeAckAfterReply` 会在发送回复后移除机器人的确认反应（仅适用于 Slack/Discord/Telegram/Google Chat）。 默认值：`false`。

#### `messages.tts`

为出站回复启用文本转语音。 When on, OpenClaw generates audio
using ElevenLabs or OpenAI and attaches it to responses. Telegram 使用 Opus 语音消息；其他渠道发送 MP3 音频。

```json5
{
  messages: {
    tts: {
      auto: "always", // off | always | inbound | tagged
      mode: "final", // final | all (include tool/block replies)
      provider: "elevenlabs",
      summaryModel: "openai/gpt-4.1-mini",
      modelOverrides: {
        enabled: true,
      },
      maxTextLength: 4000,
      timeoutMs: 30000,
      prefsPath: "~/.openclaw/settings/tts.json",
      elevenlabs: {
        apiKey: "elevenlabs_api_key",
        baseUrl: "https://api.elevenlabs.io",
        voiceId: "voice_id",
        modelId: "eleven_multilingual_v2",
        seed: 42,
        applyTextNormalization: "auto",
        languageCode: "en",
        voiceSettings: {
          stability: 0.5,
          similarityBoost: 0.75,
          style: 0.0,
          useSpeakerBoost: true,
          speed: 1.0,
        },
      },
      openai: {
        apiKey: "openai_api_key",
        model: "gpt-4o-mini-tts",
        voice: "alloy",
      },
    },
  },
}
```

Notes:

- `messages.tts.auto` 控制自动 TTS（`off`、`always`、`inbound`、`tagged`）。
- `/tts off|always|inbound|tagged` 设置每个会话的自动模式（覆盖配置）。
- `messages.tts.enabled` 为旧配置；doctor 会将其迁移到 `messages.tts.auto`。
- `prefsPath` 存储本地覆盖项（provider/limit/summarize）。
- `maxTextLength` 是 TTS 输入的硬性上限；摘要将被截断以适配。
- `summaryModel` 会覆盖 `agents.defaults.model.primary`，用于自动摘要。
  - 接受 `provider/model` 或来自 `agents.defaults.models` 的别名。
- `modelOverrides` 启用模型驱动的覆盖（如 `[[tts:...]]` 标签，默认开启）。
- `/tts limit` 和 `/tts summary` 控制每用户的摘要设置。
- `apiKey` 值会回退到 `ELEVENLABS_API_KEY`/`XI_API_KEY` 和 `OPENAI_API_KEY`。
- `elevenlabs.baseUrl` 用于覆盖 ElevenLabs API 的基础 URL。
- `elevenlabs.voiceSettings` 支持 `stability`/`similarityBoost`/`style`（0..1）、
  `useSpeakerBoost` 以及 `speed`（0.5..2.0）。

### `talk`

Talk 模式的默认设置（macOS/iOS/Android）。 当未设置时，Voice ID 会回退到 `ELEVENLABS_VOICE_ID` 或 `SAG_VOICE_ID`。
当未设置时，`apiKey` 会回退到 `ELEVENLABS_API_KEY`（或网关的 shell 配置）。
`voiceAliases` 允许 Talk 指令使用友好名称（例如 `"voice":"Clawd"`）。

```json5
{
  talk: {
    voiceId: "elevenlabs_voice_id",
    voiceAliases: {
      Clawd: "EXAVITQu4vr4xnSDxMaL",
      Roger: "CwhRBWXzGAHq8TQ4Fs17",
    },
    modelId: "eleven_v3",
    outputFormat: "mp3_44100_128",
    apiKey: "elevenlabs_api_key",
    interruptOnSpeech: true,
  },
}
```

### `agents.defaults`

控制嵌入式代理运行时（模型/思考/详细输出/超时）。
`agents.defaults.models` 定义了已配置的模型目录（并充当 `/model` 的允许列表）。
`agents.defaults.model.primary` 设置默认模型；`agents.defaults.model.fallbacks` 是全局故障转移。
`agents.defaults.imageModel` 是可选的，**仅在主模型不支持图像输入时使用**。
Each `agents.defaults.models` entry can include:

- `alias`（可选的模型快捷别名，例如 `/opus`）。
- `params`（可选的、提供商特定的 API 参数，会原样传递到模型请求中）。

`params` is also applied to streaming runs (embedded agent + compaction). 当前支持的键：`temperature`、`maxTokens`。 These merge with call-time options; caller-supplied values win. `temperature` 是高级调节项——除非你了解模型的默认值且确实需要更改，否则不要设置。

Example:

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-sonnet-4-5-20250929": {
          params: { temperature: 0.6 },
        },
        "openai/gpt-5.2": {
          params: { maxTokens: 8192 },
        },
      },
    },
  },
}
```

Z.AI GLM-4.x 模型会自动启用思考模式，除非你：

- 设置 `--thinking off`，或
- 自行定义 `agents.defaults.models["zai/<model>"].params.thinking`。

OpenClaw 还内置了一些别名简写。 Defaults only apply when the model
is already present in `agents.defaults.models`:

- `opus` -> `anthropic/claude-opus-4-6`
- `sonnet` -> `anthropic/claude-sonnet-4-5`
- `gpt` -> `openai/gpt-5.2`
- `gpt-mini` -> `openai/gpt-5-mini`
- `gemini` -> `google/gemini-3-pro-preview`
- `gemini-flash` -> `google/gemini-3-flash-preview`

如果你自己配置了同名别名（不区分大小写），以你的值为准（默认值永不覆盖）。

示例：以 Opus 4.6 为主模型，MiniMax M2.1 为回退（托管的 MiniMax）：

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "opus" },
        "minimax/MiniMax-M2.1": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["minimax/MiniMax-M2.1"],
      },
    },
  },
}
```

MiniMax 认证：设置 `MINIMAX_API_KEY`（环境变量）或配置 `models.providers.minimax`。

#### `agents.defaults.cliBackends`（CLI 回退）

用于纯文本回退运行的可选 CLI 后端（不进行工具调用）。 当 API 提供商失败时，它们可作为备用路径。 Image pass-through is supported when you configure
an `imageArg` that accepts file paths.

Notes:

- CLI 后端是**以文本为先**；工具始终被禁用。
- 当设置了 `sessionArg` 时支持会话；会话 ID 会按后端持久化。
- 对于 `claude-cli`，已内置默认配置。 如果 PATH 很精简（launchd/systemd），请覆盖命令路径。

示例：

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
        "my-cli": {
          command: "my-cli",
          args: ["--json"],
          output: "json",
          modelArg: "--model",
          sessionArg: "--session",
          sessionMode: "existing",
          systemPromptArg: "--system",
          systemPromptWhen: "first",
          imageArg: "--image",
          imageMode: "repeat",
        },
      },
    },
  },
}
```

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "Opus" },
        "anthropic/claude-sonnet-4-1": { alias: "Sonnet" },
        "openrouter/deepseek/deepseek-r1:free": {},
        "zai/glm-4.7": {
          alias: "GLM",
          params: {
            thinking: {
              type: "enabled",
              clear_thinking: false,
            },
          },
        },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: [
          "openrouter/deepseek/deepseek-r1:free",
          "openrouter/meta-llama/llama-3.3-70b-instruct:free",
        ],
      },
      imageModel: {
        primary: "openrouter/qwen/qwen-2.5-vl-72b-instruct:free",
        fallbacks: ["openrouter/google/gemini-2.0-flash-vision:free"],
      },
      thinkingDefault: "low",
      verboseDefault: "off",
      elevatedDefault: "on",
      timeoutSeconds: 600,
      mediaMaxMb: 5,
      heartbeat: {
        every: "30m",
        target: "last",
      },
      maxConcurrent: 3,
      subagents: {
        model: "minimax/MiniMax-M2.1",
        maxConcurrent: 1,
        archiveAfterMinutes: 60,
      },
      exec: {
        backgroundMs: 10000,
        timeoutSec: 1800,
        cleanupMs: 1800000,
      },
      contextTokens: 200000,
    },
  },
}
```

#### `agents.defaults.contextPruning`（工具结果裁剪）

`agents.defaults.contextPruning` 会在向 LLM 发送请求之前，从内存上下文中裁剪**较旧的工具结果**。
它**不会**修改磁盘上的会话历史（`*.jsonl` 仍保持完整）。

其目的在于减少随着时间推移累积大量工具输出的“健谈型” agent 的 token 使用量。

总体原则：

- 绝不触及用户/助手消息。
- 保护最近的 `keepLastAssistants` 条助手消息（该点之后的工具结果不被裁剪）。
- 保护引导前缀（第一条用户消息之前的内容不会被裁剪）。
- 模式：
  - `adaptive`：当估算的上下文占比超过 `softTrimRatio` 时，对超大的工具结果进行软裁剪（保留头/尾）。
    随后，当估算的上下文占比超过 `hardClearRatio` **且** 存在足够可裁剪的工具结果体量（`minPrunableToolChars`）时，硬清除最旧的、符合条件的工具结果。
  - `aggressive`: always replaces eligible tool results before the cutoff with the `hardClear.placeholder` (no ratio checks).

Soft vs hard pruning (what changes in the context sent to the LLM):

- **Soft-trim**: only for _oversized_ tool results. Keeps the beginning + end and inserts `...` in the middle.
  - Before: `toolResult("…very long output…")`
  - After: `toolResult("HEAD…\n...\n…TAIL\n\n[Tool result trimmed: …]")`
- **Hard-clear**: replaces the entire tool result with the placeholder.
  - Before: `toolResult("…very long output…")`
  - After: `toolResult("[Old tool result content cleared]")`

Notes / current limitations:

- Tool results containing **image blocks are skipped** (never trimmed/cleared) right now.
- The estimated “context ratio” is based on **characters** (approximate), not exact tokens.
- If the session doesn’t contain at least `keepLastAssistants` assistant messages yet, pruning is skipped.
- In `aggressive` mode, `hardClear.enabled` is ignored (eligible tool results are always replaced with `hardClear.placeholder`).

Default (adaptive):

```json5
{
  agents: { defaults: { contextPruning: { mode: "adaptive" } } },
}
```

To disable:

```json5
{
  agents: { defaults: { contextPruning: { mode: "off" } } },
}
```

Defaults (when `mode` is `"adaptive"` or `"aggressive"`):

- `keepLastAssistants`: `3`
- `softTrimRatio`: `0.3` (adaptive only)
- `hardClearRatio`: `0.5` (adaptive only)
- `minPrunableToolChars`: `50000` (adaptive only)
- `softTrim`: `{ maxChars: 4000, headChars: 1500, tailChars: 1500 }` (adaptive only)
- `hardClear`: `{ enabled: true, placeholder: "[Old tool result content cleared]" }`

Example (aggressive, minimal):

```json5
{
  agents: { defaults: { contextPruning: { mode: "aggressive" } } },
}
```

Example (adaptive tuned):

```json5
{
  agents: {
    defaults: {
      contextPruning: {
        mode: "adaptive",
        keepLastAssistants: 3,
        softTrimRatio: 0.3,
        hardClearRatio: 0.5,
        minPrunableToolChars: 50000,
        softTrim: { maxChars: 4000, headChars: 1500, tailChars: 1500 },
        hardClear: { enabled: true, placeholder: "[Old tool result content cleared]" },
        // Optional: restrict pruning to specific tools (deny wins; supports "*" wildcards)
        tools: { deny: ["browser", "canvas"] },
      },
    },
  },
}
```

See [/concepts/session-pruning](/concepts/session-pruning) for behavior details.

#### `agents.defaults.compaction` (reserve headroom + memory flush)

`agents.defaults.compaction.mode` selects the compaction summarization strategy. Defaults to `default`; set `safeguard` to enable chunked summarization for very long histories. See [/concepts/compaction](/concepts/compaction).

`agents.defaults.compaction.reserveTokensFloor` enforces a minimum `reserveTokens`
value for Pi compaction (default: `20000`). Set it to `0` to disable the floor.

`agents.defaults.compaction.memoryFlush` runs a **silent** agentic turn before
auto-compaction, instructing the model to store durable memories on disk (e.g.
`memory/YYYY-MM-DD.md`). It triggers when the session token estimate crosses a
soft threshold below the compaction limit.

Legacy defaults:

- `memoryFlush.enabled`: `true`
- `memoryFlush.softThresholdTokens`: `4000`
- `memoryFlush.prompt` / `memoryFlush.systemPrompt`: built-in defaults with `NO_REPLY`
- Note: memory flush is skipped when the session workspace is read-only
  (`agents.defaults.sandbox.workspaceAccess: "ro"` or `"none"`).

Example (tuned):

```json5
{
  agents: {
    defaults: {
      compaction: {
        mode: "safeguard",
        reserveTokensFloor: 24000,
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 6000,
          systemPrompt: "Session nearing compaction. Store durable memories now.",
          prompt: "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store.",
        },
      },
    },
  },
}
```

Block streaming:

- `agents.defaults.blockStreamingDefault`: `"on"`/`"off"` (default off).

- Channel overrides: `*.blockStreaming` (and per-account variants) to force block streaming on/off.
  Non-Telegram channels require an explicit `*.blockStreaming: true` to enable block replies.

- `agents.defaults.blockStreamingBreak`: `"text_end"` or `"message_end"` (default: text_end).

- `agents.defaults.blockStreamingChunk`：对流式块进行软分块。 默认值为
  800–1200 个字符，优先段落分隔（`\n\n`），其次是换行，再其次是句子。
  示例：

  ```json5
  {
    agents: { defaults: { blockStreamingChunk: { minChars: 800, maxChars: 1200 } } },
  }
  ```

- `agents.defaults.blockStreamingCoalesce`：在发送前合并流式块。
  默认值为 `{ idleMs: 1000 }`，并从 `blockStreamingChunk` 继承 `minChars`，
  同时将 `maxChars` 限制为通道文本上限。 Signal/Slack/Discord/Google Chat 默认
  使用 `minChars: 1500`，除非被覆盖。
  通道覆盖项：`channels.whatsapp.blockStreamingCoalesce`、`channels.telegram.blockStreamingCoalesce`，
  `channels.discord.blockStreamingCoalesce`、`channels.slack.blockStreamingCoalesce`、`channels.mattermost.blockStreamingCoalesce`，
  `channels.signal.blockStreamingCoalesce`、`channels.imessage.blockStreamingCoalesce`、`channels.msteams.blockStreamingCoalesce`，
  `channels.googlechat.blockStreamingCoalesce`
  （以及按账户的变体）。

- `agents.defaults.humanDelay`：首条之后 **块级回复** 之间的随机暂停。
  模式：`off`（默认）、`natural`（800–2500ms）、`custom`（使用 `minMs`/`maxMs`）。
  按代理覆盖：`agents.list[].humanDelay`。
  示例：

  ```json5
  {
    agents: { defaults: { humanDelay: { mode: "natural" } } },
  }
  ```

  有关行为与分块细节，请参见 [/concepts/streaming](/concepts/streaming)。

输入中指示器：

- `agents.defaults.typingMode`：`"never" | "instant" | "thinking" | "message"`。 默认情况下，
  直接聊天/提及使用 `instant`，未被提及的群聊使用 `message`。
- `session.typingMode`：按会话覆盖模式。
- `agents.defaults.typingIntervalSeconds`：刷新输入中信号的频率（默认：6s）。
- `session.typingIntervalSeconds`：按会话覆盖刷新间隔。
  有关行为细节，请参见 [/concepts/typing-indicators](/concepts/typing-indicators)。

`agents.defaults.model.primary` 应设置为 `provider/model`（例如 `anthropic/claude-opus-4-6`）。
别名来自 `agents.defaults.models.*.alias`（例如 `Opus`）。
如果省略提供商，OpenClaw 目前会假定为 `anthropic`，作为临时的弃用回退。
Z.AI 模型可用作 `zai/<model>`（例如 `zai/glm-4.7`），并且需要在环境中设置
`ZAI_API_KEY`（或旧版 `Z_AI_API_KEY`）。

`agents.defaults.heartbeat` 配置周期性的心跳运行：

- `every`：时长字符串（`ms`、`s`、`m`、`h`）；默认单位为分钟。 默认值：
  `30m`。 设置为 `0m` 以禁用。
- `model`: optional override model for heartbeat runs (`provider/model`).
- `includeReasoning`：当为 `true` 时，心跳在可用时也会发送单独的 `Reasoning:` 消息（形态与 `/reasoning on` 相同）。 默认值：`false`。
- `session`：可选的会话键，用于控制心跳在哪个会话中运行。 默认值：`main`。
- `to`：可选的接收者覆盖（通道特定 ID，例如 WhatsApp 的 E.164、Telegram 的 chat id）。
- `target`：可选的投递通道（`last`、`whatsapp`、`telegram`、`discord`、`slack`、`msteams`、`signal`、`imessage`、`none`）。 默认值：`last`。
- `prompt`：心跳正文的可选覆盖（默认：`Read HEARTBEAT.md if it exists (workspace context). 39. Follow it strictly. 40. Do not infer or repeat old tasks from prior chats. 41. If nothing needs attention, reply HEARTBEAT_OK.`）。 覆盖项将按原样发送；如果仍希望读取该文件，请包含一行 `Read HEARTBEAT.md`。 `ackMaxChars`：在 `HEARTBEAT_OK` 之后允许投递的最大字符数（默认：300）。 按代理心跳： 设置 `agents.list[].heartbeat` 以启用或覆盖特定代理的心跳设置。
- 如果任何代理条目定义了 `heartbeat`，**仅这些代理** 会运行心跳；默认值
  将成为这些代理共享的基线。

心跳会运行完整的代理回合。

- 更短的间隔会消耗更多令牌；请注意
  `every`，保持 `HEARTBEAT.md` 足够小，和/或选择更便宜的 `model`。
- `tools.exec` 配置后台执行默认值：

`backgroundMs`：自动转入后台前的时间（毫秒，默认 10000） Shorter intervals burn more tokens; be mindful
of `every`, keep `HEARTBEAT.md` tiny, and/or choose a cheaper `model`.

`tools.exec` configures background exec defaults:

- `backgroundMs`: time before auto-background (ms, default 10000)
- `timeoutSec`：在此运行时长后自动终止（秒，默认 1800）
- `cleanupMs`: how long to keep finished sessions in memory (ms, default 1800000)
- `notifyOnExit`：当后台执行退出时，将系统事件加入队列并请求心跳（默认 true）
- `applyPatch.enabled`：启用实验性的 `apply_patch`（仅 OpenAI/OpenAI Codex；默认 false）
- `applyPatch.allowModels`：可选的模型 ID 白名单（例如 `gpt-5.2` 或 `openai/gpt-5.2`）
  注意：`applyPatch` 仅位于 `tools.exec` 下。

`tools.web` 配置 Web 搜索与抓取工具：

- `tools.web.search.enabled`（默认：当存在密钥时为 true）
- `tools.web.search.apiKey`（推荐：通过 `openclaw configure --section web` 设置，或使用 `BRAVE_API_KEY` 环境变量）
- `tools.web.search.maxResults`（1–10，默认 5）
- `tools.web.search.timeoutSeconds`（默认 30）
- `tools.web.search.cacheTtlMinutes`（默认 15）
- `tools.web.fetch.enabled`（默认 true）
- `tools.web.fetch.maxChars`（默认 50000）
- `tools.web.fetch.maxCharsCap`（默认 50000；用于限制来自配置/工具调用的 maxChars）
- `tools.web.fetch.timeoutSeconds`（默认 30）
- `tools.web.fetch.cacheTtlMinutes`（默认 15）
- `tools.web.fetch.userAgent`（可选覆盖）
- `tools.web.fetch.readability`（默认 true；禁用则仅使用基础 HTML 清理）
- `tools.web.fetch.firecrawl.enabled`（当设置了 API key 时默认 true）
- `tools.web.fetch.firecrawl.apiKey`（可选；默认为 `FIRECRAWL_API_KEY`）
- `tools.web.fetch.firecrawl.baseUrl`（默认 [https://api.firecrawl.dev](https://api.firecrawl.dev)）
- `tools.web.fetch.firecrawl.onlyMainContent`（默认 true）
- `tools.web.fetch.firecrawl.maxAgeMs`（可选）
- `tools.web.fetch.firecrawl.timeoutSeconds` (optional)

`tools.media` 配置入站媒体理解（图像/音频/视频）：

- `tools.media.models`：共享模型列表（按能力打标签；在每个能力列表之后使用）。
- `tools.media.concurrency`：最大并发能力运行数（默认 2）。
- `tools.media.image` / `tools.media.audio` / `tools.media.video`：
  - `enabled`：选择性关闭开关（当配置了模型时默认 true）。
  - `prompt`：可选的提示覆盖（图像/视频会自动附加 `maxChars` 提示）。
  - `maxChars`：最大输出字符数（图像/视频默认 500；音频未设置）。
  - `maxBytes`：发送的最大媒体大小（默认：图像 10MB，音频 20MB，视频 50MB）。
  - `timeoutSeconds`：请求超时（默认：图像 60 秒，音频 60 秒，视频 120 秒）。
  - `language`：可选的音频提示。
  - `attachments`: attachment policy (`mode`, `maxAttachments`, `prefer`).
  - `scope`：可选的门控（首次匹配生效），使用 `match.channel`、`match.chatType` 或 `match.keyPrefix`。
  - `models`：模型条目的有序列表；失败或媒体过大时回退到下一个条目。
- 每个 `models[]` 条目：
  - 提供方条目（`type: "provider"` 或省略）：
    - `provider`：API 提供方 ID（`openai`、`anthropic`、`google`/`gemini`、`groq` 等）。
    - `model`：模型 ID 覆盖（图像必填；音频提供方默认 `gpt-4o-mini-transcribe`/`whisper-large-v3-turbo`，视频默认 `gemini-3-flash-preview`）。
    - `profile` / `preferredProfile`：鉴权配置选择。
  - CLI 条目（`type: "cli"`）：
    - `command`：要运行的可执行文件。
    - `args`：模板化参数（支持 `{{MediaPath}}`、`{{Prompt}}`、`{{MaxChars}}` 等）。
  - `capabilities`：可选列表（`image`、`audio`、`video`），用于限制共享条目。 省略时的默认值：`openai`/`anthropic`/`minimax` → 图像，`google` → 图像+音频+视频，`groq` → 音频。
  - `prompt`、`maxChars`、`maxBytes`、`timeoutSeconds`、`language` 可在每个条目中覆盖。

如果未配置模型（或 `enabled: false`），将跳过理解；模型仍会接收原始附件。

提供方鉴权遵循标准模型鉴权顺序（鉴权配置、如 `OPENAI_API_KEY`/`GROQ_API_KEY`/`GEMINI_API_KEY` 等环境变量，或 `models.providers.*.apiKey`）。

Example:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        maxBytes: 20971520,
        scope: {
          default: "deny",
          rules: [{ action: "allow", match: { chatType: "direct" } }],
        },
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          { type: "cli", command: "whisper", args: ["--model", "base", "{{MediaPath}}"] },
        ],
      },
      video: {
        enabled: true,
        maxBytes: 52428800,
        models: [{ provider: "google", model: "gemini-3-flash-preview" }],
      },
    },
  },
}
```

`agents.defaults.subagents` configures sub-agent defaults:

- `model`: default model for spawned sub-agents (string or `{ primary, fallbacks }`). If omitted, sub-agents inherit the caller’s model unless overridden per agent or per call.
- `maxConcurrent`: max concurrent sub-agent runs (default 1)
- `archiveAfterMinutes`: auto-archive sub-agent sessions after N minutes (default 60; set `0` to disable)
- Per-subagent tool policy: `tools.subagents.tools.allow` / `tools.subagents.tools.deny` (deny wins)

`tools.profile` sets a **base tool allowlist** before `tools.allow`/`tools.deny`:

- `minimal`: `session_status` only
- `coding`: `group:fs`, `group:runtime`, `group:sessions`, `group:memory`, `image`
- `messaging`: `group:messaging`, `sessions_list`, `sessions_history`, `sessions_send`, `session_status`
- `full`: no restriction (same as unset)

Per-agent override: `agents.list[].tools.profile`.

Example (messaging-only by default, allow Slack + Discord tools too):

```json5
{
  tools: {
    profile: "messaging",
    allow: ["slack", "discord"],
  },
}
```

Example (coding profile, but deny exec/process everywhere):

```json5
{
  tools: {
    profile: "coding",
    deny: ["group:runtime"],
  },
}
```

`tools.byProvider` lets you **further restrict** tools for specific providers (or a single `provider/model`).
Per-agent override: `agents.list[].tools.byProvider`.

Order: base profile → provider profile → allow/deny policies.
Provider keys accept either `provider` (e.g. `google-antigravity`) or `provider/model`
(e.g. `openai/gpt-5.2`).

Example (keep global coding profile, but minimal tools for Google Antigravity):

```json5
{
  tools: {
    profile: "coding",
    byProvider: {
      "google-antigravity": { profile: "minimal" },
    },
  },
}
```

Example (provider/model-specific allowlist):

```json5
{
  tools: {
    allow: ["group:fs", "group:runtime", "sessions_list"],
    byProvider: {
      "openai/gpt-5.2": { allow: ["group:fs", "sessions_list"] },
    },
  },
}
```

`tools.allow` / `tools.deny` configure a global tool allow/deny policy (deny wins).
Matching is case-insensitive and supports `*` wildcards (`"*"` means all tools).
This is applied even when the Docker sandbox is **off**.

Example (disable browser/canvas everywhere):

```json5
{
  tools: { deny: ["browser", "canvas"] },
}
```

Tool groups (shorthands) work in **global** and **per-agent** tool policies:

- `group:runtime`: `exec`, `bash`, `process`
- `group:fs`: `read`, `write`, `edit`, `apply_patch`
- `group:sessions`: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
- `group:memory`: `memory_search`, `memory_get`
- `group:web`: `web_search`, `web_fetch`
- `group:ui`: `browser`, `canvas`
- `group:automation`: `cron`, `gateway`
- `group:messaging`: `message`
- `group:nodes`: `nodes`
- `group:openclaw`: all built-in OpenClaw tools (excludes provider plugins)

`tools.elevated` controls elevated (host) exec access:

- `enabled`: allow elevated mode (default true)
- `allowFrom`: per-channel allowlists (empty = disabled)
  - `whatsapp`: E.164 numbers
  - `telegram`: chat ids or usernames
  - `discord`: user ids or usernames (falls back to `channels.discord.dm.allowFrom` if omitted)
  - `signal`: E.164 numbers
  - `imessage`: handles/chat ids
  - `webchat`: session ids or usernames

Example:

```json5
{
  tools: {
    elevated: {
      enabled: true,
      allowFrom: {
        whatsapp: ["+15555550123"],
        discord: ["steipete", "1234567890123"],
      },
    },
  },
}
```

按 agent 覆盖（进一步限制）：

```json5
{
  agents: {
    list: [
      {
        id: "family",
        tools: {
          elevated: { enabled: false },
        },
      },
    ],
  },
}
```

说明：

- `tools.elevated` 是全局基线。 `agents.list[].tools.elevated` 只能进一步限制（两者都必须允许）。
- `/elevated on|off|ask|full` 按会话键存储状态；行内指令仅适用于单条消息。
- 提升权限的 `exec` 在宿主机上运行并绕过沙箱。
- 工具策略仍然适用；如果 `exec` 被拒绝，则无法使用提升权限。

`agents.defaults.maxConcurrent` 设置跨会话并行执行的嵌入式 agent 运行的最大数量。 每个会话仍然是串行的（每个会话键一次只运行一个）。 默认值：1。

### `agents.defaults.sandbox`

为嵌入式 agent 提供可选的 **Docker 沙箱**。 旨在用于非主会话，使其无法访问你的宿主系统。

详情：[Sandboxing](/gateway/sandboxing)

默认值（如果启用）：

- scope：`"agent"`（每个 agent 一个容器 + 工作区）
- 基于 Debian bookworm-slim 的镜像
- agent 工作区访问：`workspaceAccess: "none"`（默认）
  - `"none"`：在 `~/.openclaw/sandboxes` 下使用按 scope 划分的沙箱工作区
- `"ro"`：将沙箱工作区保持在 `/workspace`，并将 agent 工作区以只读方式挂载到 `/agent`（禁用 `write`/`edit`/`apply_patch`）
  - `"rw"`：将 agent 工作区以读写方式挂载到 `/workspace`
- 自动清理：空闲 > 24 小时 或 存在时间 > 7 天
- 工具策略：仅允许 `exec`、`process`、`read`、`write`、`edit`、`apply_patch`、`sessions_list`、`sessions_history`、`sessions_send`、`sessions_spawn`、`session_status`（拒绝优先生效）
  - 通过 `tools.sandbox.tools` 配置；可通过 `agents.list[].tools.sandbox.tools` 按 agent 覆盖
  - 沙箱策略中支持的工具组简写：`group:runtime`、`group:fs`、`group:sessions`、`group:memory`（参见 [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated#tool-groups-shorthands)）
- 可选的沙箱化浏览器（Chromium + CDP，noVNC 观察器）
- 加固参数：`network`、`user`、`pidsLimit`、`memory`、`cpus`、`ulimits`、`seccompProfile`、`apparmorProfile`

警告：`scope: "shared"` 表示共享容器和共享工作区。 没有跨会话隔离。 使用 `scope: "session"` 进行按会话隔离。

兼容旧版：仍支持 `perSession`（`true` → `scope: "session"`，`false` → `scope: "shared"`）。

`setupCommand` 在容器创建后 **仅运行一次**（在容器内通过 `sh -lc` 执行）。
进行软件包安装时，请确保网络出站可用、根文件系统可写，并且使用 root 用户。

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // off | non-main | all
        scope: "agent", // session | agent | shared (agent is default)
        workspaceAccess: "none", // none | ro | rw
        workspaceRoot: "~/.openclaw/sandboxes",
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          containerPrefix: "openclaw-sbx-",
          workdir: "/workspace",
          readOnlyRoot: true,
          tmpfs: ["/tmp", "/var/tmp", "/run"],
          network: "none",
          user: "1000:1000",
          capDrop: ["ALL"],
          env: { LANG: "C.UTF-8" },
          setupCommand: "apt-get update && apt-get install -y git curl jq",
          // Per-agent override (multi-agent): agents.list[].sandbox.docker.*
          pidsLimit: 256,
          memory: "1g",
          memorySwap: "2g",
          cpus: 1,
          ulimits: {
            nofile: { soft: 1024, hard: 2048 },
            nproc: 256,
          },
          seccompProfile: "/path/to/seccomp.json",
          apparmorProfile: "openclaw-sandbox",
          dns: ["1.1.1.1", "8.8.8.8"],
          extraHosts: ["internal.service:10.0.0.5"],
          binds: ["/var/run/docker.sock:/var/run/docker.sock", "/home/user/source:/source:rw"],
        },
        browser: {
          enabled: false,
          image: "openclaw-sandbox-browser:bookworm-slim",
          containerPrefix: "openclaw-sbx-browser-",
          cdpPort: 9222,
          vncPort: 5900,
          noVncPort: 6080,
          headless: false,
          enableNoVnc: true,
          allowHostControl: false,
          allowedControlUrls: ["http://10.0.0.42:18791"],
          allowedControlHosts: ["browser.lab.local", "10.0.0.42"],
          allowedControlPorts: [18791],
          autoStart: true,
          autoStartTimeoutMs: 12000,
        },
        prune: {
          idleHours: 24, // 0 disables idle pruning
          maxAgeDays: 7, // 0 disables max-age pruning
        },
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        allow: [
          "exec",
          "process",
          "read",
          "write",
          "edit",
          "apply_patch",
          "sessions_list",
          "sessions_history",
          "sessions_send",
          "sessions_spawn",
          "session_status",
        ],
        deny: ["browser", "canvas", "nodes", "cron", "discord", "gateway"],
      },
    },
  },
}
```

使用以下命令构建默认沙箱镜像一次：

```bash
scripts/sandbox-setup.sh
```

注意：沙箱容器默认使用 `network: "none"`；如果 agent 需要出站访问，请将 `agents.defaults.sandbox.docker.network` 设置为 `"bridge"`（或你的自定义网络）。

注意：入站附件会被暂存到活动工作区的 `media/inbound/*`。 在 `workspaceAccess: "rw"` 时，这意味着文件会写入 agent 工作区。

注意：`docker.binds` 会挂载额外的宿主目录；全局和按 agent 的 binds 会合并。

使用以下命令构建可选的浏览器镜像：

```bash
scripts/sandbox-browser-setup.sh
```

当 `agents.defaults.sandbox.browser.enabled=true` 时，浏览器工具会使用沙箱化的 Chromium 实例（CDP）。 如果启用了 noVNC（当 headless=false 时为默认），noVNC URL 会被注入到系统提示中，供 agent 引用。
这不需要在主配置中设置 `browser.enabled`；沙箱控制 URL 会按会话注入。

`agents.defaults.sandbox.browser.allowHostControl`（默认：false）允许沙箱化会话通过浏览器工具（`target: "host"`）显式指向 **宿主** 浏览器控制服务器。 Leave this off if you want strict
sandbox isolation.

Allowlists for remote control:

- `allowedControlUrls`: exact control URLs permitted for `target: "custom"`.
- `allowedControlHosts`: hostnames permitted (hostname only, no port).
- `allowedControlPorts`: ports permitted (defaults: http=80, https=443).
  Defaults: all allowlists are unset (no restriction). `allowHostControl` defaults to false.

### `models` (custom providers + base URLs)

OpenClaw uses the **pi-coding-agent** model catalog. You can add custom providers
(LiteLLM, local OpenAI-compatible servers, Anthropic proxies, etc.) by writing
`~/.openclaw/agents/<agentId>/agent/models.json` or by defining the same schema inside your
OpenClaw config under `models.providers`.
Provider-by-provider overview + examples: [/concepts/model-providers](/concepts/model-providers).

When `models.providers` is present, OpenClaw writes/merges a `models.json` into
`~/.openclaw/agents/<agentId>/agent/` on startup:

- default behavior: **merge** (keeps existing providers, overrides on name)
- set `models.mode: "replace"` to overwrite the file contents

Select the model via `agents.defaults.model.primary` (provider/model).

```json5
{
  agents: {
    defaults: {
      model: { primary: "custom-proxy/llama-3.1-8b" },
      models: {
        "custom-proxy/llama-3.1-8b": {},
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      "custom-proxy": {
        baseUrl: "http://localhost:4000/v1",
        apiKey: "LITELLM_KEY",
        api: "openai-completions",
        models: [
          {
            id: "llama-3.1-8b",
            name: "Llama 3.1 8B",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            maxTokens: 32000,
          },
        ],
      },
    },
  },
}
```

### OpenCode Zen (multi-model proxy)

OpenCode Zen is a multi-model gateway with per-model endpoints. OpenClaw uses
the built-in `opencode` provider from pi-ai; set `OPENCODE_API_KEY` (or
`OPENCODE_ZEN_API_KEY`) from [https://opencode.ai/auth](https://opencode.ai/auth).

Notes:

- Model refs use `opencode/<modelId>` (example: `opencode/claude-opus-4-6`).
- If you enable an allowlist via `agents.defaults.models`, add each model you plan to use.
- Shortcut: `openclaw onboard --auth-choice opencode-zen`.

```json5
{
  agents: {
    defaults: {
      model: { primary: "opencode/claude-opus-4-6" },
      models: { "opencode/claude-opus-4-6": { alias: "Opus" } },
    },
  },
}
```

### Z.AI (GLM-4.7) — provider alias support

Z.AI models are available via the built-in `zai` provider. Set `ZAI_API_KEY`
in your environment and reference the model by provider/model.

Shortcut: `openclaw onboard --auth-choice zai-api-key`.

```json5
{
  agents: {
    defaults: {
      model: { primary: "zai/glm-4.7" },
      models: { "zai/glm-4.7": {} },
    },
  },
}
```

Notes:

- `z.ai/*` and `z-ai/*` are accepted aliases and normalize to `zai/*`.
- If `ZAI_API_KEY` is missing, requests to `zai/*` will fail with an auth error at runtime.
- Example error: `No API key found for provider "zai".`
- Z.AI’s general API endpoint is `https://api.z.ai/api/paas/v4`. GLM coding
  requests use the dedicated Coding endpoint `https://api.z.ai/api/coding/paas/v4`.
  The built-in `zai` provider uses the Coding endpoint. If you need the general
  endpoint, define a custom provider in `models.providers` with the base URL
  override (see the custom providers section above).
- Use a fake placeholder in docs/configs; never commit real API keys.

### Moonshot AI (Kimi)

Use Moonshot's OpenAI-compatible endpoint:

```json5
{
  env: { MOONSHOT_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "moonshot/kimi-k2.5" },
      models: { "moonshot/kimi-k2.5": { alias: "Kimi K2.5" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "kimi-k2.5",
            name: "Kimi K2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Notes:

- Set `MOONSHOT_API_KEY` in the environment or use `openclaw onboard --auth-choice moonshot-api-key`.
- Model ref: `moonshot/kimi-k2.5`.
- For the China endpoint, either:
  - Run `openclaw onboard --auth-choice moonshot-api-key-cn` (wizard will set `https://api.moonshot.cn/v1`), or
  - Manually set `baseUrl: "https://api.moonshot.cn/v1"` in `models.providers.moonshot`.

### Kimi Coding

Use Moonshot AI's Kimi Coding endpoint (Anthropic-compatible, built-in provider):

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "kimi-coding/k2p5" },
      models: { "kimi-coding/k2p5": { alias: "Kimi K2.5" } },
    },
  },
}
```

Notes:

- Set `KIMI_API_KEY` in the environment or use `openclaw onboard --auth-choice kimi-code-api-key`.
- Model ref: `kimi-coding/k2p5`.

### Synthetic (Anthropic-compatible)

Use Synthetic's Anthropic-compatible endpoint:

```json5
{
  env: { SYNTHETIC_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.1" },
      models: { "synthetic/hf:MiniMaxAI/MiniMax-M2.1": { alias: "MiniMax M2.1" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "hf:MiniMaxAI/MiniMax-M2.1",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 192000,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

Notes:

- Set `SYNTHETIC_API_KEY` or use `openclaw onboard --auth-choice synthetic-api-key`.
- Model ref: `synthetic/hf:MiniMaxAI/MiniMax-M2.1`.
- Base URL should omit `/v1` because the Anthropic client appends it.

### Local models (LM Studio) — recommended setup

See [/gateway/local-models](/gateway/local-models) for the current local guidance. TL;DR: run MiniMax M2.1 via LM Studio Responses API on serious hardware; keep hosted models merged for fallback.

### MiniMax M2.1

Use MiniMax M2.1 directly without LM Studio:

```json5
{
  agent: {
    model: { primary: "minimax/MiniMax-M2.1" },
    models: {
      "anthropic/claude-opus-4-6": { alias: "Opus" },
      "minimax/MiniMax-M2.1": { alias: "Minimax" },
    },
  },
  models: {
    mode: "merge",
    providers: {
      minimax: {
        baseUrl: "https://api.minimax.io/anthropic",
        apiKey: "${MINIMAX_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "MiniMax-M2.1",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            // Pricing: update in models.json if you need exact cost tracking.
            cost: { input: 15, output: 60, cacheRead: 2, cacheWrite: 10 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Notes:

- Set `MINIMAX_API_KEY` environment variable or use `openclaw onboard --auth-choice minimax-api`.
- Available model: `MiniMax-M2.1` (default).
- Update pricing in `models.json` if you need exact cost tracking.

### Cerebras (GLM 4.6 / 4.7)

Use Cerebras via their OpenAI-compatible endpoint:

```json5
{
  env: { CEREBRAS_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: {
        primary: "cerebras/zai-glm-4.7",
        fallbacks: ["cerebras/zai-glm-4.6"],
      },
      models: {
        "cerebras/zai-glm-4.7": { alias: "GLM 4.7 (Cerebras)" },
        "cerebras/zai-glm-4.6": { alias: "GLM 4.6 (Cerebras)" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      cerebras: {
        baseUrl: "https://api.cerebras.ai/v1",
        apiKey: "${CEREBRAS_API_KEY}",
        api: "openai-completions",
        models: [
          { id: "zai-glm-4.7", name: "GLM 4.7 (Cerebras)" },
          { id: "zai-glm-4.6", name: "GLM 4.6 (Cerebras)" },
        ],
      },
    },
  },
}
```

Notes:

- Use `cerebras/zai-glm-4.7` for Cerebras; use `zai/glm-4.7` for Z.AI direct.
- Set `CEREBRAS_API_KEY` in the environment or config.

Notes:

- Supported APIs: `openai-completions`, `openai-responses`, `anthropic-messages`,
  `google-generative-ai`
- Use `authHeader: true` + `headers` for custom auth needs.
- Override the agent config root with `OPENCLAW_AGENT_DIR` (or `PI_CODING_AGENT_DIR`)
  if you want `models.json` stored elsewhere (default: `~/.openclaw/agents/main/agent`).

### `session`

Controls session scoping, reset policy, reset triggers, and where the session store is written.

```json5
{
  session: {
    scope: "per-sender",
    dmScope: "main",
    identityLinks: {
      alice: ["telegram:123456789", "discord:987654321012345678"],
    },
    reset: {
      mode: "daily",
      atHour: 4,
      idleMinutes: 60,
    },
    resetByType: {
      thread: { mode: "daily", atHour: 4 },
      direct: { mode: "idle", idleMinutes: 240 },
      group: { mode: "idle", idleMinutes: 120 },
    },
    resetTriggers: ["/new", "/reset"],
    // Default is already per-agent under ~/.openclaw/agents/<agentId>/sessions/sessions.json
    // You can override with {agentId} templating:
    store: "~/.openclaw/agents/{agentId}/sessions/sessions.json",
    // Direct chats collapse to agent:<agentId>:<mainKey> (default: "main").
    mainKey: "main",
    agentToAgent: {
      // Max ping-pong reply turns between requester/target (0–5).
      maxPingPongTurns: 5,
    },
    sendPolicy: {
      rules: [{ action: "deny", match: { channel: "discord", chatType: "group" } }],
      default: "allow",
    },
  },
}
```

Fields:

- `mainKey`: direct-chat bucket key (default: `"main"`). Useful when you want to “rename” the primary DM thread without changing `agentId`.
  - Sandbox note: `agents.defaults.sandbox.mode: "non-main"` uses this key to detect the main session. Any session key that does not match `mainKey` (groups/channels) is sandboxed.
- `dmScope`: how DM sessions are grouped (default: `"main"`).
  - `main`: all DMs share the main session for continuity.
  - `per-peer`: isolate DMs by sender id across channels.
  - `per-channel-peer`: isolate DMs per channel + sender (recommended for multi-user inboxes).
  - `per-account-channel-peer`: isolate DMs per account + channel + sender (recommended for multi-account inboxes).
  - Secure DM mode (recommended): set `session.dmScope: "per-channel-peer"` when multiple people can DM the bot (shared inboxes, multi-person allowlists, or `dmPolicy: "open"`).
- `identityLinks`: map canonical ids to provider-prefixed peers so the same person shares a DM session across channels when using `per-peer`, `per-channel-peer`, or `per-account-channel-peer`.
  - Example: `alice: ["telegram:123456789", "discord:987654321012345678"]`.
- `reset`: primary reset policy. Defaults to daily resets at 4:00 AM local time on the gateway host.
  - `mode`: `daily` or `idle` (default: `daily` when `reset` is present).
  - `atHour`: local hour (0-23) for the daily reset boundary.
  - 1. `idleMinutes`：以分钟为单位的滑动空闲窗口。 2. 当同时配置了每日重置和空闲重置时，先到期的规则生效。
- `resetByType`: per-session overrides for `direct`, `group`, and `thread`. 遗留的 `dm` 键被接受作为 `direct` 的别名。
  - If you only set legacy `session.idleMinutes` without any `reset`/`resetByType`, OpenClaw stays in idle-only mode for backward compatibility.
- 4. `heartbeatIdleMinutes`：用于心跳检查的可选空闲覆盖（启用时仍然适用每日重置）。
- 5. `agentToAgent.maxPingPongTurns`：请求方/目标之间的最大往返回复次数（0–5，默认 5）。
- 6. `sendPolicy.default`：当没有规则匹配时的回退策略（`allow` 或 `deny`）。
- 7. `sendPolicy.rules[]`：可按 `channel`、`chatType`（`direct|group|room`）或 `keyPrefix`（例如 `cron:`）匹配。 8. 优先拒绝；否则允许。

### 9. `skills`（技能配置）

10. 控制内置白名单、安装偏好、额外技能文件夹以及按技能的覆盖配置。 11. 适用于**内置**技能和 `~/.openclaw/skills`（在名称冲突时，工作区技能仍然优先）。

12. 字段：

- 13. `allowBundled`：仅用于**内置**技能的可选白名单。 If set, only those
      bundled skills are eligible (managed/workspace skills unaffected).
- 15. `load.extraDirs`：要扫描的额外技能目录（最低优先级）。
- 16. `install.preferBrew`：在可用时优先使用 brew 安装器（默认：true）。
- 17. `install.nodeManager`：Node 安装器偏好（`npm` | `pnpm` | `yarn`，默认：npm）。
- 18. `entries.<skillKey>`19. \`：按技能的配置覆盖。

20. 单个技能字段：

- `enabled`: set `false` to disable a skill even if it’s bundled/installed.
- 22. `env`：为代理运行注入的环境变量（仅在尚未设置时）。
- 23. `apiKey`：为声明了主环境变量的技能提供的可选便捷项（例如 `nano-banana-pro` → `GEMINI_API_KEY`）。

24. 示例：

```json5
25. {
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills", "~/Projects/oss/some-skill-pack/skills"],
    },
    install: {
      preferBrew: true,
      nodeManager: "npm",
    },
    entries: {
      "nano-banana-pro": {
        apiKey: "GEMINI_KEY_HERE",
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

### 26. `plugins`（扩展）

27. 控制插件发现、允许/拒绝以及按插件的配置。 28. 插件从 `~/.openclaw/extensions`、`<workspace>/.openclaw/extensions` 以及任何 `plugins.load.paths` 条目中加载。 29. **配置更改需要重启网关。**
    参见 [/plugin](/tools/plugin) 了解完整用法。

30. 字段：

- `enabled`: master toggle for plugin loading (default: true).
- `allow`: optional allowlist of plugin ids; when set, only listed plugins load.
- 33. `deny`：插件 ID 的可选黑名单（拒绝优先）。
- `load.paths`: extra plugin files or directories to load (absolute or `~`).
- 35. \`entries.<pluginId>\`\`: per-plugin overrides.
  - 37. `enabled`：设置为 `false` 可禁用。
  - 38. `config`：插件特定的配置对象（如提供，将由插件进行校验）。

39. 示例：

```json5
40. {
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    load: {
      paths: ["~/Projects/oss/voice-call-extension"],
    },
    entries: {
      "voice-call": {
        enabled: true,
        config: {
          provider: "twilio",
        },
      },
    },
  },
}
```

### 41. `browser`（由 openclaw 管理的浏览器）

42. OpenClaw 可以为 openclaw 启动一个**专用、隔离**的 Chrome/Brave/Edge/Chromium 实例，并暴露一个小型回环控制服务。
43. 配置文件可以通过 `profiles.<name>` 指向一个**远程**的基于 Chromium 的浏览器，44. `.cdpUrl`。 45. 远程配置文件仅支持附加（禁用启动/停止/重置）。

46. `browser.cdpUrl` 仍然保留，用于旧版单配置文件配置，以及作为仅设置了 `cdpPort` 的配置文件的基础 scheme/host。

47. 默认值：

- 48. enabled：`true`
- 49. evaluateEnabled：`true`（设置为 `false` 以禁用 `act:evaluate` 和 `wait --fn`）
- 50. 控制服务：仅回环（端口从 `gateway.port` 派生，默认 `18791`）
- CDP URL: `http://127.0.0.1:18792` (control service + 1, legacy single-profile)
- profile color: `#FF4500` (lobster-orange)
- Note: the control server is started by the running gateway (OpenClaw.app menubar, or `openclaw gateway`).
- Auto-detect order: default browser if Chromium-based; otherwise Chrome → Brave → Edge → Chromium → Chrome Canary.

```json5
{
  browser: {
    enabled: true,
    evaluateEnabled: true,
    // cdpUrl: "http://127.0.0.1:18792", // legacy single-profile override
    defaultProfile: "chrome",
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC" },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
    },
    color: "#FF4500",
    // Advanced:
    // headless: false,
    // noSandbox: false,
    // executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    // attachOnly: false, // set true when tunneling a remote CDP to localhost
  },
}
```

### `ui` (Appearance)

Optional accent color used by the native apps for UI chrome (e.g. Talk Mode bubble tint).

1. 如果未设置，客户端将回退为柔和的浅蓝色。

```json5
{
  ui: {
    seamColor: "#FF4500", // hex (RRGGBB or #RRGGBB)
    // Optional: Control UI assistant identity override.
    // If unset, the Control UI uses the active agent identity (config or IDENTITY.md).
    assistant: {
      name: "OpenClaw",
      avatar: "CB", // emoji, short text, or image URL/data URI
    },
  },
}
```

### `gateway` (Gateway server mode + bind)

Use `gateway.mode` to explicitly declare whether this machine should run the Gateway.

Defaults:

- mode: **unset** (treated as “do not auto-start”)
- bind: `loopback`
- port: `18789` (single port for WS + HTTP)

```json5
{
  gateway: {
    mode: "local", // or "remote"
    port: 18789, // WS + HTTP multiplex
    bind: "loopback",
    // controlUi: { enabled: true, basePath: "/openclaw" }
    // auth: { mode: "token", token: "your-token" } // token gates WS + Control UI access
    // tailscale: { mode: "off" | "serve" | "funnel" }
  },
}
```

Control UI base path:

- 2. `gateway.controlUi.basePath` 设置 Control UI 提供服务的 URL 前缀。
- 3. 示例：`"/ui"`、`"/openclaw"`、`"/apps/openclaw"`。
- Default: root (`/`) (unchanged).
- `gateway.controlUi.root` sets the filesystem root for Control UI assets (default: `dist/control-ui`).
- `gateway.controlUi.allowInsecureAuth` allows token-only auth for the Control UI when
  device identity is omitted (typically over HTTP). Default: `false`. Prefer HTTPS
  (Tailscale Serve) or `127.0.0.1`.
- 4. `gateway.controlUi.dangerouslyDisableDeviceAuth` 会为 Control UI 禁用设备身份检查（仅使用令牌/密码）。 5. 默认值：`false`。 Break-glass only.

Related docs:

- [Control UI](/web/control-ui)
- [Web overview](/web)
- [Tailscale](/gateway/tailscale)
- [Remote access](/gateway/remote)

Trusted proxies:

- `gateway.trustedProxies`: list of reverse proxy IPs that terminate TLS in front of the Gateway.
- When a connection comes from one of these IPs, OpenClaw uses `x-forwarded-for` (or `x-real-ip`) to determine the client IP for local pairing checks and HTTP auth/local checks.
- Only list proxies you fully control, and ensure they **overwrite** incoming `x-forwarded-for`.

Notes:

- `openclaw gateway` refuses to start unless `gateway.mode` is set to `local` (or you pass the override flag).
- `gateway.port` controls the single multiplexed port used for WebSocket + HTTP (control UI, hooks, A2UI).
- OpenAI Chat Completions endpoint: **disabled by default**; enable with `gateway.http.endpoints.chatCompletions.enabled: true`.
- Precedence: `--port` > `OPENCLAW_GATEWAY_PORT` > `gateway.port` > default `18789`.
- Gateway auth is required by default (token/password or Tailscale Serve identity). Non-loopback binds require a shared token/password.
- The onboarding wizard generates a gateway token by default (even on loopback).
- `gateway.remote.token` is **only** for remote CLI calls; it does not enable local gateway auth. `gateway.token` is ignored.

Auth and Tailscale:

- `gateway.auth.mode` sets the handshake requirements (`token` or `password`). When unset, token auth is assumed.
- `gateway.auth.token` stores the shared token for token auth (used by the CLI on the same machine).
- 1. 当设置了 `gateway.auth.mode` 时，只接受该认证方式（外加可选的 Tailscale 头）。
- 6. `gateway.auth.password` 可以在此处设置，或通过 `OPENCLAW_GATEWAY_PASSWORD` 设置（推荐）。
- 7. `gateway.auth.allowTailscale` 允许 Tailscale Serve 身份标头（`tailscale-user-login`）在请求到达回环地址并携带 `x-forwarded-for`、`x-forwarded-proto` 和 `x-forwarded-host` 时满足认证要求。 4. OpenClaw
     在接受之前，通过 `tailscale whois` 解析 `x-forwarded-for` 地址来验证身份。 5. 当为 `true` 时，Serve 请求不需要 token/密码；设置为 `false` 以要求显式凭据。 6. 当 `tailscale.mode = "serve"` 且认证模式不是 `password` 时，默认值为
     `true`。
- 7. `gateway.tailscale.mode: "serve"` 使用 Tailscale Serve（仅 tailnet，回环绑定）。
- 8. `gateway.tailscale.mode: "funnel"` 将仪表板公开暴露；需要认证。
- 9. `gateway.tailscale.resetOnExit` 在关闭时重置 Serve/Funnel 配置。

10. 远程客户端默认值（CLI）：

- 11. 当 `gateway.mode = "remote"` 时，`gateway.remote.url` 设置 CLI 调用的默认 Gateway WebSocket URL。
- 12. `gateway.remote.transport` 选择 macOS 远程传输方式（默认 `ssh`，`direct` 用于 ws/wss）。 13. 当使用 `direct` 时，`gateway.remote.url` 必须是 `ws://` 或 `wss://`。 14. `ws://host` 默认端口为 `18789`。
- 15. `gateway.remote.token` 为远程调用提供 token（留空表示不启用认证）。
- 16. `gateway.remote.password` 为远程调用提供密码（留空表示不启用认证）。

17. macOS 应用行为：

- 18. OpenClaw.app 监视 `~/.openclaw/openclaw.json`，当 `gateway.mode` 或 `gateway.remote.url` 发生变化时实时切换模式。
- 19. 如果未设置 `gateway.mode` 但设置了 `gateway.remote.url`，macOS 应用会将其视为远程模式。
- 20. 当你在 macOS 应用中更改连接模式时，它会将 `gateway.mode`（以及远程模式下的 `gateway.remote.url` + `gateway.remote.transport`）写回配置文件。

```json5
21. {
  gateway: {
    mode: "remote",
    remote: {
      url: "ws://gateway.tailnet:18789",
      token: "your-token",
      password: "your-password",
    },
  },
}
```

22. 直连传输示例（macOS 应用）：

```json5
23. {
  gateway: {
    mode: "remote",
    remote: {
      transport: "direct",
      url: "wss://gateway.example.ts.net",
      token: "your-token",
    },
  },
}
```

### 24. `gateway.reload`（配置热重载）

25. Gateway 会监视 `~/.openclaw/openclaw.json`（或 `OPENCLAW_CONFIG_PATH`），并自动应用更改。

8. 模式：

- 27. `hybrid`（默认）：热应用安全更改；关键更改需重启 Gateway。
- 9. `hot`：仅应用热安全更改；当需要重启时记录日志。
- 29. `restart`：在任何配置更改时重启 Gateway。
- 30. `off`：禁用热重载。

```json5
31. {
  gateway: {
    reload: {
      mode: "hybrid",
      debounceMs: 300,
    },
  },
}
```

#### 32. 热重载矩阵（文件 + 影响）

10. 监视的文件：

- 34. `~/.openclaw/openclaw.json`（或 `OPENCLAW_CONFIG_PATH`）

35. 热应用（无需完整 Gateway 重启）：

- 36. `hooks`（Webhook 认证/路径/映射）+ `hooks.gmail`（Gmail 监听器重启）
- 37. `browser`（浏览器控制服务器重启）
- 38. `cron`（cron 服务重启 + 并发更新）
- 39. `agents.defaults.heartbeat`（心跳运行器重启）
- 40. `web`（WhatsApp Web 通道重启）
- 41. `telegram`、`discord`、`signal`、`imessage`（通道重启）
- 11. `agent`、`models`、`routing`、`messages`、`session`、`whatsapp`、`logging`、`skills`、`ui`、`talk`、`identity`、`wizard`（动态读取）

12. 需要完整 Gateway 重启：

- 44. `gateway`（端口/绑定/认证/控制 UI/Tailscale）
- 45. `bridge`（遗留）
- 46. `discovery`
- 13. `canvasHost`
- 14. `plugins`
- 49. 任何未知/不支持的配置路径（为安全起见默认重启）

### 50. 多实例隔离

To run multiple gateways on one host (for redundancy or a rescue bot), isolate per-instance state + config and use unique ports:

- `OPENCLAW_CONFIG_PATH` (per-instance config)
- `OPENCLAW_STATE_DIR` (sessions/creds)
- `agents.defaults.workspace` (memories)
- `gateway.port` (unique per instance)

Convenience flags (CLI):

- `openclaw --dev …` → uses `~/.openclaw-dev` + shifts ports from base `19001`
- `openclaw --profile <name> …` → uses `~/.openclaw-<name>` (port via config/env/flags)

See [Gateway runbook](/gateway) for the derived port mapping (gateway/browser/canvas).
See [Multiple gateways](/gateway/multiple-gateways) for browser/CDP port isolation details.

Example:

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json \
OPENCLAW_STATE_DIR=~/.openclaw-a \
openclaw gateway --port 19001
```

### `hooks` (Gateway webhooks)

Enable a simple HTTP webhook endpoint on the Gateway HTTP server.

Defaults:

- enabled: `false`
- path: `/hooks`
- maxBodyBytes: `262144` (256 KB)

```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
    presets: ["gmail"],
    transformsDir: "~/.openclaw/hooks",
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        wakeMode: "now",
        name: "Gmail",
        sessionKey: "hook:gmail:{{messages[0].id}}",
        messageTemplate: "From: {{messages[0].from}}\nSubject: {{messages[0].subject}}\n{{messages[0].snippet}}",
        deliver: true,
        channel: "last",
        model: "openai/gpt-5.2-mini",
      },
    ],
  },
}
```

Requests must include the hook token:

- `Authorization: Bearer <token>` **or**
- `x-openclaw-token: <token>`

Endpoints:

- `POST /hooks/wake` → `{ text, mode?: "now"|"next-heartbeat" }`
- `POST /hooks/agent` → `{ message, name?, sessionKey?, wakeMode?, deliver?, channel?, to?, model?, thinking?, timeoutSeconds? }`
- `POST /hooks/<name>` → resolved via `hooks.mappings`

`/hooks/agent` always posts a summary into the main session (and can optionally trigger an immediate heartbeat via `wakeMode: "now"`).

Mapping notes:

- `match.path` matches the sub-path after `/hooks` (e.g. `/hooks/gmail` → `gmail`).
- `match.source` matches a payload field (e.g. `{ source: "gmail" }`) so you can use a generic `/hooks/ingest` path.
- Templates like `{{messages[0].subject}}` read from the payload.
- `transform` can point to a JS/TS module that returns a hook action.
- `deliver: true` sends the final reply to a channel; `channel` defaults to `last` (falls back to WhatsApp).
- If there is no prior delivery route, set `channel` + `to` explicitly (required for Telegram/Discord/Google Chat/Slack/Signal/iMessage/MS Teams).
- `model` overrides the LLM for this hook run (`provider/model` or alias; must be allowed if `agents.defaults.models` is set).

Gmail helper config (used by `openclaw webhooks gmail setup` / `run`):

```json5
{
  hooks: {
    gmail: {
      account: "openclaw@gmail.com",
      topic: "projects/<project-id>/topics/gog-gmail-watch",
      subscription: "gog-gmail-watch-push",
      pushToken: "shared-push-token",
      hookUrl: "http://127.0.0.1:18789/hooks/gmail",
      includeBody: true,
      maxBytes: 20000,
      renewEveryMinutes: 720,
      serve: { bind: "127.0.0.1", port: 8788, path: "/" },
      tailscale: { mode: "funnel", path: "/gmail-pubsub" },

      // Optional: use a cheaper model for Gmail hook processing
      // Falls back to agents.defaults.model.fallbacks, then primary, on auth/rate-limit/timeout
      model: "openrouter/meta-llama/llama-3.3-70b-instruct:free",
      // Optional: default thinking level for Gmail hooks
      thinking: "off",
    },
  },
}
```

Model override for Gmail hooks:

- `hooks.gmail.model` specifies a model to use for Gmail hook processing (defaults to session primary).
- Accepts `provider/model` refs or aliases from `agents.defaults.models`.
- Falls back to `agents.defaults.model.fallbacks`, then `agents.defaults.model.primary`, on auth/rate-limit/timeouts.
- If `agents.defaults.models` is set, include the hooks model in the allowlist.
- At startup, warns if the configured model is not in the model catalog or allowlist.
- `hooks.gmail.thinking` sets the default thinking level for Gmail hooks and is overridden by per-hook `thinking`.

Gateway auto-start:

- If `hooks.enabled=true` and `hooks.gmail.account` is set, the Gateway starts
  `gog gmail watch serve` on boot and auto-renews the watch.
- Set `OPENCLAW_SKIP_GMAIL_WATCHER=1` to disable the auto-start (for manual runs).
- Avoid running a separate `gog gmail watch serve` alongside the Gateway; it will
  fail with `listen tcp 127.0.0.1:8788: bind: address already in use`.

Note: when `tailscale.mode` is on, OpenClaw defaults `serve.path` to `/` so
Tailscale can proxy `/gmail-pubsub` correctly (it strips the set-path prefix).1) 如果你需要后端接收带前缀的路径，请将
   `hooks.gmail.tailscale.target` 设置为完整 URL（并对齐 `serve.path`）。

### 2. `canvasHost`（LAN/尾网 Canvas 文件服务器 + 实时重载）

3. Gateway 通过 HTTP 提供一个包含 HTML/CSS/JS 的目录，使 iOS/Android 节点可以直接 `canvas.navigate` 访问。

4. 默认根目录：`~/.openclaw/workspace/canvas`  
   默认端口：`18793`（选择该端口是为了避开 openclaw 浏览器 CDP 端口 `18792`）  
   服务器监听 **gateway 绑定主机**（LAN 或 Tailnet），以便节点能够访问。

5. 服务器：

- 6. 提供 `canvasHost.root` 下的文件
- 7. 向所提供的 HTML 中注入一个极小的实时重载客户端
- 8. 监视目录并通过位于 `/__openclaw__/ws` 的 WebSocket 端点广播重载事件
- 9. 当目录为空时自动创建一个示例 `index.html`（这样你可以立即看到内容）
- 10. 同时在 `/__openclaw__/a2ui/` 提供 A2UI，并以 `canvasHostUrl` 的形式向节点发布
      （节点始终使用该地址访问 Canvas/A2UI）

11. 如果目录很大或遇到 `EMFILE`，请禁用实时重载（以及文件监视）：

- 12. 配置：`canvasHost: { liveReload: false }`

```json5
13. {
  canvasHost: {
    root: "~/.openclaw/workspace/canvas",
    port: 18793,
    liveReload: true,
  },
}
```

14. 对 `canvasHost.*` 的更改需要重启 gateway（配置重载将触发重启）。

15. 禁用方式：

- 16. 配置：`canvasHost: { enabled: false }`
- 17. 环境变量：`OPENCLAW_SKIP_CANVAS_HOST=1`

### 15. `bridge`（旧版 TCP 桥接，已移除）

16. 当前构建不再包含 TCP 桥接监听器；`bridge.*` 配置键将被忽略。
17. 节点通过 Gateway WebSocket 连接。 17. 本节保留用于历史参考。

18. 旧版行为：

- 23. Gateway 可以为节点（iOS/Android）暴露一个简单的 TCP 桥接，通常使用端口 `18790`。

19. 默认值：

- 25. enabled: `true`
- 26. port: `18790`
- 27. bind: `lan`（绑定到 `0.0.0.0`）

28. 绑定模式：

- 20. `lan`：`0.0.0.0`（可通过任何接口访问，包括 LAN/Wi‑Fi 和 Tailscale）
- 30. `tailnet`：仅绑定到机器的 Tailscale IP（推荐用于 Vienna ⇄ London）
- 21. `loopback`：`127.0.0.1`（仅本地）
- 32. `auto`：如果存在 tailnet IP 则优先使用，否则使用 `lan`

33. TLS：

- 34. `bridge.tls.enabled`：为桥接连接启用 TLS（启用后仅允许 TLS）。
- 35. `bridge.tls.autoGenerate`：当未提供证书/密钥时生成自签名证书（默认：true）。
- 36. `bridge.tls.certPath` / `bridge.tls.keyPath`：桥接证书和私钥的 PEM 路径。
- 37. `bridge.tls.caPath`：可选的 PEM CA 包（自定义根证书或未来的 mTLS）。

38. 启用 TLS 后，Gateway 会在发现 TXT 记录中发布 `bridgeTls=1` 和 `bridgeTlsSha256`，
    以便节点固定证书。 39. 如果尚未存储指纹，手动连接将使用首次信任（TOFU）。
39. 自动生成的证书需要 PATH 中存在 `openssl`；如果生成失败，桥接将不会启动。

```json5
41. {
  bridge: {
    enabled: true,
    port: 18790,
    bind: "tailnet",
    tls: {
      enabled: true,
      // 省略时使用 ~/.openclaw/bridge/tls/bridge-{cert,key}.pem。
      // certPath: "~/.openclaw/bridge/tls/bridge-cert.pem",
      // keyPath: "~/.openclaw/bridge/tls/bridge-key.pem"
    },
  },
}
```

### 42. `discovery.mdns`（Bonjour / mDNS 广播模式）

43. 控制 LAN 上的 mDNS 发现广播（`_openclaw-gw._tcp`）。

- 44. `minimal`（默认）：在 TXT 记录中省略 `cliPath` + `sshPort`
- 45. `full`：在 TXT 记录中包含 `cliPath` + `sshPort`
- 46. `off`：完全禁用 mDNS 广播
- 47. 主机名：默认为 `openclaw`（发布为 `openclaw.local`）。 48. 可通过 `OPENCLAW_MDNS_HOSTNAME` 覆盖。

```json5
49. {
  discovery: { mdns: { mode: "minimal" } },
}
```

### 50. `discovery.wideArea`（广域 Bonjour / 单播 DNS‑SD）

启用后，Gateway 会使用配置的发现域（例如：`openclaw.internal.`）在 `~/.openclaw/dns/` 下为 `_openclaw-gw._tcp` 写入一个单播 DNS-SD 区域。

要让 iOS/Android 跨网络（维也纳 ⇄ 伦敦）发现，请配合使用：

- 在网关主机上运行的 DNS 服务器，用于提供你选择的域（推荐 CoreDNS）
- Tailscale **拆分 DNS**，使客户端通过网关 DNS 服务器解析该域

一次性设置助手（网关主机）：

```bash
openclaw dns setup --apply
```

```json5
{
  discovery: { wideArea: { enabled: true } },
}
```

## 媒体模型模板变量

模板占位符会在 `tools.media.*.models[].args` 和 `tools.media.models[].args`（以及未来任何使用模板的参数字段）中展开。

\| 变量               | 描述                                                                                 |
\| ------------------ | ------------------------------------------------------------------------------------ | -------- | ------- | ---------- | ----- | ------ | -------- | ------- | ------- | --- |
\| `{{Body}}`         | 完整的入站消息正文                                                                   |
\| `{{RawBody}}`      | 原始入站消息正文（无历史/发送者包装；最适合命令解析）                                |
\| `{{BodyStripped}}` | 去除群提及的正文（代理的最佳默认值）                                                 |
\| `{{From}}`         | 发送者标识（WhatsApp 为 E.164；可能因渠道而异）                                      |
\| `{{To}}`           | 目标标识                                                                             |
\| `{{MessageSid}}`   | 渠道消息 ID（可用时）                                                                |
\| `{{SessionId}}`    | 当前会话 UUID                                                                       |
\| `{{IsNewSession}}` | 当创建了新会话时为 `"true"`                                                        |
\| `{{MediaUrl}}`     | 入站媒体伪 URL（如存在）                                                            |
\| `{{MediaPath}}`    | 本地媒体路径（如已下载）                                                            |
\| `{{MediaType}}`    | 媒体类型（image/audio/document/…）                                             |
\| `{{Transcript}}`   | 音频转录（启用时）                                                                  |
\| `{{Prompt}}`       | CLI 条目的已解析媒体提示                                                           |
\| `{{MaxChars}}`     | CLI 条目的已解析最大输出字符数                                                     |
\| `{{ChatType}}`     | `"direct"` 或 `"group"`                                                         |
\| `{{GroupSubject}}` | 群组主题（尽力而为）                                                               |
\| `{{GroupMembers}}` | 群成员预览（尽力而为）                                                             |
\| `{{SenderName}}`   | 发送者显示名称（尽力而为）                                                         |
\| `{{SenderE164}}`   | 发送者电话号码（尽力而为）                                                         |
\| `{{Provider}}`     | 提供方提示（whatsapp | telegram | discord | googlechat | slack | signal | imessage | msteams | webchat | …）  |

## Cron（Gateway 调度器）

Cron 是 Gateway 自有的调度器，用于唤醒和计划任务。 有关功能概览和 CLI 示例，请参阅 [Cron jobs](/automation/cron-jobs)。

```json5
22. {
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
  },
}
```

---

_下一步：[Agent Runtime](/concepts/agent)_ 🦞
