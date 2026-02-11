---
summary: "`openclaw voicecall` uchun CLI ma’lumotnomasi (voice-call plagin buyruqlari yuzasi)"
read_when:
  - "`voicecall call|continue|status|tail|expose` uchun tezkor misollarni xohlaysiz"
  - "Voice-call plagini: [Voice Call](/plugins/voice-call)"
title: "voicecall"
---

# `openclaw voicecall`

`voicecall` — plagin tomonidan taqdim etilgan buyruq. U faqat voice-call plagini o‘rnatilgan va yoqilgan bo‘lsa ko‘rinadi.

Asosiy hujjat:

- Umumiy buyruqlar

## webhooks

```bash
openclaw voicecall status --call-id <id>
openclaw voicecall call --to "+15555550123" --message "Hello" --mode notify
openclaw voicecall continue --call-id <id> --message "Any questions?"
openclaw voicecall end --call-id <id>
```

## Webhooklarni ochish (Tailscale)

```bash
openclaw voicecall expose --mode serve
openclaw voicecall expose --mode funnel
openclaw voicecall unexpose
```

Xavfsizlik eslatmasi: webhook endpointini faqat ishonchli tarmoqlarga oching. Imkon bo‘lsa Funnel o‘rniga Tailscale Serve’dan foydalaning.
