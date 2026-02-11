---
summary: "Twitch 聊天机器人配置与设置"
read_when:
  - 为 OpenClaw 设置 Twitch 聊天集成
title: "Twitch"
---

# Twitch（插件）

通过 IRC 连接提供 Twitch 聊天支持。 OpenClaw connects as a Twitch user (bot account) to receive and send messages in channels.

## Plugin required

16. Twitch 以插件形式提供，未随核心安装包一起提供。

17. 通过 CLI 安装（npm 注册表）：

```bash
openclaw plugins install @openclaw/twitch
```

Local checkout (when running from a git repo):

```bash
openclaw plugins install ./extensions/twitch
```

Details: [Plugins](/tools/plugin)

## Quick setup (beginner)

1. Create a dedicated Twitch account for the bot (or use an existing account).
2. Generate credentials: [Twitch Token Generator](https://twitchtokengenerator.com/)
   - Select **Bot Token**
   - Verify scopes `chat:read` and `chat:write` are selected
   - Copy the **Client ID** and **Access Token**
3. Find your Twitch user ID: [https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/](https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/)
4. Configure the token:
   - 18. 环境变量：`OPENCLAW_TWITCH_ACCESS_TOKEN=...`（仅默认账号）
   - Or config: `channels.twitch.accessToken`
   - If both are set, config takes precedence (env fallback is default-account only).
5. Start the gateway.

**⚠️ Important:** Add access control (`allowFrom` or `allowedRoles`) to prevent unauthorized users from triggering the bot. `requireMention` defaults to `true`.

Minimal config:

```json5
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw", // Bot's Twitch account
      accessToken: "oauth:abc123...", // OAuth Access Token (or use OPENCLAW_TWITCH_ACCESS_TOKEN env var)
      clientId: "xyz789...", // Client ID from Token Generator
      channel: "vevisk", // Which Twitch channel's chat to join (required)
      allowFrom: ["123456789"], // (recommended) Your Twitch user ID only - get it from https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/
    },
  },
}
```

## What it is

- A Twitch channel owned by the Gateway.
- Deterministic routing: replies always go back to Twitch.
- Each account maps to an isolated session key `agent:<agentId>:twitch:<accountName>`.
- `username` is the bot's account (who authenticates), `channel` is which chat room to join.

## Setup (detailed)

### Generate credentials

Use [Twitch Token Generator](https://twitchtokengenerator.com/):

- Select **Bot Token**
- Verify scopes `chat:read` and `chat:write` are selected
- Copy the **Client ID** and **Access Token**

No manual app registration needed. Tokens expire after several hours.

### Configure the bot

**Env var (default account only):**

```bash
OPENCLAW_TWITCH_ACCESS_TOKEN=oauth:abc123...
```

**Or config:**

```json5
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw",
      accessToken: "oauth:abc123...",
      clientId: "xyz789...",
      channel: "vevisk",
    },
  },
}
```

If both env and config are set, config takes precedence.

### Access control (recommended)

```json5
{
  channels: {
    twitch: {
      allowFrom: ["123456789"], // (recommended) Your Twitch user ID only
    },
  },
}
```

Prefer `allowFrom` for a hard allowlist. Use `allowedRoles` instead if you want role-based access.

**Available roles:** `"moderator"`, `"owner"`, `"vip"`, `"subscriber"`, `"all"`.

**Why user IDs?** Usernames can change, allowing impersonation. User IDs are permanent.

Find your Twitch user ID: [https://www.streamweasels.com/tools/convert-twitch-username-%20to-user-id/](https://www.streamweasels.com/tools/convert-twitch-username-%20to-user-id/) (Convert your Twitch username to ID)

## Token refresh (optional)

Tokens from [Twitch Token Generator](https://twitchtokengenerator.com/) cannot be automatically refreshed - regenerate when expired.

For automatic token refresh, create your own Twitch application at [Twitch Developer Console](https://dev.twitch.tv/console) and add to config:

```json5
{
  channels: {
    twitch: {
      clientSecret: "your_client_secret",
      refreshToken: "your_refresh_token",
    },
  },
}
```

The bot automatically refreshes tokens before expiration and logs refresh events.

## 19. 多账号支持

Use `channels.twitch.accounts` with per-account tokens. See [`gateway/configuration`](/gateway/configuration) for the shared pattern.

Example (one bot account in two channels):

```json5
{
  channels: {
    twitch: {
      accounts: {
        channel1: {
          username: "openclaw",
          accessToken: "oauth:abc123...",
          clientId: "xyz789...",
          channel: "vevisk",
        },
        channel2: {
          username: "openclaw",
          accessToken: "oauth:def456...",
          clientId: "uvw012...",
          channel: "secondchannel",
        },
      },
    },
  },
}
```

**Note:** Each account needs its own token (one token per channel).

## Access control

### Role-based restrictions

```json5
{
  channels: {
    twitch: {
      accounts: {
        default: {
          allowedRoles: ["moderator", "vip"],
        },
      },
    },
  },
}
```

### Allowlist by User ID (most secure)

```json5
{
  channels: {
    twitch: {
      accounts: {
        default: {
          allowFrom: ["123456789", "987654321"],
        },
      },
    },
  },
}
```

### Role-based access (alternative)

21. `allowFrom` 是一个严格的允许列表。 When set, only those user IDs are allowed.
    If you want role-based access, leave `allowFrom` unset and configure `allowedRoles` instead:

```json5
{
  channels: {
    twitch: {
      accounts: {
        default: {
          allowedRoles: ["moderator"],
        },
      },
    },
  },
}
```

### Disable @mention requirement

By default, `requireMention` is `true`. To disable and respond to all messages:

```json5
{
  channels: {
    twitch: {
      accounts: {
        default: {
          requireMention: false,
        },
      },
    },
  },
}
```

## Troubleshooting

First, run diagnostic commands:

```bash
openclaw doctor
openclaw channels status --probe
```

### Bot doesn't respond to messages

**Check access control:** Ensure your user ID is in `allowFrom`, or temporarily remove
`allowFrom` and set `allowedRoles: ["all"]` to test.

**Check the bot is in the channel:** The bot must join the channel specified in `channel`.

### Token issues

**"Failed to connect" or authentication errors:**

- Verify `accessToken` is the OAuth access token value (typically starts with `oauth:` prefix)
- Check token has `chat:read` and `chat:write` scopes
- If using token refresh, verify `clientSecret` and `refreshToken` are set

### Token refresh not working

**Check logs for refresh events:**

```
Using env token source for mybot
Access token refreshed for user 123456 (expires in 14400s)
```

22. 如果你看到“token refresh disabled (no refresh token)”：

- Ensure `clientSecret` is provided
- Ensure `refreshToken` is provided

## Config

**Account config:**

- `username` - Bot username
- `accessToken` - OAuth access token with `chat:read` and `chat:write`
- `clientId` - Twitch Client ID (from Token Generator or your app)
- `channel` - Channel to join (required)
- `enabled` - Enable this account (default: `true`)
- `clientSecret` - 可选：用于自动刷新令牌
- `refreshToken` - 可选：用于自动刷新令牌
- `expiresIn` - 令牌过期时间（秒）
- `obtainmentTimestamp` - 令牌获取时间戳
- `allowFrom` - User ID allowlist
- `allowedRoles` - Role-based access control (`"moderator" | "owner" | "vip" | "subscriber" | "all"`)
- `requireMention` - 需要 @ 提及（默认：`true`）

**提供方选项：**

- `channels.twitch.enabled` - 启用/禁用频道启动
- `channels.twitch.username` - 机器人用户名（简化的单账号配置）
- `channels.twitch.accessToken` - OAuth 访问令牌（简化的单账号配置）
- `channels.twitch.clientId` - Twitch Client ID（简化的单账号配置）
- `channels.twitch.channel` - 要加入的频道（简化的单账号配置）
- `channels.twitch.accounts.<accountName>` - 多账号配置（包含上述所有账号字段）

完整示例：

```json5
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw",
      accessToken: "oauth:abc123...",
      clientId: "xyz789...",
      channel: "vevisk",
      clientSecret: "secret123...",
      refreshToken: "refresh456...",
      allowFrom: ["123456789"],
      allowedRoles: ["moderator", "vip"],
      accounts: {
        default: {
          username: "mybot",
          accessToken: "oauth:abc123...",
          clientId: "xyz789...",
          channel: "your_channel",
          enabled: true,
          clientSecret: "secret123...",
          refreshToken: "refresh456...",
          expiresIn: 14400,
          obtainmentTimestamp: 1706092800000,
          allowFrom: ["123456789", "987654321"],
          allowedRoles: ["moderator"],
        },
      },
    },
  },
}
```

## 工具操作

代理可以使用以下动作调用 `twitch`：

- `send` - 向频道发送消息

示例：

```json5
{
  action: "twitch",
  params: {
    message: "Hello Twitch!",
    to: "#mychannel",
  },
}
```

## 安全与运维

- **将令牌视为密码** - 切勿将令牌提交到 git
- **使用自动令牌刷新** 以支持长期运行的机器人
- **使用用户 ID 白名单** 而不是用户名进行访问控制
- **监控日志** 以关注令牌刷新事件和连接状态
- **最小化令牌作用域** - 只请求 `chat:read` 和 `chat:write`
- **如果卡住**：确认没有其他进程占用会话后重启网关

## 限制

- **每条消息 500 个字符**（在词边界自动分块）
- 分块前会移除 Markdown
- 无速率限制（使用 Twitch 内置的速率限制）
