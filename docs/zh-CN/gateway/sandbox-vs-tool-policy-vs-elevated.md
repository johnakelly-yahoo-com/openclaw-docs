---
title: Sandbox vs 工具策略 vs 提权
summary: "工具被阻止的原因：sandbox 运行时、工具允许/拒绝策略，以及提权执行关卡。"
read_when: "你遇到了“sandbox jail”或看到工具/提权被拒，并希望知道需要修改的确切配置键。"
status: active
---

# Sandbox vs 工具策略 vs 提权

OpenClaw 有三种相关（但不同）的控制：

1. **Sandbox**（`agents.defaults.sandbox.*` / `agents.list[].sandbox.*`）决定**工具在哪里运行**（Docker vs 主机）。
2. **工具策略**（`tools.*`、`tools.sandbox.tools.*`、`agents.list[].tools.*`）决定**哪些工具可用/被允许**。
3. **提权**（`tools.elevated.*`、`agents.list[].tools.elevated.*`）是一个**仅用于 exec 的逃生口**，在你被 sandbox 时允许在主机上运行。

## 快速调试

使用检查器查看 OpenClaw **实际**在做什么：

```bash
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work
openclaw sandbox explain --json
```

它会打印：

- 生效的 sandbox 模式/作用域/工作区访问
- 当前会话是否处于 sandbox（main vs 非 main）
- 有效的沙箱工具允许/拒绝状态（以及其来源：agent/全局/默认）
- 提权关卡以及对应的修复配置键路径

## 沙箱：工具运行的位置

Sandbox 由 `agents.defaults.sandbox.mode` 控制：

- `"off"`：所有内容都在主机上运行。
- `"non-main"`：仅非 main 会话被 sandbox（对群组/频道来说是常见“惊喜”）。
- `"all"`：所有内容都被 sandbox。

完整矩阵（作用域、工作区挂载、镜像）请参见 [Sandboxing](/gateway/sandboxing)。

### 绑定挂载（安全快速检查）

- `docker.binds` 会**穿透** sandbox 文件系统：你挂载的任何内容都会以你设置的模式（`:ro` 或 `:rw`）在容器内可见。
- 如果省略模式，默认是读写；对源码/机密请优先使用 `:ro`。
- `scope: "shared"` 会忽略按 agent 的绑定（仅应用全局绑定）。
- 绑定 `/var/run/docker.sock` 实际上会把主机控制权交给 sandbox；仅在明确需要时才这样做。
- 工作区访问（`workspaceAccess: "ro"`/`"rw"`）与绑定模式相互独立。

## 工具策略：哪些工具存在/可被调用

Two layers matter:

- **Tool profile**: `tools.profile` and `agents.list[].tools.profile` (base allowlist)
- **Provider tool profile**: `tools.byProvider[provider].profile` and `agents.list[].tools.byProvider[provider].profile`
- **Global/per-agent tool policy**: `tools.allow`/`tools.deny` and `agents.list[].tools.allow`/`agents.list[].tools.deny`
- **Provider tool policy**: `tools.byProvider[provider].allow/deny` and `agents.list[].tools.byProvider[provider].allow/deny`
- **Sandbox tool policy** (only applies when sandboxed): `tools.sandbox.tools.allow`/`tools.sandbox.tools.deny` and `agents.list[].tools.sandbox.tools.*`

Rules of thumb:

- `deny` always wins.
- If `allow` is non-empty, everything else is treated as blocked.
- 工具策略是硬性限制：`/exec` 不能覆盖被拒绝的 `exec` 工具。
- `/exec` only changes session defaults for authorized senders; it does not grant tool access.
  Provider tool keys accept either `provider` (e.g. `google-antigravity`) or `provider/model` (e.g. `openai/gpt-5.2`).

### Tool groups (shorthands)

Tool policies (global, agent, sandbox) support `group:*` entries that expand to multiple tools:

```json5
{
  tools: {
    sandbox: {
      tools: {
        allow: ["group:runtime", "group:fs", "group:sessions", "group:memory"],
      },
    },
  },
}
```

Available groups:

- `group:runtime`: `exec`, `bash`, `process`
- `group:fs`: `read`, `write`, `edit`, `apply_patch`
- `group:sessions`: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
- `group:memory`: `memory_search`, `memory_get`
- `group:ui`：`browser`、`canvas`
- `group:automation`: `cron`, `gateway`
- `group:messaging`: `message`
- `group:nodes`：`nodes`
- `group:openclaw`：所有内置的 OpenClaw 工具（不包括提供方插件）

## Elevated: exec-only “run on host”

提升权限**不会**授予额外工具；它只影响 `exec`。

- If you’re sandboxed, `/elevated on` (or `exec` with `elevated: true`) runs on the host (approvals may still apply).
- Use `/elevated full` to skip exec approvals for the session.
- If you’re already running direct, elevated is effectively a no-op (still gated).
- Elevated is **not** skill-scoped and does **not** override tool allow/deny.
- `/exec` is separate from elevated. It only adjusts per-session exec defaults for authorized senders.

Gates:

- Enablement: `tools.elevated.enabled` (and optionally `agents.list[].tools.elevated.enabled`)
- Sender allowlists: `tools.elevated.allowFrom.<provider>` (and optionally `agents.list[].tools.elevated.allowFrom.<provider>`)

See [Elevated Mode](/tools/elevated).

## Common “sandbox jail” fixes

### “Tool X blocked by sandbox tool policy”

Fix-it keys (pick one):

- Disable sandbox: `agents.defaults.sandbox.mode=off` (or per-agent `agents.list[].sandbox.mode=off`)
- Allow the tool inside sandbox:
  - remove it from `tools.sandbox.tools.deny` (or per-agent `agents.list[].tools.sandbox.tools.deny`)
  - or add it to `tools.sandbox.tools.allow` (or per-agent allow)

### “I thought this was main, why is it sandboxed?”

In `"non-main"` mode, group/channel keys are _not_ main. Use the main session key (shown by `sandbox explain`) or switch mode to `"off"`.
