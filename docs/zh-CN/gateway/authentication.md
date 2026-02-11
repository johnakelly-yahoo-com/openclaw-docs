---
summary: "14. 模型认证：OAuth、API 密钥以及 setup-token"
read_when:
  - 15. 调试模型认证或 OAuth 过期问题
  - 16. 记录认证或凭证存储方式
title: "17. 认证"
---

# 18. 认证

19. OpenClaw 支持模型提供商的 OAuth 和 API 密钥。 20. 对于 Anthropic 账户，我们建议使用 **API 密钥**。 21. 对于 Claude 订阅访问，使用通过 `claude setup-token` 创建的长期有效令牌。

22. 有关完整的 OAuth 流程和存储布局，请参见 [/concepts/oauth](/concepts/oauth)。

## 23. 推荐的 Anthropic 设置（API 密钥）

24. 如果你直接使用 Anthropic，请使用 API 密钥。

1. 25. 在 Anthropic 控制台中创建一个 API 密钥。
2. 26. 将其放在 **网关主机**（运行 `openclaw gateway` 的机器）上。

```bash
27. export ANTHROPIC_API_KEY="..."
openclaw models status
```

3. 28. 如果 Gateway 运行在 systemd/launchd 下，建议把密钥放在 `~/.openclaw/.env` 中，以便守护进程可以读取：

```bash
29. cat >> ~/.openclaw/.env <<'EOF'
ANTHROPIC_API_KEY=...
EOF
```

30. 然后重启守护进程（或重启你的 Gateway 进程），并重新检查：

```bash
openclaw models status
openclaw doctor
```

32. 如果你不想自己管理环境变量，引导向导可以为守护进程使用而存储 API 密钥：`openclaw onboard`。

33. 有关环境继承（`env.shellEnv`、`~/.openclaw/.env`、systemd/launchd）的详细信息，请参见 [Help](/help)。

## 34. Anthropic：setup-token（订阅认证）

35. 对于 Anthropic，推荐的路径是 **API 密钥**。 36. 如果你使用的是 Claude 订阅，也支持 setup-token 流程。 37. 在 **网关主机** 上运行：

```bash
38. claude setup-token
```

Then paste it into OpenClaw:

```bash
openclaw models auth setup-token --provider anthropic
```

41. 如果令牌是在另一台机器上创建的，请手动粘贴：

```bash
openclaw models auth paste-token --provider anthropic
```

43. 如果你看到类似下面的 Anthropic 错误：

```
44. This credential is only authorized for use with Claude Code and cannot be used for other API requests.
```

45. ……请改用 Anthropic API 密钥。

46. 手动输入令牌（任何提供商；会写入 `auth-profiles.json` 并更新配置）：

```bash
47. openclaw models auth paste-token --provider anthropic
openclaw models auth paste-token --provider openrouter
```

48. 适合自动化的检查（过期或缺失时退出码为 `1`，即将过期时为 `2`）：

```bash
49. openclaw models status --check
```

50. 可选的运维脚本（systemd/Termux）在此处有文档说明：
    [/automation/auth-monitoring](/automation/auth-monitoring)

> `claude setup-token` requires an interactive TTY.

## Checking model auth status

```bash
openclaw models status
openclaw doctor
```

## Controlling which credential is used

### Per-session (chat command)

Use `/model <alias-or-id>@<profileId>` to pin a specific provider credential for the current session (example profile ids: `anthropic:default`, `anthropic:work`).

Use `/model` (or `/model list`) for a compact picker; use `/model status` for the full view (candidates + next auth profile, plus provider endpoint details when configured).

### Per-agent (CLI override)

Set an explicit auth profile order override for an agent (stored in that agent’s `auth-profiles.json`):

```bash
openclaw models auth order get --provider anthropic
openclaw models auth order set --provider anthropic anthropic:default
openclaw models auth order clear --provider anthropic
```

Use `--agent <id>` to target a specific agent; omit it to use the configured default agent.

## Troubleshooting

### “No credentials found”

If the Anthropic token profile is missing, run `claude setup-token` on the
**gateway host**, then re-check:

```bash
openclaw models status
```

### Token expiring/expired

Run `openclaw models status` to confirm which profile is expiring. If the profile
is missing, rerun `claude setup-token` and paste the token again.

## Requirements

- Claude Max or Pro subscription (for `claude setup-token`)
- Claude Code CLI installed (`claude` command available)
