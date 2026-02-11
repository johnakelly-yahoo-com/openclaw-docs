---
summary: "10. 深入解析：会话存储与转录、生命周期，以及（自动）压缩的内部机制"
read_when:
  - 11. 你需要调试会话 ID、转录 JSONL，或 sessions.json 字段
  - 12. 你正在更改自动压缩行为，或添加“压缩前”的整理工作
  - 13. 你想实现内存刷新或静默的系统轮次
title: "14. 会话管理深度解析"
---

# 15. 会话管理与压缩（深度解析）

16. 本文档解释了 OpenClaw 如何端到端地管理会话：

- 17. **会话路由**（入站消息如何映射到 `sessionKey`）
- 18. **会话存储**（`sessions.json`）及其跟踪内容
- 19. **转录持久化**（`*.jsonl`）及其结构
- 20. **转录卫生**（运行前的提供方特定修复）
- 21. **上下文限制**（上下文窗口 vs 已跟踪的 token）
- 22. **压缩**（手动 + 自动压缩）以及在何处挂接压缩前工作
- **Silent housekeeping** (e.g. memory writes that shouldn’t produce user-visible output)

24. 如果你想先了解更高层级的概览，请从以下内容开始：

- 25. [/concepts/session](/concepts/session)
- [/concepts/compaction](/concepts/compaction)
- 27. [/concepts/session-pruning](/concepts/session-pruning)
- 28. [/reference/transcript-hygiene](/reference/transcript-hygiene)

---

## 29. 唯一事实来源：Gateway

30. OpenClaw 的设计以单一的 **Gateway 进程** 为中心，用于拥有会话状态。

- 31. UI（macOS 应用、Web 控制 UI、TUI）应向 Gateway 查询会话列表和 token 计数。
- 32. 在远程模式下，会话文件位于远程主机；“检查你本地 Mac 的文件”并不能反映 Gateway 实际使用的内容。

---

## 33. 两层持久化

34. OpenClaw 通过两层进行会话持久化：

1. 35. **会话存储（`sessions.json`）**
   - 36. 键/值映射：`sessionKey -> SessionEntry`
   - 37. 体量小、可变，且可安全编辑（或删除条目）
   - 38. 跟踪会话元数据（当前会话 ID、最近活动、开关、token 计数器等）

2. 39. **转录（`<sessionId>.jsonl`）**
   - 40. 仅追加的转录，具有树状结构（条目包含 `id` + `parentId`）
   - 41. 存储实际对话、工具调用以及压缩摘要
   - 42. 用于为后续轮次重建模型上下文

---

## 43. 磁盘上的位置

44. 在 Gateway 主机上，按代理划分：

- 45. 存储：`~/.openclaw/agents/<agentId>/sessions/sessions.json`
- 46. 转录：`~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl`
  - 47. Telegram 主题会话：`.../<sessionId>-topic-<threadId>.jsonl`

48. OpenClaw 通过 `src/config/sessions.ts` 解析这些路径。

---

## 49. 会话键（`sessionKey`）

50. `sessionKey` 用于标识你所在的_对话桶_（路由 + 隔离）。

Common patterns:

- Main/direct chat (per agent): `agent:<agentId>:<mainKey>` (default `main`)
- Group: `agent:<agentId>:<channel>:group:<id>`
- Room/channel (Discord/Slack): `agent:<agentId>:<channel>:channel:<id>` or `...:room:<id>`
- Cron: `cron:<job.id>`
- Webhook: `hook:<uuid>` (unless overridden)

The canonical rules are documented at [/concepts/session](/concepts/session).

---

## Session ids (`sessionId`)

Each `sessionKey` points at a current `sessionId` (the transcript file that continues the conversation).

Rules of thumb:

- **Reset** (`/new`, `/reset`) creates a new `sessionId` for that `sessionKey`.
- **Daily reset** (default 4:00 AM local time on the gateway host) creates a new `sessionId` on the next message after the reset boundary.
- **Idle expiry** (`session.reset.idleMinutes` or legacy `session.idleMinutes`) creates a new `sessionId` when a message arrives after the idle window. When daily + idle are both configured, whichever expires first wins.

Implementation detail: the decision happens in `initSessionState()` in `src/auto-reply/reply/session.ts`.

---

## Session store schema (`sessions.json`)

The store’s value type is `SessionEntry` in `src/config/sessions.ts`.

Key fields (not exhaustive):

- `sessionId`: current transcript id (filename is derived from this unless `sessionFile` is set)
- `updatedAt`: last activity timestamp
- `sessionFile`: optional explicit transcript path override
- `chatType`: `direct | group | room` (helps UIs and send policy)
- `provider`, `subject`, `room`, `space`, `displayName`: metadata for group/channel labeling
- Toggles:
  - `thinkingLevel`, `verboseLevel`, `reasoningLevel`, `elevatedLevel`
  - `sendPolicy` (per-session override)
- Model selection:
  - `providerOverride`, `modelOverride`, `authProfileOverride`
- Token counters (best-effort / provider-dependent):
  - `inputTokens`, `outputTokens`, `totalTokens`, `contextTokens`
- `compactionCount`: how often auto-compaction completed for this session key
- `memoryFlushAt`: timestamp for the last pre-compaction memory flush
- `memoryFlushCompactionCount`: compaction count when the last flush ran

The store is safe to edit, but the Gateway is the authority: it may rewrite or rehydrate entries as sessions run.

---

## Transcript structure (`*.jsonl`)

Transcripts are managed by `@mariozechner/pi-coding-agent`’s `SessionManager`.

The file is JSONL:

- First line: session header (`type: "session"`, includes `id`, `cwd`, `timestamp`, optional `parentSession`)
- Then: session entries with `id` + `parentId` (tree)

Notable entry types:

- `message`: user/assistant/toolResult messages
- `custom_message`: extension-injected messages that _do_ enter model context (can be hidden from UI)
- `custom`: extension state that does _not_ enter model context
- `compaction`: persisted compaction summary with `firstKeptEntryId` and `tokensBefore`
- `branch_summary`: persisted summary when navigating a tree branch

OpenClaw intentionally does **not** “fix up” transcripts; the Gateway uses `SessionManager` to read/write them.

---

## Context windows vs tracked tokens

Two different concepts matter:

1. **Model context window**: hard cap per model (tokens visible to the model)
2. **Session store counters**: rolling stats written into `sessions.json` (used for /status and dashboards)

If you’re tuning limits:

- The context window comes from the model catalog (and can be overridden via config).
- `contextTokens` in the store is a runtime estimate/reporting value; don’t treat it as a strict guarantee.

For more, see [/token-use](/reference/token-use).

---

## Compaction: what it is

Compaction summarizes older conversation into a persisted `compaction` entry in the transcript and keeps recent messages intact.

After compaction, future turns see:

- The compaction summary
- Messages after `firstKeptEntryId`

Compaction is **persistent** (unlike session pruning). See [/concepts/session-pruning](/concepts/session-pruning).

---

## When auto-compaction happens (Pi runtime)

In the embedded Pi agent, auto-compaction triggers in two cases:

1. **Overflow recovery**: the model returns a context overflow error → compact → retry.
2. **Threshold maintenance**: after a successful turn, when:

`contextTokens > contextWindow - reserveTokens`

Where:

- `contextWindow` is the model’s context window
- `reserveTokens` is headroom reserved for prompts + the next model output

These are Pi runtime semantics (OpenClaw consumes the events, but Pi decides when to compact).

---

## Compaction settings (`reserveTokens`, `keepRecentTokens`)

Pi’s compaction settings live in Pi settings:

```json5
{
  compaction: {
    enabled: true,
    reserveTokens: 16384,
    keepRecentTokens: 20000,
  },
}
```

OpenClaw also enforces a safety floor for embedded runs:

- If `compaction.reserveTokens < reserveTokensFloor`, OpenClaw bumps it.
- Default floor is `20000` tokens.
- Set `agents.defaults.compaction.reserveTokensFloor: 0` to disable the floor.
- If it’s already higher, OpenClaw leaves it alone.

Why: leave enough headroom for multi-turn “housekeeping” (like memory writes) before compaction becomes unavoidable.

Implementation: `ensurePiCompactionReserveTokens()` in `src/agents/pi-settings.ts`
(called from `src/agents/pi-embedded-runner.ts`).

---

## User-visible surfaces

You can observe compaction and session state via:

- `/status` (in any chat session)
- `openclaw status` (CLI)
- `openclaw sessions` / `sessions --json`
- Verbose mode: `🧹 Auto-compaction complete` + compaction count

---

## Silent housekeeping (`NO_REPLY`)

OpenClaw supports “silent” turns for background tasks where the user should not see intermediate output.

Convention:

- The assistant starts its output with `NO_REPLY` to indicate “do not deliver a reply to the user”.
- OpenClaw strips/suppresses this in the delivery layer.

As of `2026.1.10`, OpenClaw also suppresses **draft/typing streaming** when a partial chunk begins with `NO_REPLY`, so silent operations don’t leak partial output mid-turn.

---

## Pre-compaction “memory flush” (implemented)

Goal: before auto-compaction happens, run a silent agentic turn that writes durable
state to disk (e.g. `memory/YYYY-MM-DD.md` in the agent workspace) so compaction can’t
erase critical context.

OpenClaw uses the **pre-threshold flush** approach:

1. Monitor session context usage.
2. When it crosses a “soft threshold” (below Pi’s compaction threshold), run a silent
   “write memory now” directive to the agent.
3. Use `NO_REPLY` so the user sees nothing.

Config (`agents.defaults.compaction.memoryFlush`):

- `enabled` (default: `true`)
- `softThresholdTokens`（默认值：`4000`）
- `prompt`（用于 flush 轮次的用户消息）
- `systemPrompt` (extra system prompt appended for the flush turn)

Notes:

- 默认的 prompt / system prompt 包含一个 `NO_REPLY` 提示，用于抑制输出。
- flush 在每个压缩周期中运行一次（在 `sessions.json` 中跟踪）。
- flush 仅对嵌入式 Pi 会话运行（CLI 后端会跳过）。
- 当会话工作区为只读时会跳过 flush（`workspaceAccess: "ro"` 或 `"none"`）。
- 有关工作区文件布局和写入模式，请参见 [Memory](/concepts/memory)。

Pi 还在扩展 API 中暴露了一个 `session_before_compact` 钩子，但 OpenClaw 的 flush 逻辑目前位于 Gateway 侧。

---

## 故障排查清单

- 会话键错误？ 从 [/concepts/session](/concepts/session) 开始，并在 `/status` 中确认 `sessionKey`。
- 存储与转录不匹配？ 通过 `openclaw status` 确认 Gateway 主机和存储路径。
- Compaction spam? 检查：
  - 模型上下文窗口（过小）
  - compaction settings (`reserveTokens` too high for the model window can cause earlier compaction)
  - 工具结果膨胀：启用/调整会话裁剪
- 静默轮次泄漏？ 确认回复以 `NO_REPLY`（精确 token）开头，并且你使用的是包含流式抑制修复的构建版本。
