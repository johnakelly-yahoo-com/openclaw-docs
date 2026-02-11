---
summary: "35. Kiruvchi kanal joylashuvini tahlil qilish (Telegram + WhatsApp) va kontekst maydonlari"
read_when:
  - 36. Kanal joylashuvini tahlil qilishni qo‘shish yoki o‘zgartirish
  - 37. Agent promptlari yoki vositalarida joylashuv kontekst maydonlaridan foydalanish
title: "38. Kanal joylashuvini tahlil qilish"
---

# 39. Kanal joylashuvini tahlil qilish

40. OpenClaw chat kanallaridan ulashilgan joylashuvlarni quyidagilarga normallashtiradi:

- 41. kiruvchi matn oxiriga qo‘shilgan o‘qilishi oson matn, va
- 42. avtomatik javob kontekst yuklamasidagi tuzilgan maydonlar.

43. Hozirda qo‘llab-quvvatlanadi:

- 44. **Telegram** (joylashuv pinlari + maskanlar + jonli joylashuvlar)
- 45. **WhatsApp** (locationMessage + liveLocationMessage)
- 46. **Matrix** (`m.location` bilan `geo_uri`)

## 47. Matnni formatlash

48. Joylashuvlar qavslarsiz, qulay satrlar ko‘rinishida chiqariladi:

- 49. Pin:
  - 50. `📍 48.858844, 2.294351 ±12m`
- 1. Nomlangan joy:
  - 2. `📍 Eiffel Tower — Champ de Mars, Paris (48.858844, 2.294351 ±12m)`
- 3. Jonli ulashish:
  - 4. `🛰 Jonli joylashuv: 48.858844, 2.294351 ±12m`

5. Agar kanalga sarlavha/izoh qo‘shilgan bo‘lsa, u keyingi qatorda qo‘shiladi:

```
6. 📍 48.858844, 2.294351 ±12m
Bu yerda uchrashaylik
```

## 7. Kontekst maydonlari

8. Joylashuv mavjud bo‘lsa, ushbu maydonlar `ctx` ga qo‘shiladi:

- 9. `LocationLat` (raqam)
- 10. `LocationLon` (raqam)
- 11. `LocationAccuracy` (raqam, metr; ixtiyoriy)
- 12. `LocationName` (satr; ixtiyoriy)
- 13. `LocationAddress` (satr; ixtiyoriy)
- 14. `LocationSource` (`pin | place | live`)
- 15. `LocationIsLive` (boolean)

## 16. Kanal eslatmalari

- 17. **Telegram**: joylar `LocationName/LocationAddress` ga mos keladi; jonli joylashuvlar `live_period` dan foydalanadi.
- 18. **WhatsApp**: `locationMessage.comment` va `liveLocationMessage.caption` sarlavha qatori sifatida qo‘shiladi.
- 19. **Matrix**: `geo_uri` pin joylashuv sifatida tahlil qilinadi; balandlik e’tiborga olinmaydi va `LocationIsLive` har doim false bo‘ladi.
