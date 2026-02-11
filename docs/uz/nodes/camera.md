---
summary: "Camera capture (iOS node + macOS app) for agent use: photos (jpg) and short video clips (mp4)"
read_when:
  - Adding or modifying camera capture on iOS nodes or macOS
  - Extending agent-accessible MEDIA temp-file workflows
title: "Camera Capture"
---

# Camera capture (agent)

OpenClaw supports **camera capture** for agent workflows:

- **iOS node** (paired via Gateway): capture a **photo** (`jpg`) or **short video clip** (`mp4`, with optional audio) via `node.invoke`.
- **Android node** (paired via Gateway): capture a **photo** (`jpg`) or **short video clip** (`mp4`, with optional audio) via `node.invoke`.
- **macOS app** (node via Gateway): capture a **photo** (`jpg`) or **short video clip** (`mp4`, with optional audio) via `node.invoke`.

All camera access is gated behind **user-controlled settings**.

## iOS node

### User setting (default on)

- iOS Settings tab → **Camera** → **Allow Camera** (`camera.enabled`)
  - Default: **on** (missing key is treated as enabled).
  - When off: `camera.*` commands return `CAMERA_DISABLED`.

### Commands (via Gateway `node.invoke`)

- `camera.list`
  - Response payload:
    - `devices`: array of `{ id, name, position, deviceType }`

- `camera.snap`
  - Params:
    - `facing`: `front|back` (default: `front`)
    - `maxWidth`: number (optional; default `1600` on the iOS node)
    - `quality`: `0..1` (optional; default `0.9`)
    - `format`: currently `jpg`
    - `delayMs`: number (optional; default `0`)
    - `deviceId`: string (optional; from `camera.list`)
  - Response payload:
    - `format: "jpg"`
    - `base64: "<...>"`
    - `width`, `height`
  - Payload guard: photos are recompressed to keep the base64 payload under 5 MB.

- `camera.clip`
  - Params:
    - `facing`: `front|back` (default: `front`)
    - `durationMs`: number (default `3000`, clamped to a max of `60000`)
    - `includeAudio`: boolean (default `true`)
    - `format`: currently `mp4`
    - `deviceId`: string (optional; from `camera.list`)
  - Response payload:
    - `format: "mp4"`
    - `base64: "<...>"`
    - `durationMs`
    - `hasAudio`

### Foreground requirement

`canvas.*` kabi, iOS tuguni faqat **foreground** holatida `camera.*` buyruqlariga ruxsat beradi. Background chaqiruvlar `NODE_BACKGROUND_UNAVAILABLE` ni qaytaradi.

### CLI yordamchisi (vaqtinchalik fayllar + MEDIA)

Biriktirmalarni olishning eng oson yo‘li — CLI yordamchisi orqali bo‘lib, u dekodlangan mediani vaqtinchalik faylga yozadi va `MEDIA:<path>` ni chiqaradi.

Misollar:

```bash
openclaw nodes camera snap --node <id>               # standart: old + orqa (2 ta MEDIA qatori)
openclaw nodes camera snap --node <id> --facing front
openclaw nodes camera clip --node <id> --duration 3000
openclaw nodes camera clip --node <id> --no-audio
```

Eslatmalar:

- `nodes camera snap` agentga ikkala ko‘rinishni berish uchun standart holatda **ikkala** tomonni tanlaydi.
- Agar o‘zingiz wrapper yozmasangiz, chiqish fayllari vaqtinchalik (OS temp katalogida) bo‘ladi.

## Android tuguni

### Android foydalanuvchi sozlamasi (standart: yoqilgan)

- Android Sozlamalar oynasi → **Camera** → **Allow Camera** (`camera.enabled`)
  - Standart: **yoqilgan** (kalit yo‘q bo‘lsa ham yoqilgan deb hisoblanadi).
  - O‘chirilganida: `camera.*` buyruqlari `CAMERA_DISABLED` ni qaytaradi.

### Ruxsatlar

- Android ish vaqtida ruxsatlarni talab qiladi:
  - `camera.snap` va `camera.clip` uchun `CAMERA`.
  - `includeAudio=true` bo‘lganda `camera.clip` uchun `RECORD_AUDIO`.

Agar ruxsatlar yetishmasa, ilova imkon bo‘lsa so‘rov chiqaradi; rad etilsa, `camera.*` so‘rovlari `*_PERMISSION_REQUIRED` xatosi bilan muvaffaqiyatsiz bo‘ladi.

### Android foreground talabi

`canvas.*` kabi, Android tuguni ham faqat **foreground** holatida `camera.*` buyruqlariga ruxsat beradi. Background chaqiruvlar `NODE_BACKGROUND_UNAVAILABLE` ni qaytaradi.

### Payload himoyasi

Fotosuratlar base64 payload 5 MB dan oshmasligi uchun qayta siqiladi.

## macOS ilovasi

### Foydalanuvchi sozlamasi (standart: o‘chirilgan)

macOS companion ilovasi quyidagi belgilash katagini taqdim etadi:

- **Settings → General → Allow Camera** (`openclaw.cameraEnabled`)
  - Standart: **o‘chirilgan**
  - O‘chirilganida: kamera so‘rovlari “Camera disabled by user” ni qaytaradi.

### CLI yordamchisi (node invoke)

macOS tugunida kamera buyruqlarini chaqirish uchun asosiy `openclaw` CLI dan foydalaning.

Misollar:

```bash
openclaw nodes camera list --node <id>            # kamera id larini ro‘yxatlash
openclaw nodes camera snap --node <id>            # MEDIA:<path> ni chiqaradi
openclaw nodes camera snap --node <id> --max-width 1280
openclaw nodes camera snap --node <id> --delay-ms 2000
openclaw nodes camera snap --node <id> --device-id <id>
openclaw nodes camera clip --node <id> --duration 10s          # MEDIA:<path> ni chiqaradi
openclaw nodes camera clip --node <id> --duration-ms 3000      # MEDIA:<path> ni chiqaradi (eski flag)
openclaw nodes camera clip --node <id> --device-id <id>
openclaw nodes camera clip --node <id> --no-audio
```

Eslatmalar:

- `openclaw nodes camera snap` standart holatda, agar o‘zgartirilmasa, `maxWidth=1600` ni ishlatadi.
- macOS da `camera.snap` suratga olishdan oldin warm-up/ekspozitsiya barqarorlashishi uchun `delayMs` (standart 2000ms) ni kutadi.
- Foto payloadlari base64 5 MB dan oshmasligi uchun qayta siqiladi.

## Xavfsizlik + amaliy cheklovlar

- Kamera va mikrofon kirishi odatiy OS ruxsat so‘rovlarini chiqaradi (va Info.plist da foydalanish satrlarini talab qiladi).
- Video kliplar juda katta node payloadlarini oldini olish uchun cheklanadi (hozirda `<= 60s`) (base64 ustama + xabar cheklovlari).

## macOS ekran videosi (OS darajasida)

_Ekran_ videosi (kamera emas) uchun macOS companion dan foydalaning:

```bash
openclaw nodes screen record --node <id> --duration 10s --fps 15   # MEDIA:<path> ni chiqaradi
```

Eslatmalar:

- macOS **Screen Recording** ruxsatini (TCC) talab qiladi.
