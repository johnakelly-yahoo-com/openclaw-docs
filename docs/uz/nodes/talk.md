---
summary: "1. Talk rejimi: ElevenLabs TTS bilan uzluksiz nutq suhbatlari"
read_when:
  - 2. macOS/iOS/Android’da Talk rejimini joriy etish
  - 3. Ovoz/TTS/bo‘lish (interrupt) xatti-harakatlarini o‘zgartirish
title: "4. Talk Rejimi"
---

# 5. Talk Rejimi

6. Talk rejimi — uzluksiz ovozli suhbat aylanasidir:

1. 7. Nutqni tinglash
2. 8. Transkriptni modelga yuborish (asosiy sessiya, chat.send)
3. 9. Javobni kutish
4. 10. Uni ElevenLabs orqali aytish (oqimli ijro)

## 11) Xatti-harakat (macOS)

- 12. Talk rejimi yoqilgan paytda **har doim ko‘rinadigan overlay**.
- 13. **Tinglash → O‘ylash → Gapirish** bosqichlari o‘tishlari.
- 14. **Qisqa pauza** (sukut oynasi) bo‘lganda, joriy transkript yuboriladi.
- 15. Javoblar **WebChat’ga yoziladi** (matn terish bilan bir xil).
- 16. **Nutqda to‘xtatish** (standart yoqilgan): foydalanuvchi assistent gapirayotganda gapira boshlasa, ijro to‘xtatiladi va keyingi prompt uchun to‘xtatish vaqti qayd etiladi.

## 17. Javoblardagi ovoz ko‘rsatmalari

18. Assistent javobini ovozni boshqarish uchun **bitta JSON qatori** bilan boshlashi mumkin:

```json
19. { "voice": "<voice-id>", "once": true }
```

20. Qoidalar:

- 21. Faqat birinchi bo‘sh bo‘lmagan qatordan foydalaniladi.
- 22. Noma’lum kalitlar e’tiborsiz qoldiriladi.
- 23. `once: true` faqat joriy javobga qo‘llanadi.
- 24. `once` bo‘lmasa, ovoz Talk rejimi uchun yangi standartga aylanadi.
- 25. JSON qatori TTS ijrosidan oldin olib tashlanadi.

26. Qo‘llab-quvvatlanadigan kalitlar:

- 27. `voice` / `voice_id` / `voiceId`
- 28. `model` / `model_id` / `modelId`
- 29. `speed`, `rate` (WPM), `stability`, `similarity`, `style`, `speakerBoost`
- 30. `seed`, `normalize`, `lang`, `output_format`, `latency_tier`
- 31. `once`

## 32. Sozlamalar (`~/.openclaw/openclaw.json`)

```json5
33. {
  talk: {
    voiceId: "elevenlabs_voice_id",
    modelId: "eleven_v3",
    outputFormat: "mp3_44100_128",
    apiKey: "elevenlabs_api_key",
    interruptOnSpeech: true,
  },
}
```

34. Standartlar:

- 35. `interruptOnSpeech`: true
- 36. `voiceId`: `ELEVENLABS_VOICE_ID` / `SAG_VOICE_ID` ga qaytadi (yoki API kaliti mavjud bo‘lsa, birinchi ElevenLabs ovozi)
- 37. `modelId`: o‘rnatilmagan bo‘lsa, `eleven_v3` ga standartlanadi
- 38. `apiKey`: `ELEVENLABS_API_KEY` ga qaytadi (yoki mavjud bo‘lsa, gateway shell profili)
- 39. `outputFormat`: macOS/iOS’da `pcm_44100`, Android’da `pcm_24000` (MP3 oqimini majburlash uchun `mp3_*` ni o‘rnating)

## 40. macOS UI

- 41. Menyu paneli tugmasi: **Talk**
- 42. Sozlamalar yorlig‘i: **Talk Mode** guruhi (voice id + to‘xtatish tumchog‘i)
- 43. Overlay:
  - 44. **Tinglash**: mikrofon darajasi bilan bulut pulsatsiyalari
  - 45. **O‘ylash**: cho‘kib boruvchi animatsiya
  - 46. **Gapirish**: tarqaluvchi halqalar
  - 47. Bulutni bosish: gapirishni to‘xtatish
  - 48. X ni bosish: Talk rejimidan chiqish

## 49. Eslatmalar

- 50. Nutq + Mikrofon ruxsatlari talab etiladi.
- Uses `chat.send` against session key `main`.
- TTS uses ElevenLabs streaming API with `ELEVENLABS_API_KEY` and incremental playback on macOS/iOS/Android for lower latency.
- `stability` for `eleven_v3` is validated to `0.0`, `0.5`, or `1.0`; other models accept `0..1`.
- `latency_tier` is validated to `0..4` when set.
- Android supports `pcm_16000`, `pcm_22050`, `pcm_24000`, and `pcm_44100` output formats for low-latency AudioTrack streaming.
