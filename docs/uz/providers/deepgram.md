---
summary: "Siz audio biriktirmalar uchun Deepgram speech-to-text’dan foydalanmoqchisiz"
read_when:
  - Sizga Deepgram konfiguratsiyasining tezkor namunasi kerak
  - Deepgram
title: "Deepgram (Audio transkripsiya)"
---

# Deepgram — bu speech-to-text API.

OpenClaw’da u `tools.media.audio` orqali **kiruvchi audio/ovozli eslatmalar
transkripsiyasi** uchun ishlatiladi. Yoqilganda, OpenClaw audio faylni Deepgram’ga yuklaydi va transkriptni
javob pipeline’iga (`{{Transcript}}` + `[Audio]` bloki) qo‘shadi.

Bu **streaming emas**;
u oldindan yozib olingan transkripsiya endpoint’idan foydalanadi. Veb-sayt: [https://deepgram.com](https://deepgram.com)  
Hujjatlar: [https://developers.deepgram.com](https://developers.deepgram.com)

Tezkor boshlash

## API kalitingizni sozlang:

1. DEEPGRAM_API_KEY=dg_...

```
Provider’ni yoqing:
```

2. {
   tools: {
   media: {
   audio: {
   enabled: true,
   models: [{ provider: "deepgram", model: "nova-3" }],
   },
   },
   },
   }

```json5
Variantlar
```

## `model`: Deepgram model ID’si (standart: `nova-3`)

- `language`: til bo‘yicha ko‘rsatma (ixtiyoriy)
- `tools.media.audio.providerOptions.deepgram.detect_language`: tilni aniqlashni yoqish (ixtiyoriy)
- `tools.media.audio.providerOptions.deepgram.punctuate`: tinish belgilarini yoqish (ixtiyoriy)
- `tools.media.audio.providerOptions.deepgram.smart_format`: aqlli formatlashni yoqish (ixtiyoriy)
- Til bilan misol:

{
tools: {
media: {
audio: {
enabled: true,
models: [{ provider: "deepgram", model: "nova-3", language: "en" }],
},
},
},
}

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "deepgram", model: "nova-3", language: "en" }],
      },
    },
  },
}
```

1. Deepgram opsiyalari bilan misol:

```json5
2. {
  tools: {
    media: {
      audio: {
        enabled: true,
        providerOptions: {
          deepgram: {
            detect_language: true,
            punctuate: true,
            smart_format: true,
          },
        },
        models: [{ provider: "deepgram", model: "nova-3" }],
      },
    },
  },
}
```

## 3. Eslatmalar

- Autentifikatsiya provayderning standart tartibiga amal qiladi; `DEEPGRAM_API_KEY` eng sodda yo‘ldir.
- 5. Proksi ishlatilganda `tools.media.audio.baseUrl` va `tools.media.audio.headers` orqali endpointlar yoki sarlavhalarni almashtiring.
- Output follows the same audio rules as other providers (size caps, timeouts, transcript injection).
