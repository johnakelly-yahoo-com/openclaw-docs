---
summary: "Bridge protocol (legacy nodes): TCP JSONL, pairing, scoped RPC"
read_when:
  - Building or debugging node clients (iOS/Android/macOS node mode)
  - Investigating pairing or bridge auth failures
  - UI’lar ko‘rsatish uchun dekod qilishi kerak (iOS `BonjourEscapes.decode` dan foydalanadi).
title: "Bridge Protocol"
---

# Bridge protocol (legacy node transport)

The Bridge protocol is a **legacy** node transport (TCP JSONL). New node clients
should use the unified Gateway WebSocket protocol instead.

If you are building an operator or node client, use the
[Gateway protocol](/gateway/protocol).

**Note:** Current OpenClaw builds no longer ship the TCP bridge listener; this document is kept for historical reference.
Legacy `bridge.*` config keys are no longer part of the config schema.

## Why we have both

- **Security boundary**: the bridge exposes a small allowlist instead of the
  full gateway API surface.
- **Pairing + node identity**: node admission is owned by the gateway and tied
  to a per-node token.
- **Discovery UX**: nodes can discover gateways via Bonjour on LAN, or connect
  directly over a tailnet.
- **Loopback WS**: the full WS control plane stays local unless tunneled via SSH.

## Transport

- TCP, one JSON object per line (JSONL).
- Optional TLS (when `bridge.tls.enabled` is true).
- Legacy default listener port was `18790` (current builds do not start a TCP bridge).

When TLS is enabled, discovery TXT records include `bridgeTls=1` plus
`bridgeTlsSha256` so nodes can pin the certificate.

## Handshake + pairing

1. Gateway tomonidan ochilgan tugun yuzasini audit qilish
2. If not paired, gateway replies `error` (`NOT_PAIRED`/`UNAUTHORIZED`).
3. Client sends `pair-request`.
4. Gateway waits for approval, then sends `pair-ok` and `hello-ok`.

`hello-ok` returns `serverName` and may include `canvasHostUrl`.

## Frames

1. Mijoz → Shlyuz:

- 2. `req` / `res`: shlyuz doirasidagi RPC (chat, sessions, config, health, voicewake, skills.bins)
- 3. `event`: tugun signallari (ovoz transkripti, agent so‘rovi, chat obunasi, exec hayotiy sikli)

4. Shlyuz → Mijoz:

- 5. `invoke` / `invoke-res`: tugun buyruqlari (`canvas.*`, `camera.*`, `screen.record`,
     `location.get`, `sms.send`)
- 6. `event`: obuna qilingan sessiyalar uchun chat yangilanishlari
- 7. `ping` / `pong`: aloqani saqlab turish

8. Legacy ruxsat ro‘yxati (allowlist) majburiyati `src/gateway/server-bridge.ts` da edi (olib tashlangan).

## 9. Exec hayotiy sikli hodisalari

10. Tugunlar `exec.finished` yoki `exec.denied` hodisalarini chiqarib, system.run faoliyatini yuzaga chiqarishi mumkin.
11. Bular shlyuzda tizim hodisalariga xaritalanadi. 12. (Legacy tugunlar hali ham `exec.started` ni chiqarishi mumkin.)

13. Yuklama maydonlari (belgilanmaganlari ixtiyoriy):

- 14. `sessionKey` (majburiy): tizim hodisasini qabul qiladigan agent sessiyasi.
- 15. `runId`: guruhlash uchun yagona exec identifikatori.
- 16. `command`: xom yoki formatlangan buyruq satri.
- 17. `exitCode`, `timedOut`, `success`, `output`: yakunlash tafsilotlari (faqat finished).
- 18. `reason`: rad etish sababi (faqat denied).

## 19. Tailnet’dan foydalanish

- 20. Ko‘prikni tailnet IP ga bog‘lang: `bridge.bind: "tailnet"` bu yerda
      `~/.openclaw/openclaw.json`.
- 21. Mijozlar MagicDNS nomi yoki tailnet IP orqali ulanadi.
- 22. Bonjour tarmoqlarni **kesib o‘tmaydi**; kerak bo‘lganda qo‘lda host/port yoki keng hududli DNS‑SD dan foydalaning.

## 23. Versiyalash

24. Ko‘prik hozirda **implicit v1** (min/max kelishuvsiz). 25. Orqaga moslik
    kutiladi; har qanday buzuvchi o‘zgarishdan oldin ko‘prik protokoli versiyasi maydonini qo‘shing.
