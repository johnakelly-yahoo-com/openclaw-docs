---
summary: "[Lume CLI Reference](https://cua.ai/docs/lume/reference/cli-reference)"
read_when:
  - "[Unattended VM Setup](https://cua.ai/docs/lume/guide/fundamentals/unattended-setup)（高级）"
  - "[Docker Sandboxing](/install/docker)（替代的隔离方案）"
title: "Migration Guide"
---

# 你正在将 OpenClaw 迁移到一台新的笔记本电脑或服务器

你希望保留会话、认证以及频道登录（WhatsApp 等）

迁移指南

- 将 OpenClaw 迁移到新机器
- 本指南将在**无需重新进行引导设置**的情况下，将 OpenClaw Gateway 从一台机器迁移到另一台机器。

从概念上讲，迁移非常简单：

## Before you start (what you are migrating)

### 1. Identify your state directory

Most installs use the default:

- **State dir:** `~/.openclaw/`

But it may be different if you use:

- `--profile <name>` (often becomes `~/.openclaw-<profile>/`)
- `OPENCLAW_STATE_DIR=/some/path`

If you’re not sure, run on the **old** machine:

```bash
openclaw status
```

Look for mentions of `OPENCLAW_STATE_DIR` / profile in the output. If you run multiple gateways, repeat for each profile.

### 2. Identify your workspace

Common defaults:

- `~/.openclaw/workspace/` (recommended workspace)
- a custom folder you created

Your workspace is where files like `MEMORY.md`, `USER.md`, and `memory/*.md` live.

### 3. Understand what you will preserve

If you copy **both** the state dir and workspace, you keep:

- Gateway configuration (`openclaw.json`)
- Auth profiles / API keys / OAuth tokens
- Session history + agent state
- Channel state (e.g. WhatsApp login/session)
- Your workspace files (memory, skills notes, etc.)

If you copy **only** the workspace (e.g., via Git), you do **not** preserve:

- sessions
- credentials
- channel logins

Those live under `$OPENCLAW_STATE_DIR`.

## Migration steps (recommended)

### Step 0 — Make a backup (old machine)

On the **old** machine, stop the gateway first so files aren’t changing mid-copy:

```bash
openclaw gateway stop
```

(Optional but recommended) archive the state dir and workspace:

```bash
# Adjust paths if you use a profile or custom locations
cd ~
tar -czf openclaw-state.tgz .openclaw

tar -czf openclaw-workspace.tgz .openclaw/workspace
```

If you have multiple profiles/state dirs (e.g. `~/.openclaw-main`, `~/.openclaw-work`), archive each.

### Step 1 — Install OpenClaw on the new machine

On the **new** machine, install the CLI (and Node if needed):

- See: [Install](/install)

At this stage, it’s OK if onboarding creates a fresh `~/.openclaw/` — you will overwrite it in the next step.

### Step 2 — Copy the state dir + workspace to the new machine

复制 **两者**：

- `$OPENCLAW_STATE_DIR` (default `~/.openclaw/`)
- your workspace (default `~/.openclaw/workspace/`)

Common approaches:

- `scp` the tarballs and extract
- `rsync -a` over SSH
- external drive

After copying, ensure:

- Hidden directories were included (e.g. `.openclaw/`)
- File ownership is correct for the user running the gateway

### 1. 步骤 3 — 运行 Doctor（迁移 + 服务修复）

2. 在**新**机器上：

```bash
3. openclaw doctor
```

4. Doctor 是一个“安全且无聊”的命令。 5. 它会修复服务、应用配置迁移，并对不匹配情况发出警告。

6. 然后：

```bash
7. openclaw gateway restart
openclaw status
```

## 8. 常见踩坑点（以及如何避免）

### 9. 踩坑点：profile / state-dir 不匹配

10. 如果你之前使用某个 profile（或 `OPENCLAW_STATE_DIR`）运行旧的 gateway，而新的 gateway 使用了不同的 profile，你会看到如下症状：

- 11. 配置更改未生效
- 12. 频道缺失 / 被登出
- 13. 会话历史为空

14. 解决方法：使用**相同**的 profile/state 目录来运行你已迁移的 gateway/service，然后重新运行：

```bash
15. openclaw doctor
```

### 16. 踩坑点：只复制 `openclaw.json`

17. 仅有 `openclaw.json` 是不够的。 18. 许多提供方会将状态存储在：

- 19. `$OPENCLAW_STATE_DIR/credentials/`
- 20. `$OPENCLAW_STATE_DIR/agents/<agentId>/...`

21. 始终迁移整个 `$OPENCLAW_STATE_DIR` 文件夹。

### 22. 踩坑点：权限 / 所有权

23. 如果你以 root 复制或更换了用户，gateway 可能无法读取凭据/会话。

24. 解决方法：确保 state 目录和 workspace 归运行 gateway 的用户所有。

### 25. 踩坑点：在远程/本地模式之间迁移

- 26. 如果你的 UI（WebUI/TUI）指向**远程** gateway，那么会话存储和 workspace 归远程主机所有。
- 27. 迁移你的笔记本不会移动远程 gateway 的状态。

28. 如果你处于远程模式，请迁移**gateway 主机**。

### 29. 踩坑点：备份中的秘密信息

30. `$OPENCLAW_STATE_DIR` 包含敏感信息（API 密钥、OAuth 令牌、WhatsApp 凭据）。 31. 将备份视同生产环境的秘密：

- 32. 加密存储
- 33. 避免通过不安全的渠道共享
- 34. 如果怀疑泄露，轮换密钥

## 35. 验证清单

36. 在新机器上，确认：

- 37. `openclaw status` 显示 gateway 正在运行
- 38. 你的频道仍保持连接（例如 WhatsApp 不需要重新配对）
- 仪表板打开并显示现有会话
- 40. 你的 workspace 文件（内存、配置）仍然存在

## 41. 相关内容

- 42. [Doctor](/gateway/doctor)
- 43. [Gateway 故障排查](/gateway/troubleshooting)
- 44. [OpenClaw 将数据存储在哪里？](/help/faq#where-does-openclaw-store-its-data)
