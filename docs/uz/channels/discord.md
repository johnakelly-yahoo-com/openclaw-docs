---
summary: "Discord bot support status, capabilities, and configuration"
read_when:
  - Working on Discord channel features
title: "Discord"
---

# Discord (Bot API)

Status: ready for DM and guild text channels via the official Discord bot gateway.

## Quick setup (beginner)

1. Create a Discord bot and copy the bot token.
2. 30. Discord ilova sozlamalarida **Message Content Intent** ni yoqing (va agar ruxsat ro‘yxatlaridan yoki nom bo‘yicha qidirishdan foydalanmoqchi bo‘lsangiz **Server Members Intent** ni ham).
3. Set the token for OpenClaw:
   - Env: `DISCORD_BOT_TOKEN=...`
   - Or config: `channels.discord.token: "..."`.
   - If both are set, config takes precedence (env fallback is default-account only).
4. Invite the bot to your server with message permissions (create a private server if you just want DMs).
5. Start the gateway.
6. DM access is pairing by default; approve the pairing code on first contact.

Minimal config:

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "YOUR_BOT_TOKEN",
    },
  },
}
```

## Goals

- 31. OpenClaw bilan Discord DMlari yoki guild kanallari orqali muloqot qiling.
- Direct chats collapse into the agent's main session (default `agent:main:main`); guild channels stay isolated as `agent:<agentId>:discord:channel:<channelId>` (display names use `discord:<guildSlug>#<channelSlug>`).
- Group DMs are ignored by default; enable via `channels.discord.dm.groupEnabled` and optionally restrict by `channels.discord.dm.groupChannels`.
- Keep routing deterministic: replies always go back to the channel they arrived on.

## 32. Qanday ishlaydi

1. Create a Discord application → Bot, enable the intents you need (DMs + guild messages + message content), and grab the bot token.
2. 33. Botni serveringizga taklif qiling va undan foydalanmoqchi bo‘lgan joylarda xabarlarni o‘qish/jo‘natish uchun zarur ruxsatlarni bering.
3. Configure OpenClaw with `channels.discord.token` (or `DISCORD_BOT_TOKEN` as a fallback).
4. Run the gateway; it auto-starts the Discord channel when a token is available (config first, env fallback) and `channels.discord.enabled` is not `false`.
   - If you prefer env vars, set `DISCORD_BOT_TOKEN` (a config block is optional).
5. Direct chats: use `user:<id>` (or a `<@id>` mention) when delivering; all turns land in the shared `main` session. Bare numeric IDs are ambiguous and rejected.
6. Guild channels: use `channel:<channelId>` for delivery. Mentions are required by default and can be set per guild or per channel.
7. Direct chats: secure by default via `channels.discord.dm.policy` (default: `"pairing"`). Unknown senders get a pairing code (expires after 1 hour); approve via `openclaw pairing approve discord <code>`.
   - To keep old “open to anyone” behavior: set `channels.discord.dm.policy="open"` and `channels.discord.dm.allowFrom=["*"]`.
   - To hard-allowlist: set `channels.discord.dm.policy="allowlist"` and list senders in `channels.discord.dm.allowFrom`.
   - To ignore all DMs: set `channels.discord.dm.enabled=false` or `channels.discord.dm.policy="disabled"`.
8. Group DMs are ignored by default; enable via `channels.discord.dm.groupEnabled` and optionally restrict by `channels.discord.dm.groupChannels`.
9. Optional guild rules: set `channels.discord.guilds` keyed by guild id (preferred) or slug, with per-channel rules.
10. Optional native commands: `commands.native` defaults to `"auto"` (on for Discord/Telegram, off for Slack). Override with `channels.discord.commands.native: true|false|"auto"`; `false` clears previously registered commands. Text commands are controlled by `commands.text` and must be sent as standalone `/...` messages. Use `commands.useAccessGroups: false` to bypass access-group checks for commands.
    - To‘liq buyruqlar ro‘yxati + konfiguratsiya: [Slash commands](/tools/slash-commands)
11. Ixtiyoriy guild kontekst tarixi: eslatmaga javob berishda oxirgi N ta guild xabarlarini kontekst sifatida qo‘shish uchun `channels.discord.historyLimit` (standart 20, `messages.groupChat.historyLimit` ga qaytadi) ni sozlang. O‘chirish uchun `0` ga o‘rnating.
12. Reaksiyalar: agent `discord` vositasi orqali reaksiyalarni ishga tushirishi mumkin (`channels.discord.actions.*` bilan cheklangan).
    - Reaksiyani olib tashlash semantikasi: [/tools/reactions](/tools/reactions) ga qarang.
    - `discord` vositasi faqat joriy kanal Discord bo‘lganda ochiladi.
13. Mahalliy buyruqlar umumiy `main` sessiyasi o‘rniga izolyatsiyalangan sessiya kalitlaridan (`agent:<agentId>:discord:slash:<userId>`) foydalanadi.

Eslatma: Ism → id aniqlash guild a’zolarini qidirishdan foydalanadi va Server Members Intent ni talab qiladi; agar bot a’zolarni qidira olmasa, idlardan yoki `<@id>` eslatmalaridan foydalaning.
Eslatma: Sluglar kichik harflarda bo‘ladi va bo‘shliqlar `-` bilan almashtiriladi. Kanal nomlari boshidagi `#`siz sluglanadi.
Eslatma: Guild kontekstidagи `[from:]` satrlari pingga tayyor javoblarni osonlashtirish uchun `author.tag` + `id` ni o‘z ichiga oladi.

## Konfiguratsiyani yozish

Standart bo‘yicha Discord `/config set|unset` orqali ishga tushirilgan konfiguratsiya yangilanishlarini yozishga ruxsat beradi (`commands.config: true` talab qilinadi).

Quyidagicha o‘chiring:

```json5
{
  channels: { discord: { configWrites: false } },
}
```

## O‘zingizning botingizni qanday yaratish

Bu OpenClaw’ni `#help` kabi server (guild) kanalida ishga tushirish uchun “Discord Developer Portal” sozlamalaridir.

### 1. Discord ilovasi + bot foydalanuvchisini yarating

1. Discord Developer Portal → **Applications** → **New Application**
2. Ilovangizda:
   - **Bot** → **Add Bot**
   - **Bot Token** ni nusxalab oling (buni `DISCORD_BOT_TOKEN` ga qo‘yasiz)

### 2) OpenClaw ga kerak bo‘lgan gateway intentlarni yoqing

Discord “privileged intents”ni faqat siz ularni aniq yoqsangizgina ruxsat beradi.

**Bot** → **Privileged Gateway Intents** bo‘limida quyidagilarni yoqing:

- **Message Content Intent** (ko‘pgina guildlarda xabar matnini o‘qish uchun talab qilinadi; bo‘lmasa “Used disallowed intents”ni ko‘rasiz yoki bot ulanadi-yu, lekin xabarlarga javob bermaydi)
- **Server Members Intent** (tavsiya etiladi; ayrim a’zo/foydalanuvchi qidiruvlari va guildlarda allowlist moslash uchun talab qilinadi)

Odatda **Presence Intent** kerak **emas**. Botning o‘z presence’ini sozlash (`setPresence` amali) gateway OP3 dan foydalanadi va bu intentni talab qilmaydi; u faqat boshqa guild a’zolarining presence yangilanishlarini olishni istasangiz kerak bo‘ladi.

### 3. Taklif URL’ini yarating (OAuth2 URL Generator)

Ilovangizda: **OAuth2** → **URL Generator**

**Scopes**

- ✅ `bot`
- ✅ `applications.commands` (mahalliy buyruqlar uchun talab qilinadi)

**Bot Permissions** (minimal asos)

- ✅ Kanallarni ko‘rish
- ✅ Xabar yuborish
- ✅ Xabarlar tarixini o‘qish
- ✅ Havolalarni joylash (Embed Links)
- ✅ Fayllarni biriktirish
- ✅ Reaksiya qo‘shish (ixtiyoriy, ammo tavsiya etiladi)
- ✅ Tashqi emoji / stikerlardan foydalanish (ixtiyoriy; faqat xohlasangiz)

Nosozliklarni tuzatishdan tashqari va botga to‘liq ishonmasangiz **Administrator** dan qoching.

Yaratilgan URL’ni nusxalab oling, uni oching, serveringizni tanlang va botni o‘rnating.

### 4. Idlarni oling (guild/foydalanuvchi/kanal)

Discord hamma joyda raqamli idlardan foydalanadi; OpenClaw konfiguratsiyasi idlarni afzal ko‘radi.

1. Discord (desktop/web) → **User Settings** → **Advanced** → **Developer Mode** ni yoqing
2. O‘ng tugma bilan bosing:
   - Server nomi → **Copy Server ID** (guild id)
   - Kanal (masalan, `#help`) → **Copy Channel ID**
   - Sizning foydalanuvchingiz → **Foydalanuvchi ID nusxalash**

### 5) OpenClaw’ni sozlash

#### Token

Bot tokenini env o‘zgaruvchisi orqali o‘rnating (serverlarda tavsiya etiladi):

- `DISCORD_BOT_TOKEN=...`

Yoki config orqali:

```json5
34. {
  channels: {
    discord: {
      enabled: true,
      token: "YOUR_BOT_TOKEN",
    },
  },
}
```

Ko‘p akkauntli qo‘llab-quvvatlash: har bir akkaunt uchun tokenlar va ixtiyoriy `name` bilan `channels.discord.accounts` dan foydalaning. Umumiy andoza uchun [`gateway/configuration`](/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) sahifasiga qarang.

#### Allowlist + kanal marshrutlash

Misol “bitta server, faqat menga ruxsat, faqat #help ga ruxsat”:

```json5
{
  channels: {
    discord: {
      enabled: true,
      dm: { enabled: false },
      guilds: {
        YOUR_GUILD_ID: {
          users: ["YOUR_USER_ID"],
          requireMention: true,
          channels: {
            help: { allow: true, requireMention: true },
          },
        },
      },
      retry: {
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}
```

Eslatmalar:

- `requireMention: true` — bot faqat tilga olinganda javob beradi (umumiy kanallar uchun tavsiya etiladi).
- `agents.list[].groupChat.mentionPatterns` (yoki `messages.groupChat.mentionPatterns`) ham guild xabarlari uchun tilga olish sifatida hisoblanadi.
- Ko‘p agentli override: `agents.list[].groupChat.mentionPatterns` da har bir agent uchun alohida andozalarni o‘rnating.
- Agar `channels` mavjud bo‘lsa, ro‘yxatda ko‘rsatilmagan har qanday kanal sukut bo‘yicha rad etiladi.
- Barcha kanallar bo‘ylab standartlarni qo‘llash uchun `"*"` kanal yozuvidan foydalaning; aniq kanal yozuvlari wildcard’ni bekor qiladi.
- Threadlar ota-ona kanal sozlamalarini meros oladi (allowlist, `requireMention`, ko‘nikmalar, promptlar va hokazo). Agar thread kanal ID sini aniq qo‘shmasangiz.
- Ega (owner) ishorasi: per-guild yoki per-channel `users` allowlist jo‘natuvchiga mos kelsa, OpenClaw tizim promptida uni ega sifatida ko‘radi. Kanallar bo‘ylab global ega uchun `commands.ownerAllowFrom` ni o‘rnating.
- Bot tomonidan yozilgan xabarlar sukut bo‘yicha e’tiborsiz qoldiriladi; ularga ruxsat berish uchun `channels.discord.allowBots=true` ni o‘rnating (o‘z xabarlaringiz baribir filtrlanadi).
- Ogohlantirish: Agar boshqa botlarga javob berishga ruxsat bersangiz (`channels.discord.allowBots=true`), botdan-botga javob aylanasini `requireMention`, `channels.discord.guilds.*.channels.<id>.users` allowlistlari va/yoki `AGENTS.md` hamda `SOUL.md` dagi aniq guardrail’lar bilan oldini oling.6) Ishlashini tekshirish

### Gateway’ni ishga tushiring.

1. Server kanalingizda yuboring: `@Krill hello` (yoki bot nomingiz qanday bo‘lsa).
2. Agar hech narsa bo‘lmasa: quyidagi **Troubleshooting** ni tekshiring.
3. Nosozliklarni bartaraf etish

### Birinchi qadam: `openclaw doctor` va `openclaw channels status --probe` ni ishga tushiring (amaliy ogohlantirishlar + tezkor auditlar).

- **“Used disallowed intents”**: Developer Portal’da **Message Content Intent** (va ehtimol **Server Members Intent**) ni yoqing, so‘ng gateway’ni qayta ishga tushiring.
- **Bot ulanadi, lekin guild kanalida hech qachon javob bermaydi**:
- **Message Content Intent** yo‘q, yoki
  - Botda kanal ruxsatlari yo‘q (View/Send/Read History), yoki
  - Config tilga olishni talab qiladi va siz uni tilga olmadingiz, yoki
  - Guild/kanal allowlist’ingiz kanal/foydalanuvchini rad etadi.
  - **`requireMention: false`, lekin baribir javob yo‘q**:
- `channels.discord.groupPolicy` sukut bo‘yicha **allowlist**; uni `"open"` ga o‘rnating yoki `channels.discord.guilds` ostida guild yozuvi qo‘shing (ixtiyoriy ravishda `channels.discord.guilds.<id>.channels` ostida kanallarni cheklash uchun ro‘yxatlang).
- Agar siz faqat `DISCORD_BOT_TOKEN` ni o‘rnatib, hech qachon `channels.discord` bo‘limini yaratmagan bo‘lsangiz, runtime `groupPolicy` ni `open` ga sukut bo‘yicha o‘rnatadi.Uni qulflash uchun `channels.discord.groupPolicy`, `channels.defaults.groupPolicy` yoki guild/kanal allowlist qo‘shing.
  - `requireMention` `channels.discord.guilds` ostida (yoki aniq kanal ostida) joylashishi kerak. Yuqori darajadagi `channels.discord.requireMention` e’tiborsiz qoldiriladi.
- **Ruxsat auditlari** (`channels status --probe`) faqat raqamli kanal ID’larini tekshiradi. Agar `channels.discord.guilds.*.channels` kalitlari sifatida slug/nomlardan foydalansangiz, audit ruxsatlarni tekshira olmaydi.
- **DM’lar ishlamaydi**: `channels.discord.dm.enabled=false`, `channels.discord.dm.policy="disabled"`, yoki hali tasdiqlanmagansiz (`channels.discord.dm.policy="pairing"`). **Discord’da exec tasdiqlari**: Discord DM’larda exec tasdiqlari uchun **tugma UI** ni qo‘llab-quvvatlaydi (Bir marta ruxsat / Har doim ruxsat / Rad etish).
- `/approve <id> ...` faqat yo‘naltirilgan tasdiqlar uchun va Discord’ning tugma promptlarini hal qilmaydi.
- Agar `❌ Failed to submit approval: Error: unknown approval id` ni ko‘rsangiz yoki UI umuman chiqmasa, tekshiring: `/approve <id> ...` is only for forwarded approvals and won’t resolve Discord’s button prompts. If you see `❌ Failed to submit approval: Error: unknown approval id` or the UI never shows up, check:
  - 35. Konfiguratsiyangizda `channels.discord.execApprovals.enabled: true`.
  - Your Discord user ID is listed in `channels.discord.execApprovals.approvers` (the UI is only sent to approvers).
  - Use the buttons in the DM prompt (**Allow once**, **Always allow**, **Deny**).
  - See [Exec approvals](/tools/exec-approvals) and [Slash commands](/tools/slash-commands) for the broader approvals and command flow.

## Capabilities & limits

- DMs and guild text channels (threads are treated as separate channels; voice not supported).
- Typing indicators sent best-effort; message chunking uses `channels.discord.textChunkLimit` (default 2000) and splits tall replies by line count (`channels.discord.maxLinesPerMessage`, default 17).
- Optional newline chunking: set `channels.discord.chunkMode="newline"` to split on blank lines (paragraph boundaries) before length chunking.
- File uploads supported up to the configured `channels.discord.mediaMaxMb` (default 8 MB).
- Mention-gated guild replies by default to avoid noisy bots.
- Reply context is injected when a message references another message (quoted content + ids).
- Native reply threading is **off by default**; enable with `channels.discord.replyToMode` and reply tags.

## 36. Qayta urinish siyosati

37. Chiquvchi Discord API chaqiruvlari tezlik cheklovlari (429) bo‘lganda, mavjud bo‘lsa Discord `retry_after` dan foydalanib, eksponentsial backoff va jitter bilan qayta urinadi. 38. `channels.discord.retry` orqali sozlang. See [Retry policy](/concepts/retry).

## Config

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "abc.123",
      groupPolicy: "allowlist",
      guilds: {
        "*": {
          channels: {
            general: { allow: true },
          },
        },
      },
      mediaMaxMb: 8,
      actions: {
        reactions: true,
        stickers: true,
        emojiUploads: true,
        stickerUploads: true,
        polls: true,
        permissions: true,
        messages: true,
        threads: true,
        pins: true,
        search: true,
        memberInfo: true,
        roleInfo: true,
        roles: false,
        channelInfo: true,
        channels: true,
        voiceStatus: true,
        events: true,
        moderation: false,
        presence: false,
      },
      replyToMode: "off",
      dm: {
        enabled: true,
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["123456789012345678", "steipete"],
        groupEnabled: false,
        groupChannels: ["openclaw-dm"],
      },
      guilds: {
        "*": { requireMention: true },
        "123456789012345678": {
          slug: "friends-of-openclaw",
          requireMention: false,
          reactionNotifications: "own",
          users: ["987654321098765432", "steipete"],
          channels: {
            general: { allow: true },
            help: {
              allow: true,
              requireMention: true,
              users: ["987654321098765432"],
              skills: ["search", "docs"],
              systemPrompt: "Keep answers short.",
            },
          },
        },
      },
    },
  },
}
```

Ack reactions are controlled globally via `messages.ackReaction` +
`messages.ackReactionScope`. Use `messages.removeAckAfterReply` to clear the
ack reaction after the bot replies.

- `dm.enabled`: set `false` to ignore all DMs (default `true`).
- `dm.policy`: DM access control (`pairing` recommended). `"open"` requires `dm.allowFrom=["*"]`.
- `dm.allowFrom`: DM allowlist (user ids or names). Used by `dm.policy="allowlist"` and for `dm.policy="open"` validation. The wizard accepts usernames and resolves them to ids when the bot can search members.
- `dm.groupEnabled`: enable group DMs (default `false`).
- `dm.groupChannels`: optional allowlist for group DM channel ids or slugs.
- `groupPolicy`: controls guild channel handling (`open|disabled|allowlist`); `allowlist` requires channel allowlists.
- `guilds`: per-guild rules keyed by guild id (preferred) or slug.
- `guilds."*"`: default per-guild settings applied when no explicit entry exists.
- `guilds.<id>.slug`: optional friendly slug used for display names.
- `guilds.<id>.users`: optional per-guild user allowlist (ids or names).
- `guilds.<id>.tools`: optional per-guild tool policy overrides (`allow`/`deny`/`alsoAllow`) used when the channel override is missing.
- `guilds.<id>.toolsBySender`: optional per-sender tool policy overrides at the guild level (applies when the channel override is missing; `"*"` wildcard supported).
- `guilds.<id>.channels.<channel>.allow`: allow/deny the channel when `groupPolicy="allowlist"`.
- `guilds.<id>.channels.<channel>.requireMention`: mention gating for the channel.
- `guilds.<id>.channels.<channel>.tools`: optional per-channel tool policy overrides (`allow`/`deny`/`alsoAllow`).
- `guilds.<id>.channels.<channel>.toolsBySender`: optional per-sender tool policy overrides within the channel (`"*"` wildcard supported).
- `guilds.<id>.channels.<channel>.users`: optional per-channel user allowlist.
- `guilds.<id>.channels.<channel>39. `.skills\`: ko‘nikmalar filtri (qoldirilsa = barcha ko‘nikmalar, bo‘sh = hech biri).
- `guilds.<id>40. `.channels.<channel>`.systemPrompt`: extra system prompt for the channel. Discord channel topics are injected as **untrusted** context (not system prompt).
- 41. `guilds.<id>`.channels.<channel>.enabled`: set `false\` to disable the channel.
- `guilds.<id>.channels`: channel rules (keys are channel slugs or ids).
- `guilds.<id>.requireMention`: per-guild mention requirement (overridable per channel).
- `guilds.<id>42. `.reactionNotifications`: reaksiya tizimi hodisa rejimi (`off`, `own`, `all`, `allowlist\`).
- `textChunkLimit`: outbound text chunk size (chars). Default: 2000.
- `chunkMode`: `length` (default) splits only when exceeding `textChunkLimit`; `newline` splits on blank lines (paragraph boundaries) before length chunking.
- `maxLinesPerMessage`: soft max line count per message. Default: 17.
- `mediaMaxMb`: clamp inbound media saved to disk.
- `historyLimit`: number of recent guild messages to include as context when replying to a mention (default 20; falls back to `messages.groupChat.historyLimit`; `0` disables).
- `dmHistoryLimit`: DM history limit in user turns. Per-user overrides: `dms["<user_id>"].historyLimit`.
- `retry`: retry policy for outbound Discord API calls (attempts, minDelayMs, maxDelayMs, jitter).
- `pluralkit`: resolve PluralKit proxied messages so system members appear as distinct senders.
- `actions`: per-action tool gates; omit to allow all (set `false` to disable).
  - `reactions` (covers react + read reactions)
  - `stickers`, `emojiUploads`, `stickerUploads`, `polls`, `permissions`, `messages`, `threads`, `pins`, `search`
  - `memberInfo`, `roleInfo`, `channelInfo`, `voiceStatus`, `events`
  - `channels` (create/edit/delete channels + categories + permissions)
  - 43. `roles` (rol qo‘shish/olib tashlash, sukut bo‘yicha `false`)
  - `moderation` (timeout/kick/ban, default `false`)
  - `presence` (bot status/activity, default `false`)
- `execApprovals`: Discord-only exec approval DMs (button UI). Supports `enabled`, `approvers`, `agentFilter`, `sessionFilter`.

Reaction notifications use `guilds.<id>.reactionNotifications`:

- `off`: no reaction events.
- `own`: reactions on the bot's own messages (default).
- `all`: all reactions on all messages.
- `allowlist`: reactions from `guilds.<id>.users` on all messages (empty list disables).

### PluralKit (PK) support

Enable PK lookups so proxied messages resolve to the underlying system + member.
Yoqilganda, OpenClaw ruxsat roʻyxatlari uchun aʼzo identifikatoridan foydalanadi va tasodifiy Discord pinglarini oldini olish uchun joʻnatuvchini `Member (PK:System)` deb belgilaydi.

```json5
{
  channels: {
    discord: {
      pluralkit: {
        enabled: true,
        token: "pk_live_...", // optional; required for private systems
      },
    },
  },
}
```

Ruxsat roʻyxati izohlari (PK yoqilgan):

- `dm.allowFrom`, `guilds.<id>`.users`yoki kanal bo‘yicha`users`ichida`pk:<memberId>\` dan foydalaning.
- Aʼzo ko‘rsatish nomlari ham nom/slug bo‘yicha moslashtiriladi.
- Qidiruvlar **asl** Discord xabar ID’sidan (proksi oldidagi xabar) foydalanadi, shuning uchun PK API uni faqat 30 daqiqalik oynasi ichida aniqlay oladi.
- Agar PK qidiruvlari muvaffaqiyatsiz bo‘lsa (masalan, tokenisiz maxfiy tizim), proksi qilingan xabarlar bot xabarlari sifatida ko‘riladi va `channels.discord.allowBots=true` bo‘lmasa, bekor qilinadi.

### Asbob amalining standart sozlamalari

| Amallar guruhi                         | Standart                               | Izohlar                                                                          |
| -------------------------------------- | -------------------------------------- | -------------------------------------------------------------------------------- |
| reaksiyalar                            | yoqilgan                               | Reaksiya qilish + reaksiya roʻyxati + emojiList                                  |
| stikerlar                              | yoqilgan                               | Stikerlarni yuborish                                                             |
| emoji yuklamalari                      | yoqilgan                               | Emojilarni yuklash                                                               |
| stiker yuklamalari                     | yoqilgan                               | Stikerlarni yuklash                                                              |
| soʻrovnomalar                          | yoqilgan                               | Soʻrovnomalar yaratish                                                           |
| ruxsatlar                              | yoqilgan                               | Kanal ruxsatlari oniy nusxasi                                                    |
| xabarlar                               | yoqilgan                               | O‘qish/yuborish/tahrirlash/o‘chirish                                             |
| mavzular                               | yoqilgan                               | Yaratish/ro‘yxatlash/javob berish                                                |
| pinlar                                 | yoqilgan                               | Qadash/olib tashlash/ro‘yxatlash                                                 |
| qidiruv                                | yoqilgan                               | Xabarlarni qidirish (oldindan ko‘rish funksiyasi)             |
| aʼzo maʼlumoti                         | yoqilgan                               | Aʼzo maʼlumoti                                                                   |
| rol maʼlumoti                          | yoqilgan                               | Rollar roʻyxati                                                                  |
| kanal maʼlumoti                        | yoqilgan                               | 1. Kanal maʼlumoti + roʻyxat                              |
| 44. kanallar    | 3. yoqilgan     | 4. Kanal/toifa boshqaruvi                                 |
| 5. voiceStatus  | 6. yoqilgan     | 7. Ovoz holatini aniqlash                                 |
| 8. hodisalar    | 9. yoqilgan     | 10. Rejalashtirilgan hodisalarni roʻyxatlash/yaratish     |
| 45. rollar      | 12. oʻchirilgan | 13. Rol qoʻshish/oʻchirish                                |
| 46. moderatsiya | 15. oʻchirilgan | 16. Timeout/kick/ban                                      |
| 17. presence    | 18. oʻchirilgan | 19. Bot holati/faoliyati (setPresence) |

- 20. `replyToMode`: `off` (standart), `first` yoki `all`. 21. Faqat model javob tegi mavjud bo‘lganda qo‘llaniladi.

## 22. Javob teglari

23. Tarmoqlangan javobni so‘rash uchun model o‘z chiqishida bitta tegni kiritishi mumkin:

- 24. `[[reply_to_current]]` — qo‘zg‘atuvchi Discord xabariga javob berish.
- 25. `[[reply_to:<id>]]` — kontekst/tarixdan aniq xabar identifikatoriga javob berish.
  26. Joriy xabar identifikatorlari so‘rovlarga `[message_id: …]` ko‘rinishida qo‘shiladi; tarix yozuvlari allaqachon identifikatorlarni o‘z ichiga oladi.

27. Xatti-harakat `channels.discord.replyToMode` orqali boshqariladi:

- 28. `off`: teglarni e’tiborsiz qoldirish.
- 29. `first`: faqat birinchi chiqish qismi/ilova javob bo‘ladi.
- 30. `all`: har bir chiqish qismi/ilova javob bo‘ladi.

31. Allowlist moslashtirish bo‘yicha eslatmalar:

- 32. `allowFrom`/`users`/`groupChannels` identifikatorlar, nomlar, teglar yoki `<@id>` kabi eslatmalarni qabul qiladi.
- 33. `discord:`/`user:` (foydalanuvchilar) va `channel:` (guruh DMlari) kabi prefikslar qo‘llab-quvvatlanadi.
- 34. Istalgan yuboruvchi/kanalga ruxsat berish uchun `*` dan foydalaning.
- 47. `guilds.<id>` bo‘lganda36. `.channels` mavjud bo‘lsa, ro‘yxatda ko‘rsatilmagan kanallar standart bo‘yicha rad etiladi.
- 37. `guilds.<id>`38. `.channels` o‘tkazib yuborilsa, allowlistga kiritilgan guilddagi barcha kanallarga ruxsat beriladi.
- 39. **Hech qanday kanalga ruxsat bermaslik** uchun `channels.discord.groupPolicy: "disabled"` qilib sozlang (yoki bo‘sh allowlistni qoldiring).
- 40. Sozlash ustasi `Guild/Channel` nomlarini (ommaviy + xususiy) qabul qiladi va imkon bo‘lsa ularni IDlarga moslashtiradi.
- 41. Ishga tushishda OpenClaw allowlistlardagi kanal/foydalanuvchi nomlarini IDlarga moslashtiradi (bot a’zolarni qidirishi mumkin bo‘lsa) va moslikni jurnalga yozadi; aniqlanmagan yozuvlar kiritilgandek saqlanadi.

42. Native buyruqlar bo‘yicha eslatmalar:

- 43. Ro‘yxatdan o‘tgan buyruqlar OpenClaw’ning chat buyruqlarini aks ettiradi.
- 44. Native buyruqlar DMlar/guild xabarlari bilan bir xil allowlistlarga amal qiladi (`channels.discord.dm.allowFrom`, `channels.discord.guilds`, kanal bo‘yicha qoidalar).
- 45. Slash buyruqlar Discord UI’da allowlistga kiritilmagan foydalanuvchilarga ham ko‘rinishi mumkin; OpenClaw bajarishda allowlistlarni majburan qo‘llaydi va “ruxsat berilmagan” deb javob beradi.

## 46. Asbob amallari

47. Agent `discord`ni quyidagi amallar bilan chaqirishi mumkin:

- 48. `react` / `reactions` (reaksiyalarni qo‘shish yoki ro‘yxatlash)
- 49. `sticker`, `poll`, `permissions`
- 50. `readMessages`, `sendMessage`, `editMessage`, `deleteMessage`
- Read/search/pin tool payloads include normalized `timestampMs` (UTC epoch ms) and `timestampUtc` alongside raw Discord `timestamp`.
- `threadCreate`, `threadList`, `threadReply`
- `pinMessage`, `unpinMessage`, `listPins`
- `searchMessages`, `memberInfo`, `roleInfo`, `roleAdd`, `roleRemove`, `emojiList`
- `channelInfo`, `channelList`, `voiceStatus`, `eventList`, `eventCreate`
- `timeout`, `kick`, `ban`
- `setPresence` (bot activity and online status)

Discord message ids are surfaced in the injected context (`[discord message id: …]` and history lines) so the agent can target them.
48. Emoji unicode bo‘lishi mumkin (masalan, `✅`) yoki `<:party_blob:1234567890>` kabi maxsus emoji sintaksisi.

## Safety & ops

- 49. Bot tokenini parol kabi saqlang; nazorat ostidagi xostlarda `DISCORD_BOT_TOKEN` muhit o‘zgaruvchisini afzal ko‘ring yoki konfiguratsiya fayli ruxsatlarini qat’iy cheklang.
- Only grant the bot permissions it needs (typically Read/Send Messages).
- 50. Agar bot tiqilib qolgan bo‘lsa yoki tezlik chekloviga uchragan bo‘lsa, Discord sessiyasiga boshqa jarayonlar egalik qilmayotganini tasdiqlagach, shlyuzni qayta ishga tushiring (`openclaw gateway --force`).
