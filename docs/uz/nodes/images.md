---
summary: "Yuborish, gateway va agent javoblari uchun tasvir va media bilan ishlash qoidalari"
read_when:
  - Media pipeline yoki biriktirmalarni o‘zgartirish
title: "Tasvir va Media qo‘llab-quvvatlashi"
---

# Tasvir va Media qo‘llab-quvvatlashi — 2025-12-05

WhatsApp kanali **Baileys Web** orqali ishlaydi. Ushbu hujjat yuborish, shlyuz va agent javoblari uchun joriy media bilan ishlash qoidalarini qamrab oladi.

## Maqsadlar

- `openclaw message send --media` orqali ixtiyoriy sarlavhali media yuborish.
- Veb inboxdan avtomatik javoblarga matn bilan birga media qo‘shilishiga ruxsat berish.
- Har bir tur bo‘yicha limitlarni oqilona va bashorat qilinadigan saqlash.

## CLI interfeysi

- `openclaw message send --media <path-or-url> [--message <caption>]`
  - `--media` ixtiyoriy; media-only yuborish uchun sarlavha bo‘sh bo‘lishi mumkin.
  - `--dry-run` yechilgan payloadni chiqaradi; `--json` `{ channel, to, messageId, mediaUrl, caption }` ni chiqaradi.

## WhatsApp Web kanali xatti-harakati

- Kirish: lokal fayl yo‘li **yoki** HTTP(S) URL.
- Oqim: Bufferga yuklash, media turini aniqlash va to‘g‘ri payloadni qurish:
  - **Rasmlar:** JPEG ga qayta o‘lchash va qayta siqish (eng katta tomoni 2048px) `agents.defaults.mediaMaxMb` (standart 5 MB) ni nishonga olib, 6 MB bilan cheklanadi.
  - **Audio/Ovoz/Video:** 16 MB gacha pass-through; audio ovozli xabar sifatida yuboriladi (`ptt: true`).
  - **Hujjatlar:** boshqa hammasi, 100 MB gacha, imkon bo‘lsa fayl nomi saqlanadi.
- WhatsApp GIF-uslubidagi ijro: MP4 ni `gifPlayback: true` bilan yuboring (CLI: `--gif-playback`), shunda mobil mijozlar ichida aylana ijro etadi.
- MIME aniqlash avval sehrli baytlarga, keyin sarlavhalarga, so‘ng fayl kengaytmasiga tayanadi.
- Sarlavha `--message` yoki `reply.text` dan olinadi; bo‘sh sarlavhaga ruxsat beriladi.
- Loglash: verbose bo‘lmagan rejimda `↩️`/`✅`; verbose rejimda hajm va manba yo‘li/URL ko‘rsatiladi.

## Avtomatik javob quvuri

- `getReplyFromConfig` `{ text?, mediaUrl?, mediaUrls? }` ni qaytaradi. Media mavjud bo‘lsa, veb yuboruvchi lokal yo‘llar yoki URLlarni `openclaw message send` bilan bir xil quvur orqali yechadi.
- Agar bir nechta media berilgan bo‘lsa, ular ketma-ket yuboriladi.
- Buyruqlarga kiruvchi media (Pi)

## Kirish veb xabarlari media ni o‘z ichiga olganda, OpenClaw vaqtinchalik faylga yuklab oladi va shablonlash o‘zgaruvchilarini taqdim etadi:

- Kirish media uchun `{{MediaUrl}}` psevdo-URL.
  - Buyruqni ishga tushirishdan oldin yozilgan lokal vaqtinchalik yo‘l `{{MediaPath}}`.
  - Agar sessiya bo‘yicha Docker sandbox yoqilgan bo‘lsa, kiruvchi media sandbox ish maydoniga ko‘chiriladi va `MediaPath`/`MediaUrl` `media/inbound/<filename>` kabi nisbiy yo‘lga qayta yoziladi.
- Har bir sessiya uchun Docker sandbox yoqilganda, kiruvchi media sandbox ishchi maydoniga ko‘chiriladi va `MediaPath`/`MediaUrl` `media/inbound/<filename>` kabi nisbiy yo‘lga qayta yoziladi.
- Audio `{{Transcript}}` ni o‘rnatadi va buyruqlarni tahlil qilish uchun transkriptni ishlatadi, shunda slash-buyruqlar ishlashda davom etadi.
  - Audio `{{Transcript}}` ni o‘rnatadi va buyruqlarni tahlil qilish uchun transkriptdan foydalanadi, shuning uchun slash-buyruqlar ishlashda davom etadi.
  - Video va rasm tavsiflari buyruqlarni tahlil qilish uchun har qanday sarlavha (caption) matnini saqlab qoladi.
- By default only the first matching image/audio/video attachment is processed; set \`tools.media.<cap>**Chiqish yuborish limitlari (WhatsApp web send)**

## Rasmlar: qayta siqilgandan keyin ~6 MB limit.

Audio/ovoz/video: 16 MB limit; hujjatlar: 100 MB limit.

- Haddan tashqari katta yoki o‘qib bo‘lmaydigan media → loglarda aniq xato va javob o‘tkazib yuboriladi.
- **Media tushunish limitlari (transkripsiya/tavsif)**
- Rasm standarti: 10 MB (`tools.media.image.maxBytes`).

Audio standarti: 20 MB (`tools.media.audio.maxBytes`).

- Video standarti: 50 MB (`tools.media.video.maxBytes`).
- Haddan tashqari katta media tushunish bosqichini o‘tkazib yuboradi, ammo javoblar asl body bilan davom etadi.
- Testlar uchun eslatmalar
- Rasm/audio/hujjat holatlari uchun yuborish + javob oqimlarini qamrab oling.

## Rasmlar uchun qayta siqishni (hajm chegarasi) va audio uchun ovozli xabar bayrog‘ini tekshiring.

- Ko‘p media javoblari ketma-ket yuborilishini ta’minlang.
- Tugunlar: pairing, imkoniyatlar, ruxsatlar va canvas/camera/screen/system uchun CLI yordamchilari
- Ensure multi-media replies fan out as sequential sends.
