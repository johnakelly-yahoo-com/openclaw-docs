---
summary: "PeekabooBridge integration for macOS UI automation"
read_when:
  - Hosting PeekabooBridge in OpenClaw.app
  - Integrating Peekaboo via Swift Package Manager
  - Changing PeekabooBridge protocol/paths
title: "Peekaboo Bridge"
---

# Peekaboo Bridge (macOS UI automation)

OpenClaw can host **PeekabooBridge** as a local, permission‑aware UI automation
broker. This lets the `peekaboo` CLI drive UI automation while reusing the
macOS app’s TCC permissions.

## What this is (and isn’t)

- **Host**: OpenClaw.app can act as a PeekabooBridge host.
- **Client**: use the `peekaboo` CLI (no separate `openclaw ui ...` surface).
- **UI**: visual overlays stay in Peekaboo.app; OpenClaw is a thin broker host.

## Enable the bridge

In the macOS app:

- Settings → **Enable Peekaboo Bridge**

When enabled, OpenClaw starts a local UNIX socket server. If disabled, the host
is stopped and `peekaboo` will fall back to other available hosts.

## Client discovery order

Peekaboo clients typically try hosts in this order:

1. Peekaboo.app (full UX)
2. Claude.app (if installed)
3. OpenClaw.app (thin broker)

Use `peekaboo bridge status --verbose` to see which host is active and which
socket path is in use. You can override with:

```bash
export PEEKABOO_BRIDGE_SOCKET=/path/to/bridge.sock
```

## Security & permissions

- The bridge validates **caller code signatures**; an allowlist of TeamIDs is
  enforced (Peekaboo host TeamID + OpenClaw app TeamID).
- So‘rovlar taxminan ~10 soniyadan so‘ng vaqt tugashi bilan yakunlanadi.
- Agar zarur ruxsatlar yetishmasa, ko‘prik System Settings’ni ishga tushirish o‘rniga aniq xato xabarini qaytaradi.

## Snapshot xatti-harakati (avtomatlashtirish)

Snapshotlar xotirada saqlanadi va qisqa muddatdan so‘ng avtomatik ravishda muddati tugaydi.
Agar uzoqroq saqlash kerak bo‘lsa, mijoz tomondan qayta snapshot oling.

## Muammolarni bartaraf etish

- Agar `peekaboo` “bridge client is not authorized” deb xabar bersa, mijoz to‘g‘ri imzolanganini tekshiring yoki xostni faqat **debug** rejimida `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` bilan ishga tushiring.
- Agar hech qanday xost topilmasa, xost ilovalardan birini (Peekaboo.app yoki OpenClaw.app) oching va ruxsatlar berilganini tasdiqlang.
