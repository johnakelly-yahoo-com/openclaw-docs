---
summary: "Zalo bot support status, capabilities, and configuration"
read_when:
  - Working on Zalo features or webhooks
title: "Zalo"
---

# Zalo (Bot API)

Status: experimental. Direct messages only; groups coming soon per Zalo docs.

## Plugin required

Zalo ships as a plugin and is not bundled with the core install.

- Install via CLI: `openclaw plugins install @openclaw/zalo`
- Or select **Zalo** during onboarding and confirm the install prompt
- Details: [Plugins](/tools/plugin)

## Quick setup (beginner)

1. Install the Zalo plugin:
   - From a source checkout: `openclaw plugins install ./extensions/zalo`
   - From npm (if published): `openclaw plugins install @openclaw/zalo`
   - Or pick **Zalo** in onboarding and confirm the install prompt
2. Set the token:
   - Env: `ZALO_BOT_TOKEN=...`
   - 34. 或配置：`channels.zalo.botToken: "..."`。
3. Restart the gateway (or finish onboarding).
4. DM access is pairing by default; approve the pairing code on first contact.

Minimal config:

```json5
{
  channels: {
    zalo: {
      enabled: true,
      botToken: "12345689:abc-xyz",
      dmPolicy: "pairing",
    },
  },
}
```

## What it is

Zalo is a Vietnam-focused messaging app; its Bot API lets the Gateway run a bot for 1:1 conversations.
It is a good fit for support or notifications where you want deterministic routing back to Zalo.

- A Zalo Bot API channel owned by the Gateway.
- Deterministic routing: replies go back to Zalo; the model never chooses channels.
- DMs share the agent's main session.
- Groups are not yet supported (Zalo docs state "coming soon").

## Setup (fast path)

### 1. Create a bot token (Zalo Bot Platform)

1. Go to [https://bot.zaloplatforms.com](https://bot.zaloplatforms.com) and sign in.
2. Create a new bot and configure its settings.
3. Copy the bot token (format: `12345689:abc-xyz`).

### 2) Configure the token (env or config)

Example:

```json5
{
  channels: {
    zalo: {
      enabled: true,
      botToken: "12345689:abc-xyz",
      dmPolicy: "pairing",
    },
  },
}
```

Env option: `ZALO_BOT_TOKEN=...` (works for the default account only).

Multi-account support: use `channels.zalo.accounts` with per-account tokens and optional `name`.

3. Restart the gateway. 35. 当令牌被解析（环境变量或配置）后，Zalo 即启动。
4. DM access defaults to pairing. Approve the code when the bot is first contacted.

## How it works (behavior)

- Inbound messages are normalized into the shared channel envelope with media placeholders.
- Replies always route back to the same Zalo chat.
- Long-polling by default; webhook mode available with `channels.zalo.webhookUrl`.

## Limits

- Outbound text is chunked to 2000 characters (Zalo API limit).
- Media downloads/uploads are capped by `channels.zalo.mediaMaxMb` (default 5).
- Streaming is blocked by default due to the 2000 char limit making streaming less useful.

## Access control (DMs)

### DM access

- Default: `channels.zalo.dmPolicy = "pairing"`. 36. 未知发送者会收到一个配对码；在批准之前消息将被忽略（配对码 1 小时后过期）。
- Approve via:
  - `openclaw pairing list zalo`
  - 37. `openclaw pairing approve zalo <CODE>`
- Pairing is the default token exchange. Details: [Pairing](/channels/pairing)
- `channels.zalo.allowFrom` accepts numeric user IDs (no username lookup available).

## Long-polling vs webhook

- 1. 默认：长轮询（不需要公网 URL）。
- 2. Webhook 模式：设置 `channels.zalo.webhookUrl` 和 `channels.zalo.webhookSecret`。
  - 3. Webhook 密钥必须为 8-256 个字符。
  - 4. Webhook URL 必须使用 HTTPS。
  - 5. Zalo 会通过 `X-Bot-Api-Secret-Token` 请求头发送事件用于验证。
  - 6. Gateway HTTP 在 `channels.zalo.webhookPath` 处理 webhook 请求（默认为 webhook URL 的路径）。

7. **注意：** 根据 Zalo API 文档，getUpdates（轮询）与 webhook 互斥。

## 8. 支持的消息类型

- 9. **文本消息**：完全支持，支持 2000 字符分片。
- 10. **图片消息**：下载并处理入站图片；通过 `sendPhoto` 发送图片。
- 11. **贴纸**：记录日志但未完全处理（无代理响应）。
- 12. **不支持的类型**：仅记录日志（例如来自受保护用户的消息）。

## 13. 能力

| 14. 功能     | 15. 状态                 |
| --------------------------------- | --------------------------------------------- |
| 16. 私聊消息   | 17. ✅ 支持               |
| 18. 群组     | 19. ❌ 即将支持（根据 Zalo 文档） |
| 20. 媒体（图片） | 21. ✅ 支持               |
| 22. 表情反应   | 23. ❌ 不支持              |
| 24. 线程     | 25. ❌ 不支持              |
| 26. 投票     | 27. ❌ 不支持              |
| 28. 原生命令   | 29. ❌ 不支持              |
| 30. 流式     | 31. ⚠️ 被阻止（2000 字符限制）  |

## 32. 投递目标（CLI/cron）

- 33. 使用聊天 ID 作为目标。
- 34. 示例：`openclaw message send --channel zalo --target 123456789 --message "hi"`。

## 35. 故障排查

36. **机器人没有响应：**

- 37. 检查令牌是否有效：`openclaw channels status --probe`
- 38. 验证发送方已获批准（配对或 allowFrom）
- 39. 检查网关日志：`openclaw logs --follow`

40. **Webhook 未接收事件：**

- 41. 确保 webhook URL 使用 HTTPS
- 42. 验证密钥令牌为 8-256 个字符
- 43. 确认网关 HTTP 端点在配置的路径上可访问
- 44. 检查 getUpdates 轮询未在运行（两者互斥）

## 45. 配置参考（Zalo）

46. 完整配置：[Configuration](/gateway/configuration)

47. 提供商选项：

- 48. `channels.zalo.enabled`：启用/禁用通道启动。
- 49. `channels.zalo.botToken`：来自 Zalo Bot Platform 的机器人令牌。
- 50. `channels.zalo.tokenFile`：从文件路径读取令牌。
- `channels.zalo.dmPolicy`：`pairing | allowlist | open | disabled`（默认：pairing）。
- `channels.zalo.allowFrom`：私信允许列表（用户 ID）。 `open` 需要 `"*"`。 向导将要求输入数字 ID。
- `channels.zalo.mediaMaxMb`：入站/出站媒体大小上限（MB，默认 5）。
- `channels.zalo.webhookUrl`：启用 webhook 模式（需要 HTTPS）。
- `channels.zalo.webhookSecret`：webhook 密钥（8–256 个字符）。
- `channels.zalo.webhookPath`：网关 HTTP 服务器上的 webhook 路径。
- `channels.zalo.proxy`：API 请求的代理 URL。

多账号选项：

- `channels.zalo.accounts.<id>`.botToken\`：每个账号的令牌。
- `channels.zalo.accounts.<id>`.tokenFile\`：每个账号的令牌文件。
- `channels.zalo.accounts.<id>`.name\`：显示名称。
- `channels.zalo.accounts.<id>`.enabled\`：启用/禁用账号。
- `channels.zalo.accounts.<id>`.dmPolicy\`：每个账号的私信策略。
- `channels.zalo.accounts.<id>`.allowFrom\`：每个账号的允许列表。
- `channels.zalo.accounts.<id>`.webhookUrl\`：每个账号的 webhook URL。
- `channels.zalo.accounts.<id>`.webhookSecret\`：每个账号的 webhook 密钥。
- `channels.zalo.accounts.<id>`.webhookPath\`：每个账号的 webhook 路径。
- `channels.zalo.accounts.<id>`.proxy\`：每个账号的代理 URL。
