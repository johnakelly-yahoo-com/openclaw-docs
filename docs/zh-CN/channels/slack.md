---
summary: "Slack 的 Socket 或 HTTP Webhook 模式设置"
read_when: "Setting up Slack or debugging Slack socket/HTTP mode"
title: "Slack"
---

# Slack

## Socket 模式（默认）

### 快速设置（新手）

1. Create a Slack app and enable **Socket Mode**.
2. 创建 **App Token**（`xapp-...`）和 **Bot Token**（`xoxb-...`）。
3. 为 OpenClaw 设置令牌并启动网关。

最小配置：

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
    },
  },
}
```

### 设置

1. 在 [https://api.slack.com/apps](https://api.slack.com/apps) 中创建一个 Slack 应用（From scratch）。
2. **Socket Mode** → 打开开关。 然后前往 **Basic Information** → **App-Level Tokens** → **Generate Token and Scopes**，并添加作用域 `connections:write`。 复制 **App Token**（`xapp-...`）。
3. **OAuth & Permissions** → 添加机器人令牌作用域（使用下面的清单）。 点击 **Install to Workspace**。 复制 **Bot User OAuth Token**（`xoxb-...`）。
4. 可选：**OAuth & Permissions** → 添加 **User Token Scopes**（参见下方只读列表）。 重新安装应用并复制 **User OAuth Token**（`xoxp-...`）。
5. **Event Subscriptions** → 启用事件并订阅：
   - `message.*`（包含编辑/删除/线程广播）
   - `app_mention`
   - `reaction_added`, `reaction_removed`
   - `member_joined_channel`、`member_left_channel`
   - `channel_rename`
   - `pin_added`、`pin_removed`
6. 邀请机器人加入你希望它读取的频道。
7. Slash Commands → 如果你使用 `channels.slack.slashCommand`，则创建 `/openclaw`。 如果启用原生命令，为每个内置命令添加一个斜杠命令（名称与 `/help` 中一致）。 Slack 的原生命令默认关闭，除非你设置 `channels.slack.commands.native: true`（全局 `commands.native` 为 `"auto"`，会让 Slack 保持关闭）。
8. App Home → 启用 **Messages Tab**，以便用户可以私信机器人。

使用下面的清单以保持作用域和事件同步。

Multi-account support: use `channels.slack.accounts` with per-account tokens and optional `name`. 参见 [`gateway/configuration`](/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) 了解通用模式。

### OpenClaw 配置（Socket 模式）

通过环境变量设置令牌（推荐）：

- `SLACK_APP_TOKEN=xapp-...`
- `SLACK_BOT_TOKEN=xoxb-...`

或通过配置：

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
    },
  },
}
```

### 用户令牌（可选）

OpenClaw 可以使用 Slack 用户令牌（`xoxp-...`）进行读取操作（历史记录、置顶、反应、表情、成员信息）。 默认情况下这是只读的：在存在用户令牌时，读取操作优先使用用户令牌，而写入操作仍然使用机器人令牌，除非你明确选择启用。 即使设置了 `userTokenReadOnly: false`，在可用的情况下，写入操作仍然优先使用机器人令牌。

用户令牌在配置文件中配置（不支持环境变量）。 对于多账户，设置 `channels.slack.accounts.<id>`.userToken\`。

包含机器人 + 应用 + 用户令牌的示例：

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
      userToken: "xoxp-...",
    },
  },
}
```

显式设置 userTokenReadOnly 的示例（允许使用用户令牌写入）：

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
      userToken: "xoxp-...",
      userTokenReadOnly: false,
    },
  },
}
```

#### 令牌使用

- 读取操作（历史、反应列表、置顶列表、表情列表、成员信息、搜索）在配置了用户令牌时优先使用用户令牌，否则使用机器人令牌。
- 写入操作（发送/编辑/删除消息、添加/移除反应、置顶/取消置顶、文件上传）默认使用机器人令牌。 如果 `userTokenReadOnly: false` 且没有可用的机器人令牌，OpenClaw 会回退使用用户令牌。

### History context

- `channels.slack.historyLimit`（或 `channels.slack.accounts.*.historyLimit`）控制会将多少最近的频道/群组消息封装进提示中。
- Falls back to `messages.groupChat.historyLimit`. 设置为 `0` 可禁用（默认 50）。

## HTTP 模式（Events API）

当你的 Gateway 可以通过 HTTPS 被 Slack 访问时（典型的服务器部署），使用 HTTP Webhook 模式。
HTTP 模式使用 Events API + 交互功能 + 斜杠命令，并共享同一个请求 URL。

### 设置（HTTP 模式）

1. 创建一个 Slack 应用并 **禁用 Socket Mode**（如果你只使用 HTTP，则这是可选的）。
2. **Basic Information** → 复制 **Signing Secret**。
3. **OAuth & Permissions** → 安装应用并复制 **Bot User OAuth Token**（`xoxb-...`）。
4. **Event Subscriptions** → 启用事件并将 **Request URL** 设置为你的网关 Webhook 路径（默认 `/slack/events`）。
5. **Interactivity & Shortcuts** → 启用并设置相同的 **Request URL**。
6. **Slash Commands** → 为你的命令设置相同的 **Request URL**。

请求 URL 示例：
`https://gateway-host/slack/events`

### OpenClaw 配置（最小示例）

```json5
{
  channels: {
    slack: {
      enabled: true,
      mode: "http",
      botToken: "xoxb-...",
      signingSecret: "your-signing-secret",
      webhookPath: "/slack/events",
    },
  },
}
```

多账户 HTTP 模式：设置 `channels.slack.accounts.<id>`.mode = "http" 并为每个账户提供唯一的
`webhookPath`，以便每个 Slack 应用都指向自己的 URL。

### Manifest（可选）

使用此 Slack 应用清单可以快速创建应用（如有需要可调整名称/命令）。 如果你计划配置用户令牌，请包含用户作用域。

```json
{
  "display_information": {
    "name": "OpenClaw",
    "description": "Slack connector for OpenClaw"
  },
  "features": {
    "bot_user": {
      "display_name": "OpenClaw",
      "always_online": false
    },
    "app_home": {
      "messages_tab_enabled": true,
      "messages_tab_read_only_enabled": false
    },
    "slash_commands": [
      {
        "command": "/openclaw",
        "description": "Send a message to OpenClaw",
        "should_escape": false
      }
    ]
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "chat:write",
        "channels:history",
        "channels:read",
        "groups:history",
        "groups:read",
        "groups:write",
        "im:history",
        "im:read",
        "im:write",
        "mpim:history",
        "mpim:read",
        "mpim:write",
        "users:read",
        "app_mentions:read",
        "reactions:read",
        "reactions:write",
        "pins:read",
        "pins:write",
        "emoji:read",
        "commands",
        "files:read",
        "files:write"
      ],
      "user": [
        "channels:history",
        "channels:read",
        "groups:history",
        "groups:read",
        "im:history",
        "im:read",
        "mpim:history",
        "mpim:read",
        "users:read",
        "reactions:read",
        "pins:read",
        "emoji:read",
        "search:read"
      ]
    }
  },
  "settings": {
    "socket_mode_enabled": true,
    "event_subscriptions": {
      "bot_events": [
        "app_mention",
        "message.channels",
        "message.groups",
        "message.im",
        "message.mpim",
        "reaction_added",
        "reaction_removed",
        "member_joined_channel",
        "member_left_channel",
        "channel_rename",
        "pin_added",
        "pin_removed"
      ]
    }
  }
}
```

如果你启用了原生命令，请为每个要暴露的命令添加一个 `slash_commands` 条目（与 `/help` 列表匹配）。 使用 `channels.slack.commands.native` 覆盖。

## 作用域（当前 vs 可选）

Slack 的 Conversations API 是按类型划分作用域的：你只需要为实际使用到的会话类型配置作用域（channels、groups、im、mpim）。 概览请参见
[https://docs.slack.dev/apis/web-api/using-the-conversations-api/](https://docs.slack.dev/apis/web-api/using-the-conversations-api/)。

### 机器人令牌作用域（必需）

- `chat:write`（通过 `chat.postMessage` 发送/更新/删除消息）
  [https://docs.slack.dev/reference/methods/chat.postMessage](https://docs.slack.dev/reference/methods/chat.postMessage)
- `im:write`（通过 `conversations.open` 打开用户私信）
  [https://docs.slack.dev/reference/methods/conversations.open](https://docs.slack.dev/reference/methods/conversations.open)
- `channels:history`、`groups:history`、`im:history`、`mpim:history`
  [https://docs.slack.dev/reference/methods/conversations.history](https://docs.slack.dev/reference/methods/conversations.history)
- `channels:read`、`groups:read`、`im:read`、`mpim:read`
  [https://docs.slack.dev/reference/methods/conversations.info](https://docs.slack.dev/reference/methods/conversations.info)
- `users:read`（用户查询）
  [https://docs.slack.dev/reference/methods/users.info](https://docs.slack.dev/reference/methods/users.info)
- 1. `reactions:read`, `reactions:write`（`reactions.get` / `reactions.add`）
- [https://docs.slack.dev/reference/methods/reactions.get](https://docs.slack.dev/reference/methods/reactions.get)
- [https://docs.slack.dev/reference/methods/reactions.add](https://docs.slack.dev/reference/methods/reactions.add)
- 2. `pins:read`, `pins:write`（`pins.list` / `pins.add` / `pins.remove`）

### [https://docs.slack.dev/reference/scopes/pins.read](https://docs.slack.dev/reference/scopes/pins.read)

[https://docs.slack.dev/reference/scopes/pins.write](https://docs.slack.dev/reference/scopes/pins.write)

- 3. `emoji:read`（`emoji.list`）
- [https://docs.slack.dev/reference/scopes/emoji.read](https://docs.slack.dev/reference/scopes/emoji.read)
- 4. `files:write`（通过 `files.uploadV2` 上传）
- [https://docs.slack.dev/messaging/working-with-files/#upload](https://docs.slack.dev/messaging/working-with-files/#upload)
- 5. 用户令牌作用域（可选，默认为只读）
- 6. 如果你配置了 `channels.slack.userToken`，请将这些添加到 **User Token Scopes** 下。
- 7. `channels:history`, `groups:history`, `im:history`, `mpim:history`

### 8. `channels:read`, `groups:read`, `im:read`, `mpim:read`

- 9. `users:read`
- 10. `reactions:read`
- 11. `pins:read`
- 12. `emoji:read`
- 13. `search:read`

## 14. 当前不需要（但未来很可能需要）

15. `mpim:write`（仅当我们通过 `conversations.open` 添加群组 DM 打开/启动 DM 时） 16. `groups:write`（仅当我们添加私有频道管理：创建/重命名/邀请/归档时）

```json
17. `chat:write.public`（仅当我们希望向机器人未加入的频道发帖时）
```

[https://docs.slack.dev/reference/scopes/chat.write.public](https://docs.slack.dev/reference/scopes/chat.write.public)

- 18. `users:read.email`（仅当我们需要从 `users.info` 获取邮箱字段时）
- [https://docs.slack.dev/changelog/2017-04-narrowing-email-access](https://docs.slack.dev/changelog/2017-04-narrowing-email-access)

19. `files:read`（仅当我们开始列出/读取文件元数据时） 20. 配置

## 21. Slack 仅使用 Socket Mode（不使用 HTTP webhook 服务器）。

- 22. 提供两个令牌：
- 23. {
      "slack": {
      "enabled": true,
      "botToken": "xoxb-...",
      "appToken": "xapp-...",
      "groupPolicy": "allowlist",
      "dm": {
      "enabled": true,
      "policy": "pairing",
      "allowFrom": ["U123", "U456", "\*"],
      "groupEnabled": false,
      "groupChannels": ["G123"],
      "replyToMode": "all"
      },
      "channels": {
      "C123": { "allow": true, "requireMention": true },
      "#general": {
      "allow": true,
      "requireMention": true,
      "users": ["U123"],
      "skills": ["search", "docs"],
      "systemPrompt": "Keep answers short."
      }
      },
      "reactionNotifications": "own",
      "reactionAllowlist": ["U123"],
      "replyToMode": "off",
      "actions": {
      "reactions": true,
      "messages": true,
      "pins": true,
      "memberInfo": true,
      "emojiList": true
      },
      "slashCommand": {
      "enabled": true,
      "name": "openclaw",
      "sessionPrefix": "slack:slash",
      "ephemeral": true
      },
      "textChunkLimit": 4000,
      "mediaMaxMb": 20
      }
      }
- 24. 令牌也可以通过环境变量提供：

## 25. `SLACK_BOT_TOKEN`

26. `SLACK_APP_TOKEN` 27. 确认（Ack）反应通过 `messages.ackReaction` + `messages.ackReactionScope` 进行全局控制。

| 28. 使用 `messages.removeAckAfterReply` 在机器人回复后清除确认反应。     | 29. 限制                                                                                                                                   |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 30. 外发文本会按 `channels.slack.textChunkLimit`（默认 4000）进行分块。 | 31. 可选的换行分块：设置 `channels.slack.chunkMode="newline"`，在按长度分块前先按空行（段落边界）拆分。 32. 媒体上传受 `channels.slack.mediaMaxMb`（默认 20）限制。 |
| 33. 回复线程                                                 | 34. 默认情况下，OpenClaw 在主频道中回复。 35. 使用 `channels.slack.replyToMode` 控制自动线程化：                                                 |
| 36. 模式                                                   | 37. 行为 38. `off`                                                                                                         |

39. **默认。** 在主频道中回复。

### 40. 仅当触发消息本身已经在一个线程中时才使用线程回复。

41. `first`

```json5
42. 第一条回复进入线程（在触发消息下），后续回复发送到主频道。
```

Supported chat types:

- `direct`: 1:1 DMs (Slack `im`)
- `group`: group DMs / MPIMs (Slack `mpim`)
- `channel`: standard channels (public/private)

Precedence:

1. `replyToModeByChatType.<chatType>`
2. `replyToMode`
3. Provider default (`off`)

Legacy `channels.slack.dm.replyToMode` is still accepted as a fallback for `direct` when no chat-type override is set.

Examples:

Thread DMs only:

```json5
{
  channels: {
    slack: {
      replyToMode: "off",
      replyToModeByChatType: { direct: "all" },
    },
  },
}
```

Thread group DMs but keep channels in the root:

```json5
{
  channels: {
    slack: {
      replyToMode: "off",
      replyToModeByChatType: { group: "first" },
    },
  },
}
```

Make channels thread, keep DMs in the root:

```json5
{
  channels: {
    slack: {
      replyToMode: "first",
      replyToModeByChatType: { direct: "off", group: "off" },
    },
  },
}
```

### Manual threading tags

For fine-grained control, use these tags in agent responses:

- `[[reply_to_current]]` — reply to the triggering message (start/continue thread).
- `[[reply_to:<id>]]` — reply to a specific message id.

## Sessions + routing

- DMs share the `main` session (like WhatsApp/Telegram).
- Channels map to `agent:<agentId>:slack:channel:<channelId>` sessions.
- Slash commands use `agent:<agentId>:slack:slash:<userId>` sessions (prefix configurable via `channels.slack.slashCommand.sessionPrefix`).
- If Slack doesn’t provide `channel_type`, OpenClaw infers it from the channel ID prefix (`D`, `C`, `G`) and defaults to `channel` to keep session keys stable.
- Native command registration uses `commands.native` (global default `"auto"` → Slack off) and can be overridden per-workspace with `channels.slack.commands.native`. Text commands require standalone `/...` messages and can be disabled with `commands.text: false`. Slack slash commands are managed in the Slack app and are not removed automatically. Use `commands.useAccessGroups: false` to bypass access-group checks for commands.
- Full command list + config: [Slash commands](/tools/slash-commands)

## DM security (pairing)

- Default: `channels.slack.dm.policy="pairing"` — unknown DM senders get a pairing code (expires after 1 hour).
- Approve via: `openclaw pairing approve slack <code>`.
- To allow anyone: set `channels.slack.dm.policy="open"` and `channels.slack.dm.allowFrom=["*"]`.
- `channels.slack.dm.allowFrom` accepts user IDs, @handles, or emails (resolved at startup when tokens allow). The wizard accepts usernames and resolves them to ids during setup when tokens allow.

## Group policy

- `channels.slack.groupPolicy` controls channel handling (`open|disabled|allowlist`).
- `allowlist` requires channels to be listed in `channels.slack.channels`.
- If you only set `SLACK_BOT_TOKEN`/`SLACK_APP_TOKEN` and never create a `channels.slack` section,
  the runtime defaults `groupPolicy` to `open`. Add `channels.slack.groupPolicy`,
  `channels.defaults.groupPolicy`, or a channel allowlist to lock it down.
- The configure wizard accepts `#channel` names and resolves them to IDs when possible
  (public + private); if multiple matches exist, it prefers the active channel.
- On startup, OpenClaw resolves channel/user names in allowlists to IDs (when tokens allow)
  and logs the mapping; unresolved entries are kept as typed.
- To allow **no channels**, set `channels.slack.groupPolicy: "disabled"` (or keep an empty allowlist).

Channel options (`channels.slack.channels.<id>` or `channels.slack.channels.<name>`):

- `allow`: allow/deny the channel when `groupPolicy="allowlist"`.
- `requireMention`: mention gating for the channel.
- `tools`：可选的按频道工具策略覆盖（`allow`/`deny`/`alsoAllow`）。
- `toolsBySender`: optional per-sender tool policy overrides within the channel (keys are sender ids/@handles/emails; `"*"` wildcard supported).
- `allowBots`：允许机器人撰写的消息进入该频道（默认：false）。
- `users`：可选的按频道用户允许列表。
- `skills`: skill filter (omit = all skills, empty = none).
- `systemPrompt`：频道的额外系统提示（与主题/目的合并）。
- `enabled`：设置为 `false` 以禁用该频道。

## Delivery targets

与 cron/CLI 发送一起使用：

- `user:<id>` for DMs
- `channel:<id>` 用于频道

## 工具操作

Slack 工具操作可通过 `channels.slack.actions.*` 进行门控：

| 操作组  | Default | 说明                     |
| ---- | ------- | ---------------------- |
| 表情反应 | 启用      | React + list reactions |
| 消息   | 启用      | 读取/发送/编辑/删除            |
| 置顶   | 启用      | 置顶/取消置顶/列表             |
| 成员信息 | 启用      | 成员信息                   |
| 表情列表 | 启用      | 自定义表情列表                |

## 安全说明

- 写入操作默认使用机器人令牌，因此状态变更操作会限定在应用的机器人权限与身份范围内。
- 将 `userTokenReadOnly: false` 设为 false 允许在没有机器人令牌时使用用户令牌进行写操作，这意味着操作将以安装用户的访问权限运行。 将用户令牌视为高度特权，并保持操作门控与允许列表足够严格。
- If you enable user-token writes, make sure the user token includes the write
  scopes you expect (`chat:write`, `reactions:write`, `pins:write`,
  `files:write`) or those operations will fail.

## Troubleshooting

先运行以下阶梯：

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

如有需要，然后确认私信配对状态：

```bash
openclaw pairing list slack
```

常见故障：

- 已连接但频道无回复：频道被 `groupPolicy` 阻止或未在 `channels.slack.channels` 允许列表中。
- 私信被忽略：当 `channels.slack.dm.policy="pairing"` 时，发送者未获批准。
- API errors (`missing_scope`, `not_in_channel`, auth failures): bot/app tokens or Slack scopes are incomplete.

分诊流程请参见：[/channels/troubleshooting](/channels/troubleshooting)。

## 说明

- 提及门控由 `channels.slack.channels` 控制（将 `requireMention` 设为 `true`）；`agents.list[].groupChat.mentionPatterns`（或 `messages.groupChat.mentionPatterns`）也会计为提及。
- 多代理覆盖：在 `agents.list[].groupChat.mentionPatterns` 上为每个代理设置模式。
- 反应通知遵循 `channels.slack.reactionNotifications`（使用 `reactionAllowlist` 且模式为 `allowlist`）。
- Bot-authored messages are ignored by default; enable via `channels.slack.allowBots` or `channels.slack.channels.<id>.allowBots`.
- Warning: If you allow replies to other bots (`channels.slack.allowBots=true` or `channels.slack.channels.<id>.allowBots=true`), prevent bot-to-bot reply loops with `requireMention`, `channels.slack.channels.<id>.users` allowlists, and/or clear guardrails in `AGENTS.md` and `SOUL.md`.
- For the Slack tool, reaction removal semantics are in [/tools/reactions](/tools/reactions).
- Attachments are downloaded to the media store when permitted and under the size limit.
