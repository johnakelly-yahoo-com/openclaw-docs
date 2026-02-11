---
summary: "42. Mac ilovada voice wake va push-to-talk rejimlari hamda marshrutlash tafsilotlari"
read_when:
  - 43. Voice wake yoki PTT yo‘llari ustida ishlash
title: "44. Voice Wake"
---

# 45. Voice Wake & Push-to-Talk

## 46. Rejimlar

- 47. **Uyg‘otuvchi so‘z rejimi** (standart): doimiy yoqilgan Speech recognizer trigger tokenlarni (`swabbleTriggerWords`) kutadi. 48. Mos kelganda u yozib olishni boshlaydi, overlay’ni qisman matn bilan ko‘rsatadi va sukunatdan keyin avtomatik yuboradi.
- 49. **Push-to-talk (O‘ng Option tugmasini bosib turish)**: o‘ng Option tugmasini bosib turib darhol yozib olish — trigger kerak emas. 50. Bosib turgan paytda overlay paydo bo‘ladi; qo‘yib yuborish yakunlaydi va matnni biroz tahrirlash imkonini berish uchun qisqa kechikishdan so‘ng yo‘naltiradi.

## 1. Ish vaqtidagi xatti-harakat (wake-word)

- 2. Nutq tanib oluvchi `VoiceWakeRuntime` ichida joylashgan.
- 3. Trigger faqat wake-word va keyingi so‘z orasida **mazmunli pauza** bo‘lsa (~0.55s tanaffus) ishga tushadi. The overlay/chime can start on the pause even before the command begins.
- Silence windows: 2.0s when speech is flowing, 5.0s if only the trigger was heard.
- 6. Qattiq to‘xtash: nazoratsiz sessiyalarni oldini olish uchun 120s.
- 7. Sessiyalar orasida debounce: 350ms.
- 8. Overlay `VoiceWakeOverlayController` orqali committed/volatile ranglash bilan boshqariladi.
- 9. Yuborilgandan so‘ng, tanib oluvchi keyingi triggerni tinglash uchun toza holatda qayta ishga tushadi.

## 10. Hayotiy sikl invariantlari

- 11. Agar Voice Wake yoqilgan va ruxsatlar berilgan bo‘lsa, wake-word tanib oluvchi tinglab turishi kerak (aniq push-to-talk capture vaqtlaridan tashqari).
- 12. Overlay ko‘rinishi (jumladan X tugmasi orqali qo‘lda yopish) hech qachon tanib oluvchining qayta ishga tushishiga to‘sqinlik qilmasligi kerak.

## 13. Yopishqoq overlay nosozlik rejimi (avvalgi)

14. Avval, agar overlay ko‘rinib qolib ketgan bo‘lsa va siz uni qo‘lda yopsangiz, Voice Wake “o‘lik” bo‘lib ko‘rinishi mumkin edi, chunki runtime’ning qayta ishga tushirish urinishlari overlay ko‘rinishi bilan bloklanib, keyingi qayta ishga tushirish rejalashtirilmas edi.

15. Mustahkamlash:

- 16. Wake runtime’ni qayta ishga tushirish endi overlay ko‘rinishi bilan bloklanmaydi.
- 17. Overlay yopilishi yakunlanganda `VoiceSessionCoordinator` orqali `VoiceWakeRuntime.refresh(...)` chaqiriladi, shuning uchun X orqali qo‘lda yopish har doim tinglashni tiklaydi.

## 18. Push-to-talk xususiyatlari

- 19. Hotkey aniqlash **o‘ng Option** uchun global `.flagsChanged` monitoridan foydalanadi (`keyCode 61` + `.option`). 20. Biz faqat hodisalarni kuzatamiz (yutib yubormaymiz).
- 21. Capture pipeline `VoicePushToTalk` ichida joylashgan: Speech’ni darhol boshlaydi, qisman natijalarni overlay’ga uzatadi va qo‘yib yuborilganda `VoiceWakeForwarder`ni chaqiradi.
- 22. Push-to-talk boshlanganda audio tap’lar to‘qnashmasligi uchun wake-word runtime’ni pauza qilamiz; qo‘yib yuborilgandan so‘ng u avtomatik qayta ishga tushadi.
- 23. Ruxsatlar: Mikrofon + Speech talab qilinadi; hodisalarni ko‘rish uchun Accessibility/Input Monitoring tasdig‘i kerak.
- 24. Tashqi klaviaturalar: ba’zilari o‘ng Option’ni kutilgandek ko‘rsatmasligi mumkin — agar foydalanuvchilar o‘tkazib yuborishlar haqida xabar bersa, zaxira yorliqni taklif qiling.

## 25. Foydalanuvchi uchun sozlamalar

- 26. **Voice Wake** tumchog‘i: wake-word runtime’ni yoqadi.
- 27. **Cmd+Fn ni bosib turib gapirish**: push-to-talk monitoringini yoqadi. 28. macOS < 26 da o‘chirilgan.
- 29. Til va mikrofon tanlagichlari, jonli daraja o‘lchagichi, trigger-so‘zlar jadvali, tester (faqat lokal; uzatmaydi).
- 30. Mikrofon tanlagichi qurilma uzilib qolsa ham oxirgi tanlovni saqlab qoladi, uzilganini ko‘rsatuvchi ishorani chiqaradi va qaytguncha vaqtincha tizim sukut bo‘yicha mikrofoniga o‘tadi.
- 31. **Tovushlar**: trigger aniqlanganda va yuborilganda chime; sukut bo‘yicha macOS’ning “Glass” tizim tovushi. 32. Har bir hodisa uchun istalgan `NSSound` yuklanadigan faylni (masalan, MP3/WAV/AIFF) tanlashingiz yoki **No Sound** ni tanlashingiz mumkin.

## 33. Yo‘naltirish xatti-harakati

- 34. Voice Wake yoqilganida, transkriptlar faol gateway/agent’ga uzatiladi (mac ilovaning qolgan qismi ishlatadigan lokal vs masofaviy rejim bilan bir xil).
- 35. Javoblar **oxirgi ishlatilgan asosiy provayder**ga yetkaziladi (WhatsApp/Telegram/Discord/WebChat). 36. Agar yetkazish muvaffaqiyatsiz bo‘lsa, xato log qilinadi va ish WebChat/sessiya loglari orqali baribir ko‘rinadi.

## 37. Yo‘naltirish payload’i

- 38. `VoiceWakeForwarder.prefixedTranscript(_:)` yuborishdan oldin mashina ishorasini oldiga qo‘shadi. 39. Wake-word va push-to-talk yo‘llari o‘rtasida umumiy.

## 40. Tezkor tekshiruv

- 41. Push-to-talk’ni yoqing, Cmd+Fn ni bosib turing, gapiring, qo‘yib yuboring: overlay avval qisman natijalarni ko‘rsatib, so‘ng yuborishi kerak.
- 42. Bosib turganingizda, menyu-paneldagi quloqlar kattalashgan holda qolishi kerak (`triggerVoiceEars(ttl:nil)` ishlatiladi); qo‘yib yuborilgandan so‘ng tushadi.
