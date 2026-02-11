---
summary: "43. 子代理：生成隔离的代理运行，并将结果回传并公告到请求者的聊天中"
read_when:
  - 44. 当你希望通过代理进行后台/并行工作时
  - 45. 当你正在更改 sessions_spawn 或子代理工具策略时
title: "46. 子代理"
---

# 子代理

子代理允许你在不阻塞主对话的情况下运行后台任务。 当你生成一个子代理时，它会在自己的隔离会话中运行，完成工作后将结果回传到聊天中。

**使用场景：**

- 在主代理继续回答问题的同时研究某个主题
- 并行运行多个耗时任务（网页抓取、代码分析、文件处理）
- 在多代理架构中将任务委派给专门的代理

## 快速开始

使用子代理最简单的方法是自然地向你的代理提出请求：

> "生成一个子代理来研究最新的 Node.js 发布说明"

代理会在幕后调用 `sessions_spawn` 工具。 当子代理完成时，它会将发现结果回传到你的聊天中。

你也可以明确指定选项：

> "生成一个子代理来分析今天的服务器日志。 使用 gpt-5.2，并设置 5 分钟超时。"

## 工作原理

<Steps>
  <Step title="Main agent spawns">
    主代理使用任务描述调用 `sessions_spawn`。 该调用是 **非阻塞** 的——主代理会立即收到 `{ status: "accepted", runId, childSessionKey }`。
  </Step>
  <Step title="Sub-agent runs in the background">会创建一个新的隔离会话（`agent:
:subagent:
`），并运行在专用的 `subagent` 队列通道上。<agentId>当子代理完成时，它会将发现结果回传到请求者的聊天中。<uuid>主代理会发布一段自然语言摘要。</Step>
  <Step title="Result is announced">
    子代理会话在 60 分钟后自动归档（可配置）。 会话记录会被保留。
  </Step>
  <Step title="Session is archived">
    每个子代理都有其 **独立** 的上下文和令牌用量。 为子代理设置更便宜的模型以节省成本——参见下方的 [Setting a Default Model](#setting-a-default-model)。
  </Step>
</Steps>

<Tip>
配置 子代理开箱即用，无需任何配置。
</Tip>

## 默认值：

模型：目标代理的常规模型选择（除非设置了 `subagents.model`） 思考：不对子代理进行覆盖（除非设置了 `subagents.thinking`）

- 最大并发数：8
- 自动归档：60 分钟后
- 设置默认模型
- 为子代理使用更便宜的模型以节省令牌成本：

### {&#xA;agents: {&#xA;defaults: {&#xA;subagents: {&#xA;model: "minimax/MiniMax-M2.1",&#xA;},&#xA;},&#xA;},&#xA;}

设置默认思考级别

```json5
{
  agents: {
    defaults: {
      subagents: {
        thinking: "low",
      },
    },
  },
}
```

### 按代理覆盖

```json5
在多代理架构中，你可以为每个代理设置子代理的默认值：
```

### {&#xA;agents: {&#xA;list: [&#xA;{&#xA;id: "researcher",&#xA;subagents: {&#xA;model: "anthropic/claude-sonnet-4",&#xA;},&#xA;},&#xA;{&#xA;id: "assistant",&#xA;subagents: {&#xA;model: "minimax/MiniMax-M2.1",&#xA;},&#xA;},&#xA;],&#xA;},&#xA;}

控制同时运行的子代理数量：

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxConcurrent: 4, // default: 8
      },
    },
  },
}
```

### Concurrency

子代理使用独立于主代理队列的专用队列通道（`subagent`），因此子代理的运行不会阻塞入站回复。

```json5
自动归档
```

Sub-agents use a dedicated queue lane (`subagent`) separate from the main agent queue, so sub-agent runs don't block inbound replies.

### Auto-Archive

子代理会话会在可配置的时间段后自动归档：

```json5
{
  agents: {
    defaults: {
      subagents: {
        archiveAfterMinutes: 120, // default: 60
      },
    },
  },
}
```

<Note>归档会将会话记录重命名为 `*.deleted.<timestamp>`（同一文件夹）—— 会话记录会被保留，而不是删除。 自动归档计时器是尽力而为的；如果网关重启，尚未触发的计时器将会丢失。
</Note>

## `sessions_spawn` 工具

这是代理用于创建子代理的工具。

### 参数

| 参数                  | 类型                       | 默认值                           | 描述                                    |
| ------------------- | ------------------------ | ----------------------------- | ------------------------------------- |
| `task`              | string                   | _(必填)_     | 子代理需要执行的任务                            |
| `label`             | string                   | —                             | 用于识别的简短标签                             |
| `agentId`           | string                   | _(调用者的代理)_ | 在不同的代理 ID 下生成（必须被允许）                  |
| `model`             | string                   | _(可选)_     | 为该子代理覆盖模型                             |
| `thinking`          | string                   | _(可选)_     | 覆盖思考级别（`off`、`low`、`medium`、`high` 等） |
| `runTimeoutSeconds` | number                   | `0`（无限制）                      | 在 N 秒后中止子代理                           |
| `cleanup`           | `"delete"` \\| `"keep"` | `"keep"`                      | `"delete"` 会在公告后立即归档                  |

### 模型解析顺序

子代理模型按以下顺序解析（先匹配者生效）：

1. 在 `sessions_spawn` 调用中显式指定的 `model` 参数
2. 按代理配置：`agents.list[].subagents.model`
3. 全局默认值：`agents.defaults.subagents.model`
4. 目标代理为新会话使用的常规模型解析

思考级别按以下顺序解析：

1. 在 `sessions_spawn` 调用中显式指定的 `thinking` 参数
2. 按代理配置：`agents.list[].subagents.thinking`
3. 全局默认值：`agents.defaults.subagents.thinking`
4. Otherwise no sub-agent-specific thinking override is applied

<Note>
Invalid model values are silently skipped — the sub-agent runs on the next valid default with a warning in the tool result.
</Note>

### Cross-Agent Spawning

By default, sub-agents can only spawn under their own agent id. To allow an agent to spawn sub-agents under other agent ids:

```json5
{
  agents: {
    list: [
      {
        id: "orchestrator",
        subagents: {
          allowAgents: ["researcher", "coder"], // or ["*"] to allow any
        },
      },
    ],
  },
}
```

<Tip>
Use the `agents_list` tool to discover which agent ids are currently allowed for `sessions_spawn`.
</Tip>

## Managing Sub-Agents (`/subagents`)

Use the `/subagents` slash command to inspect and control sub-agent runs for the current session:

| Command                                      | Description                                                       |
| -------------------------------------------- | ----------------------------------------------------------------- |
| 47. `/subagents list` | List all sub-agent runs (active and completed) |
| `/subagents stop <id\\|#\\|all>`           | Stop a running sub-agent                                          |
| `/subagents log <id\\|#> [limit] [tools]`   | View sub-agent transcript                                         |
| `/subagents info <id\\|#>`                  | Show detailed run metadata                                        |
| `/subagents send <id\\|#> <message>`        | Send a message to a running sub-agent                             |

You can reference sub-agents by list index (`1`, `2`), run id prefix, full session key, or `last`.

<AccordionGroup>
  <Accordion title="Example: list and stop a sub-agent">
    ```
    /subagents list
    ```

    ````
    ```
    🧭 Subagents (current session)
    Active: 1 · Done: 2
    1) ✅ · research logs · 2m31s · run a1b2c3d4 · agent:main:subagent:...
    2) ✅ · check deps · 45s · run e5f6g7h8 · agent:main:subagent:...
    3) 🔄 · deploy staging · 1m12s · run i9j0k1l2 · agent:main:subagent:...
    ```
    
    ```
    /subagents stop 3
    ```
    
    ```
    ⚙️ Stop requested for deploy staging.
    ```
    ````

  </Accordion>
  <Accordion title="Example: inspect a sub-agent">
    ```
    /subagents info 1
    ```

    ````
    ```
    ℹ️ Subagent info
    Status: ✅
    Label: research logs
    Task: Research the latest server error logs and summarize findings
    Run: a1b2c3d4-...
    Session: agent:main:subagent:...
    Runtime: 2m31s
    Cleanup: keep
    Outcome: ok
    ```
    ````

  </Accordion>
  <Accordion title="Example: view sub-agent log">
    ```
    /subagents log 1 10
    ```

    ````
    Shows the last 10 messages from the sub-agent's transcript. Add `tools` to include tool call messages:
    
    ```
    /subagents log 1 10 tools
    ```
    ````

  </Accordion>
  <Accordion title="Example: send a follow-up message">
    ```
    /subagents send 3 "Also check the staging environment"
    ```

    ```
    Sends a message into the running sub-agent's session and waits up to 30 seconds for a reply.
    ```

  </Accordion>
</AccordionGroup>

## Announce (How Results Come Back)

When a sub-agent finishes, it goes through an **announce** step:

1. The sub-agent's final reply is captured
2. A summary message is sent to the main agent's session with the result, status, and stats
3. The main agent posts a natural-language summary to your chat

50) 公告式回复在可用时会保留线程/主题路由（Slack 线程、Telegram 话题、Matrix 线程）。

### Announce Stats

Each announce includes a stats line with:

- Runtime duration
- Token usage (input/output/total)
- Estimated cost (when model pricing is configured via `models.providers.*.models[].cost`)
- Session key, session id, and transcript path

### Announce Status

The announce message includes a status derived from the runtime outcome (not from model output):

- **successful completion** (`ok`) — task completed normally
- **error** — task failed (error details in notes)
- **timeout** — task exceeded `runTimeoutSeconds`
- **unknown** — status could not be determined

<Tip>
If no user-facing announcement is needed, the main-agent summarize step can return `NO_REPLY` and nothing is posted.
This is different from `ANNOUNCE_SKIP`, which is used in agent-to-agent announce flow (`sessions_send`).
</Tip>

## Tool Policy

By default, sub-agents get **all tools except** a set of denied tools that are unsafe or unnecessary for background tasks:

<AccordionGroup>
  <Accordion title="Default denied tools">
    | Denied tool | Reason |
    |-------------|--------|
    | `sessions_list` | Session management — main agent orchestrates |
    | `sessions_history` | Session management — main agent orchestrates |
    | `sessions_send` | Session management — main agent orchestrates |
    | `sessions_spawn` | No nested fan-out (sub-agents cannot spawn sub-agents) |
    | `gateway` | System admin — dangerous from sub-agent |
    | `agents_list` | System admin |
    | `whatsapp_login` | Interactive setup — not a task |
    | `session_status` | Status/scheduling — main agent coordinates |
    | `cron` | Status/scheduling — main agent coordinates |
    | `memory_search` | Pass relevant info in spawn prompt instead |
    | `memory_get` | Pass relevant info in spawn prompt instead |
  </Accordion>
</AccordionGroup>

### Customizing Sub-Agent Tools

You can further restrict sub-agent tools:

```json5
{
  tools: {
    subagents: {
      tools: {
        // deny always wins over allow
        deny: ["browser", "firecrawl"],
      },
    },
  },
}
```

To restrict sub-agents to **only** specific tools:

```json5
{
  tools: {
    subagents: {
      tools: {
        allow: ["read", "exec", "process", "write", "edit", "apply_patch"],
        // deny still wins if set
      },
    },
  },
}
```

<Note>
Custom deny entries are **added to** the default deny list. If `allow` is set, only those tools are available (the default deny list still applies on top).
</Note>

## 48. 认证

49. 子代理认证是通过 **代理 ID** 解析的，而不是通过会话类型：

- The auth store is loaded from the target agent's `agentDir`
- The main agent's auth profiles are merged in as a **fallback** (agent profiles win on conflicts)
- The merge is additive — main profiles are always available as fallbacks

<Note>
Fully isolated auth per sub-agent is not currently supported.
</Note>

## Context and System Prompt

Sub-agents receive a reduced system prompt compared to the main agent:

- **Included:** Tooling, Workspace, Runtime sections, plus `AGENTS.md` and `TOOLS.md`
- **Not included:** `SOUL.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOTSTRAP.md`

The sub-agent also receives a task-focused system prompt that instructs it to stay focused on the assigned task, complete it, and not act as the main agent.

## Stopping Sub-Agents

| Method                 | Effect                                                                    |
| ---------------------- | ------------------------------------------------------------------------- |
| `/stop` in the chat    | Aborts the main session **and** all active sub-agent runs spawned from it |
| `/subagents stop <id>` | Stops a specific sub-agent without affecting the main session             |
| `runTimeoutSeconds`    | Automatically aborts the sub-agent run after the specified time           |

<Note>
`runTimeoutSeconds` does **not** auto-archive the session. The session remains until the normal archive timer fires.
</Note>

## Full Configuration Example

<Accordion title="Complete sub-agent configuration">
```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-sonnet-4" },
      subagents: {
        model: "minimax/MiniMax-M2.1",
        thinking: "low",
        maxConcurrent: 4,
        archiveAfterMinutes: 30,
      },
    },
    list: [
      {
        id: "main",
        default: true,
        name: "Personal Assistant",
      },
      {
        id: "ops",
        name: "Ops Agent",
        subagents: {
          model: "anthropic/claude-sonnet-4",
          allowAgents: ["main"], // ops can spawn sub-agents under "main"
        },
      },
    ],
  },
  tools: {
    subagents: {
      tools: {
        deny: ["browser"], // sub-agents can't use the browser
      },
    },
  },
}
```
</Accordion>

## Limitations

<Warning>
- **Best-effort announce:** If the gateway restarts, pending announce work is lost.
- **No nested spawning:** Sub-agents cannot spawn their own sub-agents.
- **Shared resources:** Sub-agents share the gateway process; use `maxConcurrent` as a safety valve.
- **Auto-archive is best-effort:** Pending archive timers are lost on gateway restart.
</Warning>

## See Also

- [Session Tools](/concepts/session-tool) — details on `sessions_spawn` and other session tools
- [Multi-Agent Sandbox and Tools](/tools/multi-agent-sandbox-tools) — per-agent tool restrictions and sandboxing
- [Configuration](/gateway/configuration) — `agents.defaults.subagents` reference
- [Queue](/concepts/queue) — how the `subagent` lane works
