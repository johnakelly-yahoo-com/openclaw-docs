---
summary: "Global voice wake words (Gateway-owned) and how they sync across nodes"
read_when:
  - Changing voice wake words behavior or defaults
  - Adding new node platforms that need wake word sync
title: "Voice Wake"
---

# Voice Wake (Global Wake Words)

OpenClaw treats **wake words as a single global list** owned by the **Gateway**.

- There are **no per-node custom wake words**.
- **Any node/app UI may edit** the list; changes are persisted by the Gateway and broadcast to everyone.
- Each device still keeps its own **Voice Wake enabled/disabled** toggle (local UX + permissions differ).

## Storage (Gateway host)

Wake words are stored on the gateway machine at:

- `~/.openclaw/settings/voicewake.json`

Shape:

```json
{ "triggers": ["openclaw", "claude", "computer"], "updatedAtMs": 1730000000000 }
```

## Protocol

### Methods

- `voicewake.get` → `{ triggers: string[] }`
- `voicewake.set` with params `{ triggers: string[] }` → `{ triggers: string[] }`

Notes:

- Triggers are normalized (trimmed, empties dropped). Bo‘sh ro‘yxatlar sukut bo‘yicha qiymatlarga qaytadi.
- Xavfsizlik uchun cheklovlar qo‘llaniladi (son/uzunlik limitlari).

### Hodisalar

- `voicewake.changed` payload `{ triggers: string[] }`

Kimlar qabul qiladi:

- Barcha WebSocket mijozlari (macOS ilovasi, WebChat va boshqalar)
- Barcha ulangan tugunlar (iOS/Android), shuningdek tugun ulanganda boshlang‘ich “joriy holat” sifatida ham yuboriladi.

## Mijoz xulqi

### macOS app

- Global ro‘yxatdan `VoiceWakeRuntime` triggerlarini boshqarish uchun foydalanadi.
- Voice Wake sozlamalarida “Trigger words”ni tahrirlash `voicewake.set`ni chaqiradi va boshqa mijozlarni sinxron holatda ushlab turish uchun translyatsiyaga tayanadi.

### iOS tuguni

- `VoiceWakeManager` triggerlarini aniqlash uchun global ro‘yxatdan foydalanadi.
- Editing Wake Words in Settings calls `voicewake.set` (over the Gateway WS) and also keeps local wake-word detection responsive.

### Android tuguni

- Exposes a Wake Words editor in Settings.
- Tahrirlar hamma joyda sinxron bo‘lishi uchun Gateway WS orqali `voicewake.set`ni chaqiradi.
