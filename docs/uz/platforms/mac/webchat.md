---
summary: "43. mac ilova gateway WebChat’ni qanday joylashtiradi va uni qanday debug qilish mumkin"
read_when:
  - 44. mac WebChat ko‘rinishini yoki loopback portni debug qilish
title: "45. WebChat"
---

# 46. WebChat (macOS ilovasi)

47. macOS menyu-panel ilovasi WebChat UI’ni native SwiftUI view sifatida joylashtiradi. 48. U Gateway’ga ulanadi va tanlangan agent uchun **asosiy sessiya**ga sukut bo‘yicha ulanadi (boshqa sessiyalar uchun sessiya almashtirgichi bilan).

- 49. **Lokal rejim**: to‘g‘ridan-to‘g‘ri lokal Gateway WebSocket’iga ulanadi.
- 50. **Masofaviy rejim**: Gateway boshqaruv portini SSH orqali yo‘naltiradi va shu tunnelni ma’lumotlar tekisligi sifatida ishlatadi.

## Ishga tushirish va nosozliklarni tuzatish

- Qo‘llanma: Lobster menyusi → “Chatni ochish”.

- Sinov uchun avtomatik ochish:

  ```bash
  dist/OpenClaw.app/Contents/MacOS/OpenClaw --webchat
  ```

- Loglar: `./scripts/clawlog.sh` (subsystem `bot.molt`, category `WebChatSwiftUI`).

## Qanday ulangan

- Ma’lumotlar tekisligi: Gateway WS usullari `chat.history`, `chat.send`, `chat.abort`,
  `chat.inject` va hodisalar `chat`, `agent`, `presence`, `tick`, `health`.
- Sessiya: sukut bo‘yicha asosiy sessiya (`main`, yoki scope global bo‘lsa `global`). UI sessiyalar o‘rtasida almasha oladi.
- Onboarding birinchi ishga tushirish sozlamalarini alohida saqlash uchun maxsus sessiyadan foydalanadi.

## Xavfsizlik yuzasi

- Masofaviy rejim SSH orqali faqat Gateway WebSocket boshqaruv portini uzatadi.

## Ma’lum cheklovlar

- UI chat sessiyalari uchun optimallashtirilgan (to‘liq brauzer sandbox emas).
