---
summary: "每个代理的沙箱 + 工具限制、优先级与示例"
title: 多代理沙箱与工具
read_when: "你希望在多代理网关中实现每个代理独立的沙箱，或每个代理的工具允许/拒绝策略。"
status: active
---

# Multi-Agent Sandbox & Tools Configuration

## 概述

在多代理设置中，每个代理现在都可以拥有自己的：

- **沙箱配置**（`agents.list[].sandbox` 会覆盖 `agents.defaults.sandbox`）
- **工具限制**（`tools.allow` / `tools.deny`，以及 `agents.list[].tools`）

This allows you to run multiple agents with different security profiles:

- 拥有完全访问权限的个人助理
- Family/work agents with restricted tools
- 在沙箱中运行的对公众开放的代理

`setupCommand` 属于 `sandbox.docker`（全局或每个代理），并且在容器创建时只运行一次。

Auth is per-agent: each agent reads from its own `agentDir` auth store at:

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

凭据**不会**在代理之间共享。 Never reuse `agentDir` across agents.
如果你想共享凭据，请将 `auth-profiles.json` 复制到另一个代理的 `agentDir` 中。

有关沙箱在运行时的行为，请参见 [Sandboxing](/gateway/sandboxing)。
如需调试“为什么被阻止？”，请参见 [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated) 以及 `openclaw sandbox explain`。

---

## 配置示例

### 示例 1：个人 + 受限的家庭代理

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "name": "Personal Assistant",
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "family",
        "name": "Family Bot",
        "workspace": "~/.openclaw/workspace-family",
        "sandbox": {
          "mode": "all",
          "scope": "agent"
        },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit", "apply_patch", "process", "browser"]
        }
      }
    ]
  },
  "bindings": [
    {
      "agentId": "family",
      "match": {
        "provider": "whatsapp",
        "accountId": "*",
        "peer": {
          "kind": "group",
          "id": "120363424282127706@g.us"
        }
      }
    }
  ]
}
```

**结果：**

- `main` 代理：在主机上运行，拥有完整的工具访问权限
- `family` 代理：在 Docker 中运行（每个代理一个容器），仅允许使用 `read` 工具

---

### 示例 2：使用共享沙箱的工作代理

```json
{
  "agents": {
    "list": [
      {
        "id": "personal",
        "workspace": "~/.openclaw/workspace-personal",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "work",
        "workspace": "~/.openclaw/workspace-work",
        "sandbox": {
          "mode": "all",
          "scope": "shared",
          "workspaceRoot": "/tmp/work-sandboxes"
        },
        "tools": {
          "allow": ["read", "write", "apply_patch", "exec"],
          "deny": ["browser", "gateway", "discord"]
        }
      }
    ]
  }
}
```

---

### 示例 2b：全局编码配置 + 仅限消息的代理

```json
{
  "tools": { "profile": "coding" },
  "agents": {
    "list": [
      {
        "id": "support",
        "tools": { "profile": "messaging", "allow": ["slack"] }
      }
    ]
  }
}
```

**结果：**

- default agents get coding tools
- `support` 代理仅用于消息（+ Slack 工具）

---

### 示例 3：为每个代理设置不同的沙箱模式

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main", // Global default
        "scope": "session"
      }
    },
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw/workspace",
        "sandbox": {
          "mode": "off" // Override: main never sandboxed
        }
      },
      {
        "id": "public",
        "workspace": "~/.openclaw/workspace-public",
        "sandbox": {
          "mode": "all", // Override: public always sandboxed
          "scope": "agent"
        },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit", "apply_patch"]
        }
      }
    ]
  }
}
```

---

## 配置优先级

当同时存在全局（`agents.defaults.*`）和代理特定（`agents.list[].*`）配置时：

### 沙箱配置

代理特定设置会覆盖全局设置：

```
agents.list[].sandbox.mode > agents.defaults.sandbox.mode
agents.list[].sandbox.scope > agents.defaults.sandbox.scope
agents.list[].sandbox.workspaceRoot > agents.defaults.sandbox.workspaceRoot
agents.list[].sandbox.workspaceAccess > agents.defaults.sandbox.workspaceAccess
agents.list[].sandbox.docker.* > agents.defaults.sandbox.docker.*
agents.list[].sandbox.browser.* > agents.defaults.sandbox.browser.*
agents.list[].sandbox.prune.* > agents.defaults.sandbox.prune.*
```

**注意：**

- `agents.list[].sandbox.{docker,browser,prune}.*` 会覆盖该代理的 `agents.defaults.sandbox.{docker,browser,prune}.*`（当沙箱 scope 解析为 `"shared"` 时会被忽略）。

### 工具限制

The filtering order is:

1. **工具配置文件**（`tools.profile` 或 `agents.list[].tools.profile`）
2. **提供方工具配置文件**（`tools.byProvider[provider].profile` 或 `agents.list[].tools.byProvider[provider].profile`）
3. **全局工具策略**（`tools.allow` / `tools.deny`）
4. **提供方工具策略**（`tools.byProvider[provider].allow/deny`）
5. 1. **代理级工具策略**（`agents.list[].tools.allow/deny`）
6. 2. **代理提供方策略**（`agents.list[].tools.byProvider[provider].allow/deny`）
7. 3. **沙箱工具策略**（`tools.sandbox.tools` 或 `agents.list[].tools.sandbox.tools`）
8. 4. **子代理工具策略**（`tools.subagents.tools`，如适用）

5) 每一层级都可以进一步限制工具，但不能重新授予在更早层级中已被拒绝的工具。
6) 如果设置了 `agents.list[].tools.sandbox.tools`，则会替换该代理的 `tools.sandbox.tools`。
7) 如果设置了 `agents.list[].tools.profile`，则会覆盖该代理的 `tools.profile`。
   Provider tool keys accept either `provider` (e.g. `google-antigravity`) or `provider/model` (e.g. `openai/gpt-5.2`).

### 9. 工具组（快捷方式）

10. 工具策略（全局、代理、沙箱）支持 `group:*` 条目，可展开为多个具体工具：

- 11. `group:runtime`：`exec`、`bash`、`process`
- 12. `group:fs`：`read`、`write`、`edit`、`apply_patch`
- `group:sessions`: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
- 14. `group:memory`：`memory_search`、`memory_get`
- 15. `group:ui`：`browser`、`canvas`
- 16. `group:automation`：`cron`、`gateway`
- 17. `group:messaging`：`message`
- 18. `group:nodes`：`nodes`
- 19. `group:openclaw`：所有内置 OpenClaw 工具（不包括提供方插件）

### 20. 提升模式

21. `tools.elevated` 是全局基线（基于发送方的允许列表）。 22. `agents.list[].tools.elevated` 可以针对特定代理进一步限制提升权限（两者都必须允许）。

23. 缓解模式：

- 24. 为不受信任的代理拒绝 `exec`（`agents.list[].tools.deny: ["exec"]`）
- 25. 避免将会路由到受限代理的发送方加入允许列表
- 26. 如果只希望使用沙箱执行，可全局禁用提升模式（`tools.elevated.enabled: false`）
- 27. 针对敏感配置文件，可按代理禁用提升模式（`agents.list[].tools.elevated.enabled: false`）

---

## 28. 从单代理迁移

29. **之前（单代理）：**

```json
30. {
  "agents": {
    "defaults": {
      "workspace": "~/.openclaw/workspace",
      "sandbox": {
        "mode": "non-main"
      }
    }
  },
  "tools": {
    "sandbox": {
      "tools": {
        "allow": ["read", "write", "apply_patch", "exec"],
        "deny": []
      }
    }
  }
}
```

31. **之后（具有不同配置文件的多代理）：**

```json
32. {
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      }
    ]
  }
}
```

33. 旧版 `agent.*` 配置会由 `openclaw doctor` 迁移；今后优先使用 `agents.defaults` + `agents.list`。

---

## 34. 工具限制示例

### 35. 只读代理

```json
36. {
  "tools": {
    "allow": ["read"],
    "deny": ["exec", "write", "edit", "apply_patch", "process"]
  }
}
```

### 37. 安全执行代理（不修改文件）

```json
38. {
  "tools": {
    "allow": ["read", "exec", "process"],
    "deny": ["write", "edit", "apply_patch", "browser", "gateway"]
  }
}
```

### 39. 仅通信代理

```json
40. {
  "tools": {
    "allow": ["sessions_list", "sessions_send", "sessions_history", "session_status"],
    "deny": ["exec", "write", "edit", "apply_patch", "read", "browser"]
  }
}
```

---

## 41. 常见陷阱：“non-main”

`agents.defaults.sandbox.mode: "non-main"` is based on `session.mainKey` (default `"main"`),
not the agent id. 43. 群组/频道会话始终会获得各自的 key，因此
会被视为非 main 并被沙箱化。 44. 如果你希望某个代理永不
使用沙箱，请设置 `agents.list[].sandbox.mode: "off"`。

---

## 45. 测试

46. 在配置好多代理沙箱和工具之后：

1. 47. **检查代理解析：**

   ```exec
   48. openclaw agents list --bindings
   ```

2. 49. **验证沙箱容器：**

   ```exec
   50. docker ps --filter "name=openclaw-sbx-"
   ```

3. 1. **测试工具限制：**
   - 2. 发送一条需要受限工具的消息
   - 3. 验证代理无法使用被拒绝的工具

4. 4. **监控日志：**

   ```exec
   5. tail -f "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/logs/gateway.log" | grep -E "routing|sandbox|tools"
   ```

---

## 6. 故障排查

### 7. 尽管设置了 `mode: "all"`，代理仍未被沙箱化

- 8. 检查是否存在全局的 `agents.defaults.sandbox.mode` 覆盖了该设置
- 9. 代理级配置优先级更高，因此请设置 `agents.list[].sandbox.mode: "all"`

### 10. 尽管存在拒绝列表，工具仍然可用

- 11. 检查工具过滤顺序：全局 → 代理 → 沙箱 → 子代理
- 12. 每一层只能进一步限制，不能重新授予权限
- 13. 通过日志验证：`[tools] filtering tools for agent:${agentId}`

### 14. 容器未按代理进行隔离

- 15. 在代理专属的沙箱配置中设置 `scope: "agent"`
- 16. 默认值为 `"session"`，这会为每个会话创建一个容器

---

## 17. 另请参阅

- 18. [多代理路由](/concepts/multi-agent)
- 19. [沙箱配置](/gateway/configuration#agentsdefaults-sandbox)
- 20. [会话管理](/concepts/session)
