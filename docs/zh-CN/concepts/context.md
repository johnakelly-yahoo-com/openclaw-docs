---
summary: "24. 上下文：模型看到的内容、它是如何构建的，以及如何检查它"
read_when:
  - 25. 你想了解 OpenClaw 中“上下文”的含义
  - 26. 你正在调试为什么模型“知道”某些东西（或忘记了它）
  - 27. 你想减少上下文开销（/context, /status, /compact）
title: "28. 上下文"
---

# 29. 上下文

30. “上下文”是 **OpenClaw 在一次运行中发送给模型的所有内容**。 31. 它受模型的 **上下文窗口**（token 限制）约束。

32. 新手心智模型：

- 33. **系统提示**（由 OpenClaw 构建）：规则、工具、技能列表、时间/运行时，以及注入的工作区文件。
- 34. **对话历史**：本会话中你的消息 + 助手的消息。
- 35. **工具调用/结果 + 附件**：命令输出、文件读取、图像/音频等。

36. 上下文 _不等同于_ “记忆”：记忆可以存储到磁盘并在之后重新加载；上下文是模型当前窗口中的内容。

## 37. 快速开始（检查上下文）

- 38. `/status` → 快速查看“我的窗口有多满？”以及会话设置。
- 39. `/context list` → 注入了什么 + 大致大小（按文件 + 总计）。
- 40. `/context detail` → 更深入的拆解：按文件、按工具 schema 大小、按技能条目大小，以及系统提示大小。
- 41. `/usage tokens` → 在正常回复中附加每条回复的使用量页脚。
- 42. `/compact` → 将较早的历史总结为一个紧凑条目，以释放窗口空间。

43. 另请参阅：[Slash commands](/tools/slash-commands)、[Token use & costs](/reference/token-use)、[Compaction](/concepts/compaction)。

## 44. 示例输出

45. 数值因模型、提供方、工具策略以及你工作区中的内容而异。

### 46. `/context list`

```
47. 🧠 上下文拆解
Workspace: <workspaceDir>
Bootstrap max/file: 20,000 chars
Sandbox: mode=non-main sandboxed=false
System prompt (run): 38,412 chars (~9,603 tok) (Project Context 23,901 chars (~5,976 tok))

Injected workspace files:
- AGENTS.md: OK | raw 1,742 chars (~436 tok) | injected 1,742 chars (~436 tok)
- SOUL.md: OK | raw 912 chars (~228 tok) | injected 912 chars (~228 tok)
- TOOLS.md: TRUNCATED | raw 54,210 chars (~13,553 tok) | injected 20,962 chars (~5,241 tok)
- IDENTITY.md: OK | raw 211 chars (~53 tok) | injected 211 chars (~53 tok)
- USER.md: OK | raw 388 chars (~97 tok) | injected 388 chars (~97 tok)
- HEARTBEAT.md: MISSING | raw 0 | injected 0
- BOOTSTRAP.md: OK | raw 0 chars (~0 tok) | injected 0 chars (~0 tok)

Skills list (system prompt text): 2,184 chars (~546 tok) (12 skills)
Tools: read, edit, write, exec, process, browser, message, sessions_send, …
Tool list (system prompt text): 1,032 chars (~258 tok)
Tool schemas (JSON): 31,988 chars (~7,997 tok) (counts toward context; not shown as text)
Tools: (same as above)

Session tokens (cached): 14,250 total / ctx=32,000
```

### 48. `/context detail`

```
49. 🧠 上下文拆解（详细）
…
Top skills (prompt entry size):
- frontend-design: 412 chars (~103 tok)
- oracle: 401 chars (~101 tok)
… (+10 more skills)

Top tools (schema size):
- browser: 9,812 chars (~2,453 tok)
- exec: 6,240 chars (~1,560 tok)
… (+N more tools)
```

## 50. 哪些内容计入上下文窗口

Everything the model receives counts, including:

- System prompt (all sections).
- Conversation history.
- Tool calls + tool results.
- Attachments/transcripts (images/audio/files).
- Compaction summaries and pruning artifacts.
- Provider “wrappers” or hidden headers (not visible, still counted).

## How OpenClaw builds the system prompt

The system prompt is **OpenClaw-owned** and rebuilt each run. It includes:

- Tool list + short descriptions.
- Skills list (metadata only; see below).
- Workspace location.
- Time (UTC + converted user time if configured).
- Runtime metadata (host/OS/model/thinking).
- Injected workspace bootstrap files under **Project Context**.

Full breakdown: [System Prompt](/concepts/system-prompt).

## Injected workspace files (Project Context)

By default, OpenClaw injects a fixed set of workspace files (if present):

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `IDENTITY.md`
- `USER.md`
- `HEARTBEAT.md`
- `BOOTSTRAP.md` (first-run only)

Large files are truncated per-file using `agents.defaults.bootstrapMaxChars` (default `20000` chars). `/context` shows **raw vs injected** sizes and whether truncation happened.

## Skills: what’s injected vs loaded on-demand

The system prompt includes a compact **skills list** (name + description + location). This list has real overhead.

Skill instructions are _not_ included by default. The model is expected to `read` the skill’s `SKILL.md` **only when needed**.

## Tools: there are two costs

Tools affect context in two ways:

1. **Tool list text** in the system prompt (what you see as “Tooling”).
2. **Tool schemas** (JSON). These are sent to the model so it can call tools. They count toward context even though you don’t see them as plain text.

`/context detail` breaks down the biggest tool schemas so you can see what dominates.

## Commands, directives, and “inline shortcuts”

Slash commands are handled by the Gateway. There are a few different behaviors:

- **Standalone commands**: a message that is only `/...` runs as a command.
- **Directives**: `/think`, `/verbose`, `/reasoning`, `/elevated`, `/model`, `/queue` are stripped before the model sees the message.
  - Directive-only messages persist session settings.
  - Inline directives in a normal message act as per-message hints.
- **Inline shortcuts** (allowlisted senders only): certain `/...` tokens inside a normal message can run immediately (example: “hey /status”), and are stripped before the model sees the remaining text.

Details: [Slash commands](/tools/slash-commands).

## Sessions, compaction, and pruning (what persists)

1. 跨消息持久化的内容取决于具体机制：

- 2. **普通历史** 会在会话转录中持久化，直到根据策略被压缩或裁剪。
- 3. **压缩（Compaction）** 会将摘要持久化到转录中，并保持最近的消息不变。
- 4. **裁剪（Pruning）** 会从某次运行的 _内存中_ 提示里移除旧的工具结果，但不会重写转录。

5. 文档：[Session](/concepts/session)，[Compaction](/concepts/compaction)，[Session pruning](/concepts/session-pruning)。

## 6. `/context` 实际报告的内容

7. 当可用时，`/context` 优先使用最新的 **基于运行构建（run-built）** 的系统提示报告：

- 8. `System prompt (run)` = 从最近一次嵌入式（支持工具）的运行中捕获，并持久化到会话存储中。
- 9. `System prompt (estimate)` = 当不存在运行报告时（或通过不会生成该报告的 CLI 后端运行时）即时计算。

10. 无论哪种方式，它都会报告大小和主要贡献者；它 **不会** 输出完整的系统提示或工具架构。
