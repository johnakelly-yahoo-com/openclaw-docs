---
summary: "Guidance for choosing between heartbeat and cron jobs for automation"
read_when:
  - Deciding how to schedule recurring tasks
  - Setting up background monitoring or notifications
  - Optimizing token usage for periodic checks
title: "Cron vs Heartbeat"
---

# Cron vs Heartbeat: When to Use Each

Both heartbeats and cron jobs let you run tasks on a schedule. This guide helps you choose the right mechanism for your use case.

## Quick Decision Guide

| 使用场景                                 | Recommended                                | Why                                      |
| ------------------------------------ | ------------------------------------------ | ---------------------------------------- |
| Check inbox every 30 min             | Heartbeat                                  | Batches with other checks, context-aware |
| Send daily report at 9am sharp       | Cron (isolated)         | Exact timing needed                      |
| Monitor calendar for upcoming events | Heartbeat                                  | Natural fit for periodic awareness       |
| 1. 运行每周深度分析   | 2. Cron（隔离）         | 3. 独立任务，可使用不同模型   |
| 4. 20 分钟后提醒我  | 5. Cron（主会话，`--at`） | 6. 精确时间的一次性任务     |
| 7. 后台项目健康检查   | 8. 心跳               | 9. 搭载在现有周期之上      |

## 10. 心跳：周期性感知

11. 心跳在**主会话**中以固定间隔运行（默认：30 分钟）。 12. 它们旨在让代理检查各项情况，并呈现任何重要内容。

### 13. 何时使用心跳

- 14. **多个周期性检查**：与其用 5 个独立的 cron 任务分别检查收件箱、日历、天气、通知和项目状态，不如用一个心跳将它们批量处理。
- 15. **上下文感知决策**：代理拥有完整的主会话上下文，因此可以智能判断什么是紧急的、什么可以等待。
- 16. **对话连续性**：心跳运行共享同一会话，因此代理会记住最近的对话并能自然地跟进。
- 17. **低开销监控**：一个心跳即可替代多个小型轮询任务。

### 18. 心跳优势

- 19. **批量处理多项检查**：一次代理执行即可同时查看收件箱、日历和通知。
- 20. **减少 API 调用**：一个心跳比 5 个独立的 cron 任务更省成本。
- 21. **上下文感知**：代理知道你一直在做什么，并可据此进行优先级排序。
- 22. **智能抑制**：如果没有需要关注的内容，代理会回复 `HEARTBEAT_OK`，且不会发送任何消息。
- 23. **自然时序**：会根据队列负载略有漂移，这对大多数监控场景来说是可以接受的。

### 24. 心跳示例：HEARTBEAT.md 清单

```md
25. # 心跳清单

- 检查电子邮件中的紧急消息
- 查看未来 2 小时内的日历事件
- 如果后台任务完成，汇总结果
- 如果空闲超过 8 小时，发送简短问候
```

26. 代理会在每次心跳时读取此清单，并在一次执行中处理所有事项。

### 27. 配置心跳

```json5
28. {
  agents: {
    defaults: {
      heartbeat: {
        every: "30m", // 间隔
        target: "last", // 投递位置
        activeHours: { start: "08:00", end: "22:00" }, // 可选
      },
    },
  },
}
```

29. 完整配置请参见 [Heartbeat](/gateway/heartbeat)。

## 30. Cron：精确调度

31. Cron 任务在**精确时间**运行，并且可以在隔离会话中执行而不影响主上下文。

### 32. 何时使用 cron

- 33. **需要精确时间**：例如“每周一上午 9:00 发送”（而不是“9 点左右某个时间”）。
- 34. **独立任务**：不需要对话上下文的任务。
- 35. **不同模型/思考方式**：需要更强大模型的重度分析。
- 36. **一次性提醒**：使用 `--at` 的“20 分钟后提醒我”。
- 37. **嘈杂/高频任务**：会让主会话历史变得杂乱的任务。
- 38. **外部触发**：应当独立运行、不依赖代理是否活跃的任务。

### 39. Cron 优势

- 40. **精确时间**：支持时区的 5 字段 cron 表达式。
- 41. **会话隔离**：在 `cron:<jobId>` 中运行，不会污染主历史。
- 42. **模型覆盖**：每个任务可使用更便宜或更强大的模型。
- 43. **投递控制**：隔离任务默认使用 `announce`（摘要）；可根据需要选择 `none`。
- 44. **即时投递**：announce 模式会直接发布，而无需等待心跳。
- 45. **无需代理上下文**：即使主会话处于空闲或被压缩状态也能运行。
- 46. **一次性支持**：使用 `--at` 指定精确的未来时间戳。

### 47. Cron 示例：每日晨报

```bash
48. openclaw cron add \
  --name "Morning briefing" \
  --cron "0 7 * * *" \
  --tz "America/New_York" \
  --session isolated \
  --message "Generate today's briefing: weather, calendar, top emails, news summary." \
  --model opus \
  --announce \
  --channel whatsapp \
  --to "+15551234567"
```

49. 该任务会在纽约时间早上 7:00 准时运行，使用 Opus 以保证质量，并将摘要直接发布到 WhatsApp。

### 50. Cron 示例：一次性提醒

```bash
openclaw cron add \
  --name "Meeting reminder" \
  --at "20m" \
  --session main \
  --system-event "Reminder: standup meeting starts in 10 minutes." \
  --wake now \
  --delete-after-run
```

See [Cron jobs](/automation/cron-jobs) for full CLI reference.

## Decision Flowchart

```
Does the task need to run at an EXACT time?
  YES -> Use cron
  NO  -> Continue...

Does the task need isolation from main session?
  YES -> Use cron (isolated)
  NO  -> Continue...

Can this task be batched with other periodic checks?
  YES -> Use heartbeat (add to HEARTBEAT.md)
  NO  -> Use cron

Is this a one-shot reminder?
  YES -> Use cron with --at
  NO  -> Continue...

Does it need a different model or thinking level?
  YES -> Use cron (isolated) with --model/--thinking
  NO  -> Use heartbeat
```

## Combining Both

The most efficient setup uses **both**:

1. **Heartbeat** handles routine monitoring (inbox, calendar, notifications) in one batched turn every 30 minutes.
2. **Cron** handles precise schedules (daily reports, weekly reviews) and one-shot reminders.

### Example: Efficient automation setup

**HEARTBEAT.md** (checked every 30 min):

```md
# Heartbeat checklist

- Scan inbox for urgent emails
- Check calendar for events in next 2h
- Review any pending tasks
- Light check-in if quiet for 8+ hours
```

**Cron jobs** (precise timing):

```bash
# Daily morning briefing at 7am
openclaw cron add --name "Morning brief" --cron "0 7 * * *" --session isolated --message "..." --announce

# Weekly project review on Mondays at 9am
openclaw cron add --name "Weekly review" --cron "0 9 * * 1" --session isolated --message "..." --model opus

# One-shot reminder
openclaw cron add --name "Call back" --at "2h" --session main --system-event "Call back the client" --wake now
```

## Lobster: Deterministic workflows with approvals

Lobster is the workflow runtime for **multi-step tool pipelines** that need deterministic execution and explicit approvals.
Use it when the task is more than a single agent turn, and you want a resumable workflow with human checkpoints.

### When Lobster fits

- **Multi-step automation**: You need a fixed pipeline of tool calls, not a one-off prompt.
- **Approval gates**: Side effects should pause until you approve, then resume.
- **Resumable runs**: Continue a paused workflow without re-running earlier steps.

### How it pairs with heartbeat and cron

- **Heartbeat/cron** decide _when_ a run happens.
- **Lobster** defines _what steps_ happen once the run starts.

For scheduled workflows, use cron or heartbeat to trigger an agent turn that calls Lobster.
For ad-hoc workflows, call Lobster directly.

### Operational notes (from the code)

- Lobster runs as a **local subprocess** (`lobster` CLI) in tool mode and returns a **JSON envelope**.
- If the tool returns `needs_approval`, you resume with a `resumeToken` and `approve` flag.
- The tool is an **optional plugin**; enable it additively via `tools.alsoAllow: ["lobster"]` (recommended).
- If you pass `lobsterPath`, it must be an **absolute path**.

See [Lobster](/tools/lobster) for full usage and examples.

## Main Session vs Isolated Session

Both heartbeat and cron can interact with the main session, but differently:

|         | Heartbeat                       | Cron (main)             | Cron (isolated)            |
| ------- | ------------------------------- | ------------------------------------------ | --------------------------------------------- |
| Session | Main                            | Main (via system event) | `cron:<jobId>`                                |
| History | Shared                          | Shared                                     | Fresh each run                                |
| Context | Full                            | Full                                       | None (starts clean)        |
| Model   | Main session model              | Main session model                         | Can override                                  |
| Output  | Delivered if not `HEARTBEAT_OK` | Heartbeat prompt + event                   | Announce summary (default) |

### When to use main session cron

Use `--session main` with `--system-event` when you want:

- The reminder/event to appear in main session context
- The agent to handle it during the next heartbeat with full context
- No separate isolated run

```bash
openclaw cron add \
  --name "Check project" \
  --every "4h" \
  --session main \
  --system-event "Time for a project health check" \
  --wake now
```

### When to use isolated cron

Use `--session isolated` when you want:

- A clean slate without prior context
- Different model or thinking settings
- Announce summaries directly to a channel
- History that doesn't clutter main session

```bash
openclaw cron add \
  --name "Deep analysis" \
  --cron "0 6 * * 0" \
  --session isolated \
  --message "Weekly codebase analysis..." \
  --model opus \
  --thinking high \
  --announce
```

## Cost Considerations

| Mechanism                          | Cost Profile                                                            |
| ---------------------------------- | ----------------------------------------------------------------------- |
| Heartbeat                          | One turn every N minutes; scales with HEARTBEAT.md size |
| Cron (main)     | Adds event to next heartbeat (no isolated turn)      |
| Cron (isolated) | Full agent turn per job; can use cheaper model                          |

**Tips**:

- Keep `HEARTBEAT.md` small to minimize token overhead.
- Batch similar checks into heartbeat instead of multiple cron jobs.
- Use `target: "none"` on heartbeat if you only want internal processing.
- Use isolated cron with a cheaper model for routine tasks.

## Related

- [Heartbeat](/gateway/heartbeat) - full heartbeat configuration
- [Cron jobs](/automation/cron-jobs) - full cron CLI and API reference
- [System](/cli/system) - system events + heartbeat controls
