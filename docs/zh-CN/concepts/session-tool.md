---
summary: "23. 用于列出会话、获取历史记录以及发送跨会话消息的代理会话工具"
read_when:
  - Adding or modifying session tools
title: "24. 会话工具"
---

# Session Tools

Goal: small, hard-to-misuse tool set so agents can list sessions, fetch history, and send to another session.

## Tool Names

- `sessions_list`
- `sessions_history`
- `sessions_send`
- `sessions_spawn`

## Key Model

- Main direct chat bucket is always the literal key `"main"` (resolved to the current agent’s main key).
- Group chats use `agent:<agentId>:<channel>:group:<id>` or `agent:<agentId>:<channel>:channel:<id>` (pass the full key).
- Cron jobs use `cron:<job.id>`.
- Hooks use `hook:<uuid>` unless explicitly set.
- Node sessions use `node-<nodeId>` unless explicitly set.

`global` and `unknown` are reserved values and are never listed. If `session.scope = "global"`, we alias it to `main` for all tools so callers never see `global`.

## sessions_list

1. 以行数组的形式列出会话。

2. 参数：

- 3. `kinds?: string[]` 过滤器：`"main" | "group" | "cron" | "hook" | "node" | "other"` 中的任意值
- 4. `limit?: number` 最大行数（默认：服务器默认值，例如限制为 200）
- 5. `activeMinutes?: number` 仅返回在 N 分钟内更新的会话
- 25. `messageLimit?: number` 0 = 不包含消息（默认 0）；>0 = 包含最近 N 条消息

7. 行为：

- 8. `messageLimit > 0` 会为每个会话获取 `chat.history`，并包含最近 N 条消息。
- 9. 工具结果会在列表输出中过滤掉；如需工具消息，请使用 `sessions_history`。
- 10. 当在 **sandboxed** 代理会话中运行时，会话工具默认采用 **仅限已生成可见性**（见下文）。

11. 行结构（JSON）：

- 12. `key`：会话键（字符串）
- 13. `kind`：`main | group | cron | hook | node | other`
- 14. `channel`：`whatsapp | telegram | discord | signal | imessage | webchat | internal | unknown`
- 15. `displayName`（如果可用，则为群组显示标签）
- 16. `updatedAt`（毫秒）
- 17. `sessionId`
- 18. `model`、`contextTokens`、`totalTokens`
- 19. `thinkingLevel`、`verboseLevel`、`systemSent`、`abortedLastRun`
- 20. `sendPolicy`（如果设置，则为会话级覆盖）
- 21. `lastChannel`、`lastTo`
- 22. `deliveryContext`（可用时的规范化 `{ channel, to, accountId }`）
- 23. `transcriptPath`（根据存储目录 + sessionId 尽力推导的路径）
- 24. `messages?`（仅当 `messageLimit > 0` 时）

## 25. sessions_history

26. 获取单个会话的转录记录。

27. 参数：

- 28. `sessionKey`（必填；接受会话键或来自 `sessions_list` 的 `sessionId`）
- 29. `limit?: number` 最大消息数（服务器会进行限制）
- 30. `includeTools?: boolean`（默认 false）

31. 行为：

- 32. `includeTools=false` 会过滤 `role: "toolResult"` 的消息。
- 33. 以原始转录格式返回消息数组。
- 34. 当提供 `sessionId` 时，OpenClaw 会将其解析为对应的会话键（缺失的 id 会报错）。

## 35. sessions_send

36. 向另一个会话发送消息。

37. 参数：

- 38. `sessionKey`（必填；接受会话键或来自 `sessions_list` 的 `sessionId`）
- 39. `message`（必填）
- 40. `timeoutSeconds?: number`（默认 >0；0 = 只发送不等待）

41. 行为：

- 42. `timeoutSeconds = 0`：入队并返回 `{ runId, status: "accepted" }`。
- 43. `timeoutSeconds > 0`：最多等待 N 秒完成，然后返回 `{ runId, status: "ok", reply }`。
- 44. 如果等待超时：`{ runId, status: "timeout", error }`。 45. 运行将继续；稍后调用 `sessions_history`。
- 46. 如果运行失败：`{ runId, status: "error", error }`。
- 47. 在主运行完成后会尽力发布投递运行；`status: "ok"` 并不保证公告已成功投递。
- 48. 通过网关 `agent.wait`（服务器端）进行等待，因此重连不会中断等待。
- 49. 代理到代理的消息上下文会注入到主运行中。
- 50. 主运行完成后，OpenClaw 会运行一个 **回复回传循环**：
  - 1. 第 2+ 轮在请求方代理和目标代理之间交替进行。
  - 2. 精确回复 `REPLY_SKIP` 以停止乒乓交互。
  - 3. 最大轮数为 `session.agentToAgent.maxPingPongTurns`（0–5，默认 5）。
- 4. 循环结束后，OpenClaw 运行 **代理到代理公告步骤**（仅目标代理）：
  - 5. 精确回复 `ANNOUNCE_SKIP` 以保持静默。
  - 6. 任何其他回复都会发送到目标频道。
  - 7. 公告步骤包含原始请求 + 第 1 轮回复 + 最新的乒乓回复。

## 8. Channel 字段

- 9. 对于群组，`channel` 是记录在会话条目中的频道。
- 10. 对于私聊，`channel` 从 `lastChannel` 映射。
- 11. 对于 cron/hook/node，`channel` 为 `internal`。
- 12. 如果缺失，`channel` 为 `unknown`。

## 13. 安全 / 发送策略

14. 基于频道/聊天类型的策略阻止（非按会话 ID）。

```json
15. {
  "session": {
    "sendPolicy": {
      "rules": [
        {
          "match": { "channel": "discord", "chatType": "group" },
          "action": "deny"
        }
      ],
      "default": "allow"
    }
  }
}
```

16. 运行时覆盖（按会话条目）：

- 17. `sendPolicy: "allow" | "deny"`（未设置 = 继承配置）
- 18. 可通过 `sessions.patch` 或仅所有者可用的 `/send on|off|inherit`（独立消息）进行设置。

19. 执行点：

- 20. `chat.send` / `agent`（网关）
- 21. 自动回复投递逻辑

## 22. sessions_spawn

23. 在隔离的会话中启动一个子代理运行，并将结果公告回请求方聊天频道。

24. 参数：

- 25. `task`（必填）
- 26. `label?`（可选；用于日志/UI）
- 27. `agentId?`（可选；若允许，则在另一个代理 ID 下启动）
- 28. `model?`（可选；覆盖子代理模型；无效值将报错）
- 29. `runTimeoutSeconds?`（默认 0；设置后，在 N 秒后中止子代理运行）
- 30. `cleanup?`（`delete|keep`，默认 `keep`）

31. 允许列表：

- 32. `agents.list[].subagents.allowAgents`：通过 `agentId` 允许的代理 ID 列表（`["*"]` 表示允许任意）。 33. 默认：仅请求方代理。

34. 发现：

- 35. 使用 `agents_list` 发现哪些代理 ID 允许用于 `sessions_spawn`。

36. 行为：

- 37. 启动一个新的 `agent:<agentId>:subagent:<uuid>` 会话，`deliver: false`。
- 38. 子代理默认拥有完整工具集 **不包含会话工具**（可通过 `tools.subagents.tools` 配置）。
- 39. 子代理不允许调用 `sessions_spawn`（不允许子代理 → 子代理 的生成）。
- 40. 始终为非阻塞：立即返回 `{ status: "accepted", runId, childSessionKey }`。
- 41. 完成后，OpenClaw 运行子代理 **公告步骤** 并将结果发布到请求方聊天频道。
- 42. 在公告步骤中精确回复 `ANNOUNCE_SKIP` 以保持静默。
- 43. 公告回复会规范化为 `Status`/`Result`/`Notes`；`Status` 来自运行时结果（而非模型文本）。
- 44. 子代理会话会在 `agents.defaults.subagents.archiveAfterMinutes`（默认：60）后自动归档。
- 45. 公告回复包含一行统计信息（运行时间、tokens、sessionKey/sessionId、转录路径，以及可选的费用）。

## 46. 沙箱会话可见性

47. 沙箱化会话可以使用会话工具，但默认情况下它们只能看到通过 `sessions_spawn` 启动的会话。

48. 配置：

```json5
49. {
  agents: {
    defaults: {
      sandbox: {
        // 默认："spawned"
        sessionToolsVisibility: "spawned", // 或 "all"
      },
    },
  },
}
```
