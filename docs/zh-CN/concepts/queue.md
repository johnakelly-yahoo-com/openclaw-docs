---
summary: "32. 将入站自动回复运行串行化的命令队列设计"
read_when:
  - 33. 更改自动回复的执行方式或并发度
title: "34. Command Queue"
---

# 35. Command Queue（2026-01-16）

36. 我们通过一个极小的进程内队列，将所有入站自动回复运行（所有渠道）进行串行化，以防止多个 agent 运行发生冲突，同时仍然允许跨会话的安全并行。

## 37. 原因

- 38. 自动回复运行可能代价高昂（LLM 调用），并且当多个入站消息在很短时间内到达时可能发生冲突。
- 39. 串行化可以避免争用共享资源（会话文件、日志、CLI stdin），并降低触发上游速率限制的概率。

## 40. 工作原理

- 41. 一个具备 lane 感知的 FIFO 队列会按 lane 进行消费，并带有可配置的并发上限（未配置的 lane 默认 1；main 默认为 4，subagent 为 8）。
- 42. `runEmbeddedPiAgent` 会按 **session key** 入队（lane `session:<key>`），以保证每个会话同一时间只有一个活动运行。
- 43. 每个会话运行随后会被排入一个 **全局 lane**（默认是 `main`），从而使整体并行度受 `agents.defaults.maxConcurrent` 限制。
- 44. 启用详细日志时，如果排队运行在开始前等待超过约 2 秒，会输出一条简短提示。
- 45. 输入指示器在入队时仍会立即触发（在渠道支持的情况下），因此在等待轮到我们时，用户体验不会改变。

## 46. 队列模式（按渠道）

47. 入站消息可以引导当前运行、等待下一轮，或两者兼有：

- 48. `steer`：立即注入到当前运行中（在下一个工具边界之后取消待执行的工具调用）。 49. 如果未进行流式处理，则回退为 followup。
- 50. `followup`：在当前运行结束后，排队进入下一次 agent 回合。
- 1. `collect`：将所有排队的消息合并为**单个**后续轮次（默认）。 2. 如果消息指向不同的频道/线程，它们会分别出队以保持路由。
- 3. `steer-backlog`（又名 `steer+backlog`）：立即引导**并且**保留消息用于后续轮次。
- 4. `interrupt`（旧版）：中止该会话的当前运行，然后运行最新的消息。
- 5. `queue`（旧版别名）：与 `steer` 相同。

6. Steer-backlog 意味着在被引导的运行之后还能获得一个后续响应，因此流式界面可能看起来像是重复的。 7. 如果你希望每条入站消息只得到一次响应，优先使用 `collect`/`steer`。
7. 发送 `/queue collect` 作为独立命令（按会话）或设置 `messages.queue.byChannel.discord: "collect"`。

9. 默认值（在配置中未设置时）：

- 10. 所有界面 → `collect`

11. 通过 `messages.queue` 全局或按频道配置：

```json5
12. {
  messages: {
    queue: {
      mode: "collect",
      debounceMs: 1000,
      cap: 20,
      drop: "summarize",
      byChannel: { discord: "collect" },
    },
  },
}
```

## 13. 队列选项

14. 选项适用于 `followup`、`collect` 和 `steer-backlog`（以及当 `steer` 回退到 followup 时）：

- 15. `debounceMs`：在开始后续轮次前等待一段静默时间（防止“继续、继续”）。
- 16. `cap`：每个会话的最大排队消息数。
- 17. `drop`：溢出策略（`old`、`new`、`summarize`）。

18. Summarize 会保留一份被丢弃消息的简短要点列表，并将其作为合成的后续提示注入。
19. 默认值：`debounceMs: 1000`、`cap: 20`、`drop: summarize`。

## 20. 按会话覆盖

- 21. 发送 `/queue <mode>` 作为独立命令，将模式存储到当前会话。
- 22. 选项可以组合：`/queue collect debounce:2s cap:25 drop:summarize`
- 23. `/queue default` 或 `/queue reset` 会清除会话级覆盖。

## 24. 范围与保证

- 25. 适用于所有使用网关回复管道的入站渠道上的自动回复代理运行（WhatsApp web、Telegram、Slack、Discord、Signal、iMessage、webchat 等）。
- 26. 默认通道（`main`）在进程范围内用于入站 + main 心跳；设置 `agents.defaults.maxConcurrent` 以允许多个会话并行。
- 27. 可能存在额外通道（例如 `cron`、`subagent`），以便后台作业可以并行运行而不阻塞入站回复。
- 28. 按会话的通道保证任意时刻只有一个代理运行会触及某个给定会话。
- 29. 无外部依赖或后台工作线程；纯 TypeScript + promises。

## 30. 故障排查

- 31. 如果命令看起来卡住了，启用详细日志并查找“queued for …ms”行以确认队列正在出队。
- 18. 如果你需要队列深度，请启用详细日志并关注队列计时相关的日志行。
