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
   - Or config: `channels.zalo.botToken: "..."`.
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

3. Restart the gateway. Zalo starts when a token is resolved (env or config).
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

- Default: `channels.zalo.dmPolicy = "pairing"`. Unknown senders receive a pairing code; messages are ignored until approved (codes expire after 1 hour).
- Approve via:
  - `openclaw pairing list zalo`
  - `openclaw pairing approve zalo <CODE>`
- Pairing is the default token exchange. Details: [Pairing](/channels/pairing)
- `channels.zalo.allowFrom` accepts numeric user IDs (no username lookup available).

## Long-polling vs webhook

- 1. Standart: long-polling (ommaviy URL talab qilinmaydi).
- 2. Webhook rejimi: `channels.zalo.webhookUrl` va `channels.zalo.webhookSecret` ni sozlang.
  - 3. Webhook maxfiy kaliti 8–256 ta belgidan iborat bo‘lishi kerak.
  - 4. Webhook URL HTTPS dan foydalanishi shart.
  - 5. Zalo tekshirish uchun hodisalarni `X-Bot-Api-Secret-Token` sarlavhasi bilan yuboradi.
  - 6. Gateway HTTP webhook so‘rovlarini `channels.zalo.webhookPath` da qabul qiladi (standart holatda webhook URL yo‘liga teng).

7. **Eslatma:** Zalo API hujjatlariga ko‘ra getUpdates (polling) va webhook bir vaqtning o‘zida ishlamaydi.

## 8. Qo‘llab-quvvatlanadigan xabar turlari

- 9. **Matnli xabarlar**: 2000 belgilik bo‘laklash bilan to‘liq qo‘llab-quvvatlanadi.
- 10. **Rasm xabarlari**: Kiruvchi rasmlarni yuklab olish va qayta ishlash; rasmlarni `sendPhoto` orqali yuborish.
- 11. **Stikerlar**: Qayd etiladi, ammo to‘liq qayta ishlanmaydi (agent javobi yo‘q).
- 12. **Qo‘llab-quvvatlanmaydigan turlar**: Qayd etiladi (masalan, himoyalangan foydalanuvchilardan kelgan xabarlar).

## 13. Imkoniyatlar

| 14. Funksiya                              | 15. Holat                                                    |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 16. Shaxsiy xabarlar                      | 17. ✅ Qo‘llab-quvvatlanadi                                   |
| 18. Guruhlar                              | 19. ❌ Tez orada (Zalo hujjatlariga ko‘ra) |
| 20. Media (rasmlar)    | 21. ✅ Qo‘llab-quvvatlanadi                                   |
| 22. Reaksiyalar                           | 23. ❌ Qo‘llab-quvvatlanmaydi                                 |
| 24. Mavzular (threads) | 25. ❌ Qo‘llab-quvvatlanmaydi                                 |
| 26. So‘rovnomalar                         | 27. ❌ Qo‘llab-quvvatlanmaydi                                 |
| 28. Mahalliy buyruqlar                    | 29. ❌ Qo‘llab-quvvatlanmaydi                                 |
| 30. Oqimli uzatish                        | 31. ⚠️ Bloklangan (2000 belgi cheklovi)   |

## 32. Yetkazib berish maqsadlari (CLI/cron)

- 33. Maqsad sifatida chat ID dan foydalaning.
- 34. Misol: `openclaw message send --channel zalo --target 123456789 --message "hi"`.

## 35. Nosozliklarni bartaraf etish

36. **Bot javob bermayapti:**

- 37. Token yaroqli ekanligini tekshiring: `openclaw channels status --probe`
- 38. Yuboruvchi tasdiqlanganligini tekshiring (juftlash yoki allowFrom)
- 39. Gateway loglarini tekshiring: `openclaw logs --follow`

40. **Webhook hodisalarni qabul qilmayapti:**

- 41. Webhook URL HTTPS dan foydalanayotganini ta’minlang
- 42. Maxfiy token 8–256 belgidan iborat ekanligini tekshiring
- 43. Sozlangan yo‘lda gateway HTTP endpointi mavjudligini tasdiqlang
- 44. getUpdates polling ishlamayotganini tekshiring (ular o‘zaro mos kelmaydi)

## 45. Konfiguratsiya ma’lumotnomasi (Zalo)

46. To‘liq konfiguratsiya: [Configuration](/gateway/configuration)

47. Provayder parametrlari:

- 48. `channels.zalo.enabled`: kanal ishga tushishini yoqish/o‘chirish.
- 49. `channels.zalo.botToken`: Zalo Bot Platformasidan olingan bot tokeni.
- 50. `channels.zalo.tokenFile`: tokenni fayl yo‘lidan o‘qish.
- `channels.zalo.dmPolicy`: `pairing | allowlist | open | disabled` (default: pairing).
- `channels.zalo.allowFrom`: DM ruxsatlar ro‘yxati (foydalanuvchi ID’lari). `open` uchun `"*"` talab qilinadi. Usta (wizard) raqamli ID’larni so‘raydi.
- `channels.zalo.mediaMaxMb`: kiruvchi/chiquvchi media cheklovi (MB, standart 5).
- `channels.zalo.webhookUrl`: webhook rejimini yoqish (HTTPS talab qilinadi).
- `channels.zalo.webhookSecret`: webhook maxfiy kaliti (8–256 belgi).
- `channels.zalo.webhookPath`: gateway HTTP serveridagi webhook yo‘li.
- `channels.zalo.proxy`: API so‘rovlari uchun proxy URL.

Ko‘p akkauntli sozlamalar:

- `channels.zalo.accounts.<id>.botToken`: har bir akkaunt uchun token.
- `channels.zalo.accounts.<id>.tokenFile`: har bir akkaunt uchun token fayli.
- `channels.zalo.accounts.<id>.name`: ko‘rinadigan nom.
- `channels.zalo.accounts.<id>.enabled`: akkauntni yoqish/o‘chirish.
- `channels.zalo.accounts.<id>.dmPolicy`: har bir akkaunt uchun DM siyosati.
- `channels.zalo.accounts.<id>.allowFrom`: har bir akkaunt uchun ruxsatlar ro‘yxati.
- `channels.zalo.accounts.<id>.webhookUrl`: har bir akkaunt uchun webhook URL.
- `channels.zalo.accounts.<id>.webhookSecret`: har bir akkaunt uchun webhook maxfiy kaliti.
- `channels.zalo.accounts.<id>.webhookPath`: har bir akkaunt uchun webhook yo‘li.
- `channels.zalo.accounts.<id>.proxy`: har bir akkaunt uchun proxy URL.
