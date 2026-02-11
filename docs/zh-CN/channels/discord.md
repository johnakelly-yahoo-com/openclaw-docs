---
summary: "Discord 机器人支持状态、能力与配置"
read_when:
  - 正在开发 Discord 渠道功能
title: "Discord"
---

# Discord（Bot API）

状态：通过官方 Discord 机器人网关，已支持 DM 和服务器文本频道。

## 快速设置（新手）

1. 创建一个 Discord 机器人并复制机器人令牌。
2. 在 Discord 应用设置中，启用 **Message Content Intent**（如果你计划使用允许列表或名称查找，还需启用 **Server Members Intent**）。
3. 为 OpenClaw 设置令牌：
   - 环境变量：`DISCORD_BOT_TOKEN=...`
   - 或者配置：`channels.discord.token: "..."`。
   - 如果两者都设置，以配置为准（环境变量回退仅适用于默认账户）。
4. 使用消息权限邀请机器人加入你的服务器（如果你只想使用 DM，可以创建一个私有服务器）。
5. 启动网关。
6. DM 访问默认采用配对方式；首次联系时批准配对码。

最小配置：

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "YOUR_BOT_TOKEN",
    },
  },
}
```

## 目标

- 通过 Discord 私信或服务器频道与 OpenClaw 对话。
- 私聊会折叠到代理的主会话中（默认 `agent:main:main`）；服务器频道保持隔离，形式为 `agent:<agentId>:discord:channel:<channelId>`（显示名称使用 `discord:<guildSlug>#<channelSlug>`）。
- 默认会忽略群组私信；可通过 `channels.discord.dm.groupEnabled` 启用，并可选地通过 `channels.discord.dm.groupChannels` 进行限制。
- 保持路由确定性：回复始终返回到其到达的频道。

## 工作原理

1. 创建一个 Discord 应用 → Bot，启用所需的意图（DM + 服务器消息 + 消息内容），并获取机器人令牌。
2. 邀请机器人加入你的服务器，并授予在你希望使用它的地方读取/发送消息所需的权限。
3. 使用 `channels.discord.token`（或作为回退的 `DISCORD_BOT_TOKEN`）配置 OpenClaw。
4. 运行网关；当令牌可用（优先配置，其次环境变量）且 `channels.discord.enabled` 不为 `false` 时，它会自动启动 Discord 渠道。
   - 如果你更喜欢使用环境变量，请设置 `DISCORD_BOT_TOKEN`（配置块是可选的）。
5. 私聊：投递时使用 `user:<id>`（或 `<@id>` 提及）；所有轮次都会进入共享的 `main` 会话。 纯数字 ID 含义不明确，会被拒绝。
6. 服务器频道：投递时使用 `channel:<channelId>`。 默认需要提及（mention），并且可以按服务器或按频道进行设置。
7. 私聊：默认通过 `channels.discord.dm.policy` 进行安全控制（默认值：`"pairing"`）。 未知发送者会收到一个配对码（1 小时后过期）；通过 `openclaw pairing approve discord <code>` 批准。
   - 要保持旧的“对任何人开放”行为：设置 `channels.discord.dm.policy="open"` 且 `channels.discord.dm.allowFrom=["*"]`。
   - 要使用严格允许列表：设置 `channels.discord.dm.policy="allowlist"` 并在 `channels.discord.dm.allowFrom` 中列出发送者。
   - 要忽略所有 DM：设置 `channels.discord.dm.enabled=false` 或 `channels.discord.dm.policy="disabled"`。
8. 默认忽略群组 DM；可通过 `channels.discord.dm.groupEnabled` 启用，并可选地通过 `channels.discord.dm.groupChannels` 进行限制。
9. 可选的服务器规则：设置以服务器 ID（首选）或 slug 为键的 `channels.discord.guilds`，并包含按频道的规则。
10. 可选的原生命令：`commands.native` 默认为 `"auto"`（Discord/Telegram 开启，Slack 关闭）。 使用 `channels.discord.commands.native: true|false|"auto"` 覆盖；`false` 会清除先前注册的命令。 文本命令由 `commands.text` 控制，必须以独立的 `/...` 消息发送。 使用 `commands.useAccessGroups: false` 可绕过命令的访问组检查。
    - 1. 完整命令列表 + 配置：[斜杠命令](/tools/slash-commands)
11. Optional guild context history: set `channels.discord.historyLimit` (default 20, falls back to `messages.groupChat.historyLimit`) to include the last N guild messages as context when replying to a mention. Set `0` to disable.
12. 4. 表情反应：代理可以通过 `discord` 工具触发表情反应（受 `channels.discord.actions.*` 限制）。
    - 5. 表情反应移除语义：参见 [/tools/reactions](/tools/reactions)。
    - 6. 仅当当前频道是 Discord 时，才会暴露 `discord` 工具。
13. Native commands use isolated session keys (`agent:<agentId>:discord:slash:<userId>`) rather than the shared `main` session.

8) 注意：名称 → id 的解析使用服务器成员搜索，并需要 Server Members Intent；如果机器人无法搜索成员，请使用 id 或 `<@id>` 提及。
9) 注意：Slug 为小写，空格替换为 `-`。 10. 频道名称会被 slug 化且不包含前导的 `#`。
10) 注意：服务器上下文中的 `[from:]` 行包含 `author.tag` + `id`，以便轻松生成可 ping 的回复。

## Config writes

By default, Discord is allowed to write config updates triggered by `/config set|unset` (requires `commands.config: true`).

14. 禁用方式：

```json5
15. {
  channels: { discord: { configWrites: false } },
}
```

## 16. 如何创建你自己的机器人

This is the “Discord Developer Portal” setup for running OpenClaw in a server (guild) channel like `#help`.

### 1. Create the Discord app + bot user

1. 19. Discord Developer Portal → **Applications** → **New Application**
2. 20. 在你的应用中：
   - 21. **Bot** → **Add Bot**
   - 22. 复制 **Bot Token**（这就是你放入 `DISCORD_BOT_TOKEN` 的内容）

### 23) 2）启用 OpenClaw 所需的网关意图

24. Discord 会阻止“特权意图”，除非你明确启用它们。

25. 在 **Bot** → **Privileged Gateway Intents** 中，启用：

- 26. **Message Content Intent**（在大多数服务器中读取消息文本所必需；没有它你会看到“Used disallowed intents”，或者机器人会连接但不对消息做出反应）
- 27. **Server Members Intent**（推荐；在服务器中进行某些成员/用户查找和允许列表匹配时必需）

28. 通常**不**需要 **Presence Intent**。 29. 设置机器人自身的在线状态（`setPresence` 动作）使用网关 OP3，不需要该意图；只有当你想接收其他服务器成员的在线状态更新时才需要。

### 30. 3）生成邀请 URL（OAuth2 URL Generator）

31. 在你的应用中：**OAuth2** → **URL Generator**

32. **Scopes**

- 33. ✅ `bot`
- 34. ✅ `applications.commands`（原生命令所需）

35. **Bot Permissions**（最小基线）

- 36. ✅ 查看频道
- 37. ✅ 发送消息
- ✅ Read Message History
- 39. ✅ 嵌入链接
- 40. ✅ 附加文件
- 41. ✅ 添加反应（可选但推荐）
- 42. ✅ 使用外部表情 / 贴纸（可选；仅在你需要时）

43. 除非你在调试并且完全信任该机器人，否则请避免 **Administrator**。

44. 复制生成的 URL，打开它，选择你的服务器，然后安装机器人。

### 45. 4）获取 id（服务器/用户/频道）

46. Discord 在各处使用数字 id；OpenClaw 配置更偏好使用 id。

1. 47. Discord（桌面/网页）→ **User Settings** → **Advanced** → 启用 **Developer Mode**
2. 48. 右键单击：
   - 49. 服务器名称 → **Copy Server ID**（服务器 id）
   - 50. 频道（例如 `#help`）→ **Copy Channel ID**
   - 1. 你的用户 → **复制用户 ID**

### 2) 5）配置 OpenClaw

#### Token

Set the bot token via env var (recommended on servers):

- 5. `DISCORD_BOT_TOKEN=...`

6. 或通过配置：

```json5
7. {
  channels: {
    discord: {
      enabled: true,
      token: "YOUR_BOT_TOKEN",
    },
  },
}
```

8. 多账号支持：使用 `channels.discord.accounts`，为每个账号配置独立的令牌，并可选 `name`。 9. 参见 [`gateway/configuration`](/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) 了解通用模式。

#### 10. 允许列表 + 频道路由

11. 示例“单一服务器，只允许我，只允许 #help”：

```json5
12. {
  channels: {
    discord: {
      enabled: true,
      dm: { enabled: false },
      guilds: {
        YOUR_GUILD_ID: {
          users: ["YOUR_USER_ID"],
          requireMention: true,
          channels: {
            help: { allow: true, requireMention: true },
          },
        },
      },
      retry: {
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}
```

13. 说明：

- `requireMention: true` means the bot only replies when mentioned (recommended for shared channels).
- 15. `agents.list[].groupChat.mentionPatterns`（或 `messages.groupChat.mentionPatterns`）也会被视为公会消息中的提及。
- Multi-agent override: set per-agent patterns on `agents.list[].groupChat.mentionPatterns`.
- 17. 如果存在 `channels`，则任何未列出的频道默认被拒绝。
- 18. 使用 `"*"` 频道条目可将默认设置应用到所有频道；显式的频道条目会覆盖通配符。
- Threads inherit parent channel config (allowlist, `requireMention`, skills, prompts, etc.) 20. 除非你显式添加线程频道 ID。
- 21. 所有者提示：当每个公会或每个频道的 `users` 允许列表匹配发送者时，OpenClaw 会在系统提示中将该发送者视为所有者。 For a global owner across channels, set `commands.ownerAllowFrom`.
- 23. 默认会忽略机器人撰写的消息；设置 `channels.discord.allowBots=true` 可允许它们（自身消息仍会被过滤）。
- 24. 警告：如果你允许回复其他机器人（`channels.discord.allowBots=true`），请通过 `requireMention`、`channels.discord.guilds.*.channels.<id>`25. `.users` 允许列表，和/或在 `AGENTS.md` 与 `SOUL.md` 中设置明确的防护规则，来防止机器人之间的回复循环。

### 26. 6）验证是否正常工作

1. 27. 启动网关。
2. 28. 在你的服务器频道中发送：`@Krill hello`（或你的机器人名称）。
3. 29. 如果没有反应：请查看下面的 **故障排查**。

### 30) 故障排查

- 31. 首先：运行 `openclaw doctor` 和 `openclaw channels status --probe`（可操作的警告 + 快速审计）。
- 32. **“使用了不允许的意图”**：在开发者门户中启用 **消息内容意图**（以及很可能需要 **服务器成员意图**），然后重启网关。
- 33. **机器人已连接但在公会频道中从不回复**：
  - 34. 缺少 **消息内容意图**，或
  - 35. 机器人缺少频道权限（查看/发送/读取历史），或
  - 36. 你的配置要求提及而你没有提及它，或
  - 37. 你的公会/频道允许列表拒绝了该频道/用户。
- 38. **`requireMention: false` 但仍然没有回复**：
- 39. `channels.discord.groupPolicy` 默认为 **allowlist**；将其设置为 `"open"`，或在 `channels.discord.guilds` 下添加一个公会条目（可选地在 `channels.discord.guilds.<id>` 下列出 `channels` 以进行限制）。40. `.channels` 以限制）。
  - 41. 如果你只设置了 `DISCORD_BOT_TOKEN`，却从未创建 `channels.discord` 部分，运行时会将 `groupPolicy` 默认设置为 `open`。 42. 添加 `channels.discord.groupPolicy`、`channels.defaults.groupPolicy`，或公会/频道允许列表以进行收紧。
- 43. `requireMention` 必须位于 `channels.discord.guilds` 下（或某个具体频道）。 44. 顶层的 `channels.discord.requireMention` 会被忽略。
- 45. **权限审计**（`channels status --probe`）只检查数字形式的频道 ID。 46. 如果你使用别名/名称作为 `channels.discord.guilds.*.channels` 的键，审计将无法验证权限。
- 47. **私信不起作用**：`channels.discord.dm.enabled=false`、`channels.discord.dm.policy="disabled"`，或你尚未获批（`channels.discord.dm.policy="pairing"`）。
- 48. **Discord 中的执行审批**：Discord 在私信中支持用于执行审批的 **按钮 UI**（允许一次 / 始终允许 / 拒绝）。 49. `/approve <id> ...` 仅用于转发的审批，无法解决 Discord 的按钮提示。 50. 如果你看到 `❌ Failed to submit approval: Error: unknown approval id` 或 UI 从未出现，请检查：
  - 1. 在你的配置中设置 `channels.discord.execApprovals.enabled: true`。
  - Your Discord user ID is listed in `channels.discord.execApprovals.approvers` (the UI is only sent to approvers).
  - 3. 在 DM 提示中使用按钮（**Allow once**、**Always allow**、**Deny**）。
  - 4. 有关更完整的审批与命令流程，请参见 [Exec approvals](/tools/exec-approvals) 和 [Slash commands](/tools/slash-commands)。

## 5. 能力与限制

- 6. 支持 DM 和服务器文本频道（线程被视为独立频道；不支持语音）。
- 7. 输入指示器尽力发送；消息分块使用 `channels.discord.textChunkLimit`（默认 2000），并按行数拆分较长回复（`channels.discord.maxLinesPerMessage`，默认 17）。
- 8. 可选的按换行分块：设置 `channels.discord.chunkMode="newline"`，在按长度分块前先按空行（段落边界）拆分。
- 9. 支持文件上传，最大不超过配置的 `channels.discord.mediaMaxMb`（默认 8 MB）。
- Mention-gated guild replies by default to avoid noisy bots.
- 11. 当消息引用另一条消息时会注入回复上下文（引用内容 + ID）。
- 12. 原生回复线程**默认关闭**；通过 `channels.discord.replyToMode` 和回复标签启用。

## 13. 重试策略

14. 出站 Discord API 调用在遇到速率限制（429）时会重试；可用时使用 Discord 的 `retry_after`，并结合指数退避与抖动。 15. 通过 `channels.discord.retry` 进行配置。 See [Retry policy](/concepts/retry).

## 17. 配置

```json5
18. {
  channels: {
    discord: {
      enabled: true,
      token: "abc.123",
      groupPolicy: "allowlist",
      guilds: {
        "*": {
          channels: {
            general: { allow: true },
          },
        },
      },
      mediaMaxMb: 8,
      actions: {
        reactions: true,
        stickers: true,
        emojiUploads: true,
        stickerUploads: true,
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
        channels: true,
        voiceStatus: true,
        events: true,
        moderation: false,
        presence: false,
      },
      replyToMode: "off",
      dm: {
        enabled: true,
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["123456789012345678", "steipete"],
        groupEnabled: false,
        groupChannels: ["openclaw-dm"],
      },
      guilds: {
        "*": { requireMention: true },
        "123456789012345678": {
          slug: "friends-of-openclaw",
          requireMention: false,
          reactionNotifications: "own",
          users: ["987654321098765432", "steipete"],
          channels: {
            general: { allow: true },
            help: {
              allow: true,
              requireMention: true,
              users: ["987654321098765432"],
              skills: ["search", "docs"],
              systemPrompt: "Keep answers short.",
            },
          },
        },
      },
    },
  },
}
```

19. Ack 表情通过 `messages.ackReaction` + `messages.ackReactionScope` 进行全局控制。 20. 使用 `messages.removeAckAfterReply` 在机器人回复后清除 ack 表情。

- 21. `dm.enabled`：设置为 `false` 可忽略所有 DM（默认 `true`）。
- 22. `dm.policy`：DM 访问控制（推荐 `pairing`）。 23. `"open"` 需要设置 `dm.allowFrom=["*"]`。
- 24. `dm.allowFrom`：DM 白名单（用户 ID 或名称）。 25. 被 `dm.policy="allowlist"` 使用，并用于 `dm.policy="open"` 的校验。 26. 向导接受用户名，并在机器人可以搜索成员时将其解析为 ID。
- 27. `dm.groupEnabled`：启用群组 DM（默认 `false`）。
- `dm.groupChannels`: optional allowlist for group DM channel ids or slugs.
- 29. `groupPolicy`：控制服务器频道处理（`open|disabled|allowlist`）；`allowlist` 需要配置频道白名单。
- 30. `guilds`：按服务器配置规则，键为服务器 ID（推荐）或 slug。
- 31. `guilds."*"`：当不存在显式条目时应用的默认每服务器设置。
- 32. `guilds.<id>`33. `.slug`：可选的友好 slug，用于显示名称。
- 34. `guilds.<id>`35. `.users`：可选的每服务器用户白名单（ID 或名称）。
- 36. `guilds.<id>`37. `.tools`：可选的每服务器工具策略覆盖（`allow`/`deny`/`alsoAllow`），当缺少频道覆盖时使用。
- 38. `guilds.<id>`39. `.toolsBySender`：可选的按发送者的服务器级工具策略覆盖（当缺少频道覆盖时生效；支持 `"*"` 通配符）。
- `guilds.<id>41. `.channels.<channel>`42. `.allow`：当 `groupPolicy="allowlist"\` 时允许/禁止该频道。
- 43. `guilds.<id>`44. `.channels.<channel>`45. `.requireMention`：该频道的提及门控。
- 46. `guilds.<id>`47. `.channels.<channel>`48. `.tools`：可选的每频道工具策略覆盖（`allow`/`deny`/`alsoAllow`）。
- 49. `guilds.<id>`50. `.channels.<channel>`.toolsBySender`: optional per-sender tool policy overrides within the channel (`"\*"\` wildcard supported).
- `guilds.<id>.channels.<channel>.users`: optional per-channel user allowlist.
- `guilds.<id>.channels.<channel>.skills`: skill filter (omit = all skills, empty = none).
- `guilds.<id>.channels.<channel>.systemPrompt`: extra system prompt for the channel. Discord channel topics are injected as **untrusted** context (not system prompt).
- `guilds.<id>.channels.<channel>.enabled`: set `false` to disable the channel.
- `guilds.<id>.channels`: channel rules (keys are channel slugs or ids).
- `guilds.<id>.requireMention`: per-guild mention requirement (overridable per channel).
- `guilds.<id>.reactionNotifications`: reaction system event mode (`off`, `own`, `all`, `allowlist`).
- `textChunkLimit`: outbound text chunk size (chars). Default: 2000.
- `chunkMode`: `length` (default) splits only when exceeding `textChunkLimit`; `newline` splits on blank lines (paragraph boundaries) before length chunking.
- `maxLinesPerMessage`: soft max line count per message. Default: 17.
- `mediaMaxMb`: clamp inbound media saved to disk.
- `historyLimit`: number of recent guild messages to include as context when replying to a mention (default 20; falls back to `messages.groupChat.historyLimit`; `0` disables).
- `dmHistoryLimit`: DM history limit in user turns. Per-user overrides: `dms["<user_id>"].historyLimit`.
- `retry`: retry policy for outbound Discord API calls (attempts, minDelayMs, maxDelayMs, jitter).
- `pluralkit`: resolve PluralKit proxied messages so system members appear as distinct senders.
- `actions`: per-action tool gates; omit to allow all (set `false` to disable).
  - `reactions` (covers react + read reactions)
  - `stickers`, `emojiUploads`, `stickerUploads`, `polls`, `permissions`, `messages`, `threads`, `pins`, `search`
  - `memberInfo`, `roleInfo`, `channelInfo`, `voiceStatus`, `events`
  - `channels` (create/edit/delete channels + categories + permissions)
  - `roles` (role add/remove, default `false`)
  - `moderation` (timeout/kick/ban, default `false`)
  - `presence` (bot status/activity, default `false`)
- `execApprovals`: Discord-only exec approval DMs (button UI). Supports `enabled`, `approvers`, `agentFilter`, `sessionFilter`.

Reaction notifications use `guilds.<id>.reactionNotifications`:

- `off`: no reaction events.
- `own`: reactions on the bot's own messages (default).
- `all`: all reactions on all messages.
- `allowlist`: reactions from `guilds.<id>.users` on all messages (empty list disables).

### PluralKit (PK) support

Enable PK lookups so proxied messages resolve to the underlying system + member.
启用后，OpenClaw 会使用成员身份进行白名单匹配，并将发送者标记为 `Member (PK:System)`，以避免意外触发 Discord 提及。

```json5
{
  channels: {
    discord: {
      pluralkit: {
        enabled: true,
        token: "pk_live_...", // optional; required for private systems
      },
    },
  },
}
```

白名单备注（启用 PK）：

- 在 `dm.allowFrom`、`guilds.<id>` 中使用 `pk:<memberId>`.users`，或按频道配置的 `users\`。
- 成员显示名称也会按名称/slug 进行匹配。
- 查询使用的是 **原始** 的 Discord 消息 ID（代理前的消息），因此 PK API 只能在其 30 分钟窗口内解析。
- 如果 PK 查询失败（例如没有令牌的私有系统），代理消息将被视为机器人消息，并且除非 `channels.discord.allowBots=true`，否则会被丢弃。

### 工具操作默认值

| 操作组            | 默认       | 备注                                                   |
| -------------- | -------- | ---------------------------------------------------- |
| reactions      | enabled  | 反应 + 列出反应 + emojiList                                |
| stickers       | enabled  | 发送贴纸                                                 |
| emojiUploads   | enabled  | 上传表情                                                 |
| stickerUploads | enabled  | 上传贴纸                                                 |
| polls          | enabled  | 创建投票                                                 |
| permissions    | enabled  | 频道权限快照                                               |
| messages       | enabled  | 读取/发送/编辑/删除                                          |
| threads        | enabled  | 创建/列出/回复                                             |
| pins           | enabled  | 置顶/取消置顶/列表                                           |
| search         | enabled  | 消息搜索（预览功能）                                           |
| memberInfo     | enabled  | 成员信息                                                 |
| roleInfo       | enabled  | 角色列表                                                 |
| channelInfo    | enabled  | Channel info + list                                  |
| channels       | enabled  | Channel/category management                          |
| voiceStatus    | enabled  | Voice state lookup                                   |
| events         | enabled  | List/create scheduled events                         |
| roles          | disabled | Role add/remove                                      |
| moderation     | disabled | Timeout/kick/ban                                     |
| presence       | disabled | Bot status/activity (setPresence) |

- `replyToMode`: `off` (default), `first`, or `all`. Applies only when the model includes a reply tag.

## Reply tags

To request a threaded reply, the model can include one tag in its output:

- `[[reply_to_current]]` — reply to the triggering Discord message.
- `[[reply_to:<id>]]` — reply to a specific message id from context/history.
  Current message ids are appended to prompts as `[message_id: …]`; history entries already include ids.

Behavior is controlled by `channels.discord.replyToMode`:

- `off`: ignore tags.
- `first`: only the first outbound chunk/attachment is a reply.
- `all`: every outbound chunk/attachment is a reply.

Allowlist matching notes:

- `allowFrom`/`users`/`groupChannels` accept ids, names, tags, or mentions like `<@id>`.
- Prefixes like `discord:`/`user:` (users) and `channel:` (group DMs) are supported.
- Use `*` to allow any sender/channel.
- When `guilds.<id>.channels` is present, channels not listed are denied by default.
- When `guilds.<id>.channels` is omitted, all channels in the allowlisted guild are allowed.
- To allow **no channels**, set `channels.discord.groupPolicy: "disabled"` (or keep an empty allowlist).
- The configure wizard accepts `Guild/Channel` names (public + private) and resolves them to IDs when possible.
- On startup, OpenClaw resolves channel/user names in allowlists to IDs (when the bot can search members)
  and logs the mapping; unresolved entries are kept as typed.

Native command notes:

- The registered commands mirror OpenClaw’s chat commands.
- Native commands honor the same allowlists as DMs/guild messages (`channels.discord.dm.allowFrom`, `channels.discord.guilds`, per-channel rules).
- Slash commands may still be visible in Discord UI to users who aren’t allowlisted; OpenClaw enforces allowlists on execution and replies “not authorized”.

## Tool actions

The agent can call `discord` with actions like:

- `react` / `reactions` (add or list reactions)
- `sticker`, `poll`, `permissions`
- `readMessages`, `sendMessage`, `editMessage`, `deleteMessage`
- 读取/搜索/置顶工具的载荷包含规范化的 `timestampMs`（UTC 纪元毫秒）和 `timestampUtc`，并保留原始的 Discord `timestamp`。
- `threadCreate`、`threadList`、`threadReply`
- `pinMessage`、`unpinMessage`、`listPins`
- `searchMessages`、`memberInfo`、`roleInfo`、`roleAdd`、`roleRemove`、`emojiList`
- `channelInfo`、`channelList`、`voiceStatus`、`eventList`、`eventCreate`
- `timeout`、`kick`、`ban`
- `setPresence`（机器人活动和在线状态）

Discord 消息 ID 会在注入的上下文中展示（`[discord message id: …]` 以及历史行），以便代理可以精确定位它们。
表情符号可以是 Unicode（例如 `✅`），也可以是自定义表情语法，如 `<:party_blob:1234567890>`。

## 安全与运维

- 将机器人令牌视为密码；在受管主机上优先使用 `DISCORD_BOT_TOKEN` 环境变量，或锁定配置文件权限。
- 只授予机器人所需的权限（通常是读取/发送消息）。
- 如果机器人卡住或被限流，在确认没有其他进程占用 Discord 会话后，重启网关（`openclaw gateway --force`）。
