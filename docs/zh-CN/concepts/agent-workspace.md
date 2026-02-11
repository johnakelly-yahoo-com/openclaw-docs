---
summary: "Agent workspace: location, layout, and backup strategy"
read_when:
  - You need to explain the agent workspace or its file layout
  - You want to back up or migrate an agent workspace
title: "Agent Workspace"
---

# Agent workspace

The workspace is the agent's home. 47. 它是文件工具和工作区上下文唯一使用的工作目录。 Keep it private and treat it as memory.

This is separate from `~/.openclaw/`, which stores config, credentials, and
sessions.

**Important:** the workspace is the **default cwd**, not a hard sandbox. Tools
resolve relative paths against the workspace, but absolute paths can still reach
elsewhere on the host unless sandboxing is enabled. If you need isolation, use
[`agents.defaults.sandbox`](/gateway/sandboxing) (and/or per‑agent sandbox config).
When sandboxing is enabled and `workspaceAccess` is not `"rw"`, tools operate
inside a sandbox workspace under `~/.openclaw/sandboxes`, not your host workspace.

## Default location

- Default: `~/.openclaw/workspace`
- 1. 如果设置了 `OPENCLAW_PROFILE` 且不为 `"default"`，默认路径将变为
     `~/.openclaw/workspace-<profile>`。
- 2. 在 `~/.openclaw/openclaw.json` 中覆盖：

```json5
3. {
  agent: {
    workspace: "~/.openclaw/workspace",
  },
}
```

4. `openclaw onboard`、`openclaw configure` 或 `openclaw setup` 会在缺失时创建工作区并初始化引导文件。

5. 如果你已经自行管理工作区文件，可以禁用引导文件创建：

```json5
6. { agent: { skipBootstrap: true } }
```

## 7. 额外的工作区文件夹

8. 较早的安装版本可能创建了 `~/openclaw`。 9. 同时保留多个工作区目录可能会导致认证或状态漂移的混乱，因为一次只有一个工作区处于活动状态。

10. **建议：** 保持单一的活动工作区。 11. 如果你不再使用这些额外的文件夹，请将其归档或移至废纸篓（例如 `trash ~/openclaw`）。
11. 如果你有意保留多个工作区，请确保 `agents.defaults.workspace` 指向当前活动的那个。

13. `openclaw doctor` 在检测到额外的工作区目录时会发出警告。

## 14. 工作区文件映射（各文件的含义）

15. 以下是 OpenClaw 在工作区中期望存在的标准文件：

- 16. `AGENTS.md`
  - 17. 代理的操作说明以及它应如何使用记忆。
  - 18. 在每个会话开始时加载。
  - 19. 适合放置规则、优先级以及“如何行为”的细节。

- 20. `SOUL.md`
  - 21. 人设、语气和边界。
  - 22. 每个会话都会加载。

- 23. `USER.md`
  - 24. 用户是谁以及如何称呼他们。
  - 25. 每个会话都会加载。

- 26. `IDENTITY.md`
  - 27. 代理的名称、氛围和表情符号。
  - 28. 在引导仪式期间创建或更新。

- 29. `TOOLS.md`
  - 30. 关于本地工具和约定的说明。
  - 31. 不控制工具可用性；仅作为指导。

- 32. `HEARTBEAT.md`
  - 33. 用于心跳运行的可选简短检查清单。
  - 34. 保持简短以避免消耗过多 token。

- 35. `BOOT.md`
  - 36. 当启用内部钩子时，在网关重启时执行的可选启动检查清单。
  - 37. 保持简短；对外发送请使用消息工具。

- 38. `BOOTSTRAP.md`
  - 39. 一次性的首次运行仪式。
  - 40. 仅在全新的工作区中创建。
  - 41. 仪式完成后将其删除。

- 42. `memory/YYYY-MM-DD.md`
  - 43. 每日记忆日志（每天一个文件）。
  - 44. 建议在会话开始时读取今天 + 昨天的内容。

- 45. `MEMORY.md`（可选）
  - 46. 精选的长期记忆。
  - 47. 仅在主私有会话中加载（不用于共享/群组上下文）。

48. 有关工作流和自动记忆刷新，请参见 [Memory](/concepts/memory)。

- 49. `skills/`（可选）
  - 50. 工作区专用技能。
  - Overrides managed/bundled skills when names collide.

- `canvas/` (optional)
  - Canvas UI files for node displays (for example `canvas/index.html`).

If any bootstrap file is missing, OpenClaw injects a "missing file" marker into
the session and continues. Large bootstrap files are truncated when injected;
adjust the limit with `agents.defaults.bootstrapMaxChars` (default: 20000).
`openclaw setup` can recreate missing defaults without overwriting existing
files.

## What is NOT in the workspace

These live under `~/.openclaw/` and should NOT be committed to the workspace repo:

- `~/.openclaw/openclaw.json` (config)
- `~/.openclaw/credentials/` (OAuth tokens, API keys)
- `~/.openclaw/agents/<agentId>/sessions/` (session transcripts + metadata)
- `~/.openclaw/skills/` (managed skills)

If you need to migrate sessions or config, copy them separately and keep them
out of version control.

## Git backup (recommended, private)

Treat the workspace as private memory. Put it in a **private** git repo so it is
backed up and recoverable.

Run these steps on the machine where the Gateway runs (that is where the
workspace lives).

### 1. Initialize the repo

If git is installed, brand-new workspaces are initialized automatically. If this
workspace is not already a repo, run:

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md memory/
git commit -m "Add agent workspace"
```

### 2. Add a private remote (beginner-friendly options)

48. 选项 A：GitHub Web UI

1. Create a new **private** repository on GitHub.
2. Do not initialize with a README (avoids merge conflicts).
3. Copy the HTTPS remote URL.
4. Add the remote and push:

```bash
git branch -M main
git remote add origin <https-url>
git push -u origin main
```

Option B: GitHub CLI (`gh`)

```bash
gh auth login
gh repo create openclaw-workspace --private --source . --remote origin --push
```

Option C: GitLab web UI

1. Create a new **private** repository on GitLab.
2. Do not initialize with a README (avoids merge conflicts).
3. Copy the HTTPS remote URL.
4. Add the remote and push:

```bash
git branch -M main
git remote add origin <https-url>
git push -u origin main
```

### 3. Ongoing updates

```bash
git status
git add .
git commit -m "Update memory"
git push
```

## Do not commit secrets

Even in a private repo, avoid storing secrets in the workspace:

- API keys, OAuth tokens, passwords, or private credentials.
- Anything under `~/.openclaw/`.
- Raw dumps of chats or sensitive attachments.

If you must store sensitive references, use placeholders and keep the real
secret elsewhere (password manager, environment variables, or `~/.openclaw/`).

Suggested `.gitignore` starter:

```gitignore
.DS_Store
.env
**/*.key
**/*.pem
**/secrets*
```

## Moving the workspace to a new machine

1. Clone the repo to the desired path (default `~/.openclaw/workspace`).
2. Set `agents.defaults.workspace` to that path in `~/.openclaw/openclaw.json`.
3. Run `openclaw setup --workspace <path>` to seed any missing files.
4. If you need sessions, copy `~/.openclaw/agents/<agentId>/sessions/` from the
   old machine separately.

## Advanced notes

- Multi-agent routing can use different workspaces per agent. See
  [Channel routing](/channels/channel-routing) for routing configuration.
- If `agents.defaults.sandbox` is enabled, non-main sessions can use per-session sandbox
  workspaces under `agents.defaults.sandbox.workspaceRoot`.
