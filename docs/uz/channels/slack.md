---
summary: "Socket yoki HTTP webhook rejimi uchun Slack sozlamalari"
read_when: "Slack’ni sozlash yoki Slack socket/HTTP rejimini nosozliklarni tuzatish"
title: "Slack"
---

# Slack

## Socket rejimi (standart)

### Tezkor sozlash (boshlovchilar uchun)

1. Slack ilovasini yarating va **Socket Mode** ni yoqing.
2. **App Token** (`xapp-...`) va **Bot Token** (`xoxb-...`) yarating.
3. Tokenlarni OpenClaw uchun o‘rnating va gateway’ni ishga tushiring.

Minimal konfiguratsiya:

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
    },
  },
}
```

### Sozlash

1. [https://api.slack.com/apps](https://api.slack.com/apps) sahifasida Slack ilovasini (From scratch) yarating.
2. **Socket Mode** → yoqing. So‘ng **Basic Information** → **App-Level Tokens** → `connections:write` scope’i bilan **Generate Token and Scopes** ni tanlang. **App Token** (`xapp-...`) ni nusxalang.
3. **OAuth & Permissions** → bot token scope’larini qo‘shing (quyidagi manifestdan foydalaning). **Install to Workspace** tugmasini bosing. **Bot User OAuth Token** (`xoxb-...`) ni nusxalang.
4. Ixtiyoriy: **OAuth & Permissions** → **User Token Scopes** qo‘shing (quyidagi faqat o‘qish ro‘yxatiga qarang). Ilovani qayta o‘rnating va **User OAuth Token** (`xoxp-...`) ni nusxalang.
5. **Event Subscriptions** → hodisalarni yoqing va quyidagilarga obuna bo‘ling:
   - `message.*` (tahrirlar/o‘chirishlar/iplar oqimini o‘z ichiga oladi)
   - `app_mention`
   - `reaction_added`, `reaction_removed`
   - `member_joined_channel`, `member_left_channel`
   - `channel_rename`
   - `pin_added`, `pin_removed`
6. Botni o‘qishi kerak bo‘lgan kanallarga taklif qiling.
7. `channels.slack.slashCommand` dan foydalansangiz, Slash Commands → `/openclaw` yarating. Agar mahalliy buyruqlarni yoqsangiz, har bir ichki buyruq uchun bittadan slash command qo‘shing (`/help` dagi nomlar bilan bir xil). Slack uchun mahalliy buyruqlar sukut bo‘yicha o‘chiq; faqat `channels.slack.commands.native: true` o‘rnatilganda yoqiladi (global `commands.native` = `"auto"`, bu Slack’ni o‘chiq qoldiradi).
8. App Home → foydalanuvchilar botga DM yozishi uchun **Messages Tab** ni yoqing.

Scope’lar va hodisalar mos bo‘lib qolishi uchun quyidagi manifestdan foydalaning.

Ko‘p akkauntni qo‘llab-quvvatlash: har bir akkaunt uchun tokenlar va ixtiyoriy `name` bilan `channels.slack.accounts` dan foydalaning. Umumiy namunani ko‘rish uchun [`gateway/configuration`](/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) ga qarang.

### OpenClaw konfiguratsiyasi (Socket rejimi)

Tokenlarni muhit o‘zgaruvchilari orqali o‘rnating (tavsiya etiladi):

- `SLACK_APP_TOKEN=xapp-...`
- `SLACK_BOT_TOKEN=xoxb-...`

Yoki konfiguratsiya orqali:

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
    },
  },
}
```

### Foydalanuvchi tokeni (ixtiyoriy)

OpenClaw o‘qish amallari (tarix,
pinlar, reaksiyalar, emoji, a’zo ma’lumoti) uchun Slack foydalanuvchi tokenidan (`xoxp-...`) foydalanishi mumkin. Standart holatda bu faqat o‘qish rejimida qoladi: agar mavjud bo‘lsa, o‘qishlar foydalanuvchi tokenini afzal ko‘radi, yozishlar esa siz aniq ruxsat bermaguningizcha bot tokenidan foydalanadi. `userTokenReadOnly: false` bo‘lsa ham, yozishlar uchun bot tokeni mavjud bo‘lsa, u afzal bo‘lib qoladi.

Foydalanuvchi tokenlari konfiguratsiya faylida sozlanadi (env o‘zgaruvchilar qo‘llab-quvvatlanmaydi). Ko‘p akkauntli holatda `channels.slack.accounts.<id>` ni sozlang.userToken\`.

Bot + app + foydalanuvchi tokenlari bilan misol:

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
      userToken: "xoxp-...",
    },
  },
}
```

userTokenReadOnly aniq o‘rnatilgan misol (foydalanuvchi tokeni bilan yozishga ruxsat berish):

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
      userToken: "xoxp-...",
      userTokenReadOnly: false,
    },
  },
}
```

#### Tokenlardan foydalanish

- O‘qish amallari (tarix, reaksiyalar ro‘yxati, pinlar ro‘yxati, emoji ro‘yxati, a’zo ma’lumoti, qidiruv) sozlangan bo‘lsa foydalanuvchi tokenini, aks holda bot tokenini afzal ko‘radi.
- Yozish amallari (xabar yuborish/tahrirlash/o‘chirish, reaksiyalar qo‘shish/o‘chirish, pinlash/pindan chiqarish, fayl yuklash) standart bo‘yicha bot tokenidan foydalanadi. Agar `userTokenReadOnly: false` bo‘lsa va bot tokeni mavjud bo‘lmasa, OpenClaw foydalanuvchi tokeniga o‘tadi.

### Tarix konteksti

- `channels.slack.historyLimit` (yoki `channels.slack.accounts.*.historyLimit`) so‘rovga qancha so‘nggi kanal/guruh xabarlari qo‘shilishini boshqaradi.
- `messages.groupChat.historyLimit` ga qaytadi. O‘chirish uchun `0` ni o‘rnating (standart 50).

## HTTP rejimi (Events API)

Gateway’ingiz Slack tomonidan HTTPS orqali ochiq bo‘lsa (odatda server joylashtirishlar uchun), HTTP webhook rejimidan foydalaning.
HTTP rejimi umumiy so‘rov URL manzili bilan Events API + Interactivity + Slash Commands’dan foydalanadi.

### Sozlash (HTTP rejimi)

1. Slack ilovasini yarating va **Socket Mode** ni o‘chiring (faqat HTTP’dan foydalansangiz ixtiyoriy).
2. **Basic Information** → **Signing Secret** ni nusxalang.
3. **OAuth & Permissions** → ilovani o‘rnating va **Bot User OAuth Token** (`xoxb-...`) ni nusxalang.
4. **Event Subscriptions** → hodisalarni yoqing va **Request URL** ni gateway webhook yo‘liga o‘rnating (standart `/slack/events`).
5. **Interactivity & Shortcuts** → yoqing va xuddi shu **Request URL** ni o‘rnating.
6. **Slash Commands** → buyruqlaringiz uchun xuddi shu **Request URL** ni o‘rnating.

So‘rov URL manzili misoli:
`https://gateway-host/slack/events`

### OpenClaw konfiguratsiyasi (minimal)

```json5
{
  channels: {
    slack: {
      enabled: true,
      mode: "http",
      botToken: "xoxb-...",
      signingSecret: "your-signing-secret",
      webhookPath: "/slack/events",
    },
  },
}
```

Ko‘p akkauntli HTTP rejimi: `channels.slack.accounts.<id>` ni o‘rnating.mode = "http"`va har bir akkaunt uchun noyob`webhookPath\` taqdim eting, shunda har bir Slack ilovasi o‘z URL’iga ega bo‘ladi.

### Manifest (ixtiyoriy)

Ilovani tez yaratish uchun ushbu Slack ilova manifestidan foydalaning (xohlasangiz nom/buyruqni moslang). Agar foydalanuvchi tokenini sozlamoqchi bo‘lsangiz, foydalanuvchi scope’larini qo‘shing.

```json
{
  "display_information": {
    "name": "OpenClaw",
    "description": "Slack connector for OpenClaw"
  },
  "features": {
    "bot_user": {
      "display_name": "OpenClaw",
      "always_online": false
    },
    "app_home": {
      "messages_tab_enabled": true,
      "messages_tab_read_only_enabled": false
    },
    "slash_commands": [
      {
        "command": "/openclaw",
        "description": "Send a message to OpenClaw",
        "should_escape": false
      }
    ]
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "chat:write",
        "channels:history",
        "channels:read",
        "groups:history",
        "groups:read",
        "groups:write",
        "im:history",
        "im:read",
        "im:write",
        "mpim:history",
        "mpim:read",
        "mpim:write",
        "users:read",
        "app_mentions:read",
        "reactions:read",
        "reactions:write",
        "pins:read",
        "pins:write",
        "emoji:read",
        "commands",
        "files:read",
        "files:write"
      ],
      "user": [
        "channels:history",
        "channels:read",
        "groups:history",
        "groups:read",
        "im:history",
        "im:read",
        "mpim:history",
        "mpim:read",
        "users:read",
        "reactions:read",
        "pins:read",
        "emoji:read",
        "search:read"
      ]
    }
  },
  "settings": {
    "socket_mode_enabled": true,
    "event_subscriptions": {
      "bot_events": [
        "app_mention",
        "message.channels",
        "message.groups",
        "message.im",
        "message.mpim",
        "reaction_added",
        "reaction_removed",
        "member_joined_channel",
        "member_left_channel",
        "channel_rename",
        "pin_added",
        "pin_removed"
      ]
    }
  }
}
```

Agar mahalliy buyruqlarni yoqsangiz, ochmoqchi bo‘lgan har bir buyruq uchun bittadan `slash_commands` yozuvini qo‘shing (`/help` ro‘yxatiga mos). `channels.slack.commands.native` bilan almashtiring.

## Scope’lar (joriy va ixtiyoriy)

Slack’ning Conversations API turi bo‘yicha scope’langan: siz faqat haqiqatan ishlatadigan suhbat turlari (channels, groups, im, mpim) uchun scope’lar kerak. Umumiy ko‘rinish uchun qarang:
[https://docs.slack.dev/apis/web-api/using-the-conversations-api/](https://docs.slack.dev/apis/web-api/using-the-conversations-api/)

### Bot tokeni scope’lari (majburiy)

- `chat:write` (`chat.postMessage` orqali xabar yuborish/yangilash/o‘chirish)
  [https://docs.slack.dev/reference/methods/chat.postMessage](https://docs.slack.dev/reference/methods/chat.postMessage)
- `im:write` (`conversations.open` orqali foydalanuvchi DM’larini ochish)
  [https://docs.slack.dev/reference/methods/conversations.open](https://docs.slack.dev/reference/methods/conversations.open)
- `channels:history`, `groups:history`, `im:history`, `mpim:history`
  [https://docs.slack.dev/reference/methods/conversations.history](https://docs.slack.dev/reference/methods/conversations.history)
- `channels:read`, `groups:read`, `im:read`, `mpim:read`
  [https://docs.slack.dev/reference/methods/conversations.info](https://docs.slack.dev/reference/methods/conversations.info)
- `users:read` (foydalanuvchini topish)
  [https://docs.slack.dev/reference/methods/users.info](https://docs.slack.dev/reference/methods/users.info)
- `reactions:read`, `reactions:write` (`reactions.get` / `reactions.add`)
  [https://docs.slack.dev/reference/methods/reactions.get](https://docs.slack.dev/reference/methods/reactions.get)
  [https://docs.slack.dev/reference/methods/reactions.add](https://docs.slack.dev/reference/methods/reactions.add)
- `pins:read`, `pins:write` (`pins.list` / `pins.add` / `pins.remove`)
  [https://docs.slack.dev/reference/scopes/pins.read](https://docs.slack.dev/reference/scopes/pins.read)
  [https://docs.slack.dev/reference/scopes/pins.write](https://docs.slack.dev/reference/scopes/pins.write)
- `emoji:read` (`emoji.list`)
  [https://docs.slack.dev/reference/scopes/emoji.read](https://docs.slack.dev/reference/scopes/emoji.read)
- `files:write` (uploads via `files.uploadV2`)
  [https://docs.slack.dev/messaging/working-with-files/#upload](https://docs.slack.dev/messaging/working-with-files/#upload)

### User token scopes (optional, read-only by default)

Add these under **User Token Scopes** if you configure `channels.slack.userToken`.

- `channels:history`, `groups:history`, `im:history`, `mpim:history`
- `channels:read`, `groups:read`, `im:read`, `mpim:read`
- `users:read`
- `reactions:read`
- `pins:read`
- `emoji:read`
- `search:read`

### Not needed today (but likely future)

- `mpim:write` (only if we add group-DM open/DM start via `conversations.open`)
- `groups:write` (only if we add private-channel management: create/rename/invite/archive)
- `chat:write.public` (only if we want to post to channels the bot isn't in)
  [https://docs.slack.dev/reference/scopes/chat.write.public](https://docs.slack.dev/reference/scopes/chat.write.public)
- `users:read.email` (only if we need email fields from `users.info`)
  [https://docs.slack.dev/changelog/2017-04-narrowing-email-access](https://docs.slack.dev/changelog/2017-04-narrowing-email-access)
- `files:read` (only if we start listing/reading file metadata)

## Config

Slack uses Socket Mode only (no HTTP webhook server). Provide both tokens:

```json
{
  "slack": {
    "enabled": true,
    "botToken": "xoxb-...",
    "appToken": "xapp-...",
    "groupPolicy": "allowlist",
    "dm": {
      "enabled": true,
      "policy": "pairing",
      "allowFrom": ["U123", "U456", "*"],
      "groupEnabled": false,
      "groupChannels": ["G123"],
      "replyToMode": "all"
    },
    "channels": {
      "C123": { "allow": true, "requireMention": true },
      "#general": {
        "allow": true,
        "requireMention": true,
        "users": ["U123"],
        "skills": ["search", "docs"],
        "systemPrompt": "Keep answers short."
      }
    },
    "reactionNotifications": "own",
    "reactionAllowlist": ["U123"],
    "replyToMode": "off",
    "actions": {
      "reactions": true,
      "messages": true,
      "pins": true,
      "memberInfo": true,
      "emojiList": true
    },
    "slashCommand": {
      "enabled": true,
      "name": "openclaw",
      "sessionPrefix": "slack:slash",
      "ephemeral": true
    },
    "textChunkLimit": 4000,
    "mediaMaxMb": 20
  }
}
```

Tokens can also be supplied via env vars:

- `SLACK_BOT_TOKEN`
- `SLACK_APP_TOKEN`

Ack reactions are controlled globally via `messages.ackReaction` +
`messages.ackReactionScope`. Use `messages.removeAckAfterReply` to clear the
ack reaction after the bot replies.

## Limits

- Outbound text is chunked to `channels.slack.textChunkLimit` (default 4000).
- Optional newline chunking: set `channels.slack.chunkMode="newline"` to split on blank lines (paragraph boundaries) before length chunking.
- Media uploads are capped by `channels.slack.mediaMaxMb` (default 20).

## Reply threading

By default, OpenClaw replies in the main channel. Use `channels.slack.replyToMode` to control automatic threading:

| Mode    | Behavior                                                                                                                                                                                                               |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `off`   | **Default.** Reply in main channel. Only thread if the triggering message was already in a thread.                                                                     |
| `first` | First reply goes to thread (under the triggering message), subsequent replies go to main channel. Useful for keeping context visible while avoiding thread clutter. |
| `all`   | All replies go to thread. Keeps conversations contained but may reduce visibility.                                                                                                     |

The mode applies to both auto-replies and agent tool calls (`slack sendMessage`).

### Per-chat-type threading

You can configure different threading behavior per chat type by setting `channels.slack.replyToModeByChatType`:

```json5
{
  channels: {
    slack: {
      replyToMode: "off", // default for channels
      replyToModeByChatType: {
        direct: "all", // DMs always thread
        group: "first", // group DMs/MPIM thread first reply
      },
    },
  },
}
```

Supported chat types:

- `direct`: 1:1 DMs (Slack `im`)
- `group`: group DMs / MPIMs (Slack `mpim`)
- `channel`: standard channels (public/private)

Precedence:

1. `replyToModeByChatType.<chatType>`
2. `replyToMode`
3. Provider default (`off`)

Legacy `channels.slack.dm.replyToMode` is still accepted as a fallback for `direct` when no chat-type override is set.

Examples:

Thread DMs only:

```json5
{
  channels: {
    slack: {
      replyToMode: "off",
      replyToModeByChatType: { direct: "all" },
    },
  },
}
```

Thread group DMs but keep channels in the root:

```json5
{
  channels: {
    slack: {
      replyToMode: "off",
      replyToModeByChatType: { group: "first" },
    },
  },
}
```

Make channels thread, keep DMs in the root:

```json5
{
  channels: {
    slack: {
      replyToMode: "first",
      replyToModeByChatType: { direct: "off", group: "off" },
    },
  },
}
```

### Manual threading tags

For fine-grained control, use these tags in agent responses:

- `[[reply_to_current]]` — reply to the triggering message (start/continue thread).
- `[[reply_to:<id>]]` — reply to a specific message id.

## Sessions + routing

- DMs share the `main` session (like WhatsApp/Telegram).
- Channels map to `agent:<agentId>:slack:channel:<channelId>` sessions.
- Slash commands use `agent:<agentId>:slack:slash:<userId>` sessions (prefix configurable via `channels.slack.slashCommand.sessionPrefix`).
- If Slack doesn’t provide `channel_type`, OpenClaw infers it from the channel ID prefix (`D`, `C`, `G`) and defaults to `channel` to keep session keys stable.
- Native command registration uses `commands.native` (global default `"auto"` → Slack off) and can be overridden per-workspace with `channels.slack.commands.native`. Text commands require standalone `/...` messages and can be disabled with `commands.text: false`. Slack slash commands are managed in the Slack app and are not removed automatically. Use `commands.useAccessGroups: false` to bypass access-group checks for commands.
- Full command list + config: [Slash commands](/tools/slash-commands)

## DM security (pairing)

- Default: `channels.slack.dm.policy="pairing"` — unknown DM senders get a pairing code (expires after 1 hour).
- Approve via: `openclaw pairing approve slack <code>`.
- To allow anyone: set `channels.slack.dm.policy="open"` and `channels.slack.dm.allowFrom=["*"]`.
- `channels.slack.dm.allowFrom` accepts user IDs, @handles, or emails (resolved at startup when tokens allow). The wizard accepts usernames and resolves them to ids during setup when tokens allow.

## Group policy

- `channels.slack.groupPolicy` controls channel handling (`open|disabled|allowlist`).
- `allowlist` requires channels to be listed in `channels.slack.channels`.
- If you only set `SLACK_BOT_TOKEN`/`SLACK_APP_TOKEN` and never create a `channels.slack` section,
  the runtime defaults `groupPolicy` to `open`. Add `channels.slack.groupPolicy`,
  `channels.defaults.groupPolicy`, or a channel allowlist to lock it down.
- The configure wizard accepts `#channel` names and resolves them to IDs when possible
  (public + private); if multiple matches exist, it prefers the active channel.
- On startup, OpenClaw resolves channel/user names in allowlists to IDs (when tokens allow)
  and logs the mapping; unresolved entries are kept as typed.
- To allow **no channels**, set `channels.slack.groupPolicy: "disabled"` (or keep an empty allowlist).

Channel options (`channels.slack.channels.<id>` or `channels.slack.channels.<name>`):

- `allow`: allow/deny the channel when `groupPolicy="allowlist"`.
- `requireMention`: mention gating for the channel.
- `tools`: kanal bo‘yicha ixtiyoriy asbob siyosati override’lari (`allow`/`deny`/`alsoAllow`).
- `toolsBySender`: kanal ichida jo‘natuvchi bo‘yicha ixtiyoriy asbob siyosati override’lari (kalitlar — jo‘natuvchi ID’lari/@handle’lar/email’lar; `"*"` wildcard qo‘llab-quvvatlanadi).
- `allowBots`: ushbu kanalda bot tomonidan yozilgan xabarlarga ruxsat berish (standart: false).
- `users`: kanal bo‘yicha ixtiyoriy foydalanuvchi allowlist.
- `skills`: ko‘nikmalar filtri (qoldirilsa = barcha ko‘nikmalar, bo‘sh = hech biri).
- `systemPrompt`: kanal uchun qo‘shimcha system prompt (mavzu/maqsad bilan birlashtiriladi).
- `enabled`: `false` qilib o‘rnatsangiz kanal o‘chiriladi.

## Yetkazib berish maqsadlari

Bularni cron/CLI yuborishlar bilan ishlating:

- `user:<id>` — DM’lar uchun
- `channel:<id>` — kanallar uchun

## Asbob harakatlari

Slack asbob harakatlari `channels.slack.actions.*` orqali cheklanishi mumkin:

| Harakat guruhi | Standart | Eslatmalar                            |
| -------------- | -------- | ------------------------------------- |
| reaksiyalar    | yoqilgan | Reaksiya qo‘shish + reaksiya ro‘yxati |
| xabarlar       | yoqilgan | O‘qish/jo‘natish/tahrirlash/o‘chirish |
| pinlar         | yoqilgan | Pin qo‘yish/olib tashlash/ro‘yxat     |
| memberInfo     | yoqilgan | A’zo ma’lumoti                        |
| emojiList      | yoqilgan | Maxsus emoji ro‘yxati                 |

## Xavfsizlik bo‘yicha eslatmalar

- Yozishlar sukut bo‘yicha bot tokenidan foydalanadi, shuning uchun holatni o‘zgartiruvchi harakatlar ilovaning bot ruxsatlari va identiteti doirasida qoladi.
- `userTokenReadOnly: false` ni sozlash bot tokeni mavjud bo‘lmaganda yozish amallari uchun foydalanuvchi tokenidan foydalanishga ruxsat beradi, bu esa harakatlar o‘rnatgan foydalanuvchining kirish huquqlari bilan bajarilishini anglatadi. Foydalanuvchi tokenini yuqori darajada imtiyozli deb hisoblang va harakatlar uchun gate’lar hamda allowlist’larni qat’iy saqlang.
- Agar foydalanuvchi-token yozishlarini yoqsangiz, foydalanuvchi tokenida kutilgan yozish scope’lari (`chat:write`, `reactions:write`, `pins:write`,
  `files:write`) mavjudligiga ishonch hosil qiling, aks holda bu amallar bajarilmaydi.

## Nosozliklarni bartaraf etish

Avval ushbu ketma-ketlikni ishga tushiring:

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

So‘ngra kerak bo‘lsa DM juftlash holatini tasdiqlang:

```bash
openclaw pairing list slack
```

Keng tarqalgan nosozliklar:

- Ulangan, ammo kanalda javob yo‘q: kanal `groupPolicy` tomonidan bloklangan yoki `channels.slack.channels` allowlist’ida yo‘q.
- DM’lar e’tiborsiz qoldiriladi: `channels.slack.dm.policy="pairing"` bo‘lganda jo‘natuvchi tasdiqlanmagan.
- API xatolari (`missing_scope`, `not_in_channel`, autentifikatsiya xatolari): bot/ilova tokenlari yoki Slack scope’lari to‘liq emas.

Triage jarayoni uchun: [/channels/troubleshooting](/channels/troubleshooting).

## Eslatmalar

- Mention gate’lash `channels.slack.channels` orqali boshqariladi (`requireMention` ni `true` qilib qo‘ying); `agents.list[].groupChat.mentionPatterns` (yoki `messages.groupChat.mentionPatterns`) ham mention sifatida hisoblanadi.
- Multi-agent override: set per-agent patterns on `agents.list[].groupChat.mentionPatterns`.
- Reaksiya bildirishnomalari `channels.slack.reactionNotifications` ga amal qiladi (`reactionAllowlist` ni `allowlist` rejimi bilan ishlating).
- Bot-authored messages are ignored by default; enable via `channels.slack.allowBots` or `channels.slack.channels.<id>3. Ogohlantirish: Agar boshqa botlarga javob berishga ruxsat bersangiz (`channels.slack.allowBots=true`yoki`channels.slack.channels.<id>
  4. .allowBots=true`), `requireMention`, `channels.slack.channels.<id>
  5. .users`ruxsat ro‘yxatlari va/yoki`AGENTS.md`hamda`SOUL.md\` dagi aniq himoya qoidalari bilan botdan-botga javob aylanishlarining oldini oling.
- 6. Slack vositasi uchun reaksiya olib tashlash semantikasi [/tools/reactions](/tools/reactions) da keltirilgan..allowBots=true`), prevent bot-to-bot reply loops with `requireMention`, `channels.slack.channels.<id>8. Telegram bot qo‘llab-quvvatlash holati, imkoniyatlari va sozlamalari
- 9. Telegram funksiyalari yoki webhooklar ustida ishlash
- 10. Telegram
