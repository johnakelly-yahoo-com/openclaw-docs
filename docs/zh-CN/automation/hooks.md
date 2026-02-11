---
summary: "Hooks: event-driven automation for commands and lifecycle events"
read_when:
  - You want event-driven automation for /new, /reset, /stop, and agent lifecycle events
  - You want to build, install, or debug hooks
title: "Hooks"
---

# Hooks

Hooks provide an extensible event-driven system for automating actions in response to agent commands and events. Hooks are automatically discovered from directories and can be managed via CLI commands, similar to how skills work in OpenClaw.

## Getting Oriented

Hooks are small scripts that run when something happens. There are two kinds:

- **Hooks** (this page): run inside the Gateway when agent events fire, like `/new`, `/reset`, `/stop`, or lifecycle events.
- **Webhooks**: external HTTP webhooks that let other systems trigger work in OpenClaw. See [Webhook Hooks](/automation/webhook) or use `openclaw webhooks` for Gmail helper commands.

Hooks can also be bundled inside plugins; see [Plugins](/tools/plugin#plugin-hooks).

Common uses:

- Save a memory snapshot when you reset a session
- Keep an audit trail of commands for troubleshooting or compliance
- Trigger follow-up automation when a session starts or ends
- Write files into the agent workspace or call external APIs when events fire

If you can write a small TypeScript function, you can write a hook. Hooks are discovered automatically, and you enable or disable them via the CLI.

## Overview

The hooks system allows you to:

- Save session context to memory when `/new` is issued
- Log all commands for auditing
- Trigger custom automations on agent lifecycle events
- 2. 在不修改核心代码的情况下扩展 OpenClaw 的行为

## 3. 快速开始

### 4. 内置 Hooks

5. OpenClaw 随附四个会被自动发现的内置 hooks：

- **💾 session-memory**：当你执行 `/new` 时，将会话上下文保存到你的代理工作区（默认 `~/.openclaw/workspace/memory/`）
- 7. **📝 command-logger**：将所有命令事件记录到 `~/.openclaw/logs/commands.log`
- 8. **🚀 boot-md**：在网关启动时运行 `BOOT.md`（需要启用内部 hooks）
- 9. **😈 soul-evil**：在清理窗口期间或随机情况下，将注入的 `SOUL.md` 内容替换为 `SOUL_EVIL.md`

List available hooks:

```bash
11. openclaw hooks list
```

12. 启用一个 hook：

```bash
13. openclaw hooks enable session-memory
```

14. 检查 hook 状态：

```bash
15. openclaw hooks check
```

16. 获取详细信息：

```bash
17. openclaw hooks info session-memory
```

### 18. 新手引导

19. 在新手引导过程中（`openclaw onboard`），系统会提示你启用推荐的 hooks。 20. 向导会自动发现符合条件的 hooks，并将其呈现供你选择。

## 21. Hook 发现机制

22. Hooks 会从以下三个目录中自动发现（按优先级顺序）：

1. 23. **工作区 hooks**：`<workspace>/hooks/`（每个代理独立，优先级最高）
2. 24. **托管 hooks**：`~/.openclaw/hooks/`（用户安装，在多个工作区之间共享）
3. 25. **内置 hooks**：`<openclaw>/dist/hooks/bundled/`（随 OpenClaw 一起发布）

26) 托管 hook 目录既可以是**单个 hook**，也可以是一个**hook 包**（包目录）。

27. 每个 hook 都是一个包含以下内容的目录：

```
28. my-hook/
├── HOOK.md          # 元数据 + 文档
└── handler.ts       # 处理器实现
```

## 29. Hook 包（npm / 压缩包）

30. Hook 包是标准的 npm 包，通过在 `package.json` 中的 `openclaw.hooks` 导出一个或多个 hooks。 31. 使用以下命令安装：

```bash
32. openclaw hooks install <path-or-spec>
```

33. 示例 `package.json`：

```json
34. {
  "name": "@acme/my-hooks",
  "version": "0.1.0",
  "openclaw": {
    "hooks": ["./hooks/my-hook", "./hooks/other-hook"]
  }
}
```

35. 每个条目都指向一个包含 `HOOK.md` 和 `handler.ts`（或 `index.ts`）的 hook 目录。
36. Hook 包可以携带依赖项；它们将被安装在 `~/.openclaw/hooks/<id>` 下。

## 37. Hook 结构

### 38. HOOK.md 格式

39. `HOOK.md` 文件包含 YAML 前置元数据以及 Markdown 文档：

```markdown
40. ---
name: my-hook
description: "此 hook 功能的简要说明"
homepage: https://docs.openclaw.ai/hooks#my-hook
metadata:
  { "openclaw": { "emoji": "🔗", "events": ["command:new"], "requires": { "bins": ["node"] } } }
---

# My Hook

详细文档写在这里...

## 功能说明

- 监听 `/new` 命令
- 执行某些操作
- 记录结果

## 要求

- 必须已安装 Node.js

## 配置

无需配置。
```

### 41. 元数据字段

42. `metadata.openclaw` 对象支持：

- 43. **`emoji`**：CLI 中显示的表情符号（例如：`"💾"`）
- 44. **`events`**：要监听的事件数组（例如：`["command:new", "command:reset"]`）
- 45. **`export`**：要使用的具名导出（默认为 `"default"`）
- 46. **`homepage`**：文档 URL
- 47. **`requires`**：可选的依赖要求
  - 48. **`bins`**：PATH 中必须存在的二进制文件（例如：`["git", "node"]`）
  - 49. **`anyBins`**：这些二进制文件中至少需要存在一个
  - 50. **`env`**：必需的环境变量
  - **`config`**: Required config paths (e.g., `["workspace.dir"]`)
  - **`os`**: Required platforms (e.g., `["darwin", "linux"]`)
- **`always`**: Bypass eligibility checks (boolean)
- **`install`**: Installation methods (for bundled hooks: `[{"id":"bundled","kind":"bundled"}]`)

### Handler Implementation

The `handler.ts` file exports a `HookHandler` function:

```typescript
import type { HookHandler } from "../../src/hooks/hooks.js";

const myHandler: HookHandler = async (event) => {
  // Only trigger on 'new' command
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  console.log(`[my-hook] New command triggered`);
  console.log(`  Session: ${event.sessionKey}`);
  console.log(`  Timestamp: ${event.timestamp.toISOString()}`);

  // Your custom logic here

  // Optionally send message to user
  event.messages.push("✨ My hook executed!");
};

export default myHandler;
```

#### Event Context

Each event includes:

```typescript
{
  type: 'command' | 'session' | 'agent' | 'gateway',
  action: string,              // 例如：'new'、'reset'、'stop'
  sessionKey: string,          // 会话标识符
  timestamp: Date,             // 事件发生时间
  messages: string[],          // 在此推送要发送给用户的消息
  context: {
    sessionEntry?: SessionEntry,
    sessionId?: string,
    sessionFile?: string,
    commandSource?: string,    // 例如：'whatsapp'、'telegram'
    senderId?: string,
    workspaceDir?: string,
    bootstrapFiles?: WorkspaceBootstrapFile[],
    cfg?: OpenClawConfig
  }
}
```

## Event Types

### Command Events

Triggered when agent commands are issued:

- **`command`**: All command events (general listener)
- **`command:new`**: When `/new` command is issued
- **`command:reset`**: When `/reset` command is issued
- **`command:stop`**: When `/stop` command is issued

### Agent Events

- **`agent:bootstrap`**: Before workspace bootstrap files are injected (hooks may mutate `context.bootstrapFiles`)

### Gateway Events

Triggered when the gateway starts:

- **`gateway:startup`**: After channels start and hooks are loaded

### Tool Result Hooks (Plugin API)

这些 hooks 不是事件流监听器；它们允许插件在 OpenClaw 持久化结果之前同步调整工具结果。

- **`tool_result_persist`**: transform tool results before they are written to the session transcript. Must be synchronous; return the updated tool result payload or `undefined` to keep it as-is. See [Agent Loop](/concepts/agent-loop).

### Future Events

Planned event types:

- **`session:start`**: When a new session begins
- **`session:end`**: When a session ends
- **`agent:error`**: When an agent encounters an error
- **`message:sent`**: When a message is sent
- **`message:received`**: When a message is received

## Creating Custom Hooks

### 1. Choose Location

- **Workspace hooks** (`<workspace>/hooks/`): Per-agent, highest precedence
- **Managed hooks** (`~/.openclaw/hooks/`): Shared across workspaces

### 2. Create Directory Structure

```bash
mkdir -p ~/.openclaw/hooks/my-hook
cd ~/.openclaw/hooks/my-hook
```

### 3. Create HOOK.md

```markdown
---
name: my-hook
description: "Does something useful"
metadata: { "openclaw": { "emoji": "🎯", "events": ["command:new"] } }
---

# My Custom Hook

This hook does something useful when you issue `/new`.
```

### 4. Create handler.ts

```typescript
import type { HookHandler } from "../../src/hooks/hooks.js";

const handler: HookHandler = async (event) => {
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  console.log("[my-hook] Running!");
  // Your logic here
};

export default handler;
```

### 5. Enable and Test

```bash
# 验证钩子已被发现
openclaw hooks list

# 启用它
openclaw hooks enable my-hook

# 重启你的网关进程（macOS 上重启菜单栏应用，或重启你的开发进程）

# 触发事件
# 通过你的消息渠道发送 /new
```

## 配置

### 新配置格式（推荐）

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "session-memory": { "enabled": true },
        "command-logger": { "enabled": false }
      }
    }
  }
}
```

### 按钩子配置

钩子可以有自定义配置：

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "my-hook": {
          "enabled": true,
          "env": {
            "MY_CUSTOM_VAR": "value"
          }
        }
      }
    }
  }
}
```

### 额外目录

从附加目录加载钩子：

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "load": {
        "extraDirs": ["/path/to/more/hooks"]
      }
    }
  }
}
```

### 旧版配置格式（仍然支持）

为了向后兼容，旧的配置格式仍然可用：

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "handlers": [
        {
          "event": "command:new",
          "module": "./hooks/handlers/my-handler.ts",
          "export": "default"
        }
      ]
    }
  }
}
```

**迁移**：为新的钩子使用基于发现的新系统。 旧版处理器会在基于目录的钩子之后加载。

## CLI 命令

### 列出钩子

```bash
# 列出所有钩子
openclaw hooks list

# 仅显示符合条件的钩子
openclaw hooks list --eligible

# 详细输出（显示缺失的要求）
openclaw hooks list --verbose

# JSON 输出
openclaw hooks list --json
```

### 钩子信息

```bash
# 显示某个钩子的详细信息
openclaw hooks info session-memory

# JSON 输出
openclaw hooks info session-memory --json
```

### 检查可用性

```bash
# 显示可用性摘要
openclaw hooks check

# JSON 输出
openclaw hooks check --json
```

### 启用/禁用

```bash
# 启用一个钩子
openclaw hooks enable session-memory

# 禁用一个钩子
openclaw hooks disable command-logger
```

## 内置钩子参考

### session-memory

当你发出 `/new` 时，将会话上下文保存到内存。

**事件**：`command:new`

**要求**：必须配置 `workspace.dir`

**输出**：`<workspace>/memory/YYYY-MM-DD-slug.md`（默认为 `~/.openclaw/workspace`）

**功能说明**：

1. 使用重置前的会话条目来定位正确的对话记录
2. 提取最近 15 行对话
3. 使用 LLM 生成描述性的文件名 slug
4. 将会话元数据保存到按日期命名的内存文件中

**示例输出**：

```markdown
# 会话：2026-01-16 14:30:00 UTC

- **会话键**：agent:main:main
- **会话 ID**：abc123def456
- **来源**：telegram
```

**文件名示例**：

- `2026-01-16-vendor-pitch.md`
- `2026-01-16-api-design.md`
- `2026-01-16-1430.md`（如果 slug 生成失败时的回退时间戳）

**启用**：

```bash
openclaw hooks enable session-memory
```

### command-logger

将所有命令事件记录到一个集中式审计文件中。

**事件**：`command`

**要求**：无

**输出**：`~/.openclaw/logs/commands.log`

**功能说明**：

1. 捕获事件详情（命令动作、时间戳、会话键、发送者 ID、来源）
2. Appends to log file in JSONL format
3. Runs silently in the background

**Example log entries**:

```jsonl
{"timestamp":"2026-01-16T14:30:00.000Z","action":"new","sessionKey":"agent:main:main","senderId":"+1234567890","source":"telegram"}
{"timestamp":"2026-01-16T15:45:22.000Z","action":"stop","sessionKey":"agent:main:main","senderId":"user@example.com","source":"whatsapp"}
```

**View logs**:

```bash
# View recent commands
tail -n 20 ~/.openclaw/logs/commands.log

# Pretty-print with jq
cat ~/.openclaw/logs/commands.log | jq .

# Filter by action
grep '"action":"new"' ~/.openclaw/logs/commands.log | jq .
```

**Enable**:

```bash
openclaw hooks enable command-logger
```

### soul-evil

Swaps injected `SOUL.md` content with `SOUL_EVIL.md` during a purge window or by random chance.

**Events**: `agent:bootstrap`

**Docs**: [SOUL Evil Hook](/hooks/soul-evil)

**Output**: No files written; swaps happen in-memory only.

**Enable**:

```bash
openclaw hooks enable soul-evil
```

**Config**:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "soul-evil": {
          "enabled": true,
          "file": "SOUL_EVIL.md",
          "chance": 0.1,
          "purge": { "at": "21:00", "duration": "15m" }
        }
      }
    }
  }
}
```

### boot-md

Runs `BOOT.md` when the gateway starts (after channels start).
Internal hooks must be enabled for this to run.

**Events**: `gateway:startup`

**Requirements**: `workspace.dir` must be configured

**What it does**:

1. Reads `BOOT.md` from your workspace
2. Runs the instructions via the agent runner
3. Sends any requested outbound messages via the message tool

**Enable**:

```bash
openclaw hooks enable boot-md
```

## Best Practices

### Keep Handlers Fast

Hooks run during command processing. Keep them lightweight:

```typescript
// ✓ Good - async work, returns immediately
const handler: HookHandler = async (event) => {
  void processInBackground(event); // Fire and forget
};

// ✗ Bad - blocks command processing
const handler: HookHandler = async (event) => {
  await slowDatabaseQuery(event);
  await evenSlowerAPICall(event);
};
```

### Handle Errors Gracefully

Always wrap risky operations:

```typescript
const handler: HookHandler = async (event) => {
  try {
    await riskyOperation(event);
  } catch (err) {
    console.error("[my-handler] Failed:", err instanceof Error ? err.message : String(err));
    // Don't throw - let other handlers run
  }
};
```

### Filter Events Early

Return early if the event isn't relevant:

```typescript
const handler: HookHandler = async (event) => {
  // Only handle 'new' commands
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  // Your logic here
};
```

### Use Specific Event Keys

Specify exact events in metadata when possible:

```yaml
metadata: { "openclaw": { "events": ["command:new"] } } # Specific
```

Rather than:

```yaml
metadata: { "openclaw": { "events": ["command"] } } # General - more overhead
```

## Debugging

### Enable Hook Logging

The gateway logs hook loading at startup:

```
Registered hook: session-memory -> command:new
Registered hook: command-logger -> command
Registered hook: boot-md -> gateway:startup
```

### Check Discovery

List all discovered hooks:

```bash
openclaw hooks list --verbose
```

### 2. 检查注册状态

在你的处理器中，记录它被调用的时间：

```typescript
4. const handler: HookHandler = async (event) => {
  console.log("[my-handler] Triggered:", event.type, event.action);
  // Your logic
};
```

### 5. 验证资格

6. 检查某个 hook 为什么不符合资格：

```bash
7. openclaw hooks info my-hook
```

8. 在输出中查找缺失的要求。

## 9. 测试

### 10. 网关日志

11. 监控网关日志以查看 hook 的执行情况：

```bash
12. # macOS
./scripts/clawlog.sh -f

# Other platforms
tail -f ~/.openclaw/gateway.log
```

### 直接测试 Hooks

14. 在隔离环境中测试你的处理器：

```typescript
15. import { test } from "vitest";
import { createHookEvent } from "./src/hooks/hooks.js";
import myHandler from "./hooks/my-hook/handler.js";

test("my handler works", async () => {
  const event = createHookEvent("command", "new", "test-session", {
    foo: "bar",
  });

  await myHandler(event);

  // Assert side effects
});
```

## Architecture

### 17. 核心组件

- 18. **`src/hooks/types.ts`**：类型定义
- 19. **`src/hooks/workspace.ts`**：目录扫描与加载
- 20. **`src/hooks/frontmatter.ts`**：HOOK.md 元数据解析
- 21. **`src/hooks/config.ts`**：资格检查
- 22. **`src/hooks/hooks-status.ts`**：状态报告
- 23. **`src/hooks/loader.ts`**：动态模块加载器
- 24. **`src/cli/hooks-cli.ts`**：CLI 命令
- 25. **`src/gateway/server-startup.ts`**：在网关启动时加载 hooks
- 26. **`src/auto-reply/reply/commands-core.ts`**：触发命令事件

### 发现流程

```
28. 网关启动
    ↓
扫描目录（workspace → managed → bundled）
    ↓
解析 HOOK.md 文件
    ↓
检查资格（bins、env、config、os）
    ↓
从符合资格的 hooks 中加载处理器
    ↓
为事件注册处理器
```

### 29. 事件流程

```
30. 用户发送 /new
    ↓
命令校验
    ↓
创建 hook 事件
    ↓
触发 hook（所有已注册的处理器）
    ↓
命令处理继续
    ↓
会话重置
```

## 31. 故障排查

### 32. Hook 未被发现

1. 33. 检查目录结构：

   ```bash
   34. ls -la ~/.openclaw/hooks/my-hook/
   # Should show: HOOK.md, handler.ts
   ```

2. 35. 验证 HOOK.md 格式：

   ```bash
   36. cat ~/.openclaw/hooks/my-hook/HOOK.md
   # Should have YAML frontmatter with name and metadata
   ```

3. 37. 列出所有已发现的 hooks：

   ```bash
   38. openclaw hooks list
   ```

### 39) Hook 不符合资格

40. 检查要求：

```bash
41. openclaw hooks info my-hook
```

42. 查找缺失项：

- 43. 二进制文件（检查 PATH）
- 44. 环境变量
- 45. 配置值
- 46. 操作系统兼容性

### 47. Hook 未执行

1. 48. 确认 hook 已启用：

   ```bash
   49. openclaw hooks list
   # Should show ✓ next to enabled hooks
   ```

2. 50. 重启你的网关进程以便重新加载 hooks。

3. Check gateway logs for errors:

   ```bash
   ./scripts/clawlog.sh | grep hook
   ```

### Handler Errors

Check for TypeScript/import errors:

```bash
# Test import directly
node -e "import('./path/to/handler.ts').then(console.log)"
```

## Migration Guide

### From Legacy Config to Discovery

**Before**:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "handlers": [
        {
          "event": "command:new",
          "module": "./hooks/handlers/my-handler.ts"
        }
      ]
    }
  }
}
```

**After**:

1. Create hook directory:

   ```bash
   mkdir -p ~/.openclaw/hooks/my-hook
   mv ./hooks/handlers/my-handler.ts ~/.openclaw/hooks/my-hook/handler.ts
   ```

2. Create HOOK.md:

   ```markdown
   ---
   name: my-hook
   description: "My custom hook"
   metadata: { "openclaw": { "emoji": "🎯", "events": ["command:new"] } }
   ---

   # My Hook

   Does something useful.
   ```

3. Update config:

   ```json
   {
     "hooks": {
       "internal": {
         "enabled": true,
         "entries": {
           "my-hook": { "enabled": true }
         }
       }
     }
   }
   ```

4. Verify and restart your gateway process:

   ```bash
   openclaw hooks list
   # Should show: 🎯 my-hook ✓
   ```

**Benefits of migration**:

- Automatic discovery
- CLI management
- Eligibility checking
- Better documentation
- Consistent structure

## See Also

- [CLI Reference: hooks](/cli/hooks)
- [Bundled Hooks README](https://github.com/openclaw/openclaw/tree/main/src/hooks/bundled)
- [Webhook Hooks](/automation/webhook)
- [Configuration](/gateway/configuration#hooks)
