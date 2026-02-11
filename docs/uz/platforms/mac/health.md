---
summary: "How the macOS app reports gateway/Baileys health states"
read_when:
  - Debugging mac app health indicators
title: "Health Checks"
---

# Health Checks on macOS

How to see whether the linked channel is healthy from the menu bar app.

## Menu bar

- Status dot now reflects Baileys health:
  - Green: linked + socket opened recently.
  - Orange: connecting/retrying.
  - Red: logged out or probe failed.
- Secondary line reads "linked · auth 12m" or shows the failure reason.
- "Run Health Check" menu item triggers an on-demand probe.

## Settings

- 1. Umumiy (General) yorlig‘ida quyidagilarni ko‘rsatadigan Health kartasi paydo bo‘ladi: bog‘langan autentifikatsiya yoshi, session-store yo‘li/soni, oxirgi tekshiruv vaqti, oxirgi xato/holat kodi hamda Run Health Check / Reveal Logs tugmalari.
- 2. UI darhol yuklanishi uchun keshlangan snapshotdan foydalanadi va oflayn bo‘lganda muloyim tarzda fallback qiladi.
- 3. **Channels yorlig‘i** WhatsApp/Telegram uchun kanal holati va boshqaruvlarini ko‘rsatadi (login QR, logout, probe, oxirgi uzilish/xato).

## 4. Probe qanday ishlaydi

- 5. Ilova har ~60 soniyada va talab bo‘yicha `ShellExecutor` orqali `openclaw health --json` ni ishga tushiradi. 6. Probe credentiallarni yuklaydi va xabar yubormasdan holatni hisobot qiladi.
- 7. Miltillashni oldini olish uchun oxirgi yaxshi snapshot va oxirgi xatoni alohida keshlang; har birining vaqt tamg‘asini ko‘rsating.

## 8. Ikki yo‘l qolsa

- 9. Siz hali ham [Gateway health](/gateway/health) dagi CLI oqimidan (`openclaw status`, `openclaw status --deep`, `openclaw health --json`) foydalanishingiz va `web-heartbeat` / `web-reconnect` uchun `/tmp/openclaw/openclaw-*.log` ni tail qilishingiz mumkin.
