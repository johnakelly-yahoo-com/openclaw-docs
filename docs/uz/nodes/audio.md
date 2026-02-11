---
summary: "Kirish audio/ovozli eslatmalar qanday yuklab olinadi, transkripsiya qilinadi va javoblarga kiritiladi"
read_when:
  - Audio transkripsiyasi yoki media bilan ishlashni o‘zgartirish
title: "Audio va ovozli eslatmalar"
---

# Audio / Ovozli eslatmalar — 2026-01-17

## Nimalar ishlaydi

- **Media tushunish (audio)**: Agar audio tushunish yoqilgan bo‘lsa (yoki avtomatik aniqlansa), OpenClaw:
  1. Birinchi audio ilovani (mahalliy yo‘l yoki URL) topadi va kerak bo‘lsa yuklab oladi.
  2. Har bir model yozuviga yuborishdan oldin `maxBytes` ni majburiy qo‘llaydi.
  3. Mos keladigan birinchi model yozuvini tartib bo‘yicha ishga tushiradi (provider yoki CLI).
  4. Agar u muvaffaqiyatsiz bo‘lsa yoki o‘tkazib yuborilsa (hajm/timeout), keyingi yozuvni sinab ko‘radi.
  5. Muvaffaqiyatli bo‘lsa, `Body` ni `[Audio]` blokiga almashtiradi va `{{Transcript}}` ni o‘rnatadi.
- **Buyruqlarni tahlil qilish**: Transkripsiya muvaffaqiyatli bo‘lganda, slash buyruqlar ishlashi uchun `CommandBody`/`RawBody` transkriptga o‘rnatiladi.
- **Batafsil loglash**: `--verbose` rejimida transkripsiya qachon ishga tushgani va qachon body almashtirilgani log qilinadi.

## Avtomatik aniqlash (standart)

Agar siz **modellarni sozlamagan bo‘lsangiz** va `tools.media.audio.enabled` **`false` ga o‘rnatilmagan** bo‘lsa,
OpenClaw quyidagi tartibda avtomatik aniqlaydi va birinchi ishlaydigan variantda to‘xtaydi:

1. **Mahalliy CLI lar** (agar o‘rnatilgan bo‘lsa)
   - `sherpa-onnx-offline` (`SHERPA_ONNX_MODEL_DIR` encoder/decoder/joiner/tokens bilan talab etiladi)
   - `whisper-cli` (`whisper-cpp` dan; `WHISPER_CPP_MODEL` yoki biriktirilgan tiny modeldan foydalanadi)
   - `whisper` (Python CLI; modellarni avtomatik yuklab oladi)
2. **Gemini CLI** (`gemini`) `read_many_files` dan foydalanib
3. **Provider kalitlari** (OpenAI → Groq → Deepgram → Google)

Avtomatik aniqlashni o‘chirish uchun `tools.media.audio.enabled: false` ni o‘rnating.
Moslashtirish uchun `tools.media.audio.models` ni o‘rnating.
Eslatma: Binar aniqlash macOS/Linux/Windows bo‘ylab best-effort; CLI `PATH` da ekanini ta’minlang (`~` ni kengaytiramiz) yoki to‘liq buyruq yo‘li bilan aniq CLI modelini o‘rnating.

## Konfiguratsiya misollari

### Provider + CLI fallback (OpenAI + Whisper CLI)

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        maxBytes: 20971520,
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          {
            type: "cli",
            command: "whisper",
            args: ["--model", "base", "{{MediaPath}}"],
            timeoutSeconds: 45,
          },
        ],
      },
    },
  },
}
```

### Provider-only, scope gating bilan

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        scope: {
          default: "allow",
          rules: [{ action: "deny", match: { chatType: "group" } }],
        },
        models: [{ provider: "openai", model: "gpt-4o-mini-transcribe" }],
      },
    },
  },
}
```

### Faqat provider (Deepgram)

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "deepgram", model: "nova-3" }],
      },
    },
  },
}
```

## Eslatmalar va cheklovlar

- Provider autentifikatsiyasi standart model autentifikatsiya tartibiga amal qiladi (auth profillar, env o‘zgaruvchilar, `models.providers.*.apiKey`).
- `provider: "deepgram"` ishlatilganda Deepgram `DEEPGRAM_API_KEY` ni oladi.
- Deepgram sozlash tafsilotlari: [Deepgram (audio transkripsiya)](/providers/deepgram).
- Audio providerlar `tools.media.audio` orqali `baseUrl`, `headers` va `providerOptions` ni bekor qilishi mumkin.
- Standart hajm cheklovi 20MB (`tools.media.audio.maxBytes`). Haddan katta audio shu model uchun o‘tkazib yuboriladi va keyingi yozuv sinab ko‘riladi.
- Audio uchun standart `maxChars` **o‘rnatilmagan** (to‘liq transkript). Chiqishni qisqartirish uchun `tools.media.audio.maxChars` yoki har bir yozuv uchun `maxChars` ni o‘rnating.
- OpenAI avtomatik standarti `gpt-4o-mini-transcribe`; yuqori aniqlik uchun `model: "gpt-4o-transcribe"` ni o‘rnating.
- Bir nechta ovozli eslatmalarni qayta ishlash uchun `tools.media.audio.attachments` dan foydalaning (`mode: "all"` + `maxAttachments`).
- Transkript shablonlar uchun `{{Transcript}}` sifatida mavjud.
- CLI stdout cheklangan (5MB); CLI chiqishini ixcham saqlang.

## Gotchas

- Scope rules use first-match wins. `chatType` is normalized to `direct`, `group`, or `room`.
- Ensure your CLI exits 0 and prints plain text; JSON needs to be massaged via `jq -r .text`.
- Keep timeouts reasonable (`timeoutSeconds`, default 60s) to avoid blocking the reply queue.
