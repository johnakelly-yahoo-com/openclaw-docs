---
summary: "50. 聊天的会话管理规则、键和值持久化"
read_when:
  - Modifying session handling or storage
title: "Session Management"
---

# Session Management

OpenClaw treats **one direct-chat session per agent** as primary. Direct chats collapse to `agent:<agentId>:<mainKey>` (default `main`), while group/channel chats get their own keys. `session.mainKey` is honored.

Use `session.dmScope` to control how **direct messages** are grouped:

- `main` (default): all DMs share the main session for continuity.
- `per-peer`: isolate by sender id across channels.
- `per-channel-peer`: isolate by channel + sender (recommended for multi-user inboxes).
- `per-account-channel-peer`: isolate by account + channel + sender (recommended for multi-account inboxes).
  Use `session.identityLinks` to map provider-prefixed peer ids to a canonical identity so the same person shares a DM session across channels when using `per-peer`, `per-channel-peer`, or `per-account-channel-peer`.

## Secure DM mode (recommended for multi-user setups)

> **Security Warning:** If your agent can receive DMs from **multiple people**, you should strongly consider enabling secure DM mode. Without it, all users share the same conversation context, which can leak private information between users.

**Example of the problem with default settings:**

- Alice (`<SENDER_A>`) messages your agent about a private topic (for example, a medical appointment)
- Bob (`<SENDER_B>`) messages your agent asking "What were we talking about?"
- Because both DMs share the same session, the model may answer Bob using Alice's prior context.

**The fix:** Set `dmScope` to isolate sessions per user:

```json5
// ~/.openclaw/openclaw.json
{
  session: {
    // Secure DM mode: isolate DM context per channel + sender.
    dmScope: "per-channel-peer",
  },
}
```

**When to enable this:**

- You have pairing approvals for more than one sender
- You use a DM allowlist with multiple entries
- You set `dmPolicy: "open"`
- Multiple phone numbers or accounts can message your agent

Notes:

- Default is `dmScope: "main"` for continuity (all DMs share the main session). This is fine for single-user setups.
- For multi-account inboxes on the same channel, prefer `per-account-channel-peer`.
- If the same person contacts you on multiple channels, use `session.identityLinks` to collapse their DM sessions into one canonical identity.
- You can verify your DM settings with `openclaw security audit` (see [security](/cli/security)).

## Gateway is the source of truth

All session state is **owned by the gateway** (the “master” OpenClaw). UI clients (macOS app, WebChat, etc.) must query the gateway for session lists and token counts instead of reading local files.

- In **remote mode**, the session store you care about lives on the remote gateway host, not your Mac.
- Token counts shown in UIs come from the gateway’s store fields (`inputTokens`, `outputTokens`, `totalTokens`, `contextTokens`). Clients do not parse JSONL transcripts to “fix up” totals.

## Where state lives

- On the **gateway host**:
  - Store file: `~/.openclaw/agents/<agentId>/sessions/sessions.json` (per agent).
- Transcripts: `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl` (Telegram topic sessions use `.../<SessionId>-topic-<threadId>.jsonl`).
- The store is a map `sessionKey -> { sessionId, updatedAt, ... }`. Deleting entries is safe; they are recreated on demand.
- Group entries may include `displayName`, `channel`, `subject`, `room`, and `space` to label sessions in UIs.
- Session entries include `origin` metadata (label + routing hints) so UIs can explain where a session came from.
- OpenClaw does **not** read legacy Pi/Tau session folders.

## Session pruning

OpenClaw 默认会在调用 LLM 之前，从内存上下文中裁剪**旧的工具结果**。
这**不会**重写 JSONL 历史记录。 参见 [/concepts/session-pruning](/concepts/session-pruning)。

## 预压缩内存刷新

当会话接近自动压缩时，OpenClaw 可以运行一次**静默内存刷新**轮次，提醒模型将持久化笔记写入磁盘。 这仅在工作区可写时运行。 参见 [Memory](/concepts/memory) 和
[Compaction](/concepts/compaction)。

## 传输映射 → 会话键

- 私聊遵循 `session.dmScope`（默认 `main`）。
  - `main`: `agent:<agentId>:<mainKey>`（跨设备/渠道的连续性）。
    - 多个电话号码和渠道可以映射到同一个 agent 主键；它们作为传输入口汇入同一段对话。
  - `per-peer`: `agent:<agentId>:dm:<peerId>`。
  - `per-channel-peer`: `agent:<agentId>:<channel>:dm:<peerId>`。
  - `per-account-channel-peer`: `agent:<agentId>:<channel>:<accountId>:dm:<peerId>`（accountId 默认为 `default`）。
  - 如果 `session.identityLinks` 匹配到带提供方前缀的 peer id（例如 `telegram:123`），则使用规范化键替换 `<peerId>`，从而使同一人在不同渠道间共享一个会话。
- 群聊会隔离状态：`agent:<agentId>:<channel>:group:<id>`（房间/频道使用 `agent:<agentId>:<channel>:channel:<id>`）。
  - Telegram 论坛主题会将 `:topic:<threadId>` 追加到群组 id 以实现隔离。
  - 仍然识别旧版的 `group:<id>` 键以用于迁移。
- 入站上下文仍可能使用 `group:<id>`；渠道将从 `Provider` 推断，并规范化为 `agent:<agentId>:<channel>:group:<id>` 形式。
- 其他来源：
  - Cron 作业：`cron:<job.id>`
  - Webhook：`hook:<uuid>`（除非由 hook 明确设置）
  - Node 运行：`node-<nodeId>`

## 生命周期

- 重置策略：会话在过期前会被复用，过期在下一条入站消息时评估。
- 每日重置：默认是**网关主机本地时间的凌晨 4:00**。 当会话的最后更新时间早于最近一次每日重置时间时，该会话即为陈旧。
- 空闲重置（可选）：`idleMinutes` 增加一个滑动的空闲窗口。 当同时配置了每日重置和空闲重置时，**先到期的那个**会强制创建新会话。
- 旧版仅空闲模式：如果你只设置了 `session.idleMinutes`，而未配置任何 `session.reset`/`resetByType`，OpenClaw 将为向后兼容而保持仅空闲模式。
- Per-type overrides (optional): `resetByType` lets you override the policy for `direct`, `group`, and `thread` sessions (thread = Slack/Discord threads, Telegram topics, Matrix threads when provided by the connector).
- 按渠道覆盖（可选）：`resetByChannel` 会覆盖某个渠道的重置策略（适用于该渠道的所有会话类型，并优先于 `reset`/`resetByType`）。
- 重置触发器：精确的 `/new` 或 `/reset`（以及 `resetTriggers` 中的任何额外项）会启动一个全新的会话 id，并将消息剩余部分继续传递。 `/new <model>` 接受模型别名、`provider/model`，或提供方名称（模糊匹配）以设置新会话的模型。 如果仅发送 `/new` 或 `/reset`，OpenClaw 会运行一次简短的“hello”问候轮次以确认重置。
- 手动重置：从存储中删除特定键或移除 JSONL 转录；下一条消息会重新创建它们。
- 隔离的 cron 作业每次运行都会生成一个全新的 `sessionId`（不进行空闲复用）。

## 发送策略（可选）

在不列出具体 id 的情况下，阻止特定会话类型的投递。

```json5
{
  session: {
    sendPolicy: {
      rules: [
        { action: "deny", match: { channel: "discord", chatType: "group" } },
        { action: "deny", match: { keyPrefix: "cron:" } },
      ],
      default: "allow",
    },
  },
}
```

运行时覆盖（仅限所有者）：

- `/send on` → 允许此会话
- `/send off` → 禁止此会话
- `/send inherit` → 清除覆盖并使用配置规则
  请将这些作为独立消息发送，以便其生效。

## 配置（可选重命名示例）

```json5
// ~/.openclaw/openclaw.json
{
  session: {
    scope: "per-sender", // keep group keys separate
    dmScope: "main", // DM continuity (set per-channel-peer/per-account-channel-peer for shared inboxes)
    identityLinks: {
      alice: ["telegram:123456789", "discord:987654321012345678"],
    },
    reset: {
      // Defaults: mode=daily, atHour=4 (gateway host local time).
      // If you also set idleMinutes, whichever expires first wins.
      mode: "daily",
      atHour: 4,
      idleMinutes: 120,
    },
    resetByType: {
      thread: { mode: "daily", atHour: 4 },
      direct: { mode: "idle", idleMinutes: 240 },
      group: { mode: "idle", idleMinutes: 120 },
    },
    resetByChannel: {
      discord: { mode: "idle", idleMinutes: 10080 },
    },
    resetTriggers: ["/new", "/reset"],
    store: "~/.openclaw/agents/{agentId}/sessions/sessions.json",
    mainKey: "main",
  },
}
```

## 26. 检查

- `openclaw status` — 显示存储路径和最近的会话。
- `openclaw sessions --json` — 导出所有条目（可使用 `--active <minutes>` 进行过滤）。
- `openclaw gateway call sessions.list --params '{}'` — 从正在运行的网关获取会话（远程网关访问请使用 `--url`/`--token`）。
- 在聊天中发送 `/status` 作为独立消息，以查看代理是否可达、已使用的会话上下文比例、当前 thinking/verbose 开关，以及你的 WhatsApp Web 凭据上次刷新时间（有助于发现需要重新关联的情况）。
- 发送 `/context list` 或 `/context detail` 以查看系统提示和注入的工作区文件中包含的内容（以及最大的上下文贡献者）。
- Send `/stop` as a standalone message to abort the current run, clear queued followups for that session, and stop any sub-agent runs spawned from it (the reply includes the stopped count).
- Send `/compact` (optional instructions) as a standalone message to summarize older context and free up window space. See [/concepts/compaction](/concepts/compaction).
- JSONL transcripts can be opened directly to review full turns.

## Tips

- Keep the primary key dedicated to 1:1 traffic; let groups keep their own keys.
- 27. 在自动化清理时，删除单个键而不是整个存储，以便在其他地方保留上下文。

## Session origin metadata

Each session entry records where it came from (best-effort) in `origin`:

- `label`: human label (resolved from conversation label + group subject/channel)
- `provider`: normalized channel id (including extensions)
- `from`/`to`: raw routing ids from the inbound envelope
- 29. `accountId`：提供商账户 ID（多账户时）
- 30. `threadId`：当频道支持时的线程/主题 ID
      原始字段会为私信、频道和群组填充。 If a
      connector only updates delivery routing (for example, to keep a DM main session
      fresh), it should still provide inbound context so the session keeps its
      explainer metadata. Extensions can do this by sending `ConversationLabel`,
      `GroupSubject`, `GroupChannel`, `GroupSpace`, and `SenderName` in the inbound
      context and calling `recordSessionMetaFromInbound` (or passing the same context
      to `updateLastRoute`).
