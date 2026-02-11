---
title: 21. Lobster
summary: "22. 面向 OpenClaw 的类型化工作流运行时，支持可恢复的审批关卡。"
description: 23. 面向 OpenClaw 的类型化工作流运行时——带审批关卡的可组合流水线。
read_when:
  - 24. 你需要具有显式审批的确定性多步骤工作流
  - 25. 你需要在不重新运行早期步骤的情况下恢复工作流
---

# 26. Lobster

27. Lobster 是一个工作流 shell，使 OpenClaw 能将多步骤工具序列作为一次、具有显式审批检查点的确定性操作来运行。

## 28. Hook

29. 你的助手可以构建管理自身的工具。 30. 提出一个工作流需求，30 分钟后你就能得到一个 CLI 以及作为一次调用运行的流水线。 31. Lobster 是缺失的那一块：确定性的流水线、显式审批，以及可恢复的状态。

## 32. 为什么

33. 如今，复杂的工作流需要大量来回的工具调用。 34. 每次调用都会消耗 token，而且 LLM 必须编排每一个步骤。 35. Lobster 将这种编排移入一个类型化运行时：

- 36. **一次调用而非多次**：OpenClaw 运行一次 Lobster 工具调用并获得结构化结果。
- 37. **内置审批**：副作用（发送邮件、发布评论）会使工作流暂停，直到被明确批准。
- 38. **可恢复**：暂停的工作流会返回一个 token；批准后即可恢复，而无需重新运行所有内容。

## 39. 为什么使用 DSL 而不是普通程序？

40. Lobster 被有意设计得很小。 41. 目标不是“一种新语言”，而是一个可预测、对 AI 友好的流水线规范，具备一等公民的审批与恢复 token。

- 42. **内置批准/恢复**：普通程序可以提示人工操作，但如果不自行发明运行时，就无法用一个持久 token 来实现_暂停和恢复_。
- 43. **确定性 + 可审计性**：流水线是数据，因此易于记录、对比、重放和审查。
- **Constrained surface for AI**: A tiny grammar + JSON piping reduces “creative” code paths and makes validation realistic.
- 45. **内置安全策略**：超时、输出上限、沙箱检查和白名单由运行时强制执行，而不是由每个脚本各自处理。
- 46. **仍然可编程**：每个步骤都可以调用任意 CLI 或脚本。 47. 如果你想用 JS/TS，可从代码生成 `.lobster` 文件。

## 48. 工作原理

49. OpenClaw 以**工具模式**启动本地 `lobster` CLI，并从 stdout 解析一个 JSON 封装。
50. 如果流水线因审批而暂停，工具会返回一个 `resumeToken`，以便你稍后继续。

## 模式：小型 CLI + JSON 管道 + 审批

构建只说 JSON 的小命令，然后将它们串联成一次 Lobster 调用。 （下面是示例命令名——请替换为你自己的。）

```bash
inbox list --json
inbox categorize --json
inbox apply --json
```

```json
{
  "action": "run",
  "pipeline": "exec --json --shell 'inbox list --json' | exec --stdin json --shell 'inbox categorize --json' | exec --stdin json --shell 'inbox apply --json' | approve --preview-from-stdin --limit 5 --prompt 'Apply changes?'",
  "timeoutMs": 30000
}
```

如果管道请求审批，请使用该令牌继续：

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

AI 触发工作流；Lobster 执行各个步骤。 审批关卡使副作用保持显式且可审计。

示例：将输入项映射为工具调用：

```bash
gog.gmail.search --query 'newer_than:1d' \
  | openclaw.invoke --tool message --action send --each --item-key message --args-json '{"provider":"telegram","to":"..."}'
```

## 仅 JSON 的 LLM 步骤（llm-task）

对于需要 **结构化 LLM 步骤** 的工作流，启用可选的
`llm-task` 插件工具，并从 Lobster 调用它。 这样既能保持工作流的确定性，又允许你使用模型进行分类 / 摘要 / 起草。

启用该工具：

```json
{
  "plugins": {
    "entries": {
      "llm-task": { "enabled": true }
    }
  },
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "allow": ["llm-task"] }
      }
    ]
  }
}
```

在管道中使用：

```lobster
openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
  "input": { "subject": "Hello", "body": "Can you help?" },
  "schema": {
    "type": "object",
    "properties": {
      "intent": { "type": "string" },
      "draft": { "type": "string" }
    },
    "required": ["intent", "draft"],
    "additionalProperties": false
  }
}'
```

有关详情和配置选项，请参见 [LLM Task](/tools/llm-task)。

## 工作流文件（.lobster）

Lobster 可以运行 YAML/JSON 工作流文件，包含 `name`、`args`、`steps`、`env`、`condition` 和 `approval` 字段。 在 OpenClaw 工具调用中，将 `pipeline` 设置为文件路径。

```yaml
name: inbox-triage
args:
  tag:
    default: "family"
steps:
  - id: collect
    command: inbox list --json
  - id: categorize
    command: inbox categorize --json
    stdin: $collect.stdout
  - id: approve
    command: inbox apply --approve
    stdin: $categorize.stdout
    approval: required
  - id: execute
    command: inbox apply --execute
    stdin: $categorize.stdout
    condition: $approve.approved
```

注意：

- `stdin: $step.stdout` 和 `stdin: $step.json` 会传递上一步的输出。
- `condition`（或 `when`）可以基于 `$step.approved` 来控制步骤是否执行。

## 安装 Lobster

在运行 OpenClaw Gateway 的 **同一主机** 上安装 Lobster CLI（参见 [Lobster repo](https://github.com/openclaw/lobster)），并确保 `lobster` 在 `PATH` 中。
如果你想使用自定义的二进制位置，请在工具调用中传入 **绝对** 的 `lobsterPath`。

## 启用该工具

Lobster 是一个 **可选** 插件工具（默认未启用）。

推荐（增量式，安全）：

```json
{
  "tools": {
    "alsoAllow": ["lobster"]
  }
}
```

Or per-agent:

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "alsoAllow": ["lobster"]
        }
      }
    ]
  }
}
```

除非你打算在受限的允许列表模式下运行，否则请避免使用 `tools.allow: ["lobster"]`。

注意：允许列表是针对可选插件的选择性启用机制。 如果你的允许列表只包含
插件工具（如 `lobster`），OpenClaw 仍会保持核心工具启用。 若要限制核心
工具，也需要将你希望启用的核心工具或工具组加入允许列表。

## 示例：邮件分拣

不使用 Lobster：

```
用户：“检查我的邮件并起草回复”
→ openclaw 调用 gmail.list
→ LLM 总结
→ 用户：“给 #2 和 #5 起草回复”
→ LLM 起草
→ 用户：“发送 #2”
→ openclaw 调用 gmail.send
（每天重复，对已分拣内容没有记忆）
```

With Lobster:

```json
{
  "action": "run",
  "pipeline": "email.triage --limit 20",
  "timeoutMs": 30000
}
```

返回一个 JSON 信封（已截断）：

```json
{
  "ok": true,
  "status": "needs_approval",
  "output": [{ "summary": "5 need replies, 2 need action" }],
  "requiresApproval": {
    "type": "approval_request",
    "prompt": "Send 2 draft replies?",
    "items": [],
    "resumeToken": "..."
  }
}
```

用户批准 → 继续：

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

一个工作流。 确定性。 1. 安全。

## 2. 工具参数

### `run`

4. 在工具模式下运行一个流水线。

```json
{
  "action": "run",
  "pipeline": "gog.gmail.search --query 'newer_than:1d' | email.triage",
  "cwd": "/path/to/workspace",
  "timeoutMs": 30000,
  "maxStdoutBytes": 512000
}
```

Run a workflow file with args:

```json
{
  "action": "run",
  "pipeline": "/path/to/inbox-triage.lobster",
  "argsJson": "{\"tag\":\"family\"}"
}
```

### `resume`

9. 在获得批准后继续已暂停的工作流。

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

### 11. 可选输入

- 12. `lobsterPath`：Lobster 二进制文件的绝对路径（省略则使用 `PATH`）。
- `cwd`: Working directory for the pipeline (defaults to the current process working directory).
- 14. `timeoutMs`：如果子进程超过此时长则将其终止（默认：20000）。
- 15. `maxStdoutBytes`：如果 stdout 超过此大小则将子进程终止（默认：512000）。
- 16. `argsJson`：传递给 `lobster run --args-json` 的 JSON 字符串（仅适用于工作流文件）。

## Output envelope

18. Lobster 返回一个 JSON 封装，包含以下三种状态之一：

- 19. `ok` → 成功完成
- `needs_approval` → paused; `requiresApproval.resumeToken` is required to resume
- 21. `cancelled` → 被明确拒绝或已取消

22. 该工具会在 `content`（美化后的 JSON）和 `details`（原始对象）中同时呈现该封装。

## 23. 批准

24. 如果存在 `requiresApproval`，请检查提示并做出决定：

- 25. `approve: true` → 恢复并继续执行副作用
- 26. `approve: false` → 取消并结束工作流

27. 使用 `approve --preview-from-stdin --limit N` 可在无需自定义 jq/HereDoc 拼装的情况下，将 JSON 预览附加到审批请求中。 28. 恢复令牌现在更加精简：Lobster 会将工作流的恢复状态存储在其状态目录下，并返回一个小型的令牌键。

## 29. OpenProse

30. OpenProse 与 Lobster 搭配良好：使用 `/prose` 来编排多代理的准备工作，然后运行 Lobster 流水线以实现确定性的审批。 31. 如果某个 Prose 程序需要 Lobster，可通过 `tools.subagents.tools` 允许子代理使用 `lobster` 工具。 32. 参见 [OpenProse](/prose)。

## 33. 安全性

- 34. **仅本地子进程** —— 插件本身不进行任何网络调用。
- 35. **无密钥** —— Lobster 不管理 OAuth；它会调用负责此事的 OpenClaw 工具。
- 36. **沙箱感知** —— 当工具上下文处于沙箱环境时将被禁用。
- 37. **加固** —— 如果指定了 `lobsterPath`，则必须为绝对路径；并强制执行超时和输出上限。

## 38. 故障排除

- 39. **`lobster subprocess timed out`** → 增加 `timeoutMs`，或拆分较长的流水线。
- **`lobster output exceeded maxStdoutBytes`** → raise `maxStdoutBytes` or reduce output size.
- 41. **`lobster returned invalid JSON`** → 确保流水线在工具模式下运行，并且只输出 JSON。
- 42. **`lobster failed (code …)`** → 在终端中运行相同的流水线以检查 stderr。

## 43. 了解更多

- [Plugins](/tools/plugin)
- [Plugin tool authoring](/plugins/agent-tools)

## 46. 案例研究：社区工作流

47. 一个公开示例：“第二大脑”CLI + Lobster 流水线，用于管理三个 Markdown 知识库（个人、伴侣、共享）。 48. 该 CLI 会为统计信息、收件箱列表和过期扫描输出 JSON；Lobster 将这些命令串联成诸如 `weekly-review`、`inbox-triage`、`memory-consolidation` 和 `shared-task-sync` 的工作流，并在其中设置审批关卡。 49. 当条件允许时，AI 负责判断（分类）；在不可用时则回退到确定性的规则。

- Thread: [https://x.com/plattenschieber/status/2014508656335770033](https://x.com/plattenschieber/status/2014508656335770033)
- Repo：[https://github.com/bloomedai/brain-cli](https://github.com/bloomedai/brain-cli)
