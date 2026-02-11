---
summary: "Mattermost bot setup and OpenClaw config"
read_when:
  - Setting up Mattermost
  - Debugging Mattermost routing
title: "Mattermost"
---

# Mattermost (plugin)

Status: supported via plugin (bot token + WebSocket events). Channels, groups, and DMs are supported.
Mattermost is a self-hostable team messaging platform; see the official site at
[mattermost.com](https://mattermost.com) for product details and downloads.

## Plugin required

Mattermost ships as a plugin and is not bundled with the core install.

Install via CLI (npm registry):

```bash
openclaw plugins install @openclaw/mattermost
```

Local checkout (when running from a git repo):

```bash
openclaw plugins install ./extensions/mattermost
```

If you choose Mattermost during configure/onboarding and a git checkout is detected,
OpenClaw will offer the local install path automatically.

Details: [Plugins](/tools/plugin)

## Quick setup

1. Install the Mattermost plugin.
2. Create a Mattermost bot account and copy the **bot token**.
3. Copy the Mattermost **base URL** (e.g., `https://chat.example.com`).
4. Configure OpenClaw and start the gateway.

Minimal config:

```json5
{
  channels: {
    mattermost: {
      enabled: true,
      botToken: "mm-token",
      baseUrl: "https://chat.example.com",
      dmPolicy: "pairing",
    },
  },
}
```

## Environment variables (default account)

Set these on the gateway host if you prefer env vars:

- `MATTERMOST_BOT_TOKEN=...`
- `MATTERMOST_URL=https://chat.example.com`

Env vars apply only to the **default** account (`default`). Other accounts must use config values.

## Chat modes

Mattermost responds to DMs automatically. 1. Kanal xatti-harakati `chatmode` orqali boshqariladi:

- 2. `oncall` (standart): kanallarda faqat @mention qilinganda javob beradi.
- 3. `onmessage`: kanalga kelgan har bir xabarga javob beradi.
- 4. `onchar`: xabar trigger prefiksi bilan boshlanganida javob beradi.

5. Konfiguratsiya namunasi:

```json5
6. {
  channels: {
    mattermost: {
      chatmode: "onchar",
      oncharPrefixes: [">", "!"],
    },
  },
}
```

7. Eslatmalar:

- 8. `onchar` hali ham aniq @mentionlarga javob beradi.
- 9. `channels.mattermost.requireMention` eski konfiguratsiyalar uchun qo‘llab-quvvatlanadi, ammo `chatmode` afzal ko‘riladi.

## 10. Kirish nazorati (DMlar)

- 11. Standart: `channels.mattermost.dmPolicy = "pairing"` (noma’lum yuboruvchilar juftlash kodi oladi).
- 12. Tasdiqlash orqali:
  - 13. `openclaw pairing list mattermost`
  - 14. `openclaw pairing approve mattermost <CODE>`
- 15. Ochiq DMlar: `channels.mattermost.dmPolicy="open"` va `channels.mattermost.allowFrom=["*"]`.

## 16. Kanallar (guruhlar)

- 17. Standart: `channels.mattermost.groupPolicy = "allowlist"` (mention orqali cheklangan).
- 18. `channels.mattermost.groupAllowFrom` bilan ruxsat etilgan yuboruvchilar (foydalanuvchi IDlari yoki `@username`).
- 19. Ochiq kanallar: `channels.mattermost.groupPolicy="open"` (mention orqali cheklangan).

## 20. Chiqish (outbound) yetkazib berish uchun manzillar

21. `openclaw message send` yoki cron/webhooklar bilan quyidagi manzil formatlaridan foydalaning:

- 22. Kanal uchun `channel:<id>`
- 23. DM uchun `user:<id>`
- 24. DM uchun `@username` (Mattermost API orqali aniqlanadi)

25. Prefikssiz IDlar kanal sifatida qabul qilinadi.

## 26. Ko‘p akkauntli ishlash

27. Mattermost `channels.mattermost.accounts` ostida bir nechta akkauntni qo‘llab-quvvatlaydi:

```json5
28. {
  channels: {
    mattermost: {
      accounts: {
        default: { name: "Primary", botToken: "mm-token", baseUrl: "https://chat.example.com" },
        alerts: { name: "Alerts", botToken: "mm-token-2", baseUrl: "https://alerts.example.com" },
      },
    },
  },
}
```

## 29. Nosozliklarni bartaraf etish

- 30. Kanallarda javob yo‘q: bot kanalga qo‘shilganini va uni mention qilganingizni tekshiring (oncall), trigger prefiksidan foydalaning (onchar) yoki `chatmode: "onmessage"` ni o‘rnating.
- 31. Avtorizatsiya xatolari: bot tokeni, asosiy URL va akkaunt yoqilganligini tekshiring.
- Multi-account issues: env vars only apply to the `default` account.
