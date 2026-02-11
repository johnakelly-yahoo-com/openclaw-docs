---
summary: "Tashqi CLI’lar (signal-cli, legacy imsg) uchun RPC adapterlar va gateway naqshlari"
read_when:
  - Tashqi CLI integratsiyalarini qo‘shish yoki o‘zgartirish
  - RPC adapterlarini sozlash (signal-cli, imsg)
title: "RPC Adapterlar"
---

# RPC adapterlar

OpenClaw tashqi CLI’larni JSON-RPC orqali integratsiya qiladi. Hozirda ikki naqsh qo‘llaniladi.

## Naqsh A: HTTP demon (signal-cli)

- `signal-cli` JSON-RPC’ni HTTP orqali taqdim etuvchi demon sifatida ishlaydi.
- Hodisa oqimi SSE (`/api/v1/events`).
- Sog‘liqni tekshirish: `/api/v1/check`.
- `channels.signal.autoStart=true` bo‘lganda hayotiy sikl OpenClaw tomonidan boshqariladi.

Sozlash va endpointlar uchun [Signal](/channels/signal) ga qarang.

## Naqsh B: stdio farzand jarayon (legacy: imsg)

> **Eslatma:** Yangi iMessage sozlamalari uchun buning o‘rniga [BlueBubbles](/channels/bluebubbles) dan foydalaning.

- OpenClaw `imsg rpc` ni farzand jarayon sifatida ishga tushiradi (legacy iMessage integratsiyasi).
- JSON-RPC stdin/stdout orqali satrlar bo‘yicha uzatiladi (har bir satrda bitta JSON obyekt).
- TCP port yo‘q, demon talab qilinmaydi.

Ishlatiladigan asosiy metodlar:

- `watch.subscribe` → notifications (`method: "message"`)
- `watch.unsubscribe`
- `send`
- `chats.list` (probe/diagnostics)

See [iMessage](/channels/imessage) for legacy setup and addressing (`chat_id` preferred).

## Adapter guidelines

- Gateway owns the process (start/stop tied to provider lifecycle).
- Keep RPC clients resilient: timeouts, restart on exit.
- Prefer stable IDs (e.g., `chat_id`) over display strings.
