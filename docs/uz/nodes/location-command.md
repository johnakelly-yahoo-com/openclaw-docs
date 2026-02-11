---
summary: "5. Node’lar uchun joylashuv buyrug‘i (location.get), ruxsat rejimlari va fon xatti-harakati"
read_when:
  - 6. Joylashuv node qo‘llab-quvvatlashi yoki ruxsatlar UI’sini qo‘shish
  - 7. Fon joylashuvi + push oqimlarini loyihalash
title: "8. Joylashuv buyrug‘i"
---

# 9. Joylashuv buyrug‘i (node’lar)

## 10. TL;DR

- 11. `location.get` — bu node buyrug‘i (`node.invoke` orqali).
- 12. Sukut bo‘yicha o‘chiq.
- 13. Sozlamalar selektordan foydalanadi: O‘chiq / Foydalanayotganda / Har doim.
- 14. Alohida o‘chirgich: Aniq joylashuv.

## 15. Nega selektor (oddiy o‘chirgich emas)

16. OS ruxsatlari ko‘p darajali. 17. Biz ilova ichida selektorni ko‘rsatishimiz mumkin, ammo haqiqiy ruxsatni baribir OS belgilaydi.

- 18. iOS/macOS: foydalanuvchi tizim so‘rovlari/Sozlamalarda **Foydalanayotganda** yoki **Har doim** ni tanlashi mumkin. 19. Ilova darajani oshirishni so‘rashi mumkin, ammo OS Sozlamalarga o‘tishni talab qilishi mumkin.
- 20. Android: fon joylashuvi alohida ruxsat; Android 10+ da ko‘pincha Sozlamalar orqali jarayon talab etiladi.
- 21. Aniq joylashuv alohida ruxsat (iOS 14+ “Precise”, Android’da “fine” va “coarse”).

22. UI’dagi selektor biz so‘raydigan rejimni belgilaydi; haqiqiy ruxsat OS sozlamalarida saqlanadi.

## 23. Sozlamalar modeli

24. Har bir node qurilma uchun:

- 25. `location.enabledMode`: `off | whileUsing | always`
- 26. `location.preciseEnabled`: bool

27. UI xatti-harakati:

- 28. `whileUsing` tanlansa, oldingi (foreground) ruxsat so‘raladi.
- 29. `always` tanlansa, avval `whileUsing` ta’minlanadi, so‘ng fon ruxsati so‘raladi (yoki talab etilsa foydalanuvchi Sozlamalarga yuboriladi).
- 30. Agar OS so‘ralgan darajani rad etsa, eng yuqori berilgan darajaga qaytiladi va holat ko‘rsatiladi.

## 31. Ruxsatlar mosligi (node.permissions)

32. Ixtiyoriy. 33. macOS node `location` ni ruxsatlar xaritasi orqali bildiradi; iOS/Android uni bermasligi mumkin.

## Command: `location.get`

35. `node.invoke` orqali chaqiriladi.

36. Parametrlar (tavsiya etiladi):

```json
37. {
  "timeoutMs": 10000,
  "maxAgeMs": 15000,
  "desiredAccuracy": "coarse|balanced|precise"
}
```

Response payload:

```json
39. {
  "lat": 48.20849,
  "lon": 16.37208,
  "accuracyMeters": 12.5,
  "altitudeMeters": 182.0,
  "speedMps": 0.0,
  "headingDeg": 270.0,
  "timestamp": "2026-01-03T12:34:56.000Z",
  "isPrecise": true,
  "source": "gps|wifi|cell|unknown"
}
```

40. Xatolar (barqaror kodlar):

- 41. `LOCATION_DISABLED`: selektor o‘chiq.
- 42. `LOCATION_PERMISSION_REQUIRED`: so‘ralgan rejim uchun ruxsat yetishmaydi.
- 43. `LOCATION_BACKGROUND_UNAVAILABLE`: ilova fon rejimida, ammo faqat Foydalanayotganda ruxsat berilgan.
- 44. `LOCATION_TIMEOUT`: belgilangan vaqtda aniqlanmadi.
- 45. `LOCATION_UNAVAILABLE`: tizim xatosi / provayderlar yo‘q.

## 46. Fon xatti-harakati (kelajakda)

47. Maqsad: model node fon rejimida bo‘lsa ham joylashuvni so‘rashi mumkin, ammo faqat quyidagi holatlarda:

- 48. Foydalanuvchi **Har doim** ni tanlagan.
- 49. OS fon joylashuviga ruxsat bergan.
- 50. Ilovaga joylashuv uchun fon rejimida ishlashga ruxsat berilgan (iOS fon rejimi / Android foreground service yoki maxsus ruxsat).

Bosish orqali ishga tushadigan oqim (kelajakda):

1. Shlyuz tugunga push yuboradi (jim push yoki FCM ma’lumotlari).
2. Tugun qisqa muddatga uyg‘onadi va qurilmadan joylashuvni so‘raydi.
3. Tugun yuklamani Shlyuzga uzatadi.

Eslatmalar:

- iOS: Doimiy ruxsat + fon joylashuv rejimi talab qilinadi. Jim push cheklanishi mumkin; vaqti-vaqti bilan nosozliklar kutiladi.
- Android: fon joylashuvi oldingi (foreground) servisni talab qilishi mumkin; aks holda rad etilishi mumkin.

## Model/asbob integratsiyasi

- Asbob yuzasi: `nodes` asbobi `location_get` amalini qo‘shadi (tugun talab qilinadi).
- CLI: `openclaw nodes location get --node <id>`.
- Agent qo‘llanmalari: faqat foydalanuvchi joylashuvni yoqqan va doirani tushunganida chaqiring.

## UX matni (tavsiya etiladi)

- O‘chirilgan: “Joylashuvni ulash o‘chirilgan.”
- Foydalanayotganda: “Faqat OpenClaw ochiq bo‘lganda.”
- Doimiy: “Fon joylashuviga ruxsat bering. Tizim ruxsati talab qilinadi.”
- Aniq: “Aniq GPS joylashuvdan foydalaning. Taxminiy joylashuvni ulash uchun o‘chiring.”
