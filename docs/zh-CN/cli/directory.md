---
summary: "用于 `openclaw directory` 的 CLI 参考（self、peers、groups）"
read_when:
  - 你想要查找某个频道的联系人/群组/自身 ID
  - 你正在开发一个频道目录适配器
title: "目录"
---

# `openclaw directory`

对支持的频道进行目录查询（联系人/对等方、群组以及“我”）。

## 常用参数

- `--channel <name>`: channel id/alias (required when multiple channels are configured; auto when only one is configured)
- `--account <id>`：账号 ID（默认：频道默认账号）
- `--json`：输出 JSON

## 说明

- `directory` is meant to help you find IDs you can paste into other commands (especially `openclaw message send --target ...`).
- 对于许多频道，结果基于配置（白名单/已配置的群组），而非实时的提供方目录。
- 默认输出为以制表符分隔的 `id`（有时包含 `name`）；脚本使用请加 `--json`。

## 将结果用于 `message send`

```bash
openclaw directory peers list --channel slack --query "U0"
openclaw message send --channel slack --target user:U012ABCDEF --message "hello"
```

## ID 格式（按频道）

- WhatsApp：`+15551234567`（私聊），`1234567890-1234567890@g.us`（群组）
- Telegram：`@username` 或数字聊天 ID；群组为数字 ID
- Slack：`user:U…` 和 `channel:C…`
- Discord：`user:<id>` 和 `channel:<id>`
- Matrix（插件）：`user:@user:server`、`room:!roomId:server` 或 `#alias:server`
- Microsoft Teams (plugin): `user:<id>` and `conversation:<id>`
- Zalo（插件）：用户 ID（Bot API）
- Zalo Personal / `zalouser`（插件）：来自 `zca` 的线程 ID（私聊/群组）（`me`、`friend list`、`group list`）

## 自身（“我”）

```bash
openclaw directory self --channel zalouser
```

## 对等方（联系人/用户）

```bash
openclaw directory peers list --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory peers list --channel zalouser --limit 50
```

## 群组

```bash
openclaw directory groups list --channel zalouser
openclaw directory groups list --channel zalouser --query "work"
openclaw directory groups members --channel zalouser --group-id <id>
```
