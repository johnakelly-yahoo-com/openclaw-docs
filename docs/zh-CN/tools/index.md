---
summary: "Agent tool surface for OpenClaw (browser, canvas, nodes, message, cron) replacing legacy `openclaw-*` skills"
read_when:
  - Adding or modifying agent tools
  - Retiring or changing `openclaw-*` skills
title: "1. 工具"
---

# 2. 工具（OpenClaw）

3. OpenClaw 为浏览器、画布、节点和 cron 提供 **一等公民的代理工具**。
4. 这些取代了旧的 `openclaw-*` 技能：工具是有类型的，不通过 shell，
   并且代理应直接依赖它们。

## 5. 禁用工具

6. 你可以在 `openclaw.json` 中通过 `tools.allow` / `tools.deny` 全局允许/禁止工具
   （deny 优先）。 7. 这可以防止被禁止的工具被发送给模型提供方。

```json5
8. {
  tools: { deny: ["browser"] },
}
```

9. 说明：

- 10. 匹配不区分大小写。
- 11. 支持 `*` 通配符（`"*"` 表示所有工具）。
- 12. 如果 `tools.allow` 只引用未知或未加载的插件工具名称，OpenClaw 会记录一条警告并忽略该允许列表，以便核心工具保持可用。

## 13. 工具配置文件（基础允许列表）

14. `tools.profile` 在 `tools.allow`/`tools.deny` 之前设置一个 **基础工具允许列表**。
15. 按代理覆盖：`agents.list[].tools.profile`。

16. 配置文件：

- 17. `minimal`：仅 `session_status`
- 18. `coding`：`group:fs`、`group:runtime`、`group:sessions`、`group:memory`、`image`
- 19. `messaging`：`group:messaging`、`sessions_list`、`sessions_history`、`sessions_send`、`session_status`
- 20. `full`：不限制（与未设置相同）

21. 示例（默认仅消息工具，同时允许 Slack + Discord 工具）：

```json5
22. {
  tools: {
    profile: "messaging",
    allow: ["slack", "discord"],
  },
}
```

23. 示例（coding 配置文件，但在所有地方禁用 exec/process）：

```json5
24. {
  tools: {
    profile: "coding",
    deny: ["group:runtime"],
  },
}
```

25. 示例（全局 coding 配置文件，消息型支持代理）：

```json5
26. {
  tools: { profile: "coding" },
  agents: {
    list: [
      {
        id: "support",
        tools: { profile: "messaging", allow: ["slack"] },
      },
    ],
  },
}
```

## 27. 提供方特定的工具策略

28. 使用 `tools.byProvider` 在不更改全局默认值的情况下，**进一步限制** 特定提供方
    （或单个 `provider/model`）的工具。
29. 按代理覆盖：`agents.list[].tools.byProvider`。

30. 该策略在基础工具配置文件 **之后**、允许/禁止列表 **之前** 应用，
    因此只能缩小工具集合。
31. 提供方键可以是 `provider`（例如 `google-antigravity`）或
    `provider/model`（例如 `openai/gpt-5.2`）。

32. 示例（保持全局 coding 配置文件，但为 Google Antigravity 使用最小工具）：

```json5
33. {
  tools: {
    profile: "coding",
    byProvider: {
      "google-antigravity": { profile: "minimal" },
    },
  },
}
```

34. 示例（针对不稳定端点的 provider/model 特定允许列表）：

```json5
35. {
  tools: {
    allow: ["group:fs", "group:runtime", "sessions_list"],
    byProvider: {
      "openai/gpt-5.2": { allow: ["group:fs", "sessions_list"] },
    },
  },
}
```

36. 示例（针对单个提供方的代理级覆盖）：

```json5
37. {
  agents: {
    list: [
      {
        id: "support",
        tools: {
          byProvider: {
            "google-antigravity": { allow: ["message", "sessions_list"] },
          },
        },
      },
    ],
  },
}
```

## 38. 工具组（简写）

39. 工具策略（全局、代理、沙箱）支持 `group:*` 条目，可展开为多个工具。
40. 在 `tools.allow` / `tools.deny` 中使用这些。

41. 可用的组：

- 42. `group:runtime`：`exec`、`bash`、`process`
- 43. `group:fs`：`read`、`write`、`edit`、`apply_patch`
- 44. `group:sessions`：`sessions_list`、`sessions_history`、`sessions_send`、`sessions_spawn`、`session_status`
- 45. `group:memory`：`memory_search`、`memory_get`
- 46. `group:web`：`web_search`、`web_fetch`
- 47. `group:ui`：`browser`、`canvas`
- 48. `group:automation`：`cron`、`gateway`
- 49. `group:messaging`：`message`
- 50. `group:nodes`：`nodes`
- `group:openclaw`：所有内置的 OpenClaw 工具（不包括提供方插件）

示例（仅允许文件工具 + 浏览器）：

```json5
{
  tools: {
    allow: ["group:fs", "browser"],
  },
}
```

## 插件 + 工具

插件可以在核心工具集之外注册**额外的工具**（以及 CLI 命令）。
有关安装和配置，请参见 [Plugins](/tools/plugin)；有关如何将工具使用指南注入到提示中的说明，请参见 [Skills](/tools/skills)。 一些插件会在工具之外同时提供自己的技能（例如，语音通话插件）。

可选插件工具：

- [Lobster](/tools/lobster)：带有可恢复审批的强类型工作流运行时（需要在网关主机上安装 Lobster CLI）。
- [LLM Task](/tools/llm-task)：仅 JSON 的 LLM 步骤，用于结构化工作流输出（可选的 schema 校验）。

## Tool inventory

### `apply_patch`

在一个或多个文件中应用结构化补丁。 用于多段（multi-hunk）编辑。
实验性：通过 `tools.exec.applyPatch.enabled` 启用（仅限 OpenAI 模型）。

### `exec`

Run shell commands in the workspace.

核心参数：

- `command`（必填）
- `yieldMs`（超时后自动转入后台，默认 10000）
- `background`（立即转入后台）
- `timeout`（秒；超过则终止进程，默认 1800）
- `elevated`（布尔值；在启用/允许提升模式时在主机上运行；仅在代理被沙箱化时才会改变行为）
- `host` (`sandbox | gateway | node`)
- `security`（`deny | allowlist | full`）
- `ask`（`off | on-miss | always`）
- `node`（用于 `host=node` 的节点 id/名称）
- 需要真实的 TTY？ Set `pty: true`.

注意：

- 在转入后台时返回 `status: "running"` 以及一个 `sessionId`。
- 使用 `process` 来轮询/记录/写入/终止/清理后台会话。
- 如果不允许使用 `process`，`exec` 将同步运行并忽略 `yieldMs`/`background`。
- `elevated` 受 `tools.elevated` 以及任何 `agents.list[].tools.elevated` 覆盖项的共同限制（两者都必须允许），并且是 `host=gateway` + `security=full` 的别名。
- `elevated` 仅在代理被沙箱化时才会改变行为（否则无效果）。
- `host=node` 可以指向 macOS 伴随应用或无头节点主机（`openclaw node run`）。
- gateway/node 的审批和白名单：[Exec approvals](/tools/exec-approvals)。

### `process`

管理后台 exec 会话。

核心操作：

- `list`、`poll`、`log`、`write`、`kill`、`clear`、`remove`

注意：

- `poll` 在完成时返回新的输出和退出状态。
- `log` 支持基于行的 `offset`/`limit`（省略 `offset` 以获取最后 N 行）。
- `process` 以代理为作用域；其他代理的会话不可见。

### `web_search`

使用 Brave Search API 搜索网页。

核心参数：

- `query`（必填）
- `count`（1–10；默认值来自 `tools.web.search.maxResults`）

1. 说明：

- 2. 需要 Brave API 密钥（推荐：`openclaw configure --section web`，或设置 `BRAVE_API_KEY`）。
- 3. 通过 `tools.web.search.enabled` 启用。
- 4. 响应会被缓存（默认 15 分钟）。
- 5. 设置方法参见 [Web tools](/tools/web)。

### 6. `web_fetch`

7. 从 URL 获取并提取可读内容（HTML → markdown/text）。

8. 核心参数：

- 9. `url`（必填）
- 10. `extractMode`（`markdown` | `text`）
- 11. `maxChars`（截断过长页面）

12. 说明：

- 13. 通过 `tools.web.fetch.enabled` 启用。
- 14. `maxChars` 会被 `tools.web.fetch.maxCharsCap` 限制（默认 50000）。
- 15. 响应会被缓存（默认 15 分钟）。
- 16. 对于大量使用 JS 的站点，优先使用浏览器工具。
- 17. 设置方法参见 [Web tools](/tools/web)。
- 18. 可选的反爬虫兜底方案参见 [Firecrawl](/tools/firecrawl)。

### 19. `browser`

20. 控制由 OpenClaw 管理的专用浏览器。

21. 核心操作：

- 22. `status`、`start`、`stop`、`tabs`、`open`、`focus`、`close`
- 23. `snapshot`（aria/ai）
- 24. `screenshot`（返回图像块 + `MEDIA:<path>`）
- 25. `act`（UI 操作：click/type/press/hover/drag/select/fill/resize/wait/evaluate）
- 26. `navigate`、`console`、`pdf`、`upload`、`dialog`

27. 配置文件管理：

- 28. `profiles` —— 列出所有浏览器配置文件及其状态
- 29. `create-profile` —— 创建新配置文件并自动分配端口（或使用 `cdpUrl`）
- 30. `delete-profile` —— 停止浏览器、删除用户数据、从配置中移除（仅本地）
- 31. `reset-profile` —— 终止配置文件端口上的孤儿进程（仅本地）

32. 通用参数：

- 33. `profile`（可选；默认使用 `browser.defaultProfile`）
- 34. `target`（`sandbox` | `host` | `node`）
- 35. `node`（可选；指定特定的节点 ID/名称）
      说明：
- 36. 需要 `browser.enabled=true`（默认值为 `true`；设置为 `false` 可禁用）。
- 37. 所有操作都支持可选的 `profile` 参数，以支持多实例。
- 38. 当省略 `profile` 时，使用 `browser.defaultProfile`（默认为 "chrome"）。
- 39. 配置文件名称：仅限小写字母数字和连字符（最长 64 个字符）。
- 40. 端口范围：18800-18899（最多约 100 个配置文件）。
- 41. 远程配置文件仅支持附加（不能 start/stop/reset）。
- 42. 如果连接了支持浏览器的节点，工具可能会自动路由到该节点（除非你固定 `target`）。
- 43. 当安装了 Playwright 时，`snapshot` 默认为 `ai`；如需可访问性树请使用 `aria`。
- 44. `snapshot` 还支持角色快照选项（`interactive`、`compact`、`depth`、`selector`），返回如 `e12` 的引用。
- 45. `act` 需要来自 `snapshot` 的 `ref`（AI 快照中的数字 `12`，或角色快照中的 `e12`）；对于少见的 CSS 选择器需求，请使用 `evaluate`。
- 46. 默认避免使用 `act` → `wait`；仅在特殊情况下使用（没有可靠的 UI 状态可等待时）。
- 47. `upload` 可选传入 `ref`，以在就绪后自动点击。
- 48. `upload` 还支持 `inputRef`（aria 引用）或 `element`（CSS 选择器），以直接设置 `<input type="file">`。

### 49. `canvas`

50. 驱动节点 Canvas（present、eval、snapshot、A2UI）。

Core actions:

- `present`, `hide`, `navigate`, `eval`
- `snapshot` (returns image block + `MEDIA:<path>`)
- `a2ui_push`, `a2ui_reset`

Notes:

- Uses gateway `node.invoke` under the hood.
- If no `node` is provided, the tool picks a default (single connected node or local mac node).
- A2UI is v0.8 only (no `createSurface`); the CLI rejects v0.9 JSONL with line errors.
- Quick smoke: `openclaw nodes canvas a2ui push --node <id> --text "Hello from A2UI"`.

### `nodes`

Discover and target paired nodes; send notifications; capture camera/screen.

Core actions:

- `status`, `describe`
- `pending`, `approve`, `reject` (pairing)
- `notify` (macOS `system.notify`)
- `run` (macOS `system.run`)
- `camera_snap`, `camera_clip`, `screen_record`
- `location_get`

Notes:

- Camera/screen commands require the node app to be foregrounded.
- Images return image blocks + `MEDIA:<path>`.
- Videos return `FILE:<path>` (mp4).
- Location returns a JSON payload (lat/lon/accuracy/timestamp).
- `run` params: `command` argv array; optional `cwd`, `env` (`KEY=VAL`), `commandTimeoutMs`, `invokeTimeoutMs`, `needsScreenRecording`.

Example (`run`):

```json
{
  "action": "run",
  "node": "office-mac",
  "command": ["echo", "Hello"],
  "env": ["FOO=bar"],
  "commandTimeoutMs": 12000,
  "invokeTimeoutMs": 45000,
  "needsScreenRecording": false
}
```

### `image`

Analyze an image with the configured image model.

Core parameters:

- `image` (required path or URL)
- `prompt` (optional; defaults to "Describe the image.")
- `model` (optional override)
- `maxBytesMb` (optional size cap)

Notes:

- Only available when `agents.defaults.imageModel` is configured (primary or fallbacks), or when an implicit image model can be inferred from your default model + configured auth (best-effort pairing).
- Uses the image model directly (independent of the main chat model).

### `message`

Send messages and channel actions across Discord/Google Chat/Slack/Telegram/WhatsApp/Signal/iMessage/MS Teams.

Core actions:

- `send` (text + optional media; MS Teams also supports `card` for Adaptive Cards)
- `poll` (WhatsApp/Discord/MS Teams polls)
- `react` / `reactions` / `read` / `edit` / `delete`
- `pin` / `unpin` / `list-pins`
- `permissions`
- `thread-create` / `thread-list` / `thread-reply`
- `search`
- `sticker`
- `member-info` / `role-info`
- `emoji-list` / `emoji-upload` / `sticker-upload`
- `role-add` / `role-remove`
- `channel-info` / `channel-list`
- `voice-status`
- `event-list` / `event-create`
- `timeout` / `kick` / `ban`

Notes:

- `send` routes WhatsApp via the Gateway; other channels go direct.
- `poll` uses the Gateway for WhatsApp and MS Teams; Discord polls go direct.
- When a message tool call is bound to an active chat session, sends are constrained to that session’s target to avoid cross-context leaks.

### `cron`

Manage Gateway cron jobs and wakeups.

Core actions:

- `status`, `list`
- `add`, `update`, `remove`, `run`, `runs`
- `wake` (enqueue system event + optional immediate heartbeat)

Notes:

- `add` expects a full cron job object (same schema as `cron.add` RPC).
- `update` uses `{ jobId, patch }` (`id` accepted for compatibility).

### `gateway`

Restart or apply updates to the running Gateway process (in-place).

Core actions:

- `restart` (authorizes + sends `SIGUSR1` for in-process restart; `openclaw gateway` restart in-place)
- `config.get` / `config.schema`
- `config.apply` (validate + write config + restart + wake)
- `config.patch` (merge partial update + restart + wake)
- `update.run` (run update + restart + wake)

Notes:

- Use `delayMs` (defaults to 2000) to avoid interrupting an in-flight reply.
- `restart` is disabled by default; enable with `commands.restart: true`.

### `sessions_list` / `sessions_history` / `sessions_send` / `sessions_spawn` / `session_status`

List sessions, inspect transcript history, or send to another session.

Core parameters:

- `sessions_list`: `kinds?`, `limit?`, `activeMinutes?`, `messageLimit?` (0 = none)
- `sessions_history`: `sessionKey` (or `sessionId`), `limit?`, `includeTools?`
- `sessions_send`: `sessionKey` (or `sessionId`), `message`, `timeoutSeconds?` (0 = fire-and-forget)
- `sessions_spawn`: `task`, `label?`, `agentId?`, `model?`, `runTimeoutSeconds?`, `cleanup?`
- `session_status`: `sessionKey?` (default current; accepts `sessionId`), `model?` (`default` clears override)

Notes:

- `main` is the canonical direct-chat key; global/unknown are hidden.
- `messageLimit > 0` fetches last N messages per session (tool messages filtered).
- `sessions_send` waits for final completion when `timeoutSeconds > 0`.
- Delivery/announce happens after completion and is best-effort; `status: "ok"` confirms the agent run finished, not that the announce was delivered.
- `sessions_spawn` starts a sub-agent run and posts an announce reply back to the requester chat.
- `sessions_spawn` is non-blocking and returns `status: "accepted"` immediately.
- `sessions_send` runs a reply‑back ping‑pong (reply `REPLY_SKIP` to stop; max turns via `session.agentToAgent.maxPingPongTurns`, 0–5).
- After the ping‑pong, the target agent runs an **announce step**; reply `ANNOUNCE_SKIP` to suppress the announcement.

### `agents_list`

List agent ids that the current session may target with `sessions_spawn`.

Notes:

- Result is restricted to per-agent allowlists (`agents.list[].subagents.allowAgents`).
- When `["*"]` is configured, the tool includes all configured agents and marks `allowAny: true`.

## 1. 参数（通用）

2. 基于 Gateway 的工具（`canvas`、`nodes`、`cron`）：

- 3. `gatewayUrl`（默认 `ws://127.0.0.1:18789`）
- 4. `gatewayToken`（如果启用了认证）
- 5. `timeoutMs`

6. 注意：当设置了 `gatewayUrl` 时，请显式包含 `gatewayToken`。 7. 工具不会继承用于覆盖的配置或环境凭据，且缺少显式凭据将被视为错误。

8. 浏览器工具：

- 9. `profile`（可选；默认为 `browser.defaultProfile`）
- 10. `target`（`sandbox` | `host` | `node`）
- 11. `node`（可选；固定到特定的节点 id/名称）

## 12. 推荐的代理流程

13. 浏览器自动化：

1. 14. `browser` → `status` / `start`
2. 15. `snapshot`（ai 或 aria）
3. 16. `act`（click/type/press）
4. 17. 如果需要视觉确认，请使用 `screenshot`

18) Canvas 渲染：

1. 19. `canvas` → `present`
2. 20. `a2ui_push`（可选）
3. 21. `snapshot`

22) 节点定向：

1. 23. `nodes` → `status`
2. 24. 在所选节点上执行 `describe`
3. 25. `notify` / `run` / `camera_snap` / `screen_record`

## 26) 安全

- 27. 避免直接使用 `system.run`；仅在获得用户明确同意的情况下，通过 `nodes` → `run` 使用。
- 28. 尊重用户对摄像头/屏幕捕获的同意。
- 29. 在调用媒体命令之前，使用 `status/describe` 确认权限。

## 30. 工具如何呈现给代理

31. 工具通过两个并行通道暴露：

1. 32. **系统提示文本**：人类可读的列表 + 指导。
2. 33. **工具架构**：发送到模型 API 的结构化函数定义。

34) 这意味着代理既能看到“有哪些工具”，也能看到“如何调用它们”。 35. 如果某个工具
    未出现在系统提示或架构中，模型就无法调用它。
