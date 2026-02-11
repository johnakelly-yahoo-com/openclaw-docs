---
summary: "O‘rnatish va konfiguratsiya yangilanishlari lokal Mac’da emas, gateway hostda amalga oshiriladi."
read_when:
  - Wake-word va push-to-talk ustma-ust kelganda ovozli overlay hayotiy sikli
title: "Ovozli overlay xatti-harakatini sozlash"
---

# Voice Overlay

Voice Overlay Lifecycle (macOS) 1. Maqsad: uyg‘otuvchi so‘z va push-to-talk bir vaqtda ustma-ust kelganda ovoz overlay’ini bashoratli saqlash.

## 2. Joriy niyat

- 3. Agar overlay uyg‘otuvchi so‘z orqali allaqachon ko‘rinib turgan bo‘lsa va foydalanuvchi hotkey’ni bossa, hotkey sessiyasi matnni qayta tiklash o‘rniga mavjud matnni _o‘zlashtiradi_. 4. Hotkey bosib turilgan paytda overlay ekranda qoladi. 5. Foydalanuvchi qo‘yib yuborganda: agar kesilgan (trimmed) matn bo‘lsa — yuboriladi, aks holda yopiladi.
- Wake-word alone still auto-sends on silence; push-to-talk sends immediately on release.

## 7. Amalga oshirilgan (2025-yil 9-dekabr)

- Overlay sessions now carry a token per capture (wake-word or push-to-talk). 9. Token mos kelmasa, partial/final/send/dismiss/level yangilanishlari bekor qilinadi, bu eskirgan callback’lardan saqlaydi.
- 10. Push-to-talk ko‘rinib turgan overlay matnini prefiks sifatida o‘zlashtiradi (ya’ni, uyg‘otuvchi overlay ochiq turganda hotkey bosilsa, matn saqlanadi va yangi nutq qo‘shiladi). 11. U yakuniy transkriptni kutish uchun 1.5 soniyagacha kutadi, so‘ngra joriy matnga qaytadi.
- 12. Chime/overlay loglari `info` darajasida `voicewake.overlay`, `voicewake.ptt` va `voicewake.chime` kategoriyalarida chiqariladi (sessiya boshlanishi, partial, final, send, dismiss, chime sababi).

## 13. Keyingi qadamlar

1. 14. **VoiceSessionCoordinator (aktor)**
   - 15. Bir vaqtning o‘zida aniq bitta `VoiceSession`ga egalik qiladi.
   - 16. API (token asosida): `beginWakeCapture`, `beginPushToTalk`, `updatePartial`, `endCapture`, `cancel`, `applyCooldown`.
   - 17. Eskirgan token olib kelgan callback’larni bekor qiladi (eski recognizer’larning overlay’ni qayta ochib yuborishining oldini oladi).
2. **VoiceSession (model)**
   - 19. Maydonlar: `token`, `source` (wakeWord|pushToTalk), tasdiqlangan/vaqtinchalik matn, chime flaglari, taymerlar (auto-send, idle), `overlayMode` (display|editing|sending), cooldown muddati.
3. **Overlay binding**
   - 21. `VoiceSessionPublisher` (`ObservableObject`) faol sessiyani SwiftUI’ga aks ettiradi.
   - 22. `VoiceWakeOverlayView` faqat publisher orqali render qiladi; u hech qachon global singleton’larni bevosita o‘zgartirmaydi.
   - 23. Overlay foydalanuvchi amallari (`sendNow`, `dismiss`, `edit`) sessiya tokeni bilan coordinator’ga qayta chaqiriq qiladi.
4. 24. **Yagona yuborish yo‘li**
   - 25. `endCapture`da: agar kesilgan matn bo‘sh bo‘lsa → dismiss; aks holda `performSend(session:)` (send chime’ni bir marta chaladi, yo‘naltiradi, yopadi).
   - 26. Push-to-talk: kechikishsiz; uyg‘otuvchi so‘z: auto-send uchun ixtiyoriy kechikish.
   - 27. Push-to-talk tugagach, uyg‘otuvchi so‘z darhol qayta ishga tushmasligi uchun wake runtime’ga qisqa cooldown qo‘llanadi.
5. 28. **Logging**
   - 29. Coordinator `bot.molt` subsistemasida `voicewake.overlay` va `voicewake.chime` kategoriyalarida `.info` loglarini chiqaradi.
   - 30. Asosiy hodisalar: `session_started`, `adopted_by_push_to_talk`, `partial`, `finalized`, `send`, `dismiss`, `cancel`, `cooldown`.

## 31) Debugging tekshiruv ro‘yxati

- 32. Yopishib qolgan overlay’ni qayta yaratishda loglarni oqimda kuzating:

  ```bash
  33. sudo log stream --predicate 'subsystem == "bot.molt" AND category CONTAINS "voicewake"' --level info --style compact
  ```

- 34. Faqat bitta faol sessiya tokeni borligini tekshiring; eskirgan callback’lar coordinator tomonidan bekor qilinishi kerak.

- 35. Push-to-talk qo‘yib yuborilishi har doim faol token bilan `endCapture`ni chaqirishini ta’minlang; agar matn bo‘sh bo‘lsa, chime yoki yuborishsiz `dismiss` kutiladi.

## 36. Migratsiya bosqichlari (tavsiya etiladi)

1. 37. `VoiceSessionCoordinator`, `VoiceSession` va `VoiceSessionPublisher`ni qo‘shing.
2. 38. `VoiceWakeRuntime`ni `VoiceWakeOverlayController`ga bevosita tegmasdan, sessiyalarni yaratish/yangilash/yakunlashga refaktor qiling.
3. 39. `VoicePushToTalk`ni mavjud sessiyalarni o‘zlashtirishga va qo‘yib yuborilganda `endCapture`ni chaqirishga refaktor qiling; runtime cooldown’ni qo‘llang.
4. 40. `VoiceWakeOverlayController`ni publisher’ga ulang; runtime/PTT’dan to‘g‘ridan-to‘g‘ri chaqiriqlarni olib tashlang.
5. 41. Sessiyani o‘zlashtirish, cooldown va bo‘sh-matn dismiss uchun integratsion testlar qo‘shing.
