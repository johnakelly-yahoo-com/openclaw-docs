---
summary: "WhatsApp（Web 渠道）集成：登录、收件箱、回复、媒体和运维"
read_when:
  - 正在处理 WhatsApp/Web 渠道行为或收件箱路由
title: "WhatsApp"
---

# WhatsApp（Web 渠道）

状态：仅通过 Baileys 使用 WhatsApp Web。 网关拥有会话。

## 快速设置（新手）

1. 如有可能，使用**单独的电话号码**（推荐）。
2. 在 `~/.openclaw/openclaw.json` 中配置 WhatsApp。
3. 运行 `openclaw channels login` 扫描二维码（已链接的设备）。
4. 启动网关。

最小配置：

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551234567"],
    },
  },
}
```

## 目标

- 在一个 Gateway 进程中支持多个 WhatsApp 账号（多账号）。
- 确定性路由：回复返回到 WhatsApp，不进行模型路由。
- 模型能够看到足够的上下文以理解被引用的回复。

## 1. 配置写入

2. 默认情况下，WhatsApp 允许通过 `/config set|unset` 触发的配置更新写入（需要 `commands.config: true`）。

3. 可通过以下方式禁用：

```json5
4. {
  channels: { whatsapp: { configWrites: false } },
}
```

## 5. 架构（谁负责什么）

- 6. **Gateway** 拥有 Baileys socket 和收件循环。
- 7. **CLI / macOS 应用** 与 gateway 通信；不直接使用 Baileys。
- 8. **主动监听器** 是进行外发消息所必需的；否则发送会快速失败。

## 9. 获取手机号（两种模式）

10. WhatsApp 需要一个真实的手机号码进行验证。 11. VoIP 和虚拟号码通常会被封锁。 12. 在 WhatsApp 上运行 OpenClaw 有两种受支持的方式：

### 13. 专用号码（推荐）

14. 为 OpenClaw 使用一个**独立的手机号码**。 15. 最佳用户体验、清晰的路由、没有自聊怪癖。 16. 理想配置：**备用/旧 Android 手机 + eSIM**。 17. 保持连接 Wi‑Fi 和电源，并通过二维码进行关联。

18. **WhatsApp Business：** 你可以在同一设备上使用不同号码的 WhatsApp Business。 19. 非常适合将个人 WhatsApp 与之分离——安装 WhatsApp Business 并在那里注册 OpenClaw 的号码。

20. **示例配置（专用号码，单用户白名单）：**

```json5
21. {
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551234567"],
    },
  },
}
```

22. **配对模式（可选）：**
    如果你想使用配对而不是白名单，将 `channels.whatsapp.dmPolicy` 设置为 `pairing`。 23. 未知发送者会收到一个配对码；通过以下命令批准：
    `openclaw pairing approve whatsapp <code>`

### 24. 个人号码（备用）

25. 快速备用方案：在**你自己的号码**上运行 OpenClaw。 26. 为了测试，请给自己发消息（WhatsApp“给自己发消息”），这样不会骚扰联系人。 27. 在设置和实验过程中，预计需要在你的主手机上读取验证码。 28. **必须启用自聊模式。**
    当向导询问你的个人 WhatsApp 号码时，输入你将用来发消息的手机（所有者/发送者），而不是助手号码。

29. **示例配置（个人号码，自聊）：**

```json
30. {
  "whatsapp": {
    "selfChatMode": true,
    "dmPolicy": "allowlist",
    "allowFrom": ["+15551234567"]
  }
}
```

31. 如果 `messages.responsePrefix` 未设置，自聊回复在设置了 `identity.name` 时默认使用 `[{identity.name}]`（否则为 `[openclaw]`）。 32. 显式设置它以自定义或禁用
    该前缀（使用 `""` 将其移除）。

### 33. 号码来源建议

- 34. 来自你所在国家/地区移动运营商的**本地 eSIM**（最可靠）
  - 35. 奥地利：[hot.at](https://www.hot.at)
  - 36. 英国：[giffgaff](https://www.giffgaff.com) — 免费 SIM，无合约
- 37. **预付费 SIM** —— 便宜，只需要接收一条用于验证的短信

38. **避免：** TextNow、Google Voice、大多数“免费短信”服务——WhatsApp 会对这些进行严格封锁。

39. **提示：** 该号码只需要接收一次验证短信。 40. 之后，WhatsApp Web 会话会通过 `creds.json` 持续存在。

## 41. 为什么不用 Twilio？

- 42. 早期的 OpenClaw 版本支持 Twilio 的 WhatsApp Business 集成。
- 43. WhatsApp Business 号码并不适合作为个人助理。
- 44. Meta 强制执行 24 小时回复窗口；如果你在过去 24 小时内没有回复，业务号码将无法主动发起新消息。
- 45. 高容量或“高频聊天”的使用会触发激进的封锁，因为业务账号并非用于发送数十条个人助理消息。
- 46. 结果：投递不可靠且频繁被封锁，因此移除了相关支持。

## 47. 登录与凭据

- 48. 登录命令：`openclaw channels login`（通过“已关联设备”显示二维码）。
- 49. 多账号登录：`openclaw channels login --account <id>`（`<id>` = `accountId`）。
- 50. 默认账号（省略 `--account` 时）：如果存在则为 `default`，否则为第一个已配置的账号 ID（按排序）。
- Credentials stored in `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`.
- Backup copy at `creds.json.bak` (restored on corruption).
- Legacy compatibility: older installs stored Baileys files directly in `~/.openclaw/credentials/`.
- Logout: `openclaw channels logout` (or `--account <id>`) deletes WhatsApp auth state (but keeps shared `oauth.json`).
- Logged-out socket => error instructs re-link.

## Inbound flow (DM + group)

- WhatsApp events come from `messages.upsert` (Baileys).
- Inbox listeners are detached on shutdown to avoid accumulating event handlers in tests/restarts.
- Status/broadcast chats are ignored.
- Direct chats use E.164; groups use group JID.
- **DM policy**: `channels.whatsapp.dmPolicy` controls direct chat access (default: `pairing`).
  - Pairing: unknown senders get a pairing code (approve via `openclaw pairing approve whatsapp <code>`; codes expire after 1 hour).
  - Open: requires `channels.whatsapp.allowFrom` to include `"*"`.
  - 25. 你已关联的 WhatsApp 号码会被隐式信任，因此给自己发送的消息会跳过 `channels.whatsapp.dmPolicy` 和 `channels.whatsapp.allowFrom` 检查。

### Personal-number mode (fallback)

If you run OpenClaw on your **personal WhatsApp number**, enable `channels.whatsapp.selfChatMode` (see sample above).

Behavior:

- Outbound DMs never trigger pairing replies (prevents spamming contacts).
- Inbound unknown senders still follow `channels.whatsapp.dmPolicy`.
- 26. 自聊模式（allowFrom 包含你的号码）会避免自动已读回执，并忽略提及 JID。
- Read receipts sent for non-self-chat DMs.

## 27. 已读回执

By default, the gateway marks inbound WhatsApp messages as read (blue ticks) once they are accepted.

Disable globally:

```json5
{
  channels: { whatsapp: { sendReadReceipts: false } },
}
```

Disable per account:

```json5
{
  channels: {
    whatsapp: {
      accounts: {
        personal: { sendReadReceipts: false },
      },
    },
  },
}
```

Notes:

- Self-chat mode always skips read receipts.

## WhatsApp FAQ: sending messages + pairing

**Will OpenClaw message random contacts when I link WhatsApp?**  
No. Default DM policy is **pairing**, so unknown senders only get a pairing code and their message is **not processed**. OpenClaw only replies to chats it receives, or to sends you explicitly trigger (agent/CLI).

**How does pairing work on WhatsApp?**  
Pairing is a DM gate for unknown senders:

- First DM from a new sender returns a short code (message is not processed).
- Approve with: `openclaw pairing approve whatsapp <code>` (list with `openclaw pairing list whatsapp`).
- Codes expire after 1 hour; pending requests are capped at 3 per channel.

**Can multiple people use different OpenClaw instances on one WhatsApp number?**  
Yes, by routing each sender to a different agent via `bindings` (peer `kind: "direct"`, sender E.164 like `+15551234567`). Replies still come from the **same WhatsApp account**, and direct chats collapse to each agent's main session, so use **one agent per person**. DM access control (`dmPolicy`/`allowFrom`) is global per WhatsApp account. See [Multi-Agent Routing](/concepts/multi-agent).

**Why do you ask for my phone number in the wizard?**  
The wizard uses it to set your **allowlist/owner** so your own DMs are permitted. It’s not used for auto-sending. If you run on your personal WhatsApp number, use that same number and enable `channels.whatsapp.selfChatMode`.

## Message normalization (what the model sees)

- `Body` is the current message body with envelope.

- Quoted reply context is **always appended**:

  ```
  [Replying to +1555 id:ABC123]
  <quoted text or <media:...>>
  [/Replying]
  ```

- Reply metadata also set:
  - `ReplyToId` = stanzaId
  - `ReplyToBody` = quoted body or media placeholder
  - `ReplyToSender` = E.164 when known

- Media-only inbound messages use placeholders:
  - `<media:image|video|audio|document|sticker>`

## Groups

- Groups map to `agent:<agentId>:whatsapp:group:<jid>` sessions.
- Group policy: `channels.whatsapp.groupPolicy = open|disabled|allowlist` (default `allowlist`).
- Activation modes:
  - `mention` (default): requires @mention or regex match.
  - `always`: always triggers.
- `/activation mention|always` is owner-only and must be sent as a standalone message.
- Owner = `channels.whatsapp.allowFrom` (or self E.164 if unset).
- **History injection** (pending-only):
  - Recent _unprocessed_ messages (default 50) inserted under:
    `[Chat messages since your last reply - for context]` (messages already in the session are not re-injected)
  - Current message under:
    `[Current message - respond to this]`
  - 28. 追加发送者后缀：`[from: Name (+E164)]`
- Group metadata cached 5 min (subject + participants).

## Reply delivery (threading)

- WhatsApp Web sends standard messages (no quoted reply threading in the current gateway).
- 29. 在此频道中会忽略回复标签。

## Acknowledgment reactions (auto-react on receipt)

WhatsApp can automatically send emoji reactions to incoming messages immediately upon receipt, before the bot generates a reply. This provides instant feedback to users that their message was received.

**Configuration:**

```json
30. {
  "whatsapp": {
    "ackReaction": {
      "emoji": "👀",
      "direct": true,
      "group": "mentions"
    }
  }
}
```

**Options:**

- `emoji` (string): Emoji to use for acknowledgment (e.g., "👀", "✅", "📨"). Empty or omitted = feature disabled.
- `direct` (boolean, default: `true`): Send reactions in direct/DM chats.
- `group` (string, default: `"mentions"`): Group chat behavior:
  - `"always"`: React to all group messages (even without @mention)
  - `"mentions"`: React only when bot is @mentioned
  - `"never"`: Never react in groups

**Per-account override:**

```json
{
  "whatsapp": {
    "accounts": {
      "work": {
        "ackReaction": {
          "emoji": "✅",
          "direct": false,
          "group": "always"
        }
      }
    }
  }
}
```

**Behavior notes:**

- Reactions are sent **immediately** upon message receipt, before typing indicators or bot replies.
- In groups with `requireMention: false` (activation: always), `group: "mentions"` will react to all messages (not just @mentions).
- Fire-and-forget: reaction failures are logged but don't prevent the bot from replying.
- Participant JID is automatically included for group reactions.
- WhatsApp ignores `messages.ackReaction`; use `channels.whatsapp.ackReaction` instead.

## Agent tool (reactions)

- Tool: `whatsapp` with `react` action (`chatJid`, `messageId`, `emoji`, optional `remove`).
- Optional: `participant` (group sender), `fromMe` (reacting to your own message), `accountId` (multi-account).
- Reaction removal semantics: see [/tools/reactions](/tools/reactions).
- Tool gating: `channels.whatsapp.actions.reactions` (default: enabled).

## Limits

- Outbound text is chunked to `channels.whatsapp.textChunkLimit` (default 4000).
- Optional newline chunking: set `channels.whatsapp.chunkMode="newline"` to split on blank lines (paragraph boundaries) before length chunking.
- Inbound media saves are capped by `channels.whatsapp.mediaMaxMb` (default 50 MB).
- Outbound media items are capped by `agents.defaults.mediaMaxMb` (default 5 MB).

## Outbound send (text + media)

- Uses active web listener; error if gateway not running.
- 32. 文本分块：每条消息最多 4k（可通过 `channels.whatsapp.textChunkLimit` 配置，可选 `channels.whatsapp.chunkMode`）。
- Media:
  - Image/video/audio/document supported.
  - Audio sent as PTT; `audio/ogg` => `audio/ogg; codecs=opus`.
  - Caption only on first media item.
  - Media fetch supports HTTP(S) and local paths.
  - Animated GIFs: WhatsApp expects MP4 with `gifPlayback: true` for inline looping.
    - CLI: `openclaw message send --media <mp4> --gif-playback`
    - Gateway: `send` params include `gifPlayback: true`

## Voice notes (PTT audio)

WhatsApp sends audio as **voice notes** (PTT bubble).

- Best results: OGG/Opus. OpenClaw rewrites `audio/ogg` to `audio/ogg; codecs=opus`.
- `[[audio_as_voice]]` is ignored for WhatsApp (audio already ships as voice note).

## 33. 媒体限制 + 优化

- Default outbound cap: 5 MB (per media item).
- Override: `agents.defaults.mediaMaxMb`.
- Images are auto-optimized to JPEG under cap (resize + quality sweep).
- Oversize media => error; media reply falls back to text warning.

## Heartbeats

- **Gateway heartbeat** logs connection health (`web.heartbeatSeconds`, default 60s).
- **Agent heartbeat** can be configured per agent (`agents.list[].heartbeat`) or globally
  via `agents.defaults.heartbeat` (fallback when no per-agent entries are set).
  - Uses the configured heartbeat prompt (default: `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`) + `HEARTBEAT_OK` skip behavior.
  - Delivery defaults to the last used channel (or configured target).

## Reconnect behavior

- Backoff policy: `web.reconnect`:
  - `initialMs`, `maxMs`, `factor`, `jitter`, `maxAttempts`.
- If maxAttempts reached, web monitoring stops (degraded).
- Logged-out => stop and require re-link.

## Config quick map

- `channels.whatsapp.dmPolicy` (DM policy: pairing/allowlist/open/disabled).
- `channels.whatsapp.selfChatMode` (same-phone setup; bot uses your personal WhatsApp number).
- `channels.whatsapp.allowFrom` (DM allowlist). WhatsApp uses E.164 phone numbers (no usernames).
- `channels.whatsapp.mediaMaxMb` (inbound media save cap).
- `channels.whatsapp.ackReaction` (auto-reaction on message receipt: `{emoji, direct, group}`).
- `channels.whatsapp.accounts.<accountId>.*` (per-account settings + optional `authDir`).
- `channels.whatsapp.accounts.<accountId>.mediaMaxMb` (per-account inbound media cap).
- `channels.whatsapp.accounts.<accountId>.ackReaction` (per-account ack reaction override).
- `channels.whatsapp.groupAllowFrom` (group sender allowlist).
- `channels.whatsapp.groupPolicy` (group policy).
- `channels.whatsapp.historyLimit` / `channels.whatsapp.accounts.<accountId>.historyLimit` (group history context; `0` disables).
- `channels.whatsapp.dmHistoryLimit` (DM history limit in user turns). Per-user overrides: `channels.whatsapp.dms["<phone>"].historyLimit`.
- `channels.whatsapp.groups` (group allowlist + mention gating defaults; use `"*"` to allow all)
- `channels.whatsapp.actions.reactions` (gate WhatsApp tool reactions).
- `agents.list[].groupChat.mentionPatterns` (or `messages.groupChat.mentionPatterns`)
- `messages.groupChat.historyLimit`
- `channels.whatsapp.messagePrefix` (inbound prefix; per-account: `channels.whatsapp.accounts.<accountId>.messagePrefix`; deprecated: `messages.messagePrefix`)
- `messages.responsePrefix` (outbound prefix)
- `agents.defaults.mediaMaxMb`
- `agents.defaults.heartbeat.every`
- `agents.defaults.heartbeat.model` (optional override)
- `agents.defaults.heartbeat.target`
- `agents.defaults.heartbeat.to`
- `agents.defaults.heartbeat.session`
- `agents.list[].heartbeat.*` (per-agent overrides)
- `session.*` (scope, idle, store, mainKey)
- `web.enabled` (disable channel startup when false)
- `web.heartbeatSeconds`
- `web.reconnect.*`

## Logs + troubleshooting

- Subsystems: `whatsapp/inbound`, `whatsapp/outbound`, `web-heartbeat`, `web-reconnect`.
- Log file: `/tmp/openclaw/openclaw-YYYY-MM-DD.log` (configurable).
- Troubleshooting guide: [Gateway troubleshooting](/gateway/troubleshooting).

## Troubleshooting (quick)

**Not linked / QR login required**

- Symptom: `channels status` shows `linked: false` or warns “Not linked”.
- Fix: run `openclaw channels login` on the gateway host and scan the QR (WhatsApp → Settings → Linked Devices).

**Linked but disconnected / reconnect loop**

- Symptom: `channels status` shows `running, disconnected` or warns “Linked but disconnected”.
- Fix: `openclaw doctor` (or restart the gateway). If it persists, relink via `channels login` and inspect `openclaw logs --follow`.

**Bun runtime**

- Bun is **not recommended**. WhatsApp (Baileys) and Telegram are unreliable on Bun.
  Run the gateway with **Node**. (See Getting Started runtime note.)
