---
summary: "用于 Gateway 调度器的 Cron 作业 + 唤醒"
read_when:
  - 调度后台作业或唤醒
  - 将应与心跳一起或并行运行的自动化进行连接
  - 在计划任务中决定使用心跳还是 cron
title: "Cron 作业"
---

# Cron 作业（Gateway 调度器）

> **Cron 还是 Heartbeat？** 参见 [Cron vs Heartbeat](/automation/cron-vs-heartbeat)，了解何时使用各自方案的指导。

Cron 是 Gateway 的内置调度器。 它会持久化作业，在合适的时间唤醒代理，并且可选地将输出回传到聊天中。

如果你想要 _“每天早上运行一次”_ 或 _“20 分钟后戳一下代理”_，
cron 就是实现机制。

故障排查：[/automation/troubleshooting](/automation/troubleshooting)

## TL;DR

- Cron 在 **Gateway 内部** 运行（不在模型内部）。
- 作业持久化在 `~/.openclaw/cron/` 下，因此重启不会丢失计划。
- 两种执行方式：
  - **主会话**：入队一个系统事件，然后在下一次心跳时运行。
  - **隔离**：在 `cron:<jobId>` 中运行一个专用的代理轮次，并进行投递（默认公告或不投递）。
- 唤醒是一等公民：作业可以请求“立即唤醒”而不是“下一次心跳”。

## 快速开始（可操作）

创建一个一次性提醒，验证其存在，并立即运行：

```bash
openclaw cron add \
  --name "Reminder" \
  --at "2026-02-01T16:00:00Z" \
  --session main \
  --system-event "Reminder: check the cron docs draft" \
  --wake now \
  --delete-after-run

openclaw cron list
openclaw cron run <job-id>
openclaw cron runs --id <job-id>
```

安排一个带投递的周期性隔离作业：

```bash
openclaw cron add \
  --name "Morning brief" \
  --cron "0 7 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize overnight updates." \
  --announce \
  --channel slack \
  --to "channel:C1234567890"
```

## 工具调用等价物（Gateway cron 工具）

1. 有关规范化的 JSON 形状和示例，请参见 [JSON schema for tool calls](/automation/cron-jobs#json-schema-for-tool-calls)。

## Cron 作业存储位置

默认情况下，Cron 作业会持久化存储在 Gateway 主机上的 `~/.openclaw/cron/jobs.json`。
Gateway 会将该文件加载到内存中，并在发生更改时写回，因此只有在 Gateway 停止时手动编辑才是安全的。 5. 更改时优先使用 `openclaw cron add/edit` 或 cron
工具调用 API。

## 6. 面向初学者的概览

7. 将一个 cron 作业理解为：**何时**运行 + **做什么**。

1. 8. **选择调度**
   - 9. 一次性提醒 → `schedule.kind = "at"`（CLI：`--at`）
   - 10. 重复作业 → `schedule.kind = "every"` 或 `schedule.kind = "cron"`
   - 11. 如果你的 ISO 时间戳省略了时区，则会被视为 **UTC**。

2. 12. **选择运行位置**
   - 13. `sessionTarget: "main"` → 在下一次心跳期间以主上下文运行。
   - 14. `sessionTarget: "isolated"` → 在 `cron:<jobId>` 中运行一个专用的代理回合。

3. 15. **选择负载**
   - 16. 主会话 → `payload.kind = "systemEvent"`
   - Isolated session → `payload.kind = "agentTurn"`

18) 可选：一次性作业（`schedule.kind = "at"`）在成功后默认会被删除。 19. 设置
    `deleteAfterRun: false` 以保留它们（成功后将被禁用）。

## 20. 概念

### 21. 作业

22. 一个 cron 作业是一个包含以下内容的已存储记录：

- 23. 一个 **调度**（何时运行），
- 24. 一个 **负载**（做什么），
- optional **delivery mode** (announce or none).
- 26. 可选的 **代理绑定**（`agentId`）：在特定代理下运行作业；如果
      缺失或未知，Gateway 将回退到默认代理。

27. 作业通过稳定的 `jobId` 标识（由 CLI/Gateway API 使用）。
28. 在代理工具调用中，`jobId` 是规范字段；为兼容性也接受旧的 `id`。
29. 一次性作业默认在成功后自动删除；设置 `deleteAfterRun: false` 可保留它们。

### 30. 调度

31. Cron 支持三种调度类型：

- 32. `at`：通过 `schedule.at` 指定的一次性时间戳（ISO 8601）。
- 33. `every`：固定间隔（毫秒）。
- 34. `cron`：5 字段的 cron 表达式，可选 IANA 时区。

35. Cron 表达式使用 `croner`。 36. 如果省略时区，则使用 Gateway 主机的
    本地时区。

### 37. 主执行与隔离执行

#### 38. 主会话作业（系统事件）

39. 主作业会入队一个系统事件，并可选择唤醒心跳运行器。
40. 它们必须使用 `payload.kind = "systemEvent"`。

- 41. `wakeMode: "now"`（默认）：事件触发一次立即的心跳运行。
- 42. `wakeMode: "next-heartbeat"`：事件等待下一次计划的心跳。

43. 当你需要正常的心跳提示 + 主会话上下文时，这是最佳选择。
44. 参见 [Heartbeat](/gateway/heartbeat)。

#### 45. 隔离作业（专用的 cron 会话）

46. 隔离作业会在会话 `cron:<jobId>` 中运行一个专用的代理回合。

47. 关键行为：

- 48. 为了可追溯性，提示会以 `[cron:<jobId> <job name>]` 作为前缀。
- 49. 每次运行都会启动一个 **全新的会话 id**（不继承之前的对话）。
- 50. 默认行为：如果省略 `delivery`，隔离作业会发布一条摘要公告（`delivery.mode = "announce"`）。
- 2. `announce`：将摘要投递到目标频道，并在主会话中发布一条简要摘要。
  - 3. `none`：仅内部使用（不投递，也不发布主会话摘要）。
  - 4. `wakeMode` 控制主会话摘要何时发布：
- 5. `now`：立即心跳。
  - 6. `next-heartbeat`：等待下一个计划的心跳。
  - 7. 对于嘈杂、频繁或“不应刷屏”的“后台杂务”，请使用隔离作业，
       以免污染你的主聊天记录。

8. 负载形态（运行内容）

### 9. 支持两种负载类型：

10. `systemEvent`：仅主会话，通过心跳提示路由。

- 11. `agentTurn`：仅隔离会话，运行一个专用的代理轮次。
- 12. 常见的 `agentTurn` 字段：

13. `message`：必填的文本提示。

- 14. `model` / `thinking`：可选覆盖（见下文）。
- `model` / `thinking`：可选覆盖项（见下文）。
- 16. 投递配置（仅隔离作业）：

17. `delivery.mode`：`none` | `announce`。

- 18. `delivery.channel`：`last` 或指定的频道。
- 19. `delivery.to`：频道特定的目标（电话/聊天/频道 ID）。
- 20. `delivery.bestEffort`：若公告投递失败，避免使作业失败。
- 21. 公告投递会抑制该运行中的消息工具发送；请使用 `delivery.channel`/`delivery.to`
      将消息定向到聊天。

22. 当 `delivery.mode = "none"` 时，不会向主会话发布摘要。 23. 如果隔离作业省略了 `delivery`，OpenClaw 默认使用 `announce`。

24. 公告投递流程

#### 25. 当 `delivery.mode = "announce"` 时，cron 会通过出站频道适配器直接投递。

26. 不会启动主代理来编写或转发消息。
27. 行为细节：

28. 内容：投递使用隔离运行的出站负载（文本/媒体），并采用正常的分块与
    频道格式化。

- 29. 仅心跳响应（没有实际内容的 `HEARTBEAT_OK`）不会被投递。
- 30. 如果隔离运行已通过消息工具向同一目标发送过消息，为避免重复，将跳过投递。
- 31. 缺失或无效的投递目标会使作业失败，除非 `delivery.bestEffort = true`。
- 32. 仅当 `delivery.mode = "announce"` 时，才会向主会话发布一条简短摘要。
- 33. 主会话摘要遵循 `wakeMode`：`now` 会触发立即心跳，
      `next-heartbeat` 则等待下一个计划的心跳。
- 34. 模型与思考级别覆盖

### 35. 隔离作业（`agentTurn`）可以覆盖模型和思考级别：

36. `model`：提供商/模型字符串（例如 `anthropic/claude-sonnet-4-20250514`）或别名（例如 `opus`）。

- 37. `thinking`：思考级别（`off`、`minimal`、`low`、`medium`、`high`、`xhigh`；仅 GPT-5.2 + Codex 模型支持）。
- 38. 注意：你也可以在主会话作业上设置 `model`，但这会更改共享的主会话模型。

39. 我们建议仅对隔离作业使用模型覆盖，以避免
    意外的上下文切换。 40. 解析优先级：

41. 作业负载覆盖（最高）

1. 42. 钩子特定默认值（例如 `hooks.gmail.model`）
2. 43. 代理配置默认值
3. 44. 投递（频道 + 目标）

### 45) 隔离作业可以通过顶层 `delivery` 配置将输出投递到某个频道：

46. `delivery.mode`：`announce`（投递摘要）或 `none`。

- 47. `delivery.channel`：`whatsapp` / `telegram` / `discord` / `slack` / `mattermost`（插件）/ `signal` / `imessage` / `last`。
- 48. `delivery.to`：频道特定的收件人目标。
- 49. 投递配置仅对隔离作业有效（`sessionTarget: "isolated"`）。

50. 如果省略 `delivery.channel` 或 `delivery.to`，cron 可以回退到主会话的
    “最后路由”（代理最后一次回复的位置）。

If `delivery.channel` or `delivery.to` is omitted, cron can fall back to the main session’s
“last route” (the last place the agent replied).

1. 目标格式提醒：

- 2. Slack/Discord/Mattermost（插件）目标应使用显式前缀（例如 `channel:<id>`、`user:<id>`）以避免歧义。
- 3. Telegram 主题应使用 `:topic:` 形式（见下文）。

#### 4. Telegram 投递目标（主题 / 论坛线程）

5. Telegram 通过 `message_thread_id` 支持论坛主题。 6. 对于 cron 投递，你可以将主题/线程编码到 `to` 字段中：

- 7. `-1001234567890`（仅聊天 id）
- 8. `-1001234567890:topic:123`（推荐：显式主题标记）
- 9. `-1001234567890:123`（简写：数字后缀）

10. 也接受带前缀的目标，如 `telegram:...` / `telegram:group:...`：

- 11. `telegram:group:-1001234567890:topic:123`

## 12. 工具调用的 JSON schema

13. 直接调用 Gateway `cron.*` 工具时（代理工具调用或 RPC）请使用以下结构。
14. CLI 标志接受如 `20m` 的人类可读时长，但工具调用应为 `schedule.at` 使用 ISO 8601 字符串，并为 `schedule.everyMs` 使用毫秒。

### 15. cron.add 参数

16. 一次性、主会话作业（系统事件）：

```json
17. {
  "name": "Reminder",
  "schedule": { "kind": "at", "at": "2026-02-01T16:00:00Z" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": { "kind": "systemEvent", "text": "Reminder text" },
  "deleteAfterRun": true
}
```

18. 带投递的周期性、隔离作业：

```json
19. {
  "name": "Morning brief",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "America/Los_Angeles" },
  "sessionTarget": "isolated",
  "wakeMode": "next-heartbeat",
  "payload": {
    "kind": "agentTurn",
    "message": "Summarize overnight updates."
  },
  "delivery": {
    "mode": "announce",
    "channel": "slack",
    "to": "channel:C1234567890",
    "bestEffort": true
  }
}
```

20. 说明：

- 21. `schedule.kind`：`at`（`at`）、`every`（`everyMs`）或 `cron`（`expr`，可选 `tz`）。
- 22. `schedule.at` 接受 ISO 8601（时区可选；省略时按 UTC 处理）。
- 23. `everyMs` 以毫秒为单位。
- 24. `sessionTarget` 必须为 `"main"` 或 `"isolated"`，并且必须与 `payload.kind` 匹配。
- 25. 可选字段：`agentId`、`description`、`enabled`、`deleteAfterRun`（`at` 默认 true）、`delivery`。
- 26. 省略时，`wakeMode` 默认为 `"now"`。

### 27. cron.update 参数

```json
28. {
  "jobId": "job-123",
  "patch": {
    "enabled": false,
    "schedule": { "kind": "every", "everyMs": 3600000 }
  }
}
```

29. 说明：

- 30. `jobId` 为规范字段；为兼容性也接受 `id`。
- 31. 在 patch 中使用 `agentId: null` 可清除代理绑定。

### 32. cron.run 和 cron.remove 参数

```json
33. { "jobId": "job-123", "mode": "force" }
```

```json
34. { "jobId": "job-123" }
```

## 35. 存储与历史

- 36. 作业存储：`~/.openclaw/cron/jobs.json`（由 Gateway 管理的 JSON）。
- 37. 运行历史：`~/.openclaw/cron/runs/<jobId>.jsonl`（JSONL，自动清理）。
- 38. 覆盖存储路径：配置中的 `cron.store`。

## 39. 配置

```json5
40. {
  cron: {
    enabled: true, // 默认 true
    store: "~/.openclaw/cron/jobs.json",
    maxConcurrentRuns: 1, // 默认 1
  },
}
```

41. 完全禁用 cron：

- 42. `cron.enabled: false`（配置）
- 43. `OPENCLAW_SKIP_CRON=1`（环境变量）

## 44. CLI 快速开始

45. 一次性提醒（UTC ISO，成功后自动删除）：

```bash
46. openclaw cron add \
  --name "Send reminder" \
  --at "2026-01-12T18:00:00Z" \
  --session main \
  --system-event "Reminder: submit expense report." \
  --wake now \
  --delete-after-run
```

47. 一次性提醒（主会话，立即唤醒）：

```bash
48. openclaw cron add \
  --name "Calendar check" \
  --at "20m" \
  --session main \
  --system-event "Next heartbeat: check calendar." \
  --wake now
```

49. 周期性隔离作业（公告到 WhatsApp）：

```bash
50. openclaw cron add \
  --name "Morning status" \
  --cron "0 7 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize inbox + calendar for today." \
  --announce \
  --channel whatsapp \
  --to "+15551234567"
```

Recurring isolated job (deliver to a Telegram topic):

```bash
openclaw cron add \
  --name "Nightly summary (topic)" \
  --cron "0 22 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize today; send to the nightly topic." \
  --announce \
  --channel telegram \
  --to "-1001234567890:topic:123"
```

Isolated job with model and thinking override:

```bash
openclaw cron add \
  --name "Deep analysis" \
  --cron "0 6 * * 1" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Weekly deep analysis of project progress." \
  --model "opus" \
  --thinking high \
  --announce \
  --channel whatsapp \
  --to "+15551234567"
```

Agent selection (multi-agent setups):

```bash
# Pin a job to agent "ops" (falls back to default if that agent is missing)
openclaw cron add --name "Ops sweep" --cron "0 6 * * *" --session isolated --message "Check ops queue" --agent ops

# Switch or clear the agent on an existing job
openclaw cron edit <jobId> --agent ops
openclaw cron edit <jobId> --clear-agent
```

Manual run (force is the default, use `--due` to only run when due):

```bash
openclaw cron run <jobId>
openclaw cron run <jobId> --due
```

Edit an existing job (patch fields):

```bash
openclaw cron edit <jobId> \
  --message "Updated prompt" \
  --model "opus" \
  --thinking low
```

Run history:

```bash
openclaw cron runs --id <jobId> --limit 50
```

Immediate system event without creating a job:

```bash
openclaw system event --mode now --text "Next heartbeat: check battery."
```

## Gateway API 接口

- `cron.list`, `cron.status`, `cron.add`, `cron.update`, `cron.remove`
- `cron.run` (force or due), `cron.runs`
  For immediate system events without a job, use [`openclaw system event`](/cli/system).

## Troubleshooting

### “Nothing runs”

- Check cron is enabled: `cron.enabled` and `OPENCLAW_SKIP_CRON`.
- Check the Gateway is running continuously (cron runs inside the Gateway process).
- For `cron` schedules: confirm timezone (`--tz`) vs the host timezone.

### A recurring job keeps delaying after failures

- OpenClaw applies exponential retry backoff for recurring jobs after consecutive errors:
  30s, 1m, 5m, 15m, then 60m between retries.
- Backoff resets automatically after the next successful run.
- One-shot (`at`) jobs disable after a terminal run (`ok`, `error`, or `skipped`) and do not retry.

### Telegram delivers to the wrong place

- For forum topics, use `-100…:topic:<id>` so it’s explicit and unambiguous.
- If you see `telegram:...` prefixes in logs or stored “last route” targets, that’s normal;
  cron delivery accepts them and still parses topic IDs correctly.
