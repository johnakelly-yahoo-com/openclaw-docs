---
summary: "Telegram bot support status, capabilities, and configuration"
read_when:
  - Working on Telegram features or webhooks
title: "Telegram"
---

# Telegram (Bot API)

Status: production-ready for bot DMs + groups via grammY. Long-polling by default; webhook optional.

## Quick setup (beginner)

1. Create a bot with **@BotFather** ([direct link](https://t.me/BotFather)). Confirm the handle is exactly `@BotFather`, then copy the token.
2. Set the token:
   - Env: `TELEGRAM_BOT_TOKEN=...`
   - Or config: `channels.telegram.botToken: "..."`.
   - If both are set, config takes precedence (env fallback is default-account only).
3. Start the gateway.
4. DM access is pairing by default; approve the pairing code on first contact.

Minimal config:

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",
    },
  },
}
```

## What it is

- A Telegram Bot API channel owned by the Gateway.
- Deterministic routing: replies go back to Telegram; the model never chooses channels.
- DMs share the agent's main session; groups stay isolated (`agent:<agentId>:telegram:group:<chatId>`).

## Setup (fast path)

### 1. Create a bot token (BotFather)

1. Open Telegram and chat with **@BotFather** ([direct link](https://t.me/BotFather)). Confirm the handle is exactly `@BotFather`.
2. Run `/newbot`, then follow the prompts (name + username ending in `bot`).
3. Copy the token and store it safely.

Optional BotFather settings:

- `/setjoingroups` — allow/deny adding the bot to groups.
- `/setprivacy` — control whether the bot sees all group messages.

### 2. Configure the token (env or config)

Example:

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```

Env option: `TELEGRAM_BOT_TOKEN=...` (works for the default account).
If both env and config are set, config takes precedence.

Multi-account support: use `channels.telegram.accounts` with per-account tokens and optional `name`. See [`gateway/configuration`](/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) for the shared pattern.

3. Start the gateway. Telegram starts when a token is resolved (config first, env fallback).
4. DM access defaults to pairing. Approve the code when the bot is first contacted.
5. For groups: add the bot, decide privacy/admin behavior (below), then set `channels.telegram.groups` to control mention gating + allowlists.

## Token + privacy + permissions (Telegram side)

### Token creation (BotFather)

- `/newbot` creates the bot and returns the token (keep it secret).
- If a token leaks, revoke/regenerate it via @BotFather and update your config.

### Group message visibility (Privacy Mode)

Telegram bots default to **Privacy Mode**, which limits which group messages they receive.
If your bot must see _all_ group messages, you have two options:

- Disable privacy mode with `/setprivacy` **or**
- Add the bot as a group **admin** (admin bots receive all messages).

**Note:** When you toggle privacy mode, Telegram requires removing + re‑adding the bot
to each group for the change to take effect.

### Group permissions (admin rights)

Admin status is set inside the group (Telegram UI). Admin bots always receive all
group messages, so use admin if you need full visibility.

## How it works (behavior)

- Inbound messages are normalized into the shared channel envelope with reply context and media placeholders.
- Group replies require a mention by default (native @mention or `agents.list[].groupChat.mentionPatterns` / `messages.groupChat.mentionPatterns`).
- Multi-agent override: set per-agent patterns on `agents.list[].groupChat.mentionPatterns`.
- Replies always route back to the same Telegram chat.
- Long-polling uses grammY runner with per-chat sequencing; overall concurrency is capped by `agents.defaults.maxConcurrent`.
- Telegram Bot API does not support read receipts; there is no `sendReadReceipts` option.

## Draft streaming

OpenClaw can stream partial replies in Telegram DMs using `sendMessageDraft`.

Requirements:

- Threaded Mode enabled for the bot in @BotFather (forum topic mode).
- Private chat threads only (Telegram includes `message_thread_id` on inbound messages).
- `channels.telegram.streamMode` not set to `"off"` (default: `"partial"`, `"block"` enables chunked draft updates).

Draft streaming is DM-only; Telegram does not support it in groups or channels.

## Formatting (Telegram HTML)

- Outbound Telegram text uses `parse_mode: "HTML"` (Telegram’s supported tag subset).
- Markdown-ish input is rendered into **Telegram-safe HTML** (bold/italic/strike/code/links); block elements are flattened to text with newlines/bullets.
- Raw HTML from models is escaped to avoid Telegram parse errors.
- If Telegram rejects the HTML payload, OpenClaw retries the same message as plain text.

## Commands (native + custom)

OpenClaw registers native commands (like `/status`, `/reset`, `/model`) with Telegram’s bot menu on startup.
You can add custom commands to the menu via config:

```json5
{
  channels: {
    telegram: {
      customCommands: [
        { command: "backup", description: "Git backup" },
        { command: "generate", description: "Create an image" },
      ],
    },
  },
}
```

## Setup troubleshooting (commands)

- `setMyCommands failed` in logs usually means outbound HTTPS/DNS is blocked to `api.telegram.org`.
- If you see `sendMessage` or `sendChatAction` failures, check IPv6 routing and DNS.

More help: [Channel troubleshooting](/channels/troubleshooting).

Notes:

- Custom commands are **menu entries only**; OpenClaw does not implement them unless you handle them elsewhere.
- Some commands can be handled by plugins/skills without being registered in Telegram’s command menu. These still work when typed (they just won't show up in `/commands` / the menu).
- Command names are normalized (leading `/` stripped, lowercased) and must match `a-z`, `0-9`, `_` (1–32 chars).
- Custom commands **cannot override native commands**. Conflicts are ignored and logged.
- If `commands.native` is disabled, only custom commands are registered (or cleared if none).

### Device pairing commands (`device-pair` plugin)

If the `device-pair` plugin is installed, it adds a Telegram-first flow for pairing a new phone:

1. `/pair` generates a setup code (sent as a separate message for easy copy/paste).
2. Paste the setup code in the iOS app to connect.
3. `/pair approve` approves the latest pending device request.

More details: [Pairing](/channels/pairing#pair-via-telegram-recommended-for-ios).

## Limits

- Outbound text is chunked to `channels.telegram.textChunkLimit` (default 4000).
- Optional newline chunking: set `channels.telegram.chunkMode="newline"` to split on blank lines (paragraph boundaries) before length chunking.
- Media downloads/uploads are capped by `channels.telegram.mediaMaxMb` (default 5).
- Telegram Bot API requests time out after `channels.telegram.timeoutSeconds` (default 500 via grammY). Set lower to avoid long hangs.
- Group history context uses `channels.telegram.historyLimit` (or `channels.telegram.accounts.*.historyLimit`), falling back to `messages.groupChat.historyLimit`. Set `0` to disable (default 50).
- DM history can be limited with `channels.telegram.dmHistoryLimit` (user turns). Per-user overrides: `channels.telegram.dms["<user_id>"].historyLimit`.

## Group activation modes

By default, the bot only responds to mentions in groups (`@botname` or patterns in `agents.list[].groupChat.mentionPatterns`). To change this behavior:

### Via config (recommended)

```json5
{
  channels: {
    telegram: {
      groups: {
        "-1001234567890": { requireMention: false }, // always respond in this group
      },
    },
  },
}
```

**Important:** Setting `channels.telegram.groups` creates an **allowlist** - only listed groups (or `"*"`) will be accepted.
Forum topics inherit their parent group config (allowFrom, requireMention, skills, prompts) unless you add per-topic overrides under `channels.telegram.groups.<groupId>.topics.<topicId>`.

To allow all groups with always-respond:

```json5
{
  channels: {
    telegram: {
      groups: {
        "*": { requireMention: false }, // all groups, always respond
      },
    },
  },
}
```

To keep mention-only for all groups (default behavior):

```json5
{
  channels: {
    telegram: {
      groups: {
        "*": { requireMention: true }, // or omit groups entirely
      },
    },
  },
}
```

### Via command (session-level)

Send in the group:

- `/activation always` - respond to all messages
- `/activation mention` - require mentions (default)

**Note:** Commands update session state only. For persistent behavior across restarts, use config.

### Getting the group chat ID

Forward any message from the group to `@userinfobot` or `@getidsbot` on Telegram to see the chat ID (negative number like `-1001234567890`).

**Tip:** For your own user ID, DM the bot and it will reply with your user ID (pairing message), or use `/whoami` once commands are enabled.

**Privacy note:** `@userinfobot` is a third-party bot. If you prefer, add the bot to the group, send a message, and use `openclaw logs --follow` to read `chat.id`, or use the Bot API `getUpdates`.

## Config writes

By default, Telegram is allowed to write config updates triggered by channel events or `/config set|unset`.

This happens when:

- A group is upgraded to a supergroup and Telegram emits `migrate_to_chat_id` (chat ID changes). OpenClaw can migrate `channels.telegram.groups` automatically.
- You run `/config set` or `/config unset` in a Telegram chat (requires `commands.config: true`).

Disable with:

```json5
{
  channels: { telegram: { configWrites: false } },
}
```

## Topics (forum supergroups)

Telegram forum topics include a `message_thread_id` per message. OpenClaw:

- Appends `:topic:<threadId>` to the Telegram group session key so each topic is isolated.
- Sends typing indicators and replies with `message_thread_id` so responses stay in the topic.
- General topic (thread id `1`) is special: message sends omit `message_thread_id` (Telegram rejects it), but typing indicators still include it.
- Exposes `MessageThreadId` + `IsForum` in template context for routing/templating.
- Topic-specific configuration is available under `channels.telegram.groups.<chatId>.topics.<threadId>` (skills, allowlists, auto-reply, system prompts, disable).
- Topic configs inherit group settings (requireMention, allowlists, skills, prompts, enabled) unless overridden per topic.

Private chats can include `message_thread_id` in some edge cases. OpenClaw keeps the DM session key unchanged, but still uses the thread id for replies/draft streaming when it is present.

## Inline Buttons

Telegram supports inline keyboards with callback buttons.

```json5
{
  channels: {
    telegram: {
      capabilities: {
        inlineButtons: "allowlist",
      },
    },
  },
}
```

For per-account configuration:

```json5
{
  channels: {
    telegram: {
      accounts: {
        main: {
          capabilities: {
            inlineButtons: "allowlist",
          },
        },
      },
    },
  },
}
```

Scopes:

- `off` — inline buttons disabled
- `dm` — only DMs (group targets blocked)
- `group` — only groups (DM targets blocked)
- `all` — DMs + groups
- `allowlist` — DMs + groups, but only senders allowed by `allowFrom`/`groupAllowFrom` (same rules as control commands)

Default: `allowlist`.
Legacy: `capabilities: ["inlineButtons"]` = `inlineButtons: "all"`.

### Sending buttons

Use the message tool with the `buttons` parameter:

```json5
{
  action: "send",
  channel: "telegram",
  to: "123456789",
  message: "Choose an option:",
  buttons: [
    [
      { text: "Yes", callback_data: "yes" },
      { text: "No", callback_data: "no" },
    ],
    [{ text: "Cancel", callback_data: "cancel" }],
  ],
}
```

When a user clicks a button, the callback data is sent back to the agent as a message with the format:
`callback_data: value`

### Configuration options

Telegram capabilities can be configured at two levels (object form shown above; legacy string arrays still supported):

- `channels.telegram.capabilities`: Global default capability config applied to all Telegram accounts unless overridden.
- `channels.telegram.accounts.<account>.capabilities`: Per-account capabilities that override the global defaults for that specific account.

Use the global setting when all Telegram bots/accounts should behave the same. Use per-account configuration when different bots need different behaviors (for example, one account only handles DMs while another is allowed in groups).

## Access control (DMs + groups)

### DM access

- Default: `channels.telegram.dmPolicy = "pairing"`. Unknown senders receive a pairing code; messages are ignored until approved (codes expire after 1 hour).
- Approve via:
  - `openclaw pairing list telegram`
  - `openclaw pairing approve telegram <CODE>`
- Pairing is the default token exchange used for Telegram DMs. Details: [Pairing](/channels/pairing)
- `channels.telegram.allowFrom` accepts numeric user IDs (recommended) or `@username` entries. It is **not** the bot username; use the human sender’s ID. The wizard accepts `@username` and resolves it to the numeric ID when possible.

#### Finding your Telegram user ID

Safer (no third-party bot):

1. Start the gateway and DM your bot.
2. Run `openclaw logs --follow` and look for `from.id`.

Alternate (official Bot API):

1. DM your bot.
2. Fetch updates with your bot token and read `message.from.id`:

   ```bash
   curl "https://api.telegram.org/bot<bot_token>/getUpdates"
   ```

Third-party (less private):

- DM `@userinfobot` or `@getidsbot` and use the returned user id.

### Group access

Two independent controls:

**1. Which groups are allowed** (group allowlist via `channels.telegram.groups`):

- No `groups` config = all groups allowed
- With `groups` config = only listed groups or `"*"` are allowed
- Example: `"groups": { "-1001234567890": {}, "*": {} }` allows all groups

**2. Which senders are allowed** (sender filtering via `channels.telegram.groupPolicy`):

- `"open"` = all senders in allowed groups can message
- `"allowlist"` = only senders in `channels.telegram.groupAllowFrom` can message
- `"disabled"` = no group messages accepted at all
  Default is `groupPolicy: "allowlist"` (blocked unless you add `groupAllowFrom`).

Most users want: `groupPolicy: "allowlist"` + `groupAllowFrom` + specific groups listed in `channels.telegram.groups`

To allow **any group member** to talk in a specific group (while still keeping control commands restricted to authorized senders), set a per-group override:

```json5
{
  channels: {
    telegram: {
      groups: {
        "-1001234567890": {
          groupPolicy: "open",
          requireMention: false,
        },
      },
    },
  },
}
```

## Long-polling vs webhook

- Default: long-polling (no public URL required).
- Webhook mode: set `channels.telegram.webhookUrl` and `channels.telegram.webhookSecret` (optionally `channels.telegram.webhookPath`).
  - The local listener binds to `0.0.0.0:8787` and serves `POST /telegram-webhook` by default.
  - If your public URL is different, use a reverse proxy and point `channels.telegram.webhookUrl` at the public endpoint.

## Reply threading

Telegram supports optional threaded replies via tags:

- `[[reply_to_current]]` -- reply to the triggering message.
- `[[reply_to:<id>]]` -- reply to a specific message id.

Controlled by `channels.telegram.replyToMode`:

- `first` (default), `all`, `off`.

## Audio messages (voice vs file)

Telegram distinguishes **voice notes** (round bubble) from **audio files** (metadata card).
OpenClaw defaults to audio files for backward compatibility.

To force a voice note bubble in agent replies, include this tag anywhere in the reply:

- `[[audio_as_voice]]` — send audio as a voice note instead of a file.

The tag is stripped from the delivered text. Other channels ignore this tag.

For message tool sends, set `asVoice: true` with a voice-compatible audio `media` URL
(`message` is optional when media is present):

```json5
{
  action: "send",
  channel: "telegram",
  to: "123456789",
  media: "https://example.com/voice.ogg",
  asVoice: true,
}
```

## Video messages (video vs video note)

Telegram distinguishes **video notes** (round bubble) from **video files** (rectangular).
OpenClaw defaults to video files.

For message tool sends, set `asVideoNote: true` with a video `media` URL:

```json5
{
  action: "send",
  channel: "telegram",
  to: "123456789",
  media: "https://example.com/video.mp4",
  asVideoNote: true,
}
```

(Note: Video notes do not support captions. If you provide a message text, it will be sent as a separate message.)

## Stickers

OpenClaw supports receiving and sending Telegram stickers with intelligent caching.

### Receiving stickers

When a user sends a sticker, OpenClaw handles it based on the sticker type:

- **Static stickers (WEBP):** Downloaded and processed through vision. The sticker appears as a `<media:sticker>` placeholder in the message content.
- **Animated stickers (TGS):** Skipped (Lottie format not supported for processing).
- **Video stickers (WEBM):** Skipped (video format not supported for processing).

Template context field available when receiving stickers:

- `Sticker` — object with:
  - `emoji` — emoji associated with the sticker
  - `setName` — name of the sticker set
  - `fileId` — Telegram file ID (send the same sticker back)
  - `fileUniqueId` — stable ID for cache lookup
  - `cachedDescription` — cached vision description when available

### Sticker cache

Stickers are processed through the AI's vision capabilities to generate descriptions. Since the same stickers are often sent repeatedly, OpenClaw caches these descriptions to avoid redundant API calls.

**How it works:**

1. 1. **首次遇到：** 将贴纸图片发送给 AI 进行视觉分析。 2. AI 生成描述（例如：“一只热情挥手的卡通猫”）。
2. 3. **缓存存储：** 描述会与贴纸的文件 ID、表情符号和贴纸包名称一起保存。
3. **Subsequent encounters:** When the same sticker is seen again, the cached description is used directly. 5. 图片不会再次发送给 AI。

6) **缓存位置：** `~/.openclaw/telegram/sticker-cache.json`

7. **缓存条目格式：**

```json
{
  "fileId": "CAACAgIAAxkBAAI...",
  "fileUniqueId": "AgADBAADb6cxG2Y",
  "emoji": "👋",
  "setName": "CoolCats",
  "description": "A cartoon cat waving enthusiastically",
  "cachedAt": "2026-01-15T10:30:00.000Z"
}
```

9. **优势：**

- 10. 通过避免对同一贴纸重复调用视觉接口，降低 API 成本
- 11. 对已缓存的贴纸响应更快（无需视觉处理延迟）
- 12. 基于缓存描述实现贴纸搜索功能

13. 缓存在接收贴纸时会自动填充。 14. 无需手动管理缓存。

### 15. 发送贴纸

16. 代理可以使用 `sticker` 和 `sticker-search` 动作来发送和搜索贴纸。 17. 这些功能默认是禁用的，必须在配置中启用：

```json5
{
  channels: {
    telegram: {
      actions: {
        sticker: true,
      },
    },
  },
}
```

19. **发送贴纸：**

```json5
{
  action: "sticker",
  channel: "telegram",
  to: "123456789",
  fileId: "CAACAgIAAxkBAAI...",
}
```

21. 参数：

- 22. `fileId`（必填）— 贴纸的 Telegram 文件 ID。 23. 可在接收贴纸时从 `Sticker.fileId` 获取，或来自 `sticker-search` 的结果。
- 24. `replyTo`（可选）— 要回复的消息 ID。
- 25. `threadId`（可选）— 论坛主题的消息线程 ID。

26. **搜索贴纸：**

27. 代理可以按描述、表情符号或贴纸包名称搜索已缓存的贴纸：

```json5
{
  action: "sticker-search",
  channel: "telegram",
  query: "cat waving",
  limit: 5,
}
```

29. 返回缓存中匹配的贴纸：

```json5
{
  ok: true,
  count: 2,
  stickers: [
    {
      fileId: "CAACAgIAAxkBAAI...",
      emoji: "👋",
      description: "A cartoon cat waving enthusiastically",
      setName: "CoolCats",
    },
  ],
}
```

31. 搜索会在描述文本、表情符号字符以及贴纸包名称之间进行模糊匹配。

32. **包含线程的示例：**

```json5
{
  action: "sticker",
  channel: "telegram",
  to: "-1001234567890",
  fileId: "CAACAgIAAxkBAAI...",
  replyTo: 42,
  threadId: 123,
}
```

## 34. 流式传输（草稿）

35. 在代理生成回复期间，Telegram 可以流式显示 **草稿气泡**。
36. OpenClaw 使用 Bot API 的 `sendMessageDraft`（不是真实消息），然后将最终回复作为普通消息发送。

37. 要求（Telegram Bot API 9.3+）：

- 38. **启用了主题的私聊**（机器人的论坛主题模式）。
- 39. 传入消息必须包含 `message_thread_id`（私有主题线程）。
- 40. 在群组 / 超级群组 / 频道中将忽略流式传输。

41. 配置：

- 42. `channels.telegram.streamMode: "off" | "partial" | "block"`（默认：`partial`）
  - 43. `partial`：使用最新的流式文本更新草稿气泡。
  - 44. `block`：以较大的块（分块）更新草稿气泡。
  - 45. `off`：禁用草稿流式传输。
- 46. 可选（仅适用于 `streamMode: "block"`）：
  - 47. \`channels.telegram.draftChunk: { minChars?, maxChars?, breakPreference?
    48. }` 49. 默认值：`minChars: 200`，`maxChars: 800`，`breakPreference: "paragraph"`（限制在 `channels.telegram.textChunkLimit\` 范围内）。
    - 50. 注意：草稿流式传输与 **块级流式传输**（频道消息）是相互独立的。

Note: draft streaming is separate from **block streaming** (channel messages).
Block streaming is off by default and requires `channels.telegram.blockStreaming: true`
if you want early Telegram messages instead of draft updates.

Reasoning stream (Telegram only):

- `/reasoning stream` streams reasoning into the draft bubble while the reply is
  generating, then sends the final answer without reasoning.
- If `channels.telegram.streamMode` is `off`, reasoning stream is disabled.
  More context: [Streaming + chunking](/concepts/streaming).

## Retry policy

Outbound Telegram API calls retry on transient network/429 errors with exponential backoff and jitter. Configure via `channels.telegram.retry`. See [Retry policy](/concepts/retry).

## Agent tool (messages + reactions)

- Tool: `telegram` with `sendMessage` action (`to`, `content`, optional `mediaUrl`, `replyToMessageId`, `messageThreadId`).
- Tool: `telegram` with `react` action (`chatId`, `messageId`, `emoji`).
- Tool: `telegram` with `deleteMessage` action (`chatId`, `messageId`).
- Reaction removal semantics: see [/tools/reactions](/tools/reactions).
- Tool gating: `channels.telegram.actions.reactions`, `channels.telegram.actions.sendMessage`, `channels.telegram.actions.deleteMessage` (default: enabled), and `channels.telegram.actions.sticker` (default: disabled).

## Reaction notifications

**How reactions work:**
Telegram reactions arrive as **separate `message_reaction` events**, not as properties in message payloads. When a user adds a reaction, OpenClaw:

1. Receives the `message_reaction` update from Telegram API
2. Converts it to a **system event** with format: `"Telegram reaction added: {emoji} by {user} on msg {id}"`
3. Enqueues the system event using the **same session key** as regular messages
4. When the next message arrives in that conversation, system events are drained and prepended to the agent's context

The agent sees reactions as **system notifications** in the conversation history, not as message metadata.

**Configuration:**

- `channels.telegram.reactionNotifications`: Controls which reactions trigger notifications
  - `"off"` — ignore all reactions
  - `"own"` — notify when users react to bot messages (best-effort; in-memory) (default)
  - `"all"` — notify for all reactions

- `channels.telegram.reactionLevel`: Controls agent's reaction capability
  - `"off"` — agent cannot react to messages
  - `"ack"` — bot sends acknowledgment reactions (👀 while processing) (default)
  - `"minimal"` — agent can react sparingly (guideline: 1 per 5-10 exchanges)
  - `"extensive"` — agent can react liberally when appropriate

**Forum groups:** Reactions in forum groups include `message_thread_id` and use session keys like `agent:main:telegram:group:{chatId}:topic:{threadId}`. This ensures reactions and messages in the same topic stay together.

**Example config:**

```json5
{
  channels: {
    telegram: {
      reactionNotifications: "all", // See all reactions
      reactionLevel: "minimal", // Agent can react sparingly
    },
  },
}
```

**Requirements:**

- Telegram bots must explicitly request `message_reaction` in `allowed_updates` (configured automatically by OpenClaw)
- For webhook mode, reactions are included in the webhook `allowed_updates`
- For polling mode, reactions are included in the `getUpdates` `allowed_updates`

## Delivery targets (CLI/cron)

- Use a chat id (`123456789`) or a username (`@name`) as the target.
- Example: `openclaw message send --channel telegram --target 123456789 --message "hi"`.

## Troubleshooting

**Bot doesn’t respond to non-mention messages in a group:**

- If you set `channels.telegram.groups.*.requireMention=false`, Telegram’s Bot API **privacy mode** must be disabled.
  - BotFather: `/setprivacy` → **Disable** (then remove + re-add the bot to the group)
- `openclaw channels status` shows a warning when config expects unmentioned group messages.
- `openclaw channels status --probe` can additionally check membership for explicit numeric group IDs (it can’t audit wildcard `"*"` rules).
- 1. 快速测试：`/activation always`（仅限会话；要持久化请使用配置）

2. **机器人完全看不到群消息：**

- 3. 如果设置了 `channels.telegram.groups`，则必须将该群列出，或使用 `"*"`
- 4. 在 @BotFather 中检查隐私设置 → “Group Privacy” 应为 **OFF**
- 5. 确认机器人确实是群成员（而不是仅被设为管理员但没有读取权限）
- 6. 检查网关日志：`openclaw logs --follow`（查找“skipping group message”）

7. **机器人会响应提及，但不响应 `/activation always`：**

- 8. `/activation` 命令只会更新会话状态，不会持久化到配置
- 9. 若需要持久化行为，请将群添加到 `channels.telegram.groups`，并设置 `requireMention: false`

10. **像 `/status` 这样的命令不起作用：**

- 11. 确保你的 Telegram 用户 ID 已被授权（通过配对或 `channels.telegram.allowFrom`）
- 12. 即使在 `groupPolicy: "open"` 的群中，命令也需要授权

13. **在 Node 22+ 上长轮询会立即中止（常见于代理/自定义 fetch）：**

- 14. Node 22+ 对 `AbortSignal` 实例更严格；外部的 signal 可能会立刻中止 `fetch` 调用。
- Upgrade to a OpenClaw build that normalizes abort signals, or run the gateway on Node 20 until you can upgrade.

16. **机器人启动后，随后无声地停止响应（或记录 `HttpError: Network request ... 17. failed`）：**

- 18. 一些主机会优先将 `api.telegram.org` 解析为 IPv6。 19. 如果你的服务器没有可用的 IPv6 出站连接，grammY 可能会卡在仅 IPv6 的请求上。
- 20. 解决方法：启用 IPv6 出站 **或** 强制对 `api.telegram.org` 使用 IPv4 解析（例如，在 `/etc/hosts` 中使用 IPv4 A 记录，或在操作系统的 DNS 栈中优先 IPv4），然后重启网关。
- Quick check: `dig +short api.telegram.org A` and `dig +short api.telegram.org AAAA` to confirm what DNS returns.

## 22. 配置参考（Telegram）

23. 完整配置：[Configuration](/gateway/configuration)

24. 提供方选项：

- `channels.telegram.enabled`: enable/disable channel startup.
- 26. `channels.telegram.botToken`：机器人令牌（BotFather）。
- 27. `channels.telegram.tokenFile`：从文件路径读取令牌。
- 28. `channels.telegram.dmPolicy`：`pairing | allowlist | open | disabled`（默认：pairing）。
- 29. `channels.telegram.allowFrom`：私聊允许列表（ID/用户名）。 `open` requires `"*"`.
- 31. `channels.telegram.groupPolicy`：`open | allowlist | disabled`（默认：allowlist）。
- 32. `channels.telegram.groupAllowFrom`：群发送者允许列表（ID/用户名）。
- 33. `channels.telegram.groups`：按群的默认值 + 允许列表（使用 `"*"` 作为全局默认）。
  - `channels.telegram.groups.<id>35. `channels.telegram.groups.<id>
    .requireMention\`：提及门控的默认值。
  - 34. `channels.telegram.groups.<id>
        .groupPolicy`：按群覆盖 groupPolicy（`open | allowlist | disabled`）。37. `channels.telegram.groups.<id>
        .allowFrom`：按群覆盖的发送者允许列表。
  - 36. `channels.telegram.groups.<id>
        .skills`：技能过滤（省略 = 所有技能，空 = 无）。39. `channels.telegram.groups.<id>
        .enabled`：当为 `false` 时禁用该群。
  - 38. `channels.telegram.groups.<id>
        .systemPrompt`：该群的额外 system prompt。41. `.topics.<threadId>
        .groupPolicy`：按主题覆盖 groupPolicy（`open | allowlist | disabled`）。
  - 40. `channels.telegram.groups.<id>
        .topics.<threadId>
        .*`：按主题覆盖（与群相同的字段）。.systemPrompt\`: extra system prompt for the group.
  - `channels.telegram.groups.<id>.enabled`: disable the group when `false`.
  - `channels.telegram.groups.<id>.topics.<threadId>.*`: per-topic overrides (same fields as group).
  - `channels.telegram.groups.<id>.topics.<threadId>.groupPolicy`: per-topic override for groupPolicy (`open | allowlist | disabled`).
  - `channels.telegram.groups.<id>.topics.<threadId>.requireMention`: per-topic mention gating override.
- `channels.telegram.capabilities.inlineButtons`: `off | dm | group | all | allowlist` (default: allowlist).
- `channels.telegram.accounts.<account>.capabilities.inlineButtons`: per-account override.
- `channels.telegram.replyToMode`: `off | first | all` (default: `first`).
- `channels.telegram.textChunkLimit`: outbound chunk size (chars).
- `channels.telegram.chunkMode`: `length` (default) or `newline` to split on blank lines (paragraph boundaries) before length chunking.
- `channels.telegram.linkPreview`: toggle link previews for outbound messages (default: true).
- `channels.telegram.streamMode`: `off | partial | block` (draft streaming).
- `channels.telegram.mediaMaxMb`: inbound/outbound media cap (MB).
- `channels.telegram.retry`: retry policy for outbound Telegram API calls (attempts, minDelayMs, maxDelayMs, jitter).
- `channels.telegram.network.autoSelectFamily`: override Node autoSelectFamily (true=enable, false=disable). Defaults to disabled on Node 22 to avoid Happy Eyeballs timeouts.
- `channels.telegram.proxy`: proxy URL for Bot API calls (SOCKS/HTTP).
- `channels.telegram.webhookUrl`: enable webhook mode (requires `channels.telegram.webhookSecret`).
- `channels.telegram.webhookSecret`: webhook secret (required when webhookUrl is set).
- `channels.telegram.webhookPath`: local webhook path (default `/telegram-webhook`).
- `channels.telegram.actions.reactions`: gate Telegram tool reactions.
- `channels.telegram.actions.sendMessage`: gate Telegram tool message sends.
- `channels.telegram.actions.deleteMessage`: gate Telegram tool message deletes.
- `channels.telegram.actions.sticker`: gate Telegram sticker actions — send and search (default: false).
- `channels.telegram.reactionNotifications`: `off | own | all` — control which reactions trigger system events (default: `own` when not set).
- `channels.telegram.reactionLevel`: `off | ack | minimal | extensive` — control agent's reaction capability (default: `minimal` when not set).

Related global options:

- `agents.list[].groupChat.mentionPatterns` (mention gating patterns).
- `messages.groupChat.mentionPatterns` (global fallback).
- `commands.native` (defaults to `"auto"` → on for Telegram/Discord, off for Slack), `commands.text`, `commands.useAccessGroups` (command behavior). Override with `channels.telegram.commands.native`.
- `messages.responsePrefix`, `messages.ackReaction`, `messages.ackReactionScope`, `messages.removeAckAfterReply`.
