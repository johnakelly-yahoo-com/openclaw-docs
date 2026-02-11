---
summary: "OpenClaw ilovasi, gateway node transporti va PeekabooBridge uchun macOS IPC arxitekturasi"
read_when:
  - IPC kontraktlari yoki menyu paneli ilovasi IPCsini tahrirlash
title: "macOS IPC"
---

# OpenClaw macOS IPC arxitekturasi

**Joriy model:** lokal Unix soketi **node host xizmati**ni **macOS ilovasi** bilan exec ruxsatlari va `system.run` uchun bog‘laydi. Kashf etish/ulanish tekshiruvlari uchun `openclaw-mac` debug CLI mavjud; agent amallari hanuz Gateway WebSocket va `node.invoke` orqali oqadi. UI avtomatlashtirish PeekabooBridge’dan foydalanadi.

## Maqsadlar

- TCC bilan bog‘liq barcha ishlarni (bildirishnomalar, ekran yozuvi, mikrofon, nutq, AppleScript) bajaradigan yagona GUI ilova instansiyasi.
- Avtomatlashtirish uchun kichik yuzasi: Gateway + node buyruqlari, hamda UI avtomatlashtirish uchun PeekabooBridge.
- Oldindan aytib bo‘ladigan ruxsatlar: har doim bir xil imzolangan bundle ID, launchd tomonidan ishga tushiriladi, shuning uchun TCC ruxsatlari saqlanib qoladi.

## Qanday ishlaydi

### Gateway + node transport

- The app runs the Gateway (local mode) and connects to it as a node.
- Agent amallari `node.invoke` orqali bajariladi (masalan, `system.run`, `system.notify`, `canvas.*`).

### Node xizmati + ilova IPC

- Headless node host xizmati Gateway WebSocket’iga ulanadi.
- `system.run` so‘rovlari lokal Unix soketi orqali macOS ilovasiga uzatiladi.
- Ilova exec’ni UI kontekstida bajaradi, kerak bo‘lsa so‘raydi va natijani qaytaradi.

Diagramma (SCI):

```
Agent -> Gateway -> Node Service (WS)
                      |  IPC (UDS + token + HMAC + TTL)
                      v
                  Mac App (UI + TCC + system.run)
```

### PeekabooBridge (UI avtomatlashtirish)

- UI avtomatlashtirish `bridge.sock` nomli alohida UNIX soketi va PeekabooBridge JSON protokolidan foydalanadi.
- Xost afzallik tartibi (klient tomoni): Peekaboo.app → Claude.app → OpenClaw.app → lokal bajarish.
- Xavfsizlik: bridge xostlari ruxsat etilgan TeamID’ni talab qiladi; DEBUG-only bir xil UID uchun chetlab o‘tish `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` bilan himoyalangan (Peekaboo an’anasi).
- Batafsil ma’lumot uchun qarang: [PeekabooBridge usage](/platforms/mac/peekaboo).

## Operatsion oqimlar

- Qayta ishga tushirish/qayta yig‘ish: `SIGN_IDENTITY="Apple Development: <Developer Name> (<TEAMID>)" scripts/restart-mac.sh`
  - Mavjud instansiyalarni to‘xtatadi
  - Swift build + paketlash
  - LaunchAgent’ni yozadi/bootstraps/kickstart qiladi
- Yagona instansiya: agar xuddi shu bundle ID bilan boshqa instansiya ishlayotgan bo‘lsa, ilova erta chiqadi.

## Mustahkamlash eslatmalari

- Barcha imtiyozli yuzalar uchun TeamID mosligini talab qilishni afzal ko‘ring.
- PeekabooBridge: `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` (faqat DEBUG) lokal ishlab chiqish uchun bir xil UID’dagi chaqiruvchilarga ruxsat berishi mumkin.
- Barcha aloqa faqat lokal bo‘lib qoladi; hech qanday tarmoq soketlari ochilmaydi.
- TCC so‘rovlari faqat GUI ilova bundle’idan kelib chiqishi kerak; qayta build qilishlar orasida imzolangan bundle ID’ni barqaror saqlang.
- IPC mustahkamlash: soket rejimi `0600`, token, peer‑UID tekshiruvlari, HMAC chaqiruv/javob, qisqa TTL.
