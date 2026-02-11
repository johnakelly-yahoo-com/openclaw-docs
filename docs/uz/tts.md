---
summary: "Chiqish javoblari uchun matndan nutqqa (TTS)"
read_when:
  - Javoblar uchun matndan nutqqa funksiyasini yoqish
  - TTS provayderlari yoki limitlarini sozlash
  - /tts buyruqlaridan foydalanish
title: "Matndan Nutqqa"
---

# Matndan nutqqa (TTS)

OpenClaw ElevenLabs, OpenAI yoki Edge TTS yordamida chiqish javoblarini audioga aylantira oladi.
U OpenClaw audio yubora oladigan barcha joylarda ishlaydi; Telegram’da dumaloq ovozli xabar ko‘rinishida bo‘ladi.

## Qo‘llab-quvvatlanadigan xizmatlar

- **ElevenLabs** (asosiy yoki zaxira provayder)
- **OpenAI** (asosiy yoki zaxira provayder; xulosalar uchun ham ishlatiladi)
- **Edge TTS** (asosiy yoki zaxira provayder; `node-edge-tts` dan foydalanadi, API kalitlari bo‘lmaganda standart)

### Edge TTS bo‘yicha eslatmalar

Edge TTS Microsoft Edge’ning onlayn neyron TTS xizmatidan `node-edge-tts`
kutubxonasi orqali foydalanadi. Bu xostlangan xizmat (mahalliy emas), Microsoft’ning endpointlaridan foydalanadi va
API kalitini talab qilmaydi. `node-edge-tts` nutq sozlamalari va chiqish formatlari variantlarini taqdim etadi, ammo
Edge xizmati barcha variantlarni qo‘llab-quvvatlamaydi. citeturn2search0

Edge TTS e’lon qilingan SLA yoki kvotasiz ommaviy veb-xizmat bo‘lgani sababli, undan
eng yaxshi urinish asosida foydalaning. Agar sizga kafolatlangan cheklovlar va qo‘llab-quvvatlash kerak bo‘lsa, OpenAI yoki ElevenLabs’dan foydalaning.
Microsoft’ning Speech REST API hujjatlarida har bir so‘rov uchun 10 daqiqalik audio cheklovi ko‘rsatilgan; Edge TTS cheklovlarni e’lon qilmaydi, shuning uchun o‘xshash yoki undan past cheklovlarni taxmin qiling. citeturn0search3

## Ixtiyoriy kalitlar

Agar OpenAI yoki ElevenLabs’dan foydalanmoqchi bo‘lsangiz:

- `ELEVENLABS_API_KEY` (yoki `XI_API_KEY`)
- `OPENAI_API_KEY`

Edge TTS **API kalitini talab qilmaydi**. Agar hech qanday API kalitlari topilmasa, OpenClaw sukut bo‘yicha Edge TTS’ga o‘tadi (agar `messages.tts.edge.enabled=false` orqali o‘chirilmagan bo‘lsa).

Agar bir nechta provayder sozlangan bo‘lsa, tanlangan provayder birinchi bo‘lib ishlatiladi, qolganlari esa zaxira variantlar bo‘ladi.
Avto‑xulosa sozlangan `summaryModel` (yoki `agents.defaults.model.primary`) dan foydalanadi, shuning uchun xulosalarni yoqsangiz, o‘sha provayder ham autentifikatsiyadan o‘tgan bo‘lishi kerak.

## Xizmat havolalari

- [OpenAI Text-to-Speech guide](https://platform.openai.com/docs/guides/text-to-speech)
- [OpenAI Audio API reference](https://platform.openai.com/docs/api-reference/audio)
- [ElevenLabs Text to Speech](https://elevenlabs.io/docs/api-reference/text-to-speech)
- [ElevenLabs Authentication](https://elevenlabs.io/docs/api-reference/authentication)
- [node-edge-tts](https://github.com/SchneeHertz/node-edge-tts)
- [Microsoft Speech output formats](https://learn.microsoft.com/azure/ai-services/speech-service/rest-text-to-speech#audio-outputs)

## Sukut bo‘yicha yoqilganmi?

Yo‘q. Auto‑TTS sukut bo‘yicha **o‘chirilgan**. Uni konfiguratsiyada `messages.tts.auto` orqali yoki har bir sessiya uchun `/tts always` (alias: `/tts on`) bilan yoqing.

TTS yoqilgandan so‘ng Edge TTS sukut bo‘yicha **yoqilgan** bo‘ladi va OpenAI yoki ElevenLabs API kalitlari mavjud bo‘lmaganda avtomatik ravishda ishlatiladi.

## Konfiguratsiya

TTS konfiguratsiyasi `openclaw.json` ichida `messages.tts` ostida joylashgan.
To‘liq sxema [Gateway configuration](/gateway/configuration) da keltirilgan.

### Minimal konfiguratsiya (yoqish + provayder)

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "elevenlabs",
    },
  },
}
```

### OpenAI asosiy, ElevenLabs zaxira

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "openai",
      summaryModel: "openai/gpt-4.1-mini",
      modelOverrides: {
        enabled: true,
      },
      openai: {
        apiKey: "openai_api_key",
        model: "gpt-4o-mini-tts",
        voice: "alloy",
      },
      elevenlabs: {
        apiKey: "elevenlabs_api_key",
        baseUrl: "https://api.elevenlabs.io",
        voiceId: "voice_id",
        modelId: "eleven_multilingual_v2",
        seed: 42,
        applyTextNormalization: "auto",
        languageCode: "en",
        voiceSettings: {
          stability: 0.5,
          similarityBoost: 0.75,
          style: 0.0,
          useSpeakerBoost: true,
          speed: 1.0,
        },
      },
    },
  },
}
```

### Edge TTS asosiy (API kalitisiz)

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "edge",
      edge: {
        enabled: true,
        voice: "en-US-MichelleNeural",
        lang: "en-US",
        outputFormat: "audio-24khz-48kbitrate-mono-mp3",
        rate: "+10%",
        pitch: "-5%",
      },
    },
  },
}
```

### Edge TTS’ni o‘chirish

```json5
{
  messages: {
    tts: {
      edge: {
        enabled: false,
      },
    },
  },
}
```

### Maxsus cheklovlar + sozlamalar yo‘li

```json5
{
  messages: {
    tts: {
      auto: "always",
      maxTextLength: 4000,
      timeoutMs: 30000,
      prefsPath: "~/.openclaw/settings/tts.json",
    },
  },
}
```

### Faqat kiruvchi ovozli xabardan keyin audio bilan javob berish

```json5
{
  messages: {
    tts: {
      auto: "inbound",
    },
  },
}
```

### Uzun javoblar uchun auto‑xulosani o‘chirish

```json5
{
  messages: {
    tts: {
      auto: "always",
    },
  },
}
```

So‘ng quyidagini bajaring:

```
/tts summary off
```

### Maydonlar bo‘yicha eslatmalar

- `auto`: auto‑TTS rejimi (`off`, `always`, `inbound`, `tagged`).
  - `inbound` faqat kiruvchi ovozli xabardan keyin audio yuboradi.
  - `tagged` faqat javobda `[[tts]]` teglari bo‘lganda audio yuboradi.
- `enabled`: eski kalit (doctor buni `auto` ga ko‘chiradi).
- `mode`: `"final"` (sukut bo‘yicha) yoki `"all"` (asbob/blok javoblarini ham o‘z ichiga oladi).
- `provider`: `"elevenlabs"`, `"openai"` yoki `"edge"` (zaxira avtomatik).
- Agar `provider` **o‘rnatilmagan** bo‘lsa, OpenClaw avval `openai` (agar kalit bo‘lsa), so‘ng `elevenlabs` (agar kalit bo‘lsa), aks holda `edge` ni afzal ko‘radi.
- `summaryModel`: avtomatik xulosa uchun ixtiyoriy arzon model; standart bo‘yicha `agents.defaults.model.primary`.
  - `provider/model` yoki sozlangan model aliasini qabul qiladi.
- `modelOverrides`: modelga TTS direktivalarini chiqarishga ruxsat beradi (standart yoqilgan).
- `maxTextLength`: TTS kiritmasi uchun qat’iy maksimal chegara (belgilar). `/tts audio` oshib ketilsa muvaffaqiyatsiz bo‘ladi.
- `timeoutMs`: so‘rov vaqti tugashi (ms).
- `prefsPath`: override the local prefs JSON path (provider/limit/summary).
- `apiKey` qiymatlari muhit o‘zgaruvchilariga qaytadi (`ELEVENLABS_API_KEY`/`XI_API_KEY`, `OPENAI_API_KEY`).
- `elevenlabs.baseUrl`: ElevenLabs API asosiy URL manzilini almashtirish.
- `elevenlabs.voiceSettings`:
  - `stability`, `similarityBoost`, `style`: `0..1`
  - `useSpeakerBoost`: `true|false`
  - `speed`: `0.5..2.0` (1.0 = normal)
- `elevenlabs.applyTextNormalization`: `auto|on|off`
- `elevenlabs.languageCode`: 2-letter ISO 639-1 (e.g. `en`, `de`)
- `elevenlabs.seed`: butun son `0..4294967295` (iloji boricha deterministik)
- `edge.enabled`: Edge TTS’dan foydalanishga ruxsat (standart `true`; API kaliti yo‘q).
- `edge.voice`: Edge neyron ovoz nomi (masalan, `en-US-MichelleNeural`).
- `edge.lang`: til kodi (masalan, `en-US`).
- `edge.outputFormat`: Edge output format (e.g. `audio-24khz-48kbitrate-mono-mp3`).
  - Yaroqli qiymatlar uchun Microsoft Speech chiqish formatlariga qarang; barcha formatlar Edge tomonidan qo‘llab-quvvatlanmaydi.
- `edge.rate` / `edge.pitch` / `edge.volume`: foizli satrlar (masalan, `+10%`, `-5%`).
- `edge.saveSubtitles`: audio fayl bilan birga JSON subtitrlarni yozish.
- `edge.proxy`: Edge TTS so‘rovlari uchun proksi URL.
- `edge.timeoutMs`: so‘rov vaqti tugashini almashtirish (ms).

## Model tomonidan boshqariladigan almashtirishlar (standart yoqilgan)

Standart bo‘yicha, model bitta javob uchun TTS direktivalarini chiqarishi **mumkin**.
`messages.tts.auto` `tagged` bo‘lganda, audio ishga tushishi uchun bu direktivalar talab qilinadi.

Yoqilganda, model bitta javob uchun ovozni almashtirish maqsadida `[[tts:...]]` direktivalarini, shuningdek faqat audioga tushishi kerak bo‘lgan ifodaviy teglar (kulgi, kuylash ishoralari va h.k.)ni berish uchun ixtiyoriy `[[tts:text]]...[[/tts:text]]` blokini chiqarishi mumkin.

Namunaviy javob payloadi:

```
Mana.
```

[[tts:provider=elevenlabs voiceId=pMsXgVXv3BLzUgSXRplE model=eleven_v3 speed=1.1]]
[[tts:text]](kuladi) Qo‘shiqni yana bir bor o‘qing.[[/tts:text]]

- Mavjud direktiva kalitlari (yoqilganda):
- `provider` (`openai` | `elevenlabs` | `edge`)
- `voice` (OpenAI ovozi) yoki `voiceId` (ElevenLabs)
- `model` (OpenAI TTS modeli yoki ElevenLabs model IDsi)
- `stability`, `similarityBoost`, `style`, `speed`, `useSpeakerBoost`
- `applyTextNormalization` (`auto|on|off`)
- `seed`

`seed`

```json5
Barcha model almashtirishlarini o‘chirish:
```

{
messages: {
tts: {
modelOverrides: {
enabled: false,
},
},
},
}

```json5
Ixtiyoriy ruxsat ro‘yxati (teglar yoqilgan holda aniq almashtirishlarni o‘chirish):
```

{
messages: {
tts: {
modelOverrides: {
enabled: true,
allowProvider: false,
allowSeed: false,
},
},
},
}
-

Foydalanuvchi bo‘yicha sozlamalar

Slash buyruqlar mahalliy almashtirishlarni `prefsPath` ga yozadi (standart:
`~/.openclaw/settings/tts.json`, `OPENCLAW_TTS_PREFS` yoki
`messages.tts.prefsPath` bilan almashtiring).

- Saqlanadigan maydonlar:
- `enabled`
- `provider`
- `maxLength` (xulosa chegarasi; standart 1500 belgi)

These override `messages.tts.*` for that host.

## Output formats (fixed)

- **Telegram**: Opus voice note (`opus_48000_64` from ElevenLabs, `opus` from OpenAI).
  - 48kHz / 64kbps is a good voice-note tradeoff and required for the round bubble.
- **Other channels**: MP3 (`mp3_44100_128` from ElevenLabs, `mp3` from OpenAI).
  - 44.1kHz / 128kbps is the default balance for speech clarity.
- **Edge TTS**: uses `edge.outputFormat` (default `audio-24khz-48kbitrate-mono-mp3`).
  - `node-edge-tts` accepts an `outputFormat`, but not all formats are available
    from the Edge service. citeturn2search0
  - Output format values follow Microsoft Speech output formats (including Ogg/WebM Opus). citeturn1search0
  - Telegram `sendVoice` accepts OGG/MP3/M4A; use OpenAI/ElevenLabs if you need
    guaranteed Opus voice notes. citeturn1search1
  - If the configured Edge output format fails, OpenClaw retries with MP3.

OpenAI/ElevenLabs formats are fixed; Telegram expects Opus for voice-note UX.

## Auto-TTS behavior

When enabled, OpenClaw:

- skips TTS if the reply already contains media or a `MEDIA:` directive.
- skips very short replies (< 10 chars).
- summarizes long replies when enabled using `agents.defaults.model.primary` (or `summaryModel`).
- attaches the generated audio to the reply.

If the reply exceeds `maxLength` and summary is off (or no API key for the
summary model), audio
is skipped and the normal text reply is sent.

## Flow diagram

```
Reply -> TTS enabled?
  no  -> send text
  yes -> has media / MEDIA: / short?
          yes -> send text
          no  -> length > limit?
                   no  -> TTS -> attach audio
                   yes -> summary enabled?
                            no  -> send text
                            yes -> summarize (summaryModel or agents.defaults.model.primary)
                                      -> TTS -> attach audio
```

## Slash command usage

There is a single command: `/tts`.
See [Slash commands](/tools/slash-commands) for enablement details.

Discord note: `/tts` is a built-in Discord command, so OpenClaw registers
`/voice` as the native command there. Text `/tts ...` still works.

```
/tts off
/tts always
/tts inbound
/tts tagged
/tts status
/tts provider openai
/tts limit 2000
/tts summary off
/tts audio Hello from OpenClaw
```

Notes:

- Commands require an authorized sender (allowlist/owner rules still apply).
- `commands.text` or native command registration must be enabled.
- `off|always|inbound|tagged` are per‑session toggles (`/tts on` is an alias for `/tts always`).
- `limit` and `summary` are stored in local prefs, not the main config.
- `/tts audio` generates a one-off audio reply (does not toggle TTS on).

## Agent tool

The `tts` tool converts text to speech and returns a `MEDIA:` path. When the
result is Telegram-compatible, the tool includes `[[audio_as_voice]]` so
Telegram sends a voice bubble.

## Gateway RPC

Gateway methods:

- `tts.status`
- `tts.enable`
- `tts.disable`
- `tts.convert`
- `tts.setProvider`
- `tts.providers`
