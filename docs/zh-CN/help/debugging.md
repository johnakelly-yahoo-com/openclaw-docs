---
summary: "调试工具：观察模式、原始模型流，以及推理泄漏的追踪"
read_when:
  - 你需要检查原始模型输出以发现推理泄漏
  - 你希望在迭代时以观察模式运行 Gateway
  - 你需要一个可重复的调试工作流
title: "调试"
---

# 调试

This page covers debugging helpers for streaming output, especially when a
provider mixes reasoning into normal text.

## Runtime debug overrides

Use `/debug` in chat to set **runtime-only** config overrides (memory, not disk).
`/debug` 默认禁用；通过 `commands.debug: true` 启用。
当你需要切换一些不常见的设置而不必编辑 `openclaw.json` 时，这会很方便。

示例：

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug unset messages.responsePrefix
/debug reset
```

`/debug reset` clears all overrides and returns to the on-disk config.

## Gateway 监听模式

为了快速迭代，在文件监听器下运行 gateway：

```bash
pnpm gateway:watch --force
```

This maps to:

```bash
tsx watch src/entry.ts gateway --force
```

在 `gateway:watch` 后添加任何 gateway CLI 标志，它们都会在每次重启时被传递。

## Dev 配置文件 + dev gateway（--dev）

使用 dev 配置文件来隔离状态，并启动一个安全、可随时丢弃的调试环境。 有 **两个** `--dev` 标志：

- **全局 `--dev`（配置文件）：** 将状态隔离在 `~/.openclaw-dev` 下，并将 gateway 端口默认设置为 `19001`（派生端口也会随之偏移）。
- **`gateway --dev`：** 告诉 Gateway 在缺失时自动创建默认配置 + 工作区（并跳过 BOOTSTRAP.md）。

推荐流程（dev 配置文件 + dev bootstrap）：

```bash
pnpm gateway:dev
OPENCLAW_PROFILE=dev openclaw tui
```

If you don’t have a global install yet, run the CLI via `pnpm openclaw ...`.

它做了什么：

1. **配置文件隔离**（全局 `--dev`）
   - `OPENCLAW_PROFILE=dev`
   - `OPENCLAW_STATE_DIR=~/.openclaw-dev`
   - `OPENCLAW_CONFIG_PATH=~/.openclaw-dev/openclaw.json`
   - `OPENCLAW_GATEWAY_PORT=19001`（浏览器/画布端口也会相应偏移）

2. **Dev bootstrap**（`gateway --dev`）
   - 在缺失时写入最小配置（`gateway.mode=local`，绑定回环地址）。
   - 将 `agent.workspace` 设置为 dev 工作区。
   - 设置 `agent.skipBootstrap=true`（不使用 BOOTSTRAP.md）。
   - 如果缺失，则填充工作区文件：
     `AGENTS.md`、`SOUL.md`、`TOOLS.md`、`IDENTITY.md`、`USER.md`、`HEARTBEAT.md`。
   - 默认身份：**C3‑PO**（协议机器人）。
   - 在 dev 模式下跳过频道提供者（`OPENCLAW_SKIP_CHANNELS=1`）。

重置流程（全新开始）：

```bash
pnpm gateway:dev:reset
```

注意：`--dev` 是一个**全局**配置文件标志，某些运行器会将其吞掉。
If you need to spell it out, use the env var form:

```bash
OPENCLAW_PROFILE=dev openclaw gateway --dev --reset
```

`--reset` 会清除配置、凭据、会话以及 dev 工作区（使用 `trash`，而不是 `rm`），然后重新创建默认的 dev 设置。

提示：如果已经有一个非 dev 的 gateway 在运行（launchd/systemd），请先停止它：

```bash
openclaw gateway stop
```

## Raw stream logging (OpenClaw)

OpenClaw 可以在任何过滤/格式化之前记录 **原始助手流**。
这是查看推理是以纯文本增量到达，还是作为独立思考块到达的最佳方式。

通过 CLI 启用：

```bash
pnpm gateway:watch --force --raw-stream
```

可选的路径覆盖：

```bash
pnpm gateway:watch --force --raw-stream --raw-stream-path ~/.openclaw/logs/raw-stream.jsonl
```

等效的环境变量：

```bash
OPENCLAW_RAW_STREAM=1
OPENCLAW_RAW_STREAM_PATH=~/.openclaw/logs/raw-stream.jsonl
```

Default file:

`~/.openclaw/logs/raw-stream.jsonl`

## Raw chunk logging (pi-mono)

To capture **raw OpenAI-compat chunks** before they are parsed into blocks,
pi-mono exposes a separate logger:

```bash
PI_RAW_STREAM=1
```

Optional path:

```bash
PI_RAW_STREAM_PATH=~/.pi-mono/logs/raw-openai-completions.jsonl
```

Default file:

`~/.pi-mono/logs/raw-openai-completions.jsonl`

> Note: this is only emitted by processes using pi-mono’s
> `openai-completions` provider.

## Safety notes

- Raw stream logs can include full prompts, tool output, and user data.
- Keep logs local and delete them after debugging.
- If you share logs, scrub secrets and PII first.
