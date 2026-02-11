---
summary: "Research notes: offline memory system for Clawd workspaces (Markdown source-of-truth + derived index)"
read_when:
  - Designing workspace memory (~/.openclaw/workspace) beyond daily Markdown logs
  - Deciding: standalone CLI vs deep OpenClaw integration
  - Adding offline recall + reflection (retain/recall/reflect)
title: "Workspace Memory Research"
---

# Workspace Memory v2 (offline): research notes

Target: Clawd-style workspace (`agents.defaults.workspace`, default `~/.openclaw/workspace`) where “memory” is stored as one Markdown file per day (`memory/YYYY-MM-DD.md`) plus a small set of stable files (e.g. `memory.md`, `SOUL.md`).

This doc proposes an **offline-first** memory architecture that keeps Markdown as the canonical, reviewable source of truth, but adds **structured recall** (search, entity summaries, confidence updates) via a derived index.

## Why change?

The current setup (one file per day) is excellent for:

- “append-only” journaling
- human editing
- git-backed durability + auditability
- low-friction capture (“just write it down”)

It’s weak for:

- high-recall retrieval (“what did we decide about X?”, “last time we tried Y?”)
- entity-centric answers (“tell me about Alice / The Castle / warelay”) without rereading many files
- opinion/preference stability (and evidence when it changes)
- time constraints (“what was true during Nov 2025?”) and conflict resolution

## Design goals

- **Offline**: works without network; can run on laptop/Castle; no cloud dependency.
- **Explainable**: retrieved items should be attributable (file + location) and separable from inference.
- **Low ceremony**: daily logging stays Markdown, no heavy schema work.
- 1. **增量式**：v1 仅需 FTS 即可有用；语义/向量与图谱是可选升级。
- 2. **对代理友好**：让“在 token 预算内进行回忆”变得容易（返回小型事实包）。

## 3. 北极星模型（Hindsight × Letta）

4. 需要融合的两部分：

1. 5. **Letta/MemGPT 风格的控制循环**

- 6) 始终在上下文中保留一个小型“核心”（人格 + 关键用户事实）
- 7. 其他一切都在上下文之外，并通过工具检索
- 8. 内存写入是显式的工具调用（append/replace/insert），持久化后在下一轮重新注入

2. 9. **Hindsight 风格的记忆基底**

- 10) 区分“观察到的”“相信的”“总结的”
- 11. 支持 retain / recall / reflect
- 12. 带有置信度、且可随证据演化的观点
- 13. 实体感知的检索 + 时间查询（即使没有完整的知识图谱）

## 14. 提议的架构（Markdown 为唯一事实源 + 派生索引）

### 15. 规范存储（对 git 友好）

16. 将 `~/.openclaw/workspace` 作为规范的人类可读记忆。

17. 建议的 workspace 布局：

```
18. ~/.openclaw/workspace/
  memory.md                    # 小：持久事实 + 偏好（偏核心）
  memory/
    YYYY-MM-DD.md              # 每日日志（追加；叙事）
  bank/                        # “类型化”的记忆页面（稳定、可审阅）
    world.md                   # 关于世界的客观事实
    experience.md              # 代理做了什么（第一人称）
    opinions.md                # 主观偏好/判断 + 置信度 + 证据指针
    entities/
      Peter.md
      The-Castle.md
      warelay.md
      ...
```

19. 备注：

- 20. **每日日志就保持为每日日志**。 21. 无需把它变成 JSON。
- 22. `bank/` 文件是**经整理的**，由反思任务生成，且仍可手动编辑。
- 23. `memory.md` 仍然保持“小 + 偏核心”：你希望 Clawd 每次会话都看到的内容。

### 24. 派生存储（机器回忆）

25. 在 workspace 下添加一个派生索引（不一定纳入 git）：

```
26. ~/.openclaw/workspace/.memory/index.sqlite
```

27. 其后端包括：

- 28. 用于事实 + 实体链接 + 观点元数据的 SQLite schema
- 29. 用于词法回忆的 SQLite **FTS5**（快速、体积小、离线）
- 30. 可选的嵌入表用于语义回忆（仍然离线）

31. 该索引始终**可从 Markdown 重建**。

## 32. Retain / Recall / Reflect（操作循环）

### 33. Retain：将每日日志规范化为“事实”

34. Hindsight 在此最重要的洞见：存储**叙事性的、自包含的事实**，而不是微小片段。

35. 针对 `memory/YYYY-MM-DD.md` 的实用规则：

- 36. 在一天结束时（或过程中），添加一个 `## Retain` 小节，包含 2–5 条要点，这些要点应当：
  - 37. 具有叙事性（保留跨轮次上下文）
  - 38. 自包含（单独拿出来之后仍然有意义）
  - 39. 带有类型标签 + 实体提及

40. 示例：

```
41. ## Retain
- W @Peter: 目前在马拉喀什（2025-11-27 至 12-01）为 Andy 过生日。
- B @warelay: 我通过在 connection.update 处理器中包裹 try/catch 修复了 Baileys WS 崩溃（见 memory/2025-11-27.md）。
- O(c=0.95) @Peter: 在 WhatsApp 上偏好简洁回复（<1500 字符）；较长内容放入文件。
```

42. 最小化解析：

- 43. 类型前缀：`W`（世界），`B`（经历/传记），`O`（观点），`S`（观察/总结；通常生成）
- 44. 实体：`@Peter`、`@warelay` 等（slug 映射到 `bank/entities/*.md`）
- 45. 观点置信度：`O(c=0.0..1.0)` 可选

If you don’t want authors to think about it: the reflect job can infer these bullets from the rest of the log, but having an explicit `## Retain` section is the easiest “quality lever”.

### Recall: queries over the derived index

48. Recall 应支持：

- 49. **词法**：“查找精确术语 / 名称 / 命令”（FTS5）
- 50. **实体**：“告诉我关于 X 的信息”（实体页面 + 与实体关联的事实）
- 1. **temporal**："11 月 27 日前后发生了什么" / "自上周以来"
- 2. **opinion**："Peter 更偏好什么？" 3.（包含置信度 + 证据）

4. 返回格式应当对 agent 友好并能引用来源：

- `kind` (`world|experience|opinion|observation`)
- 6. `timestamp`（来源日期，或在存在时抽取的时间范围）
- 7. `entities`（`["Peter","warelay"]`）
- `content` (the narrative fact)
- 9. `source`（`memory/2025-11-27.md#L12` 等）

### 10. 反思：生成稳定页面 + 更新信念

Reflection is a scheduled job (daily or heartbeat `ultrathink`) that:

- 12. 从近期事实更新 `bank/entities/*.md`（实体摘要）
- 13. 基于强化/矛盾更新 `bank/opinions.md` 中的置信度
- 14. 可选地提出对 `memory.md` 的编辑建议（“偏核心”的持久事实）

15. 观点演化（简单、可解释）：

- 16. 每个观点包含：
  - 17. 陈述
  - 18. 置信度 `c ∈ [0,1]`
  - 19. `last_updated`
  - 20. 证据链接（支持 + 反驳的事实 ID）
- 21. 当新事实到达时：
  - 22. 通过实体重叠 + 相似度查找候选观点（先用 FTS，之后再用向量）
  - 23. 以小幅增量更新置信度；大的跃迁需要强烈的反驳 + 重复证据

## 24. CLI 集成：独立 vs 深度集成

25. 建议：**在 OpenClaw 中进行深度集成**，但保留一个可分离的核心库。

### 26. 为什么要集成到 OpenClaw？

- 27. OpenClaw 已经知道：
  - 28. 工作区路径（`agents.defaults.workspace`）
  - 29. 会话模型 + 心跳机制
  - 30. 日志记录 + 故障排查模式
- 31. 你希望由 agent 自身来调用工具：
  - 32. `openclaw memory recall "…" --k 25 --since 30d`
  - 33. `openclaw memory reflect --since 7d`

### 34. 为什么仍要拆分成一个库？

- 35. 让内存逻辑在没有网关/运行时的情况下也可测试
- 36. 便于在其他上下文中复用（本地脚本、未来的桌面应用等）

37. 形态：
    内存工具的目标是一个小型 CLI + 库层，但这目前只是探索性的。

## 38. “S-Collide” / SuCo：何时使用它（研究）

39. 如果 “S-Collide” 指的是 **SuCo（Subspace Collision）**：这是一种 ANN 检索方法，通过在子空间中使用学习/结构化的碰撞来实现强召回率/低延迟的权衡（论文：arXiv 2411.14754，2024）。

40. 针对 `~/.openclaw/workspace` 的务实建议：

- 41. **不要一开始就用** SuCo。
- 42. 从 SQLite FTS +（可选）简单向量嵌入开始；你会立刻获得大多数 UX 收益。
- 43. 只有在以下情况下才考虑 SuCo/HNSW/ScaNN 类方案：
  - 44. 语料规模很大（数万/数十万条 chunk）
  - 45. 暴力向量搜索变得过慢
  - 46. 召回质量明显被词法搜索所瓶颈

47. 离线友好的替代方案（按复杂度递增）：

- 48. SQLite FTS5 + 元数据过滤（零 ML）
- 49. 向量嵌入 + 暴力搜索（在 chunk 数量较低时效果出奇地好）
- 50. HNSW 索引（常见、稳健；需要库绑定）
- 1. SuCo（研究级；如果有一个你可以嵌入的可靠实现会很有吸引力）

2. 开放问题：

- 3. 在你的机器（笔记本 + 台式机）上，用于“个人助理记忆”的**最佳**离线嵌入模型是什么？
  - 4. 如果你已经有 Ollama：用本地模型做嵌入；否则就在工具链中随附一个小型嵌入模型。

## 5. 最小但有用的试点

6. 如果你想要一个最小但仍然有用的版本：

- 7. 添加 `bank/` 实体页面，并在每日日志中加入一个 `## Retain` 小节。
- 8. 使用 SQLite FTS 进行带引用的回忆（路径 + 行号）。
- 9. 只有在回忆质量或规模需要时才添加嵌入。

## 10. 参考

- Letta / MemGPT concepts: “core memory blocks” + “archival memory” + tool-driven self-editing memory.
- 12. Hindsight 技术报告：“retain / recall / reflect”，四网络记忆，叙事事实抽取，观点置信度演化。
- 13. SuCo：arXiv 2411.14754（2024）：“子空间碰撞（Subspace Collision）”近似最近邻检索。
