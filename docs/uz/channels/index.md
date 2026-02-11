---
summary: "Messaging platforms OpenClaw can connect to"
read_when:
  - You want to choose a chat channel for OpenClaw
  - You need a quick overview of supported messaging platforms
title: "Chat Channels"
---

# Chat Channels

OpenClaw can talk to you on any chat app you already use. Each channel connects via the Gateway.
Text is supported everywhere; media and reactions vary by channel.

## Supported channels

- [WhatsApp](/channels/whatsapp) — Most popular; uses Baileys and requires QR pairing.
- [Telegram](/channels/telegram) — Bot API via grammY; supports groups.
- [Discord](/channels/discord) — Discord Bot API + Gateway; supports servers, channels, and DMs.
- [Slack](/channels/slack) — Bolt SDK; workspace apps.
- [Feishu](/channels/feishu) — Feishu/Lark bot via WebSocket (plugin, installed separately).
- [Google Chat](/channels/googlechat) — Google Chat API app via HTTP webhook.
- [Mattermost](/channels/mattermost) — Bot API + WebSocket; channels, groups, DMs (plugin, installed separately).
- [Signal](/channels/signal) — signal-cli; privacy-focused.
- [BlueBubbles](/channels/bluebubbles) — **Recommended for iMessage**; uses the BlueBubbles macOS server REST API with full feature support (edit, unsend, effects, reactions, group management — edit currently broken on macOS 26 Tahoe).
- [iMessage (legacy)](/channels/imessage) — Legacy macOS integration via imsg CLI (deprecated, use BlueBubbles for new setups).
- [Microsoft Teams](/channels/msteams) — Bot Framework; enterprise support (plugin, installed separately).
- 1. [LINE](/channels/line) — LINE Messaging API boti (plagin, alohida o‘rnatiladi).
- 2. [Nextcloud Talk](/channels/nextcloud-talk) — Nextcloud Talk orqali o‘z serveringizda joylashtirilgan chat (plagin, alohida o‘rnatiladi).
- 3. [Matrix](/channels/matrix) — Matrix protokoli (plagin, alohida o‘rnatiladi).
- 4. [Nostr](/channels/nostr) — NIP-04 orqali markazlashmagan shaxsiy xabarlar (plagin, alohida o‘rnatiladi).
- 5. [Tlon](/channels/tlon) — Urbit asosidagi messenjer (plagin, alohida o‘rnatiladi).
- 6. [Twitch](/channels/twitch) — IRC ulanishi orqali Twitch chati (plagin, alohida o‘rnatiladi).
- 7. [Zalo](/channels/zalo) — Zalo Bot API; Vetnamda mashhur messenjer (plagin, alohida o‘rnatiladi).
- 8. [Zalo Personal](/channels/zalouser) — QR orqali kirish bilan Zalo shaxsiy akkaunti (plagin, alohida o‘rnatiladi).
- 9. [WebChat](/web/webchat) — WebSocket orqali Gateway WebChat UI.

## 10. Eslatmalar

- 11. Kanallar bir vaqtning o‘zida ishlashi mumkin; bir nechta kanalni sozlang va OpenClaw har bir chat bo‘yicha yo‘naltiradi.
- 12. Eng tez sozlash odatda **Telegram** (oddiy bot tokeni). 13. WhatsApp QR orqali juftlashni talab qiladi va
      diskda ko‘proq holat ma’lumotlarini saqlaydi.
- 14. Guruh xatti-harakati kanalga qarab farq qiladi; [Groups](/channels/groups) bo‘limiga qarang.
- 15. Xavfsizlik uchun DM juftlash va ruxsat ro‘yxatlari qo‘llaniladi; [Security](/gateway/security) bo‘limiga qarang.
- 16. Telegram ichki mexanizmlari: [grammY notes](/channels/grammy).
- 17. Nosozliklarni bartaraf etish: [Channel troubleshooting](/channels/troubleshooting).
- 18. Model provayderlari alohida hujjatlashtirilgan; [Model Providers](/providers/models) bo‘limiga qarang.
