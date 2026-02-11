---
summary: "Multi-agent routing: isolated agents, channel accounts, and bindings"
title: Multi-Agent Routing
read_when: "You want multiple isolated agents (workspaces + auth) in one gateway process."
status: active
---

# Multi-Agent Routing

Goal: multiple _isolated_ agents (separate workspace + `agentDir` + sessions), plus multiple channel accounts (e.g. two WhatsApps) in one running Gateway. Inbound is routed to an agent via bindings.

## What is “one agent”?

An **agent** is a fully scoped brain with its own:

- **Workspace** (files, AGENTS.md/SOUL.md/USER.md, local notes, persona rules).
- **State directory** (`agentDir`) for auth profiles, model registry, and per-agent config.
- **Session store** (chat history + routing state) under `~/.openclaw/agents/<agentId>/sessions`.

Auth 配置是**按 agent**划分的。 每个 agent 都从自己的以下位置读取：

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

主 agent 的凭据**不会**自动共享。 切勿在多个 agent 之间复用 `agentDir`
（这会导致认证/会话冲突）。 如果你想共享凭据，
请将 `auth-profiles.json` 复制到其他 agent 的 `agentDir` 中。

技能是按 agent 划分的，通过各自工作区的 `skills/` 文件夹提供；
共享技能位于 `~/.openclaw/skills`。 参见 [Skills: per-agent vs shared](/tools/skills#per-agent-vs-shared-skills)。

Gateway 可以托管**一个 agent**（默认）或**多个 agent**并排运行。

**工作区说明：** 每个 agent 的工作区是**默认 cwd**，而不是一个硬性沙箱。 相对路径会在工作区内解析，但除非启用沙箱，绝对路径可以访问主机上的其他位置。 参见
[Sandboxing](/gateway/sandboxing)。

## 路径（速查表）

- 配置：`~/.openclaw/openclaw.json`（或 `OPENCLAW_CONFIG_PATH`）
- 状态目录：`~/.openclaw`（或 `OPENCLAW_STATE_DIR`）
- 工作区：`~/.openclaw/workspace`（或 `~/.openclaw/workspace-<agentId>`）
- Agent 目录：`~/.openclaw/agents/<agentId>/agent`（或 `agents.list[].agentDir`）
- 会话：`~/.openclaw/agents/<agentId>/sessions`

### 单 agent 模式（默认）

如果你什么都不做，OpenClaw 会运行一个单一 agent：

- `agentId` 默认为 **`main`**。
- 会话键格式为 `agent:main:<mainKey>`。
- 工作区默认是 `~/.openclaw/workspace`（当设置了 `OPENCLAW_PROFILE` 时为 `~/.openclaw/workspace-<profile>`）。
- 状态默认是 `~/.openclaw/agents/main/agent`。

## Agent 助手

使用 agent 向导添加一个新的隔离 agent：

```bash
openclaw agents add work
```

然后添加 `bindings`（或让向导完成）以路由入站消息。

使用以下命令验证：

```bash
openclaw agents list --bindings
```

## 多个 agent = 多个人，多种人格

在**多个 agent**情况下，每个 `agentId` 都成为一个**完全隔离的人格**：

- **不同的电话号码/账号**（按渠道的 `accountId`）。
- **不同的人格**（每个 agent 的工作区文件，如 `AGENTS.md` 和 `SOUL.md`）。
- **独立的认证 + 会话**（除非显式启用，否则不会互通）。

这使得**多人**可以共享一个 Gateway 服务器，同时保持各自的 AI“脑”和数据相互隔离。

## 一个 WhatsApp 号码，多个人（私信拆分）

你可以在**一个 WhatsApp 账号**下，将**不同的 WhatsApp 私信**路由到不同的 agent。 Match on sender E.164 (like `+15551234567`) with `peer.kind: "direct"`. 回复仍然来自同一个 WhatsApp 号码（没有按 agent 区分的发送者身份）。

重要细节：直接聊天会折叠到该 agent 的**主会话键**，因此真正的隔离需要**每人一个 agent**。

示例：

```json5
{
  agents: {
    list: [
      { id: "alex", workspace: "~/.openclaw/workspace-alex" },
      { id: "mia", workspace: "~/.openclaw/workspace-mia" },
    ],
  },
  bindings: [
    {
      agentId: "alex",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230001" } },
    },
    {
      agentId: "mia",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230002" } },
    },
  ],
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551230001", "+15551230002"],
    },
  },
}
```

注意事项：

- 私信访问控制是**按 WhatsApp 账号全局**的（配对/白名单），而不是按 agent。
- 对于共享群组，将该群组绑定到一个 agent，或使用 [Broadcast groups](/channels/broadcast-groups)。

## 路由规则（消息如何选择 agent）

Bindings 是**确定性的**，且**最具体的优先**：

1. `peer` 匹配（精确的私信/群组/频道 ID）
2. `guildId`（Discord）
3. `teamId`（Slack）
4. 按渠道的 `accountId` 匹配
5. 1. 渠道级匹配（`accountId: "*"`）
6. 2. 回退到默认 agent（`agents.list[].default`，否则取列表中的第一个，默认：`main`）

## 3) 多个账户 / 电话号码

4. 支持**多账户**的渠道（例如 WhatsApp）使用 `accountId` 来标识每次登录。 5. 每个 `accountId` 都可以路由到不同的 agent，因此一台服务器可以托管多个电话号码而不会混淆会话。

## 6. 概念

- 7. `agentId`：一个“脑”（工作区、按 agent 的鉴权、按 agent 的会话存储）。
- 8. `accountId`：一个渠道账户实例（例如 WhatsApp 账户 `"personal"` 与 `"biz"`）。
- 9. `binding`：按 `(channel, accountId, peer)`（以及可选的公会/团队 ID）将入站消息路由到某个 `agentId`。
- 10. 直接聊天会折叠为 `agent:<agentId>:<mainKey>`（每个 agent 的“主”会话；`session.mainKey`）。

## 11. 示例：两个 WhatsApp → 两个 agent

12. `~/.openclaw/openclaw.json`（JSON5）：

```js
{
  agents: {
    list: [
      {
        id: "home",
        default: true,
        name: "Home",
        workspace: "~/.openclaw/workspace-home",
        agentDir: "~/.openclaw/agents/home/agent",
      },
      {
        id: "work",
        name: "Work",
        workspace: "~/.openclaw/workspace-work",
        agentDir: "~/.openclaw/agents/work/agent",
      },
    ],
  },

  // Deterministic routing: first match wins (most-specific first).
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },

    // Optional per-peer override (example: send a specific group to work agent).
    {
      agentId: "work",
      match: {
        channel: "whatsapp",
        accountId: "personal",
        peer: { kind: "group", id: "1203630...@g.us" },
      },
    },
  ],

  // Off by default: agent-to-agent messaging must be explicitly enabled + allowlisted.
  tools: {
    agentToAgent: {
      enabled: false,
      allow: ["home", "work"],
    },
  },

  channels: {
    whatsapp: {
      accounts: {
        personal: {
          // Optional override. Default: ~/.openclaw/credentials/whatsapp/personal
          // authDir: "~/.openclaw/credentials/whatsapp/personal",
        },
        biz: {
          // Optional override. Default: ~/.openclaw/credentials/whatsapp/biz
          // authDir: "~/.openclaw/credentials/whatsapp/biz",
        },
      },
    },
  },
}
```

## 14. 示例：WhatsApp 日常聊天 + Telegram 深度工作

15. 按渠道拆分：将 WhatsApp 路由到快速的日常 agent，将 Telegram 路由到 Opus agent。

```json5
{
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "opus",
        name: "Deep Work",
        workspace: "~/.openclaw/workspace-opus",
        model: "anthropic/claude-opus-4-6",
      },
    ],
  },
  bindings: [
    { agentId: "chat", match: { channel: "whatsapp" } },
    { agentId: "opus", match: { channel: "telegram" } },
  ],
}
```

17. 说明：

- 18. 如果某个渠道有多个账户，请在绑定中添加 `accountId`（例如 `{ channel: "whatsapp", accountId: "personal" }`）。
- 19. 若要将单个私聊/群组路由到 Opus，同时其余仍走 chat，请为该 peer 添加一个 `match.peer` 绑定；peer 匹配始终优先于渠道级规则。

## 20. 示例：同一渠道，将一个 peer 路由到 Opus

21. 保持 WhatsApp 使用快速 agent，但将一个私聊路由到 Opus：

```json5
{
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "opus",
        name: "Deep Work",
        workspace: "~/.openclaw/workspace-opus",
        model: "anthropic/claude-opus-4-6",
      },
    ],
  },
  bindings: [
    {
      agentId: "opus",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551234567" } },
    },
    { agentId: "chat", match: { channel: "whatsapp" } },
  ],
}
```

22. peer 绑定始终优先，因此请将它们放在渠道级规则之上。

## 23. 绑定到 WhatsApp 群组的家庭 agent

24. 将一个专用的家庭 agent 绑定到单个 WhatsApp 群组，并启用 @提及门控以及更严格的工具策略：

```json5
{
  agents: {
    list: [
      {
        id: "family",
        name: "Family",
        workspace: "~/.openclaw/workspace-family",
        identity: { name: "Family Bot" },
        groupChat: {
          mentionPatterns: ["@family", "@familybot", "@Family Bot"],
        },
        sandbox: {
          mode: "all",
          scope: "agent",
        },
        tools: {
          allow: [
            "exec",
            "read",
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
          ],
          deny: ["write", "edit", "apply_patch", "browser", "canvas", "nodes", "cron"],
        },
      },
    ],
  },
  bindings: [
    {
      agentId: "family",
      match: {
        channel: "whatsapp",
        peer: { kind: "group", id: "120363999999999999@g.us" },
      },
    },
  ],
}
```

26. 说明：

- 27. 工具允许/拒绝列表针对的是**工具（tools）**，而不是技能（skills）。 28. 如果某个技能需要运行二进制文件，请确保已允许 `exec`，并且该二进制在沙箱中存在。
- 29. 若需更严格的门控，请设置 `agents.list[].groupChat.mentionPatterns`，并保持该渠道的群组白名单启用。

## 30. 按 agent 的沙箱与工具配置

31. 从 v2026.1.6 开始，每个 agent 都可以拥有自己的沙箱和工具限制：

```js
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: {
          mode: "off",  // No sandbox for personal agent
        },
        // No tool restrictions - all tools available
      },
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",     // Always sandboxed
          scope: "agent",  // One container per agent
          docker: {
            // Optional one-time setup after container creation
            setupCommand: "apt-get update && apt-get install -y git curl",
          },
        },
        tools: {
          allow: ["read"],                    // Only read tool
          deny: ["exec", "write", "edit", "apply_patch"],    // Deny others
        },
      },
    ],
  },
}
```

33. 注意：`setupCommand` 位于 `sandbox.docker` 下，并且只在容器创建时运行一次。
34. 当解析后的 scope 为 `"shared"` 时，按 agent 的 `sandbox.docker.*` 覆盖将被忽略。

35. **优势：**

- 36. **安全隔离**：为不受信任的 agent 限制工具
- 37. **资源控制**：将特定 agent 置于沙箱中，同时让其他 agent 直接运行在宿主机上
- 38. **灵活策略**：为不同 agent 设置不同权限

39. 注意：`tools.elevated` 是**全局**且基于发送方的；不能按 agent 配置。
40. 如果需要按 agent 的边界，请使用 `agents.list[].tools` 来拒绝 `exec`。
41. 对于群组定向，请使用 `agents.list[].groupChat.mentionPatterns`，以便 @提及能准确映射到目标 agent。

42. 详细示例请参见 [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools)。
