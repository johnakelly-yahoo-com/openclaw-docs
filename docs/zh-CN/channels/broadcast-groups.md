---
summary: "Broadcast a WhatsApp message to multiple agents"
read_when:
  - Configuring broadcast groups
  - Debugging multi-agent replies in WhatsApp
status: experimental
title: "Broadcast Groups"
---

# Broadcast Groups

**Status:** Experimental  
**Version:** Added in 2026.1.9

## Overview

Broadcast Groups enable multiple agents to process and respond to the same message simultaneously. This allows you to create specialized agent teams that work together in a single WhatsApp group or DM — all using one phone number.

Current scope: **WhatsApp only** (web channel).

Broadcast groups are evaluated after channel allowlists and group activation rules. In WhatsApp groups, this means broadcasts happen when OpenClaw would normally reply (for example: on mention, depending on your group settings).

## 1. 使用场景

### 2. 1. 3. 专业化代理团队

4. 部署多个具有原子化、专注职责的代理：

```
5. 组："开发团队"
Agents:
  - CodeReviewer（审查代码片段）
  - DocumentationBot（生成文档）
  - SecurityAuditor（检查漏洞）
  - TestGenerator（建议测试用例）
```

6. 每个代理处理相同的消息，并提供其专业视角。

### 7. 2. 多语言支持

```
9. 组："国际支持"
Agents:
  - Agent_EN（使用英语回复）
  - Agent_DE（使用德语回复）
  - Agent_ES（使用西班牙语回复）
```

### 10. 3. 11. 质量保证工作流

```
12. 组："客户支持"
Agents:
  - SupportAgent（提供答案）
  - QAAgent（审查质量，仅在发现问题时回复）
```

### 13. 4. 任务自动化

```
15. 组："项目管理"
Agents:
  - TaskTracker（更新任务数据库）
  - TimeLogger（记录花费时间）
  - ReportGenerator（生成汇总）
```

## 16. 配置

### 17. 基本设置

18. 添加一个顶层 `broadcast` 区段（与 `bindings` 同级）。 19. 键为 WhatsApp 对等 ID：

- 20. 群聊：群 JID（例如 `120363403215116621@g.us`）
- 21. 私聊：E.164 电话号码（例如 `+15551234567`）

```json
{
  "broadcast": {
    "120363403215116621@g.us": ["alfred", "baerbel", "assistant3"]
  }
}
```

23. **结果：** 当 OpenClaw 在此聊天中回复时，将运行这三个代理。

### 24. 处理策略

25. 控制代理如何处理消息：

#### 26. 并行（默认）

27. 所有代理同时处理：

```json
{
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": ["alfred", "baerbel"]
  }
}
```

#### 29. 顺序

30. 代理按顺序处理（一个等待前一个完成）：

```json
{
  "broadcast": {
    "strategy": "sequential",
    "120363403215116621@g.us": ["alfred", "baerbel"]
  }
}
```

### 32. 完整示例

```json
{
  "agents": {
    "list": [
      {
        "id": "code-reviewer",
        "name": "Code Reviewer",
        "workspace": "/path/to/code-reviewer",
        "sandbox": { "mode": "all" }
      },
      {
        "id": "security-auditor",
        "name": "Security Auditor",
        "workspace": "/path/to/security-auditor",
        "sandbox": { "mode": "all" }
      },
      {
        "id": "docs-generator",
        "name": "Documentation Generator",
        "workspace": "/path/to/docs-generator",
        "sandbox": { "mode": "all" }
      }
    ]
  },
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": ["code-reviewer", "security-auditor", "docs-generator"],
    "120363424282127706@g.us": ["support-en", "support-de"],
    "+15555550123": ["assistant", "logger"]
  }
}
```

## 34. 工作原理

### 35. 消息流

1. 36. **传入消息** 到达一个 WhatsApp 群组
2. 37. **广播检查**：系统检查对等 ID 是否在 `broadcast` 中
3. 38. **如果在广播列表中**：
   - 39. 所有列出的代理都会处理该消息
   - 40. 每个代理都有自己的会话键和隔离的上下文
   - 41. 代理以并行（默认）或顺序方式处理
4. 42. **如果不在广播列表中**：
   - 43. 应用正常路由（第一个匹配的绑定）

44) 注意：广播群组不会绕过频道允许列表或群组激活规则（提及/命令等）。 45. 它们只会改变在消息符合处理条件时 _运行哪些代理_。

### 46. 会话隔离

47. 广播组中的每个代理都完全独立地维护：

- 48. **会话键**（`agent:alfred:whatsapp:group:120363...` 与 `agent:baerbel:whatsapp:group:120363...`）
- 49. **对话历史**（代理看不到其他代理的消息）
- 50. **工作区**（如果已配置，则为独立的沙箱）
- **Tool access** (different allow/deny lists)
- **Memory/context** (separate IDENTITY.md, SOUL.md, etc.)
- **Group context buffer** (recent group messages used for context) is shared per peer, so all broadcast agents see the same context when triggered

This allows each agent to have:

- Different personalities
- Different tool access (e.g., read-only vs. read-write)
- Different models (e.g., opus vs. sonnet)
- Different skills installed

### Example: Isolated Sessions

In group `120363403215116621@g.us` with agents `["alfred", "baerbel"]`:

**Alfred's context:**

```
Session: agent:alfred:whatsapp:group:120363403215116621@g.us
History: [user message, alfred's previous responses]
Workspace: /Users/pascal/openclaw-alfred/
Tools: read, write, exec
```

**Bärbel's context:**

```
Session: agent:baerbel:whatsapp:group:120363403215116621@g.us
History: [user message, baerbel's previous responses]
Workspace: /Users/pascal/openclaw-baerbel/
Tools: read only
```

## Best Practices

### 1. Keep Agents Focused

Design each agent with a single, clear responsibility:

```json
{
  "broadcast": {
    "DEV_GROUP": ["formatter", "linter", "tester"]
  }
}
```

✅ **Good:** Each agent has one job  
❌ **Bad:** One generic "dev-helper" agent

### 2. Use Descriptive Names

Make it clear what each agent does:

```json
{
  "agents": {
    "security-scanner": { "name": "Security Scanner" },
    "code-formatter": { "name": "Code Formatter" },
    "test-generator": { "name": "Test Generator" }
  }
}
```

### 3. Configure Different Tool Access

Give agents only the tools they need:

```json
{
  "agents": {
    "reviewer": {
      "tools": { "allow": ["read", "exec"] } // Read-only
    },
    "fixer": {
      "tools": { "allow": ["read", "write", "edit", "exec"] } // Read-write
    }
  }
}
```

### 4. Monitor Performance

With many agents, consider:

- Using `"strategy": "parallel"` (default) for speed
- Limiting broadcast groups to 5-10 agents
- Using faster models for simpler agents

### 5. Handle Failures Gracefully

Agents fail independently. One agent's error doesn't block others:

```
Message → [Agent A ✓, Agent B ✗ error, Agent C ✓]
Result: Agent A and C respond, Agent B logs error
```

## Compatibility

### Providers

Broadcast groups currently work with:

- ✅ WhatsApp (implemented)
- 🚧 Telegram (planned)
- 🚧 Discord (planned)
- 🚧 Slack (planned)

### Routing

Broadcast groups work alongside existing routing:

```json
{
  "bindings": [
    {
      "match": { "channel": "whatsapp", "peer": { "kind": "group", "id": "GROUP_A" } },
      "agentId": "alfred"
    }
  ],
  "broadcast": {
    "GROUP_B": ["agent1", "agent2"]
  }
}
```

- `GROUP_A`: Only alfred responds (normal routing)
- `GROUP_B`：agent1 和 agent2 都会响应（广播）

**优先级：** `broadcast` 的优先级高于 `bindings`。

## 故障排查

### 代理未响应

**检查：**

1. 代理 ID 存在于 `agents.list` 中
2. Peer ID 格式正确（例如 `120363403215116621@g.us`）
3. 代理不在拒绝列表中

**调试：**

```bash
tail -f ~/.openclaw/logs/gateway.log | grep broadcast
```

### 只有一个代理响应

**原因：** Peer ID 可能在 `bindings` 中，但不在 `broadcast` 中。

**解决方法：** 添加到 broadcast 配置中，或从 bindings 中移除。

### 性能问题

**如果在代理数量较多时变慢：**

- 减少每个组中的代理数量
- 使用更轻量的模型（使用 sonnet 而不是 opus）
- 检查沙箱启动时间

## 示例

### 示例 1：代码审查团队

```json
{
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": [
      "code-formatter",
      "security-scanner",
      "test-coverage",
      "docs-checker"
    ]
  },
  "agents": {
    "list": [
      {
        "id": "code-formatter",
        "workspace": "~/agents/formatter",
        "tools": { "allow": ["read", "write"] }
      },
      {
        "id": "security-scanner",
        "workspace": "~/agents/security",
        "tools": { "allow": ["read", "exec"] }
      },
      {
        "id": "test-coverage",
        "workspace": "~/agents/testing",
        "tools": { "allow": ["read", "exec"] }
      },
      { "id": "docs-checker", "workspace": "~/agents/docs", "tools": { "allow": ["read"] } }
    ]
  }
}
```

**用户发送：** 代码片段  
**响应：**

- code-formatter：“已修复缩进并添加了类型提示”
- security-scanner：“⚠️ 第 12 行存在 SQL 注入漏洞”
- test-coverage：“覆盖率为 45%，缺少错误场景的测试”
- docs-checker：“函数 `process_data` 缺少文档字符串”

### 示例 2：多语言支持

```json
{
  "broadcast": {
    "strategy": "sequential",
    "+15555550123": ["detect-language", "translator-en", "translator-de"]
  },
  "agents": {
    "list": [
      { "id": "detect-language", "workspace": "~/agents/lang-detect" },
      { "id": "translator-en", "workspace": "~/agents/translate-en" },
      { "id": "translator-de", "workspace": "~/agents/translate-de" }
    ]
  }
}
```

## API 参考

### 配置模式

```typescript
interface OpenClawConfig {
  broadcast?: {
    strategy?: "parallel" | "sequential";
    [peerId: string]: string[];
  };
}
```

### 字段

- `strategy`（可选）：如何处理代理
  - `"parallel"`（默认）：所有代理同时处理
  - `"sequential"`：代理按数组顺序处理
- `[peerId]`：WhatsApp 群组 JID、E.164 号码或其他 Peer ID
  - 值：应处理消息的代理 ID 数组

## 限制

1. **最大代理数：** 没有硬性限制，但 10 个以上代理可能会变慢
2. **共享上下文：** 代理彼此看不到对方的响应（设计如此）
3. **消息顺序：** 并行响应可能以任意顺序到达
4. **速率限制：** 所有代理都会计入 WhatsApp 的速率限制

## 未来增强

计划功能：

- [ ] 共享上下文模式（代理可以看到彼此的响应）
- [ ] 代理协作（代理可以相互发送信号）
- [ ] 动态代理选择（根据消息内容选择代理）
- [ ] 代理优先级（某些代理先于其他代理响应）

## 另请参阅

- [Multi-Agent Configuration](/tools/multi-agent-sandbox-tools)
- [Routing Configuration](/channels/channel-routing)
- [Session Management](/concepts/sessions)
