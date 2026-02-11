---
summary: "48. 心跳轮询消息与通知规则"
read_when:
  - 49. 调整心跳频率或消息方式
  - 50. 在定时任务中如何在心跳与 cron 之间做出选择
title: "1. 心跳"
---

# 2. 心跳（网关）

> 3. **心跳 vs Cron？** 参见 [Cron vs Heartbeat](/automation/cron-vs-heartbeat)，了解何时使用各自。

4. 心跳会在主会话中运行**周期性的代理轮次**，使模型能够在不刷屏的情况下，主动提示任何需要关注的事项。

5. 故障排除：[/automation/troubleshooting](/automation/troubleshooting)

## 6. 快速开始（新手）

1. 7. 保持心跳启用（默认是 `30m`，Anthropic OAuth/setup-token 时为 `1h`），或设置你自己的频率。
2. 38. 在代理工作区创建一个微型 `HEARTBEAT.md` 清单（可选但推荐）。
3. 9. 决定心跳消息应发送到哪里（默认是 `target: "last"`）。
4. 10. 可选：启用心跳推理传递以提高透明度。
5. 11. 可选：将心跳限制在活跃时段（本地时间）。

12) 示例配置：

```json5
13. {
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last",
        // activeHours: { start: "08:00", end: "24:00" },
        // includeReasoning: true, // optional: send separate `Reasoning:` message too
      },
    },
  },
}
```

## 14. 默认值

- 15. 间隔：`30m`（当检测到 Anthropic OAuth/setup-token 作为认证模式时为 `1h`）。 16. 设置 `agents.defaults.heartbeat.every` 或每个代理的 `agents.list[].heartbeat.every`；使用 `0m` 可禁用。
- 17. 提示正文（可通过 `agents.defaults.heartbeat.prompt` 配置）：
      \`Read HEARTBEAT.md if it exists (workspace context).
  18. Follow it strictly.
  19. Do not infer or repeat old tasks from prior chats.
  20. If nothing needs attention, reply HEARTBEAT_OK.` 21. 心跳提示会**逐字**作为用户消息发送。 22. 系统
        提示包含一个“Heartbeat”部分，并且该运行在内部被标记。 23. 活跃时段（`heartbeat.activeHours\`）会在配置的时区内进行检查。
- 24. 在时间窗口之外，心跳会被跳过，直到下一个位于窗口内的节拍。 39. 系统提示包含一个“Heartbeat”部分，并在内部标记该运行。
- 40. 活跃时段（`heartbeat.activeHours`）会在配置的时区中进行检查。
  41. **后台任务**：“考虑未完成的任务”会促使代理回顾
      后续事项（收件箱、日历、提醒、排队中的工作），并提示任何紧急情况。

28. **人工关怀**：“在白天偶尔检查一下你的人类”会促使
    偶尔发送轻量的“需要我做点什么吗？”消息，但会通过你配置的本地时区避免夜间打扰（参见 [/concepts/timezone](/concepts/timezone)）。
-----------------------------------------------------------------------------------------

41. 默认提示有意保持宽泛：

- 42. **后台任务**：“Consider outstanding tasks” 会促使代理回顾待办事项（收件箱、日历、提醒、排队工作），并突出任何紧急事项。
- 31. 如果没有需要关注的事项，请回复 **`HEARTBEAT_OK`**。

32. 在心跳运行期间，当 `HEARTBEAT_OK` 出现在回复的**开头或结尾**时，OpenClaw 会将其视为确认（ack）。

## 33. 该标记会被移除，如果剩余内容 **≤ `ackMaxChars`**（默认：300），回复将被丢弃。

- 34. 如果 `HEARTBEAT_OK` 出现在回复的**中间**，则不会被特殊处理。
- 35. 对于告警，**不要**包含 `HEARTBEAT_OK`；只返回告警文本。 36. 在非心跳场景下，出现在消息开头/结尾的多余 `HEARTBEAT_OK` 会被移除并记录；仅包含 `HEARTBEAT_OK` 的消息会被丢弃。
- 37. 配置
- 38. {
      agents: {
      defaults: {
      heartbeat: {
      every: "30m", // default: 30m (0m disables)
      model: "anthropic/claude-opus-4-6",
      includeReasoning: false, // default: false (deliver separate Reasoning: message when available)
      target: "last", // last | none | <channel id> (core or plugin, e.g. "bluebubbles")
      to: "+15551234567", // optional channel-specific override
      accountId: "ops-bot", // optional multi-account channel id
      prompt: "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.",
      ackMaxChars: 300, // max chars allowed after HEARTBEAT_OK
      },
      },
      },
      }

39. 作用域与优先级

## 40. `agents.defaults.heartbeat` 设置全局心跳行为。

```json5
41. `agents.list[].heartbeat` 在其之上合并；如果任何代理具有 `heartbeat` 块，**只有这些代理**会运行心跳。
```

### 42. `channels.defaults.heartbeat` 设置所有通道的可见性默认值。

- 43. `channels.<channel>`
- 44. `.heartbeat` 覆盖通道默认值。
- 45. `channels.<channel>`
- 46. `.accounts.<id>`47. `.heartbeat`（多账户通道）覆盖每个通道的设置。
- 48. 每代理心跳49. 如果任何 `agents.list[]` 条目包含 `heartbeat` 块，**只有这些代理**
      运行心跳。50. 每代理块会在 `agents.defaults.heartbeat`
      之上合并（因此你可以一次性设置共享默认值，并按代理进行覆盖）。

### Per-agent heartbeats

If any `agents.list[]` entry includes a `heartbeat` block, **only those agents**
run heartbeats. The per-agent block merges on top of `agents.defaults.heartbeat`
(so you can set shared defaults once and override per agent).

Example: two agents, only the second agent runs heartbeats.

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last",
      },
    },
    list: [
      { id: "main", default: true },
      {
        id: "ops",
        heartbeat: {
          every: "1h",
          target: "whatsapp",
          to: "+15551234567",
          prompt: "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.",
        },
      },
    ],
  },
}
```

### 43. 活跃时段示例

Restrict heartbeats to business hours in a specific timezone:

```json5
44. {
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last",
        activeHours: {
          start: "09:00",
          end: "22:00",
          timezone: "America/New_York", // optional; uses your userTimezone if set, otherwise host tz
        },
      },
    },
  },
}
```

Outside this window (before 9am or after 10pm Eastern), heartbeats are skipped. The next scheduled tick inside the window will run normally.

### Multi account example

Use `accountId` to target a specific account on multi-account channels like Telegram:

```json5
{
  agents: {
    list: [
      {
        id: "ops",
        heartbeat: {
          every: "1h",
          target: "telegram",
          to: "12345678",
          accountId: "ops-bot",
        },
      },
    ],
  },
  channels: {
    telegram: {
      accounts: {
        "ops-bot": { botToken: "YOUR_TELEGRAM_BOT_TOKEN" },
      },
    },
  },
}
```

### Field notes

- `every`: heartbeat interval (duration string; default unit = minutes).
- `model`: optional model override for heartbeat runs (`provider/model`).
- 45. `includeReasoning`：启用后，在可用时也会传递单独的 `Reasoning:` 消息（与 `/reasoning on` 形态相同）。
- 46. `session`：用于心跳运行的可选会话键。
  - `main` (default): agent main session.
  - Explicit session key (copy from `openclaw sessions --json` or the [sessions CLI](/cli/sessions)).
  - Session key formats: see [Sessions](/concepts/session) and [Groups](/channels/groups).
- `target`:
  - `last` (default): deliver to the last used external channel.
  - explicit channel: `whatsapp` / `telegram` / `discord` / `googlechat` / `slack` / `msteams` / `signal` / `imessage`.
  - `none`: run the heartbeat but **do not deliver** externally.
- `to`: optional recipient override (channel-specific id, e.g. E.164 for WhatsApp or a Telegram chat id).
- `accountId`: optional account id for multi-account channels. When `target: "last"`, the account id applies to the resolved last channel if it supports accounts; otherwise it is ignored. If the account id does not match a configured account for the resolved channel, delivery is skipped.
- `prompt`: overrides the default prompt body (not merged).
- `ackMaxChars`: max chars allowed after `HEARTBEAT_OK` before delivery.
- `activeHours`: restricts heartbeat runs to a time window. Object with `start` (HH:MM, inclusive), `end` (HH:MM exclusive; `24:00` allowed for end-of-day), and optional `timezone`.
  - Omitted or `"user"`: uses your `agents.defaults.userTimezone` if set, otherwise falls back to the host system timezone.
  - `"local"`: always uses the host system timezone.
  - Any IANA identifier (e.g. `America/New_York`): used directly; if invalid, falls back to the `"user"` behavior above.
  - Outside the active window, heartbeats are skipped until the next tick inside the window.

## Delivery behavior

- Heartbeats run in the agent’s main session by default (`agent:<id>:<mainKey>`),
  or `global` when `session.scope = "global"`. Set `session` to override to a
  specific channel session (Discord/WhatsApp/etc.).
- `session` only affects the run context; delivery is controlled by `target` and `to`.
- To deliver to a specific channel/recipient, set `target` + `to`. With
  `target: "last"`, delivery uses the last external channel for that session.
- If the main queue is busy, the heartbeat is skipped and retried later.
- If `target` resolves to no external destination, the run still happens but no
  outbound message is sent.
- 47. 仅心跳的回复**不会**保持会话存活；`updatedAt` 将被恢复，因此空闲过期行为保持正常。

## 48. 可见性控制

By default, `HEARTBEAT_OK` acknowledgments are suppressed while alert content is
delivered. You can adjust this per channel or per account:

```yaml
channels:
  defaults:
    heartbeat:
      showOk: false # Hide HEARTBEAT_OK (default)
      showAlerts: true # Show alert messages (default)
      useIndicator: true # Emit indicator events (default)
  telegram:
    heartbeat:
      showOk: true # Show OK acknowledgments on Telegram
  whatsapp:
    accounts:
      work:
        heartbeat:
          showAlerts: false # Suppress alert delivery for this account
```

Precedence: per-account → per-channel → channel defaults → built-in defaults.

### What each flag does

- `showOk`: sends a `HEARTBEAT_OK` acknowledgment when the model returns an OK-only reply.
- `showAlerts`：当模型返回非 OK 回复时发送警报内容。
- `useIndicator`：为 UI 状态展示发出指示器事件。

如果**三个**都为 false，OpenClaw 会完全跳过心跳运行（不会调用模型）。

### 按频道 vs 按账号的示例

```yaml
channels:
  defaults:
    heartbeat:
      showOk: false
      showAlerts: true
      useIndicator: true
  slack:
    heartbeat:
      showOk: true # 所有 Slack 账号
    accounts:
      ops:
        heartbeat:
          showAlerts: false # 仅为 ops 账号抑制警报
  telegram:
    heartbeat:
      showOk: true
```

### 常见模式

| 目标               | 配置                                                                                       |
| ---------------- | ---------------------------------------------------------------------------------------- |
| 默认行为（OK 静默，开启警报） | _（无需配置）_                                                                                 |
| 完全静默（无消息、无指示器）   | `channels.defaults.heartbeat: { showOk: false, showAlerts: false, useIndicator: false }` |
| 仅指示器（无消息）        | `channels.defaults.heartbeat: { showOk: false, showAlerts: false, useIndicator: true }`  |
| 仅在一个频道显示 OK      | `channels.telegram.heartbeat: { showOk: true }`                                          |

## HEARTBEAT.md（可选）

如果工作区中存在 `HEARTBEAT.md` 文件，默认提示会指示代理读取它。 把它当作你的“心跳清单”：小而稳定，
并且可以安全地每 30 分钟包含一次。

如果 `HEARTBEAT.md` 存在但实际上是空的（只有空行和诸如 `# Heading` 的 Markdown 标题），OpenClaw 会跳过心跳运行以节省 API 调用。
如果文件缺失，心跳仍会运行，由模型决定要做什么。

保持内容精简（简短清单或提醒），以避免提示膨胀。

示例 `HEARTBEAT.md`：

```md
# Heartbeat checklist

- 快速浏览：收件箱里有没有紧急事项？
- 如果是白天且没有其他待办，进行一次轻量级的签到。
- 如果某个任务被阻塞，写下_缺少的内容_，下次问 Peter。
```

### 代理可以更新 HEARTBEAT.md 吗？

可以——如果你让它这么做。

`HEARTBEAT.md` 只是代理工作区中的一个普通文件，因此你可以（在普通聊天中）对代理说类似：

- “更新 `HEARTBEAT.md`，添加一个每日日历检查。”
- “重写 `HEARTBEAT.md`，让它更短并聚焦于收件箱跟进。”

如果你希望这能主动发生，也可以在心跳提示中包含一行明确的话，例如：“如果清单变得陈旧，用更好的版本更新 HEARTBEAT.md。”

安全提示：不要把机密信息（API 密钥、电话号码、私有令牌）放入 `HEARTBEAT.md` ——它会成为提示上下文的一部分。

## 手动唤醒（按需）

你可以排入一个系统事件并通过以下方式触发一次立即心跳：

```bash
openclaw system event --text "Check for urgent follow-ups" --mode now
```

如果多个代理配置了 `heartbeat`，手动唤醒会立即运行每个代理的心跳。

使用 `--mode next-heartbeat` 来等待下一次计划的触发。

## 推理内容交付（可选）

默认情况下，心跳只交付最终的“答案”负载。

49. 如果你希望透明度，请启用：

- 50. `agents.defaults.heartbeat.includeReasoning: true`

When enabled, heartbeats will also deliver a separate message prefixed
`Reasoning:` (same shape as `/reasoning on`). 当代理
正在管理多个会话/代码库而你想知道它为什么决定提醒你时，这会很有用——但也可能泄露比你希望更多的内部细节。 Prefer keeping it
off in group chats.

## 成本考量

心跳会运行完整的代理轮次。 更短的间隔会消耗更多 token。 Keep
`HEARTBEAT.md` small and consider a cheaper `model` or `target: "none"` if you
only want internal state updates.
