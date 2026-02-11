---
summary: "`openclaw channels` 的 CLI 参考（账户、状态、登录/登出、日志）"
read_when:
  - 你想要添加/移除频道账户（WhatsApp/Telegram/Discord/Google Chat/Slack/Mattermost（插件）/Signal/iMessage）
  - 你想要检查频道状态或实时查看频道日志
title: "channels"
---

# `openclaw channels`

在 Gateway 上管理聊天频道账户及其运行时状态。

相关文档：

- Channel guides: [Channels](/channels/index)
- Gateway configuration: [Configuration](/gateway/configuration)

## 常用命令

```bash
openclaw channels list
openclaw channels status
openclaw channels capabilities
openclaw channels capabilities --channel discord --target channel:123
openclaw channels resolve --channel slack "#general" "@jane"
openclaw channels logs --channel all
```

## 添加 / 移除账户

```bash
openclaw channels add --channel telegram --token <bot-token>
openclaw channels remove --channel telegram --delete
```

提示：`openclaw channels add --help` 会显示各频道的参数（token、app token、signal-cli 路径等）。

## 登录 / 登出（交互式）

```bash
openclaw channels login --channel whatsapp
openclaw channels logout --channel whatsapp
```

## 故障排除

- 运行 `openclaw status --deep` 进行全面探测。
- 使用 `openclaw doctor` 进行引导式修复。
- `openclaw channels list` 打印 `Claude: HTTP 403 ... user:profile` → 使用情况快照需要 `user:profile` 作用域。 使用 `--no-usage`，或提供一个 claude.ai 会话密钥（`CLAUDE_WEB_SESSION_KEY` / `CLAUDE_WEB_COOKIE`），或通过 Claude Code CLI 重新认证。

## 能力探测

Fetch provider capability hints (intents/scopes where available) plus static feature support:

```bash
openclaw channels capabilities
openclaw channels capabilities --channel discord --target channel:123
```

说明：

- `--channel` 为可选；省略则列出所有频道（包括扩展）。
- `--target` 接受 `channel:<id>` 或原始数字频道 ID，仅适用于 Discord。
- 探测是提供方特定的：Discord 意图 + 可选频道权限；Slack 机器人 + 用户作用域；Telegram 机器人标志 + webhook；Signal 守护进程版本；MS Teams 应用令牌 + Graph 角色/作用域（在已知处标注）。 没有探测的频道会报告 `Probe: unavailable`。

## Resolve names to IDs

使用提供方目录将频道/用户名称解析为 ID：

```bash
openclaw channels resolve --channel slack "#general" "@jane"
openclaw channels resolve --channel discord "My Server/#support" "@someone"
openclaw channels resolve --channel matrix "Project Room"
```

说明：

- 使用 `--kind user|group|auto` 来强制目标类型。
- 当多个条目具有相同名称时，解析将优先选择活跃匹配项。
