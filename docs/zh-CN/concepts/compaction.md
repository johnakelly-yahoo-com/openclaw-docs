---
summary: "Context window + compaction: how OpenClaw keeps sessions under model limits"
read_when:
  - You want to understand auto-compaction and /compact
  - You are debugging long sessions hitting context limits
title: "Compaction"
---

# Context Window & Compaction

Every model has a **context window** (max tokens it can see). Long-running chats accumulate messages and tool results; once the window is tight, OpenClaw **compacts** older history to stay within limits.

## What compaction is

Compaction **summarizes older conversation** into a compact summary entry and keeps recent messages intact. The summary is stored in the session history, so future requests use:

- The compaction summary
- Recent messages after the compaction point

Compaction **persists** in the session’s JSONL history.

## 1. 配置

2. 请参阅 [Compaction config & modes](/concepts/compaction) 了解 `agents.defaults.compaction` 的设置。

## 3. 自动压缩（默认开启）

4. 当会话接近或超过模型的上下文窗口时，OpenClaw 会触发自动压缩，并可能使用压缩后的上下文重试原始请求。

5. 你将看到：

- 6. 在详细模式中显示 `🧹 Auto-compaction complete`
- 7. `/status` 显示 `🧹 Compactions: <count>`

8. 在压缩之前，OpenClaw 可以运行一次 **静默内存刷新** 回合，将持久化笔记存储到磁盘。 9. 详情和配置请参阅 [Memory](/concepts/memory)。

## 10. 手动压缩

11. 使用 `/compact`（可选附带指令）来强制执行一次压缩：

```
12. /compact Focus on decisions and open questions
```

## 13. 上下文窗口来源

14. 上下文窗口是模型特定的。 15. OpenClaw 使用已配置的提供方目录中的模型定义来确定限制。

## 16. 压缩 vs 修剪

- 17. **压缩**：进行总结并以 JSONL 形式**持久化**。
- 18. **会话修剪**：仅修剪旧的 **工具结果**，**仅在内存中**，按请求进行。

19. 修剪详情请参阅 [/concepts/session-pruning](/concepts/session-pruning)。

## 20. 提示

- 21. 当会话感觉陈旧或上下文膨胀时，使用 `/compact`。
- 22. 大型工具输出已被截断；修剪可以进一步减少工具结果的堆积。
- 23. 如果你需要一个全新的开始，`/new` 或 `/reset` 会启动一个新的会话 ID。
