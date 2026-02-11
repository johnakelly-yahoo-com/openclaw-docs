---
summary: "1. Exec 审批、允许列表和沙盒逃逸提示"
read_when:
  - 2. 配置 Exec 审批或允许列表
  - 3. 在 macOS 应用中实现 Exec 审批 UX
  - 4. 审查沙盒逃逸提示及其影响
title: "5. Exec 审批"
---

# 6. Exec 审批

7. Exec 审批是用于让沙盒化代理在真实主机（`gateway` 或 `node`）上运行命令的 **配套应用 / 节点主机防护栏**。 Think of it like a safety interlock:
   commands are allowed only when policy + allowlist + (optional) user approval all agree.
8. Exec 审批是 **额外** 叠加在工具策略和提升级别门控之上的（除非 elevated 设置为 `full`，此时会跳过审批）。
9. 生效策略取 `tools.exec.*` 与审批默认值中 **更严格** 的那个；如果某个审批字段被省略，则使用 `tools.exec` 的值。

11. 如果 **配套应用 UI 不可用**，任何需要提示的请求都会
    由 **询问回退** 处理（默认：拒绝）。

## 12. 适用范围

13. Exec 审批在执行主机上本地强制执行：

- 14. **gateway 主机** → 网关机器上的 `openclaw` 进程
- 15. **node 主机** → 节点运行器（macOS 配套应用或无头节点主机）

16. macOS 拆分：

- 17. **node 主机服务** 通过本地 IPC 将 `system.run` 转发给 **macOS 应用**。
- 18. **macOS 应用** 执行审批并在 UI 上下文中执行命令。

## 19. 设置与存储

20. 审批存储在执行主机上的本地 JSON 文件中：

21. `~/.openclaw/exec-approvals.json`

22. 示例 schema：

```json
23. {
  "version": 1,
  "socket": {
    "path": "~/.openclaw/exec-approvals.sock",
    "token": "base64url-token"
  },
  "defaults": {
    "security": "deny",
    "ask": "on-miss",
    "askFallback": "deny",
    "autoAllowSkills": false
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "askFallback": "deny",
      "autoAllowSkills": true,
      "allowlist": [
        {
          "id": "B0C8C0B3-2C2D-4F8A-9A3C-5A4B3C2D1E0F",
          "pattern": "~/Projects/**/bin/rg",
          "lastUsedAt": 1737150000000,
          "lastUsedCommand": "rg -n TODO",
          "lastResolvedPath": "/Users/user/Projects/.../bin/rg"
        }
      ]
    }
  }
}
```

## 24. 策略旋钮

### 25. 安全性（`exec.security`）

- 26. **deny**：阻止所有主机 exec 请求。
- 27. **allowlist**：仅允许允许列表中的命令。
- 28. **full**：允许所有内容（等同于 elevated）。

### Ask (`exec.ask`)

- 30. **off**：从不提示。
- 31. **on-miss**：仅当未命中允许列表时提示。
- 32. **always**：每个命令都提示。

### 33. 询问回退（`askFallback`）

34. 如果需要提示但没有可达的 UI，由回退策略决定：

- 35. **deny**：阻止。
- 36. **allowlist**：仅当命中允许列表时允许。
- 37. **full**：允许。

## 38. 允许列表（按代理）

39. 允许列表是 **按代理** 的。 40. 如果存在多个代理，请在 macOS 应用中切换你正在编辑的代理。 41. 模式是 **不区分大小写的 glob 匹配**。
40. 模式应解析为 **二进制路径**（仅基名的条目会被忽略）。
41. 旧版 `agents.default` 条目在加载时会迁移到 `agents.main`。

44. 示例：

- 45. `~/Projects/**/bin/peekaboo`
- 46. `~/.local/bin/*`
- 47. `/opt/homebrew/bin/rg`

48. 每个允许列表条目会跟踪：

- 49. **id**：用于 UI 标识的稳定 UUID（可选）
- 50. **最近使用** 时间戳
- **上次使用的命令**
- **上次解析的路径**

## 自动允许技能 CLI

当启用 **自动允许技能 CLI** 时，已知技能引用的可执行文件会在节点（macOS 节点或无头节点主机）上被视为已加入允许列表。 这通过 Gateway RPC 使用 `skills.bins` 来获取技能二进制列表。 如果你希望严格的手动允许列表，请禁用此项。

## 安全二进制（仅 stdin）

`tools.exec.safeBins` 定义了一小部分 **仅 stdin** 的二进制程序（例如 `jq`），它们可以在 **无需** 显式允许列表条目的情况下以允许列表模式运行。 安全二进制会拒绝位置参数中的文件参数和类似路径的标记，因此它们只能作用于传入的流。
在允许列表模式下，不会自动允许 Shell 链接和重定向。

当每个顶级片段都满足允许列表（包括安全二进制或技能自动允许）时，允许使用 Shell 链接（`&&`、`||`、`;`）。 在允许列表模式下仍然不支持重定向。
在允许列表解析期间会拒绝命令替换（`$()` / 反引号），即使在双引号内也是如此；如果需要字面量 `$()` 文本，请使用单引号。

默认安全二进制：`jq`、`grep`、`cut`、`sort`、`uniq`、`head`、`tail`、`tr`、`wc`。

## 控制 UI 编辑

使用 **控制 UI → Nodes → Exec approvals** 卡片来编辑默认值、按代理的覆盖项以及允许列表。 选择一个作用域（默认值或某个代理），调整策略，添加/移除允许列表模式，然后点击 **保存**。 UI 会按模式显示 **上次使用** 的元数据，便于你保持列表整洁。

目标选择器可选择 **Gateway**（本地审批）或 **Node**。 节点必须声明 `system.execApprovals.get/set`（macOS 应用或无头节点主机）。
如果某个节点尚未声明 exec 审批，请直接编辑其本地的 `~/.openclaw/exec-approvals.json`。

CLI：`openclaw approvals` 支持 Gateway 或节点编辑（参见 [Approvals CLI](/cli/approvals)）。

## 审批流程

当需要提示时，Gateway 会向操作员客户端广播 `exec.approval.requested`。
控制 UI 和 macOS 应用通过 `exec.approval.resolve` 进行处理，然后 Gateway 将已批准的请求转发给节点主机。

当需要审批时，exec 工具会立即返回一个审批 id。 使用该 id 来关联后续的系统事件（`Exec finished` / `Exec denied`）。 如果在超时之前没有收到决定，请求将被视为审批超时，并以拒绝原因呈现。

确认对话框包含：

- 命令 + 参数
- cwd
- 代理 id
- 已解析的可执行文件路径
- 主机 + 策略元数据

操作：

- **仅允许一次** → 立即运行
- **始终允许** → 添加到允许列表 + 运行
- **拒绝** → 阻止

## 将审批转发到聊天频道

你可以将 exec 审批提示转发到任意聊天频道（包括插件频道），并使用 `/approve` 进行审批。 这使用的是正常的出站投递流水线。

配置：

```json5
{
  approvals: {
    exec: {
      enabled: true,
      mode: "session", // "session" | "targets" | "both"
      agentFilter: ["main"],
      sessionFilter: ["discord"], // substring or regex
      targets: [
        { channel: "slack", to: "U12345678" },
        { channel: "telegram", to: "123456789" },
      ],
    },
  },
}
```

在聊天中回复：

```
/approve <id> allow-once
/approve <id> allow-always
/approve <id> deny
```

### macOS IPC 流程

```
Gateway -> Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + approvals + system.run)
```

安全说明：

- Unix 套接字模式 `0600`，令牌存储在 `exec-approvals.json` 中。
- 同 UID 对等方检查。
- Challenge/response (nonce + HMAC token + request hash) + short TTL.

## System events

Exec lifecycle is surfaced as system messages:

- `Exec running` (only if the command exceeds the running notice threshold)
- `Exec finished`
- `Exec denied`

These are posted to the agent’s session after the node reports the event.
Gateway-host exec approvals emit the same lifecycle events when the command finishes (and optionally when running longer than the threshold).
Approval-gated execs reuse the approval id as the `runId` in these messages for easy correlation.

## Implications

- **full** is powerful; prefer allowlists when possible.
- **ask** keeps you in the loop while still allowing fast approvals.
- Per-agent allowlists prevent one agent’s approvals from leaking into others.
- Approvals only apply to host exec requests from **authorized senders**. Unauthorized senders cannot issue `/exec`.
- `/exec security=full` is a session-level convenience for authorized operators and skips approvals by design.
  To hard-block host exec, set approvals security to `deny` or deny the `exec` tool via tool policy.

Related:

- [Exec tool](/tools/exec)
- [Elevated mode](/tools/elevated)
- [Skills](/tools/skills)
