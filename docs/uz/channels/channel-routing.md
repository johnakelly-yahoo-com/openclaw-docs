---
summary: "Har bir kanal uchun yo‘naltirish qoidalari (WhatsApp, Telegram, Discord, Slack) va umumiy kontekst"
read_when:
  - Kanal yo‘naltirishini yoki inbox xatti-harakatini o‘zgartirish
title: "Kanal yo‘naltirishi"
---

# Kanallar va yo‘naltirish

OpenClaw javoblarni **xabar kelgan kanalning o‘ziga qaytaradi**. Model kanalni tanlamaydi; yo‘naltirish deterministik bo‘lib, xost konfiguratsiyasi tomonidan boshqariladi.

## Asosiy atamalar

- **Kanal**: `whatsapp`, `telegram`, `discord`, `slack`, `signal`, `imessage`, `webchat`.
- **AccountId**: kanal bo‘yicha akkaunt instansiyasi (mavjud bo‘lsa).
- **AgentId**: ajratilgan ish maydoni + sessiyalar ombori (“miya”).
- **SessionKey**: kontekstni saqlash va parallellikni boshqarish uchun ishlatiladigan kalit.

## Sessiya kaliti shakllari (misollar)

To‘g‘ridan-to‘g‘ri xabarlar agentning **asosiy** sessiyasiga birlashtiriladi:

- `agent:<agentId>:<mainKey>` (standart: `agent:main:main`)

Guruhlar va kanallar kanal bo‘yicha alohida izolyatsiya qilinadi:

- Guruhlar: `agent:<agentId>:<channel>:group:<id>`
- Kanallar/xonalar: `agent:<agentId>:<channel>:channel:<id>`

Threadlar:

- Slack/Discord threadlari asosiy kalitga `:thread:<threadId>` ni qo‘shadi.
- Telegram forum mavzulari guruh kalitiga `:topic:<topicId>` ni joylaydi.

Misollar:

- `agent:main:telegram:group:-1001234567890:topic:42`
- `agent:main:discord:channel:123456:thread:987654`

## Yo‘naltirish qoidalari (agent qanday tanlanadi)

Yo‘naltirish har bir kiruvchi xabar uchun **bitta agentni** tanlaydi:

1. **Aniq peer mosligi** (`peer.kind` + `peer.id` bilan `bindings`).
2. **Guild mosligi** (Discord) `guildId` orqali.
3. **Team mosligi** (Slack) `teamId` orqali.
4. **Account mosligi** (kanaldagi `accountId`).
5. **Kanal mosligi** (ushbu kanaldagi istalgan akkaunt).
6. **Standart agent** (`agents.list[].default`, aks holda ro‘yxatdagi birinchi element, zaxira sifatida `main`).

Mos kelgan agent qaysi ish maydoni va sessiya ombori ishlatilishini belgilaydi.

## Broadcast guruhlar (bir nechta agentlarni ishga tushirish)

Broadcast guruhlar OpenClaw odatda javob beradigan holatlarda **bir xil peer uchun bir nechta agentlarni** ishga tushirishga imkon beradi (masalan: WhatsApp guruhlarida, eslatma/faollashtirishdan keyin).

Konfiguratsiya:

```json5
{
  broadcast: {
    strategy: "parallel",
    "120363403215116621@g.us": ["alfred", "baerbel"],
    "+15555550123": ["support", "logger"],
  },
}
```

Qarang: [Broadcast Groups](/channels/broadcast-groups).

## Konfiguratsiya umumiy ko‘rinishi

- `agents.list`: nomlangan agent ta’riflari (ish maydoni, model va h.k.).
- `bindings`: kiruvchi kanallar/akkauntlar/peerlarni agentlarga moslash xaritasi.

Misol:

```json5
{
  agents: {
    list: [{ id: "support", name: "Support", workspace: "~/.openclaw/workspace-support" }],
  },
  bindings: [
    { match: { channel: "slack", teamId: "T123" }, agentId: "support" },
    { match: { channel: "telegram", peer: { kind: "group", id: "-100123" } }, agentId: "support" },
  ],
}
```

## Sessiya saqlash

Sessiya omborlari holat katalogi ostida joylashadi (standart `~/.openclaw`):

- `~/.openclaw/agents/<agentId>/sessions/sessions.json`
- JSONL transkriptlari ombor bilan yonma-yon joylashadi

`session.store` va `{agentId}` shablonlash orqali ombor yo‘lini o‘zgartirishingiz mumkin.

## WebChat xatti-harakati

WebChat attaches to the **selected agent** and defaults to the agent’s main
session. Because of this, WebChat lets you see cross‑channel context for that
agent in one place.

## Reply context

Inbound replies include:

- `ReplyToId`, `ReplyToBody`, and `ReplyToSender` when available.
- Quoted context is appended to `Body` as a `[Replying to ...]` block.

This is consistent across channels.
