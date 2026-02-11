---
summary: "33. Chiquvchi provayder chaqiruvlari uchun qayta urinish siyosati"
read_when:
  - 34. Provayderning qayta urinish xatti-harakatini yoki standartlarini yangilash
  - 35. Provayder yuborish xatolari yoki tezlik cheklovlarini nosozlikdan chiqarish
title: "36. Qayta urinish siyosati"
---

# 37. Qayta urinish siyosati

## 38. Maqsadlar

- 39. Har bir HTTP so‘rovi bo‘yicha qayta urinish, ko‘p bosqichli oqim bo‘yicha emas.
- 40. Faqat joriy bosqichni qayta urinib, tartibni saqlash.
- 41. Idempotent bo‘lmagan amallarni takrorlab yuborishdan qochish.

## 42. Standartlar

- 43. Urinishlar: 3
- 44. Maksimal kechikish chegarasi: 30000 ms
- 45. Jitter: 0.1 (10 foiz)
- 46. Provayder standartlari:
  - 47. Telegram minimal kechikish: 400 ms
  - 48. Discord minimal kechikish: 500 ms

## 49. Xatti-harakat

### 50. Discord

- Retries only on rate-limit errors (HTTP 429).
- Uses Discord `retry_after` when available, otherwise exponential backoff.

### Telegram

- Retries on transient errors (429, timeout, connect/reset/closed, temporarily unavailable).
- Uses `retry_after` when available, otherwise exponential backoff.
- Markdown parse errors are not retried; they fall back to plain text.

## Configuration

Set retry policy per provider in `~/.openclaw/openclaw.json`:

```json5
{
  channels: {
    telegram: {
      retry: {
        attempts: 3,
        minDelayMs: 400,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
    discord: {
      retry: {
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}
```

## Notes

- Retries apply per request (message send, media upload, reaction, poll, sticker).
- Composite flows do not retry completed steps.
