---
summary: "46. Twitch chat-bot konfiguratsiyasi va sozlash"
read_when:
  - 47. OpenClaw uchun Twitch chat integratsiyasini sozlash
title: "48. Twitch"
---

# 49. Twitch (plagin)

50. IRC ulanishi orqali Twitch chat qo‘llab-quvvatlashi. OpenClaw Twitch foydalanuvchisi (bot akkaunti) sifatida ulanib, kanallarda xabarlarni qabul qiladi va yuboradi.

## Plagin talab qilinadi

Twitch plagin sifatida yetkazib beriladi va asosiy o‘rnatmaga kiritilmagan.

CLI orqali o‘rnatish (npm reyestri):

```bash
openclaw plugins install @openclaw/twitch
```

Mahalliy checkout (git repodan ishga tushirilganda):

```bash
openclaw plugins install ./extensions/twitch
```

Batafsil: [Plugins](/tools/plugin)

## Tezkor sozlash (boshlovchilar uchun)

1. Bot uchun alohida Twitch akkaunti yarating (yoki mavjud akkauntdan foydalaning).
2. Kirish ma’lumotlarini yarating: [Twitch Token Generator](https://twitchtokengenerator.com/)
   - **Bot Token** ni tanlang
   - `chat:read` va `chat:write` scope’lari tanlanganini tasdiqlang
   - **Client ID** va **Access Token** ni nusxalab oling
3. Twitch foydalanuvchi ID’ingizni toping: [https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/](https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/)
4. Tokenni sozlash:
   - Env: `OPENCLAW_TWITCH_ACCESS_TOKEN=...` (faqat standart akkaunt uchun)
   - Yoki config: `channels.twitch.accessToken`
   - Agar ikkalasi ham sozlangan bo‘lsa, config ustunlikka ega (env fallback faqat standart akkaunt uchun).
5. Gateway’ni ishga tushiring.

**⚠️ Muhim:** Ruxsatsiz foydalanuvchilar botni ishga tushira olmasligi uchun access control (`allowFrom` yoki `allowedRoles`) qo‘shing. `requireMention` standart holatda `true`.

Minimal config:

```json5
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw", // Botning Twitch akkaunti
      accessToken: "oauth:abc123...", // OAuth Access Token (yoki OPENCLAW_TWITCH_ACCESS_TOKEN env var’dan foydalaning)
      clientId: "xyz789...", // Token Generator’dan olingan Client ID
      channel: "vevisk", // Qaysi Twitch kanal chatiga ulanish (majburiy)
      allowFrom: ["123456789"], // (tavsiya etiladi) Faqat sizning Twitch user ID’ingiz - uni https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/ dan oling
    },
  },
}
```

## Bu nima

- Gateway’ga tegishli Twitch kanali.
- Deterministik marshrutlash: javoblar har doim Twitch’ga qaytadi.
- Har bir akkaunt alohida sessiya kalitiga mos keladi: `agent:<agentId>:twitch:<accountName>`.
- `username` — autentifikatsiya qilinadigan bot akkaunti, `channel` esa qaysi chat xonasiga ulanishini bildiradi.

## Sozlash (batafsil)

### Kirish ma’lumotlarini yaratish

[Twitch Token Generator](https://twitchtokengenerator.com/) dan foydalaning:

- **Bot Token** ni tanlang
- `chat:read` va `chat:write` scope’lari tanlanganini tasdiqlang
- **Client ID** va **Access Token** ni nusxalab oling

Qo‘lda ilova ro‘yxatdan o‘tkazish talab qilinmaydi. Tokenlar bir necha soatdan keyin muddati tugaydi.

### Botni sozlash

**Env o‘zgaruvchisi (faqat standart akkaunt uchun):**

```bash
OPENCLAW_TWITCH_ACCESS_TOKEN=oauth:abc123...
```

**Yoki config:**

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

Agar ham env, ham config o‘rnatilgan bo‘lsa, config ustuvor bo‘ladi.

### Access control (tavsiya etiladi)

```json5
{
  channels: {
    twitch: {
      allowFrom: ["123456789"], // (tavsiya etiladi) Faqat sizning Twitch user ID’ingiz
    },
  },
}
```

Qattiq allowlist uchun `allowFrom` dan foydalanishni afzal ko‘ring. Agar rolga asoslangan kirishni xohlasangiz, `allowedRoles` dan foydalaning.

**Mavjud rollar:** `"moderator"`, `"owner"`, `"vip"`, `"subscriber"`, `"all"`.

**Nega user ID’lar?** Username’lar o‘zgarishi mumkin, bu esa o‘zini boshqaga o‘xshatib ko‘rsatishga imkon beradi. User ID’lar doimiy hisoblanadi.

Find your Twitch user ID: [https://www.streamweasels.com/tools/convert-twitch-username-%20to-user-id/](https://www.streamweasels.com/tools/convert-twitch-username-%20to-user-id/) (Convert your Twitch username to ID)

## Tokenni yangilash (ixtiyoriy)

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

## Multi-account support

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

`allowFrom` is a hard allowlist. When set, only those user IDs are allowed.
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

If you see "token refresh disabled (no refresh token)":

- Ensure `clientSecret` is provided
- Ensure `refreshToken` is provided

## Config

**Account config:**

- `username` - Bot username
- `accessToken` - OAuth access token with `chat:read` and `chat:write`
- `clientId` - Twitch Client ID (from Token Generator or your app)
- `channel` - Channel to join (required)
- `enabled` - Enable this account (default: `true`)
- `clientSecret` - Optional: For automatic token refresh
- `refreshToken` - Optional: For automatic token refresh
- `expiresIn` - Token expiry in seconds
- `obtainmentTimestamp` - Token obtained timestamp
- `allowFrom` - User ID allowlist
- `allowedRoles` - Role-based access control (`"moderator" | "owner" | "vip" | "subscriber" | "all"`)
- `requireMention` - Require @mention (default: `true`)

**Provider options:**

- `channels.twitch.enabled` - Enable/disable channel startup
- `channels.twitch.username` - Bot username (simplified single-account config)
- `channels.twitch.accessToken` - OAuth access token (simplified single-account config)
- `channels.twitch.clientId` - Twitch Client ID (simplified single-account config)
- `channels.twitch.channel` - Channel to join (simplified single-account config)
- `channels.twitch.accounts.<accountName>` - Multi-account config (all account fields above)

Full example:

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

## Tool actions

The agent can call `twitch` with action:

- `send` - Send a message to a channel

Example:

```json5
{
  action: "twitch",
  params: {
    message: "Hello Twitch!",
    to: "#mychannel",
  },
}
```

## Safety & ops

- **Treat tokens like passwords** - Never commit tokens to git
- **Use automatic token refresh** for long-running bots
- **Use user ID allowlists** instead of usernames for access control
- **Monitor logs** for token refresh events and connection status
- **Scope tokens minimally** - Only request `chat:read` and `chat:write`
- **If stuck**: Restart the gateway after confirming no other process owns the session

## Limits

- **500 characters** per message (auto-chunked at word boundaries)
- Markdown is stripped before chunking
- No rate limiting (uses Twitch's built-in rate limits)
