---
summary: "Kirish tasvir/audio/video tushunish (ixtiyoriy) provayder + CLI zaxira variantlari bilan"
read_when:
  - Media tushunishni loyihalash yoki qayta refaktorlash
  - Kirish audio/video/tasvirni oldindan qayta ishlashni sozlash
title: "Media tushunish"
---

# Media tushunish (Kirish) — 2026-01-17

OpenClaw **kirish mediasini qisqacha bayon qilishi** (tasvir/audio/video) javob pipeline’i ishga tushishidan oldin mumkin. U mahalliy asboblar yoki provayder kalitlari mavjudligini avtomatik aniqlaydi va o‘chirib qo‘yilishi yoki moslashtirilishi mumkin. Agar tushunish o‘chirilgan bo‘lsa, modellar odatdagidek asl fayllar/URL’larni qabul qiladi.

## Maqsadlar

- Ixtiyoriy: tezroq marshrutlash va yaxshiroq buyruq tahlili uchun kirish mediasini qisqa matnga oldindan hazm qilish.
- Asl mediani modelga yetkazishni saqlab qolish (har doim).
- **Provayder API’lari** va **CLI zaxira variantlari**ni qo‘llab-quvvatlash.
- Xatolik/o‘lcham/vaqt tugashi bo‘yicha tartiblangan zaxira bilan bir nechta modellarni ruxsat etish.

## Yuqori darajadagi xatti-harakat

1. Kirish ilovalarini yig‘ish (`MediaPaths`, `MediaUrls`, `MediaTypes`).
2. Har bir yoqilgan imkoniyat (tasvir/audio/video) uchun siyosat bo‘yicha ilovalarni tanlash (standart: **birinchi**).
3. Birinchi mos model yozuvini tanlash (o‘lcham + imkoniyat + autentifikatsiya).
4. Agar model ishlamasa yoki media juda katta bo‘lsa, **keyingi yozuvga o‘ting**.
5. Muvaffaqiyatli bo‘lsa:
   - `Body` `[Image]`, `[Audio]` yoki `[Video]` blokiga aylanadi.
   - Audio `{{Transcript}}`ni o‘rnatadi; buyruq tahlili mavjud bo‘lsa sarlavha matnidan, aks holda transkriptdan foydalanadi.
   - Sarlavhalar blok ichida `User text:` sifatida saqlanadi.

Agar tushunish muvaffaqiyatsiz bo‘lsa yoki o‘chirilgan bo‘lsa, **javob oqimi davom etadi** asl body + ilovalar bilan.

## Konfiguratsiya sharhi

`tools.media` **umumiy modellar**ni hamda imkoniyatlar bo‘yicha alohida override’larni qo‘llab-quvvatlaydi:

- `tools.media.models`: umumiy model ro‘yxati (`capabilities` orqali cheklash).
- `tools.media.image` / `tools.media.audio` / `tools.media.video`:
  - standartlar (`prompt`, `maxChars`, `maxBytes`, `timeoutSeconds`, `language`)
  - provayder override’lari (`baseUrl`, `headers`, `providerOptions`)
  - Deepgram audio variantlari `tools.media.audio.providerOptions.deepgram` orqali
  - optional **per‑capability `models` list** (preferred before shared models)
  - `attachments` siyosati (`mode`, `maxAttachments`, `prefer`)
  - `scope` (kanal/chatType/sessiya kaliti bo‘yicha ixtiyoriy cheklash)
- `tools.media.concurrency`: imkoniyatlarni bir vaqtda ishga tushirishning maksimal soni (standart **2**).

```json5
{
  tools: {
    media: {
      models: [
        /* umumiy ro‘yxat */
      ],
      image: {
        /* ixtiyoriy override’lar */
      },
      audio: {
        /* ixtiyoriy override’lar */
      },
      video: {
        /* ixtiyoriy override’lar */
      },
    },
  },
}
```

### Model yozuvlari

Har bir `models[]` yozuvi **provider** yoki **CLI** bo‘lishi mumkin:

```json5
{
  type: "provider", // ko‘rsatilmasa, standart
  provider: "openai",
  model: "gpt-5.2",
  prompt: "Tasvirni <= 500 belgi ichida tasvirlab bering.",
  maxChars: 500,
  maxBytes: 10485760,
  timeoutSeconds: 60,
  capabilities: ["image"], // ixtiyoriy, ko‘p‑modal yozuvlar uchun
  profile: "vision-profile",
  preferredProfile: "vision-fallback",
}
```

```json5
{
  type: "cli",
  command: "gemini",
  args: [
    "-m",
    "gemini-3-flash",
    "--allowed-tools",
    "read_file",
    "{{MediaPath}} dagi mediani o‘qing va uni <= {{MaxChars}} belgida tasvirlab bering.",
  ],
  maxChars: 500,
  maxBytes: 52428800,
  timeoutSeconds: 120,
  capabilities: ["video", "image"],
}
```

CLI shablonlari quyidagilardan ham foydalanishi mumkin:

- `{{MediaDir}}` (media fayl joylashgan katalog)
- `{{OutputDir}}` (ushbu ishga tushirish uchun yaratilgan vaqtinchalik katalog)
- `{{OutputBase}}` (kengaytmasiz vaqtinchalik fayl bazaviy yo‘li)

## Standartlar va cheklovlar

Tavsiya etilgan standartlar:

- `maxChars`: rasm/video uchun **500** (qisqa, buyruqga qulay)
- `maxChars`: audio uchun **o‘rnatilmagan** (cheklov qo‘ymasangiz, to‘liq transkript)
- `maxBytes`:
  - rasm: **10MB**
  - audio: **20MB**
  - video: **50MB**

Qoidalar:

- Agar media `maxBytes` dan oshsa, ushbu model o‘tkazib yuboriladi va **keyingi model sinab ko‘riladi**.
- Agar model `maxChars` dan ko‘p qaytarsa, chiqish qisqartiriladi.
- `prompt` sukut bo‘yicha oddiy “Describe the {media}.” va `maxChars` bo‘yicha ko‘rsatma bilan keladi (faqat rasm/video).
- Agar `<capability>.enabled: true` bo‘lsa, lekin modellar sozlanmagan bo‘lsa, OpenClaw ushbu imkoniyatni qo‘llab-quvvatlaydigan provayderda **faol javob modeli**ni sinab ko‘radi.

### Medianing tushunilishini avtomatik aniqlash (standart)

Agar `tools.media.<capability>
.enabled` `false` ga o‘rnatilmagan bo‘lsa va siz
modellarni sozlamagan bo‘lsangiz, OpenClaw quyidagi tartibda avtomatik aniqlaydi va **birinchi ishlagan variantda to‘xtaydi**:**Mahalliy CLI’lar** (faqat audio; o‘rnatilgan bo‘lsa)

1. `sherpa-onnx-offline` (`SHERPA_ONNX_MODEL_DIR` ichida encoder/decoder/joiner/tokens talab etiladi)
   - `whisper-cli` (`whisper-cpp`; `WHISPER_CPP_MODEL` yoki biriktirilgan tiny modeldan foydalanadi)
   - `whisper` (Python CLI; modellarni avtomatik yuklaydi)
   - **Gemini CLI** (`gemini`) `read_many_files` dan foydalanib
2. **Provayder kalitlari**
3. Audio: OpenAI → Groq → Deepgram → Google
   - Rasm: OpenAI → Anthropic → Google → MiniMax
   - Video: Google
   - Avtomatik aniqlashni o‘chirish uchun quyidagini o‘rnating:

{
tools: {
media: {
audio: {
enabled: false,
},
},
},
}

```json5
Eslatma: Ikkilik (binary) aniqlash macOS/Linux/Windows bo‘ylab imkon qadar amalga oshiriladi; CLI `PATH` da ekanligiga ishonch hosil qiling (`~` kengaytiriladi) yoki to‘liq buyruq yo‘li bilan aniq CLI modelini belgilang.
```

Imkoniyatlar (ixtiyoriy)

## Agar `capabilities` ni o‘rnatsangiz, yozuv faqat shu media turlari uchun ishlaydi.

Umumiy ro‘yxatlar uchun OpenClaw standartlarni aniqlashi mumkin: `openai`, `anthropic`, `minimax`: **image**

- `google` (Gemini API): **image + audio + video**
- `groq`: **audio**
- `groq`: **audio**
- CLI yozuvlari uchun kutilmagan mosliklarning oldini olish maqsadida **`capabilities` ni aniq belgilang**.

Agar `capabilities` ni ko‘rsatmasangiz, yozuv joylashgan ro‘yxat uchun mos hisoblanadi.
Provayderlarni qo‘llab-quvvatlash matritsasi (OpenClaw integratsiyalari)

## Provider support matrix (OpenClaw integrations)

| 1. Imkoniyat | 2. Provayder integratsiyasi                               | 3. Eslatmalar                                                                              |
| ----------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| 4. Rasm      | 5. OpenAI / Anthropic / Google / boshqalar `pi-ai` orqali | 6. Roʻyxatdagi rasmni qoʻllab-quvvatlaydigan istalgan model ishlaydi.      |
| 7. Audio     | 8. OpenAI, Groq, Deepgram, Google                         | 9. Provayder transkripsiyasi (Whisper/Deepgram/Gemini). |
| 10. Video    | 11. Google (Gemini API)                | 12. Provayderning video tushunishi.                                        |

## 13. Tavsiya etilgan provayderlar

14. **Rasm**

- 15. Agar faol modelingiz rasmlarni qoʻllab-quvvatlasa, uni afzal koʻring.
- 16. Yaxshi standartlar: `openai/gpt-5.2`, `anthropic/claude-opus-4-6`, `google/gemini-3-pro-preview`.

17. **Audio**

- 18. `openai/gpt-4o-mini-transcribe`, `groq/whisper-large-v3-turbo` yoki `deepgram/nova-3`.
- 19. CLI zaxira varianti: `whisper-cli` (whisper-cpp) yoki `whisper`.
- 20. Deepgram sozlamalari: [Deepgram (audio transkripsiya)](/providers/deepgram).

21. **Video**

- 22. `google/gemini-3-flash-preview` (tez), `google/gemini-3-pro-preview` (batafsilroq).
- 23. CLI zaxira varianti: `gemini` CLI (video/audio uchun `read_file` ni qoʻllab-quvvatlaydi).

## Attachment policy

25. Har bir imkoniyat uchun `attachments` qaysi biriktirmalar qayta ishlanishini boshqaradi:

- 26. `mode`: `first` (standart) yoki `all`
- 27. `maxAttachments`: qayta ishlanadigan maksimal son (standart **1**)
- 28. `prefer`: `first`, `last`, `path`, `url`

29. `mode: "all"` bo‘lganda, chiqishlar `[Image 1/2]`, `[Audio 2/2]` va hokazo tarzda belgilanadi.

## 30. Konfiguratsiya misollari

### 31. 1. Umumiy modellar roʻyxati + qayta aniqlashlar

```json5
32. {
  tools: {
    media: {
      models: [
        { provider: "openai", model: "gpt-5.2", capabilities: ["image"] },
        {
          provider: "google",
          model: "gemini-3-flash-preview",
          capabilities: ["image", "audio", "video"],
        },
        {
          type: "cli",
          command: "gemini",
          args: [
            "-m",
            "gemini-3-flash",
            "--allowed-tools",
            "read_file",
            "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
          ],
          capabilities: ["image", "video"],
        },
      ],
      audio: {
        attachments: { mode: "all", maxAttachments: 2 },
      },
      video: {
        maxChars: 500,
      },
    },
  },
}
```

### 33. 2. Faqat Audio + Video (rasm o‘chirilgan)

```json5
34. {
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          {
            type: "cli",
            command: "whisper",
            args: ["--model", "base", "{{MediaPath}}"],
          },
        ],
      },
      video: {
        enabled: true,
        maxChars: 500,
        models: [
          { provider: "google", model: "gemini-3-flash-preview" },
          {
            type: "cli",
            command: "gemini",
            args: [
              "-m",
              "gemini-3-flash",
              "--allowed-tools",
              "read_file",
              "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
            ],
          },
        ],
      },
    },
  },
}
```

### 35. 3. Ixtiyoriy rasmni tushunish

```json5
36. {
  tools: {
    media: {
      image: {
        enabled: true,
        maxBytes: 10485760,
        maxChars: 500,
        models: [
          { provider: "openai", model: "gpt-5.2" },
          { provider: "anthropic", model: "claude-opus-4-6" },
          {
            type: "cli",
            command: "gemini",
            args: [
              "-m",
              "gemini-3-flash",
              "--allowed-tools",
              "read_file",
              "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
            ],
          },
        ],
      },
    },
  },
}
```

### 37. 4. Ko‘p modal bitta yozuv (aniq imkoniyatlar bilan)

```json5
38. {
  tools: {
    media: {
      image: {
        models: [
          {
            provider: "google",
            model: "gemini-3-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
      audio: {
        models: [
          {
            provider: "google",
            model: "gemini-3-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
      video: {
        models: [
          {
            provider: "google",
            model: "gemini-3-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
    },
  },
}
```

## 39. Holat chiqishi

40. Media tushunilishi ishga tushganda, `/status` qisqa xulosa qatorini o‘z ichiga oladi:

```
41. 📎 Media: rasm ok (openai/gpt-5.2) · audio o‘tkazib yuborildi (maxBytes)
```

42. Bu har bir imkoniyat bo‘yicha natijalarni va mos kelganda tanlangan provayder/modelni ko‘rsatadi.

## 43. Eslatmalar

- 44. Tushunish **imkon qadar** amalga oshiriladi. 45. Xatolar javoblarni to‘sib qo‘ymaydi.
- 46. Tushunish o‘chirilgan bo‘lsa ham, biriktirmalar modellarga uzatiladi.
- 47. Tushunish qayerda ishlashini cheklash uchun `scope` dan foydalaning (masalan, faqat DMlarda).

## 48. Tegishli hujjatlar

- 49. [Konfiguratsiya](/gateway/configuration)
- 50. [Rasm va Media qo‘llab-quvvatlashi](/nodes/images)
