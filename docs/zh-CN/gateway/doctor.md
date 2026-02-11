---
summary: "49. Doctor 命令：健康检查、配置迁移和修复步骤"
read_when:
  - 50. 添加或修改 doctor 迁移
  - 1. 引入破坏性的配置更改
title: "2. Doctor"
---

# 3. Doctor

4. `openclaw doctor` 是 OpenClaw 的修复 + 迁移工具。 5. 它可修复过期的
   配置/状态、进行健康检查，并提供可执行的修复步骤。

## 6. 快速开始

```bash
7. openclaw doctor
```

### 8. 无头 / 自动化

```bash
9. openclaw doctor --yes
```

10. 在不提示的情况下接受默认值（在适用时包括重启/服务/沙箱修复步骤）。

```bash
11. openclaw doctor --repair
```

12. 在不提示的情况下应用推荐的修复（在安全时包含修复 + 重启）。

```bash
13. openclaw doctor --repair --force
```

14. 也会应用激进的修复（覆盖自定义的 supervisor 配置）。

```bash
15. openclaw doctor --non-interactive
```

16. 在无提示的情况下运行，仅应用安全的迁移（配置规范化 + 磁盘上的状态迁移）。 17. 跳过需要人工确认的重启/服务/沙箱操作。
17. 检测到旧版状态迁移时会自动运行。

```bash
19. openclaw doctor --deep
```

20. 扫描系统服务以查找额外的网关安装（launchd/systemd/schtasks）。

21. 如果你希望在写入之前查看更改，请先打开配置文件：

```bash
22. cat ~/.openclaw/openclaw.json
```

## 23. 它的作用（摘要）

- 24. 可选的预检更新（仅限交互式，适用于 git 安装）。
- 25. UI 协议新鲜度检查（当协议 schema 较新时会重建 Control UI）。
- 26. 健康检查 + 重启提示。
- 27. 技能状态汇总（可用/缺失/被阻止）。
- 28. 对旧版值进行配置规范化。
- 29. OpenCode Zen 提供方覆盖警告（`models.providers.opencode`）。
- 30. 旧版磁盘状态迁移（会话/agent 目录/WhatsApp 认证）。
- 31. 状态完整性与权限检查（会话、转录、状态目录）。
- 32. 在本地运行时检查配置文件权限（chmod 600）。
- 33. 模型认证健康状况：检查 OAuth 过期情况、可刷新即将过期的令牌，并报告认证配置的冷却/禁用状态。
- 34. 额外工作区目录检测（`~/openclaw`）。
- 35. 启用沙箱时进行沙箱镜像修复。
- 36. 旧版服务迁移与额外网关检测。
- 37. 网关运行时检查（服务已安装但未运行；缓存的 launchd 标签）。
- 38. 通道状态警告（从正在运行的网关探测）。
- 39. Supervisor 配置审计（launchd/systemd/schtasks），并提供可选修复。
- 40. 网关运行时最佳实践检查（Node vs Bun，版本管理器路径）。
- 41. 网关端口冲突诊断（默认 `18789`）。
- 42. 针对开放 DM 策略的安全警告。
- 43. 当未设置 `gateway.auth.token` 时的网关认证警告（本地模式；提供令牌生成）。
- 44. Linux 上的 systemd linger 检查。
- 45. 源码安装检查（pnpm 工作区不匹配、缺失 UI 资源、缺失 tsx 二进制）。
- 46. 写入更新后的配置 + 向导元数据。

## 47. 详细行为与原理说明。

### 48. 0. 可选更新（git 安装）

49. 如果这是一个 git 检出且 doctor 以交互方式运行，它会在运行 doctor 之前提供更新（fetch/rebase/build）。

### 50. 1. 配置规范化

1. 如果配置包含旧版的值结构（例如 `messages.ackReaction`
   在没有特定频道覆盖的情况下），doctor 会将其规范化为当前的
   schema。

### 2. 2. 旧版配置键迁移

3. 当配置中包含已弃用的键时，其他命令将拒绝运行，并要求
   你运行 `openclaw doctor`。

4. Doctor 将会：

- 5. 说明发现了哪些旧版键。
- 6. 展示它应用的迁移内容。
- 7. 使用更新后的 schema 重写 `~/.openclaw/openclaw.json`。

8. Gateway 在启动时也会在检测到
   旧版配置格式时自动运行 doctor 迁移，因此无需手动干预即可修复过期配置。

9. 当前迁移项：

- 10. `routing.allowFrom` → `channels.whatsapp.allowFrom`
- 11. `routing.groupChat.requireMention` → `channels.whatsapp/telegram/imessage.groups."*".requireMention`
- 12. `routing.groupChat.historyLimit` → `messages.groupChat.historyLimit`
- 13. `routing.groupChat.mentionPatterns` → `messages.groupChat.mentionPatterns`
- 14. `routing.queue` → `messages.queue`
- 15. `routing.bindings` → 顶层 `bindings`
- 16. `routing.agents`/`routing.defaultAgentId` → `agents.list` + `agents.list[].default`
- 17. `routing.agentToAgent` → `tools.agentToAgent`
- 18. `routing.transcribeAudio` → `tools.media.audio.models`
- 19. `bindings[].match.accountID` → `bindings[].match.accountId`
- 20. `identity` → `agents.list[].identity`
- 21. `agent.*` → `agents.defaults` + `tools.*`（tools/elevated/exec/sandbox/subagents）
- 22. `agent.model`/`allowedModels`/`modelAliases`/`modelFallbacks`/`imageModelFallbacks`
      → `agents.defaults.models` + `agents.defaults.model.primary/fallbacks` + `agents.defaults.imageModel.primary/fallbacks`

### 23. 2b) OpenCode Zen 提供方覆盖

24. 如果你手动添加了 `models.providers.opencode`（或 `opencode-zen`），它将
    覆盖来自 `@mariozechner/pi-ai` 的内置 OpenCode Zen 目录。 25. 这可能会
    强制所有模型使用单一 API，或将成本清零。 26. Doctor 会发出警告，以便你
    移除该覆盖并恢复按模型划分的 API 路由和成本。

### 27. 3. 旧版状态迁移（磁盘布局）

28. Doctor 可以将较旧的磁盘布局迁移到当前结构：

- 29. 会话存储 + 转录：
  - 30. 从 `~/.openclaw/sessions/` 到 `~/.openclaw/agents/<agentId>/sessions/`
- 31. Agent 目录：
  - 32. 从 `~/.openclaw/agent/` 到 `~/.openclaw/agents/<agentId>/agent/`
- 33. WhatsApp 认证状态（Baileys）：
  - 34. 从旧版 `~/.openclaw/credentials/*.json`（不包括 `oauth.json`）
  - 35. 到 `~/.openclaw/credentials/whatsapp/<accountId>/...`（默认 account id：`default`）

36. 这些迁移是尽力而为且幂等的；当它将任何旧版文件夹作为备份保留下来时，doctor 会发出警告。 37. Gateway/CLI 也会在启动时自动迁移
    旧版会话和 agent 目录，使历史记录/认证/模型落在
    按 agent 划分的路径中，而无需手动运行 doctor。 38. WhatsApp 认证有意只通过
    `openclaw doctor` 进行迁移。

### 39. 4. 状态完整性检查（会话持久化、路由和安全）

40. 状态目录是运行时的中枢神经。 41. 如果它消失，你将丢失
    会话、凭据、日志和配置（除非你在其他地方有备份）。

42. Doctor 检查项：

- 43. **状态目录缺失**：警告灾难性的状态丢失，提示重新创建
      该目录，并提醒无法恢复缺失的数据。
- 44. **状态目录权限**：验证是否可写；提供修复权限的选项
      （在检测到所有者/组不匹配时会给出 `chown` 提示）。
- 45. **会话目录缺失**：`sessions/` 和会话存储目录是
      持久化历史并避免 `ENOENT` 崩溃所必需的。
- 46. **转录不匹配**：当最近的会话条目缺少
      转录文件时发出警告。
- 47. **主会话“单行 JSONL”**：当主转录只有一行时
      发出标记（历史未在累积）。
- 48. **多个状态目录**：当在不同的主目录中存在多个 `~/.openclaw`
      文件夹，或 `OPENCLAW_STATE_DIR` 指向其他位置时发出警告（历史可能在不同安装之间分裂）。
- 49. **远程模式提醒**：如果 `gateway.mode=remote`，doctor 会提醒你
      在远程主机上运行（状态存储在那里）。
- 50. **配置文件权限**：如果 `~/.openclaw/openclaw.json` 对
      组/所有人可读，则发出警告并提供将权限收紧到 `600` 的选项。

### 1. 5. 模型鉴权健康（OAuth 过期）

2. Doctor 会检查鉴权存储中的 OAuth 配置文件，在令牌即将过期或已过期时发出警告，并在安全时可刷新它们。 3. 如果 Anthropic Claude Code 配置文件已过期，它会建议运行 `claude setup-token`（或粘贴一个 setup-token）。
3. 刷新提示仅在交互式运行（TTY）时出现；`--non-interactive` 会跳过刷新尝试。

5. Doctor 还会报告由于以下原因而暂时不可用的鉴权配置文件：

- 6. 短暂冷却（速率限制/超时/鉴权失败）
- 7. 较长时间的禁用（计费/额度失败）

### 8. 6. Hooks 模型校验

9. 如果设置了 `hooks.gmail.model`，Doctor 会根据目录和允许列表校验模型引用，并在无法解析或被禁止时发出警告。

### 10. 7. 沙箱镜像修复

11. 启用沙箱时，Doctor 会检查 Docker 镜像，并在当前镜像缺失时提供构建或切换到旧版名称的选项。

### 12. 8. 网关服务迁移与清理提示

13. Doctor 会检测遗留的网关服务（launchd/systemd/schtasks），并提供移除它们、使用当前网关端口安装 OpenClaw 服务的选项。 14. 它还可以扫描额外的类网关服务并输出清理提示。
14. 以配置文件命名的 OpenClaw 网关服务被视为一等公民，不会被标记为“额外”。

### 16. 9. 安全警告

17. 当提供方在没有允许列表的情况下对私信开放，或策略以危险方式配置时，Doctor 会发出警告。

### 18. 10. systemd linger（Linux）

19. 如果作为 systemd 用户服务运行，Doctor 会确保启用 lingering，以便在注销后网关仍保持运行。

### 20. 11. 技能状态

21. Doctor 会打印当前工作区中可用/缺失/被阻止技能的快速摘要。

### 22. 12. 网关鉴权检查（本地令牌）

23. 当本地网关缺少 `gateway.auth` 时，Doctor 会发出警告并提供生成令牌的选项。 24. 使用 `openclaw doctor --generate-gateway-token` 可在自动化中强制创建令牌。

### 25. 13. 网关健康检查 + 重启

26. Doctor 会运行健康检查，并在看起来不健康时提供重启网关的选项。

### 27. 14. 通道状态警告

28. 如果网关健康，Doctor 会运行通道状态探测，并报告带有修复建议的警告。

### 29. 15. Supervisor 配置审计 + 修复

30. Doctor 会检查已安装的 supervisor 配置（launchd/systemd/schtasks），查找缺失或过期的默认项（例如 systemd 的 network-online 依赖和重启延迟）。 31. 发现不匹配时，它会推荐更新，并可将服务文件/任务重写为当前默认值。

32. 备注：

- 33. `openclaw doctor` 在重写 supervisor 配置前会进行提示。
- 34. `openclaw doctor --yes` 接受默认的修复提示。
- 35. `openclaw doctor --repair` 在无提示的情况下应用推荐修复。
- 36. `openclaw doctor --repair --force` 会覆盖自定义的 supervisor 配置。
- 37. 你也可以通过 `openclaw gateway install --force` 强制进行完整重写。

### 38. 16. 网关运行时 + 端口诊断

39. Doctor 会检查服务运行时（PID、上次退出状态），并在服务已安装但实际上未运行时发出警告。 40. 它还会检查网关端口（默认 `18789`）的端口冲突，并报告可能原因（网关已在运行、SSH 隧道）。

### 41. 17. 网关运行时最佳实践

42. 当网关服务运行在 Bun 或版本管理的 Node 路径（`nvm`、`fnm`、`volta`、`asdf` 等）上时，Doctor 会发出警告。 43. WhatsApp + Telegram 通道需要 Node，而版本管理器路径可能在升级后失效，因为服务不会加载你的 shell 初始化。 44. 在可用时（Homebrew/apt/choco），Doctor 会提供迁移到系统 Node 安装的选项。

### 45. 18. 配置写入 + 向导元数据

46. Doctor 会持久化任何配置更改，并标记向导元数据以记录本次 doctor 运行。

### 47. 19. 工作区提示（备份 + 记忆系统）

48. 当缺少时，Doctor 会建议使用工作区记忆系统；如果工作区尚未纳入 git，它会打印备份提示。

49. 有关工作区结构和 git 备份（推荐私有 GitHub 或 GitLab）的完整指南，请参见 [/concepts/agent-workspace](/concepts/agent-workspace)。
