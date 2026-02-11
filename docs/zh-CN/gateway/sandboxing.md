---
summary: "How OpenClaw sandboxing works: modes, scopes, workspace access, and images"
title: Sandboxing
read_when: "You want a dedicated explanation of sandboxing or need to tune agents.defaults.sandbox."
status: active
---

# Sandboxing

OpenClaw can run **tools inside Docker containers** to reduce blast radius.
This is **optional** and controlled by configuration (`agents.defaults.sandbox` or
`agents.list[].sandbox`). If sandboxing is off, tools run on the host.
The Gateway stays on the host; tool execution runs in an isolated sandbox
when enabled.

This is not a perfect security boundary, but it materially limits filesystem
and process access when the model does something dumb.

## What gets sandboxed

- Tool execution (`exec`, `read`, `write`, `edit`, `apply_patch`, `process`, etc.).
- Optional sandboxed browser (`agents.defaults.sandbox.browser`).
  - By default, the sandbox browser auto-starts (ensures CDP is reachable) when the browser tool needs it.
    Configure via `agents.defaults.sandbox.browser.autoStart` and `agents.defaults.sandbox.browser.autoStartTimeoutMs`.
  - `agents.defaults.sandbox.browser.allowHostControl` lets sandboxed sessions target the host browser explicitly.
  - Optional allowlists gate `target: "custom"`: `allowedControlUrls`, `allowedControlHosts`, `allowedControlPorts`.

Not sandboxed:

- The Gateway process itself.
- Any tool explicitly allowed to run on the host (e.g. `tools.elevated`).
  - **Elevated exec runs on the host and bypasses sandboxing.**
  - If sandboxing is off, `tools.elevated` does not change execution (already on host). See [Elevated Mode](/tools/elevated).

## Modes

`agents.defaults.sandbox.mode` controls **when** sandboxing is used:

- `"off"`: no sandboxing.
- `"non-main"`: sandbox only **non-main** sessions (default if you want normal chats on host).
- `"all"`: every session runs in a sandbox.
  Note: `"non-main"` is based on `session.mainKey` (default `"main"`), not agent id.
  Group/channel sessions use their own keys, so they count as non-main and will be sandboxed.

## Scope

`agents.defaults.sandbox.scope` controls **how many containers** are created:

- `"session"` (default): one container per session.
- `"agent"`: one container per agent.
- `"shared"`: one container shared by all sandboxed sessions.

## Workspace access

`agents.defaults.sandbox.workspaceAccess` controls **what the sandbox can see**:

- `"none"` (default): tools see a sandbox workspace under `~/.openclaw/sandboxes`.
- `"ro"`: mounts the agent workspace read-only at `/agent` (disables `write`/`edit`/`apply_patch`).
- `"rw"`: mounts the agent workspace read/write at `/workspace`.

Inbound media is copied into the active sandbox workspace (`media/inbound/*`).
Skills note: the `read` tool is sandbox-rooted. With `workspaceAccess: "none"`,
OpenClaw mirrors eligible skills into the sandbox workspace (`.../skills`) so
they can be read. With `"rw"`, workspace skills are readable from
`/workspace/skills`.

## Custom bind mounts

`agents.defaults.sandbox.docker.binds` mounts additional host directories into the container.
Format: `host:container:mode` (e.g., `"/home/user/source:/source:rw"`).

Global and per-agent binds are **merged** (not replaced). Under `scope: "shared"`, per-agent binds are ignored.

Example (read-only source + docker socket):

```json5
{
  agents: {
    defaults: {
      sandbox: {
        docker: {
          binds: ["/home/user/source:/source:ro", "/var/run/docker.sock:/var/run/docker.sock"],
        },
      },
    },
    list: [
      {
        id: "build",
        sandbox: {
          docker: {
            binds: ["/mnt/cache:/cache:rw"],
          },
        },
      },
    ],
  },
}
```

Security notes:

- 2. 绑定（bind）会绕过沙箱文件系统：它们会以你设置的模式（`:ro` 或 `:rw`）暴露宿主机路径。
- 3. 敏感挂载（例如 `docker.sock`、密钥、SSH 密钥）除非绝对必要，否则应使用 `:ro`。
- 4. 如果你只需要对工作区的只读访问，可结合使用 `workspaceAccess: "ro"`；绑定模式彼此独立。
- 5. 参见 [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated) 了解绑定如何与工具策略和提升执行（elevated exec）交互。

## Images + setup

7. 默认镜像：`openclaw-sandbox:bookworm-slim`

8. 构建一次：

```bash
scripts/sandbox-setup.sh
```

10. 注意：默认镜像**不**包含 Node。 11. 如果某个技能需要 Node（或
    其他运行时），可以烘焙一个自定义镜像，或通过
    `sandbox.docker.setupCommand` 安装（需要网络出口 + 可写根文件系统 + root 用户）。

12. 沙箱化浏览器镜像：

```bash
scripts/sandbox-browser-setup.sh
```

14. 默认情况下，沙箱容器**没有网络**。
15. 可通过 `agents.defaults.sandbox.docker.network` 覆盖。

16. Docker 安装以及容器化的网关位于此处：
    [Docker](/install/docker)

## 17. setupCommand（一次性容器设置）

18. `setupCommand` 在沙箱容器创建后**只运行一次**（不是每次运行）。
    It executes inside the container via `sh -lc`.

20. 路径：

- 21. 全局：`agents.defaults.sandbox.docker.setupCommand`
- 22. 按代理：`agents.list[].sandbox.docker.setupCommand`

23. 常见陷阱：

- 24. 默认的 `docker.network` 是 `"none"`（无出口），因此包安装会失败。
- `readOnlyRoot: true` prevents writes; set `readOnlyRoot: false` or bake a custom image.
- 26. 进行包安装时 `user` 必须为 root（省略 `user` 或设置 `user: "0:0"`）。
- Sandbox exec does **not** inherit host `process.env`. 28. 使用
  `agents.defaults.sandbox.docker.env`（或自定义镜像）来提供技能的 API 密钥。

## 29. 工具策略 + 逃生舱（escape hatches）

30. 在沙箱规则之前，工具的允许/拒绝策略仍然适用。 If a tool is denied
    globally or per-agent, sandboxing doesn’t bring it back.

32. `tools.elevated` 是一个显式的逃生舱，会在宿主机上运行 `exec`。
33. `/exec` 指令仅适用于已授权的发送者并在每个会话中持久化；若要硬性禁用
    `exec`，请使用工具策略拒绝（参见 [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated)）。

34. 调试：

- 35. 使用 `openclaw sandbox explain` 来检查生效的沙箱模式、工具策略以及修复配置键。
- 36. 参见 [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated) 以理解“为什么被阻止？”的心智模型。
  37. 保持严格锁定。

## 38. 多代理覆盖

39. 每个代理都可以覆盖沙箱 + 工具：
    `agents.list[].sandbox` 和 `agents.list[].tools`（以及用于沙箱工具策略的 `agents.list[].tools.sandbox.tools`）。
40. 参见 [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools) 了解优先级。

## 41. 最小启用示例

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "none",
      },
    },
  },
}
```

## 43. 相关文档

- 44. [Sandbox Configuration](/gateway/configuration#agentsdefaults-sandbox)
- 45. [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools)
- 46. [Security](/gateway/security)
