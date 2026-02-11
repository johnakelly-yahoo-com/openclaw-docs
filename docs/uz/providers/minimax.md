---
summary: "OpenClaw’da MiniMax M2.1’dan foydalanish"
read_when:
  - Siz OpenClaw’da MiniMax modellarini xohlaysiz
  - Sizga MiniMax sozlash bo‘yicha yo‘riqnoma kerak
title: "MiniMax"
---

# MiniMax

MiniMax — **M2/M2.1** model oilasini yaratadigan AI kompaniya. Joriy kodlashga yo‘naltirilgan reliz — **MiniMax M2.1** (2025-yil 23-dekabr), real hayotdagi murakkab vazifalar uchun yaratilgan.

Manba: [MiniMax M2.1 reliz eslatmasi](https://www.minimax.io/news/minimax-m21)

## Modelga umumiy nazar (M2.1)

MiniMax M2.1 dagi quyidagi yaxshilanishlarni ta’kidlaydi:

- Kuchliroq **ko‘p tilli kodlash** (Rust, Java, Go, C++, Kotlin, Objective-C, TS/JS).
- Yaxshiroq **veb/ilova ishlab chiqish** va estetik chiqish sifati (jumladan, native mobil).
- Ofis uslubidagi ish jarayonlari uchun **murakkab ko‘rsatmalarni** yaxshiroq qayta ishlash, navbatma-navbat fikrlash va integratsiyalashgan cheklovlarni bajarishga asoslangan.
- Token sarfi kamroq bo‘lgan va iteratsiya sikllari tezroq bo‘lgan **yanada ixcham javoblar**.
- Kuchliroq **tool/agent framework** mosligi va kontekstni boshqarish (Claude Code,
  Droid/Factory AI, Cline, Kilo Code, Roo Code, BlackBox).
- Yuqori sifatli **dialog va texnik yozuv** natijalari.

## MiniMax M2.1 va MiniMax M2.1 Lightning taqqoslanishi

- **Tezlik:** Lightning — MiniMax narxlash hujjatlarida “tezkor” variant.
- **Narx:** Narxlashda kirish (input) narxi bir xil, ammo Lightning chiqish (output) narxi yuqoriroq.
- **Kodlash rejasini yo‘naltirish:** Lightning backend’i MiniMax kodlash rejasida to‘g‘ridan-to‘g‘ri mavjud emas. MiniMax so‘rovlarning ko‘p qismini avtomatik ravishda Lightning’ga yo‘naltiradi, ammo trafik oshib ketganda oddiy M2.1 backend’iga qaytadi.

## Sozlamani tanlang

### MiniMax OAuth (Coding Plan) — tavsiya etiladi

**Eng mos:** MiniMax Coding Plan orqali OAuth bilan tez sozlash, API kaliti talab qilinmaydi.

Biriktirilgan OAuth plaginini yoqing va autentifikatsiyadan o‘ting:

```bash
openclaw plugins enable minimax-portal-auth  # agar allaqachon yuklangan bo‘lsa, o‘tkazib yuboring.
openclaw gateway restart  # agar gateway allaqachon ishlayotgan bo‘lsa, qayta ishga tushiring
openclaw onboard --auth-choice minimax-portal
```

Sizdan endpoint tanlash so‘raladi:

- **Global** — Xalqaro foydalanuvchilar (`api.minimax.io`)
- **CN** - Xitoydagi foydalanuvchilar (`api.minimaxi.com`)

Batafsil ma’lumot uchun [MiniMax OAuth plugin README](https://github.com/openclaw/openclaw/tree/main/extensions/minimax-portal-auth) sahifasiga qarang.

### MiniMax M2.1 (API kaliti)

**Eng mos:** Anthropic-ga mos API bilan xostlangan MiniMax.

CLI orqali sozlang:

- `openclaw configure` ni ishga tushiring
- **Model/auth** ni tanlang
- **MiniMax M2.1** ni tanlang

```json5
{
  env: { MINIMAX_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "minimax/MiniMax-M2.1" } } },
  models: {
    mode: "merge",
    providers: {
      minimax: {
        baseUrl: "https://api.minimax.io/anthropic",
        apiKey: "${MINIMAX_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "MiniMax-M2.1",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            cost: { input: 15, output: 60, cacheRead: 2, cacheWrite: 10 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

### MiniMax M2.1 zaxira (Opus asosiy)

**Eng yaxshisi uchun:** asosiy sifatida Opus 4.6’ni saqlang, nosozlikda MiniMax M2.1’ga o‘ting.

```json5
{
  env: { MINIMAX_API_KEY: "sk-..." },
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "opus" },
        "minimax/MiniMax-M2.1": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["minimax/MiniMax-M2.1"],
      },
    },
  },
}
```

### Ixtiyoriy: LM Studio orqali lokal (qo‘lda)

**Eng mos:** LM Studio bilan lokal inferens.
Biz kuchli apparatda (masalan, desktop/server) LM Studio’ning lokal serveridan foydalangan holda MiniMax M2.1 bilan kuchli natijalarni ko‘rdik.

`openclaw.json` orqali qo‘lda sozlang:

```json5
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/minimax-m2.1-gs32" },
      models: { "lmstudio/minimax-m2.1-gs32": { alias: "Minimax" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [
          {
            id: "minimax-m2.1-gs32",
            name: "MiniMax M2.1 GS32",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 196608,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## `openclaw configure` orqali sozlang

JSON tahrirlamasdan MiniMax’ni sozlash uchun interaktiv konfiguratsiya ustasidan foydalaning:

1. `openclaw configure` ni ishga tushiring.
2. **Model/auth** ni tanlang.
3. **MiniMax M2.1** ni tanlang.
4. So‘ralganda standart modelingizni tanlang.

## Konfiguratsiya variantlari

- `models.providers.minimax.baseUrl`: `https://api.minimax.io/anthropic` ni afzal ko‘ring (Anthropic-ga mos); OpenAI-ga mos payloadlar uchun `https://api.minimax.io/v1` ixtiyoriy.
- `models.providers.minimax.api`: `anthropic-messages` ni afzal ko‘ring; OpenAI-ga mos payloadlar uchun `openai-completions` ixtiyoriy.
- `models.providers.minimax.apiKey`: MiniMax API kaliti (`MINIMAX_API_KEY`).
- `models.providers.minimax.models`: `id`, `name`, `reasoning`, `contextWindow`, `maxTokens`, `cost` ni aniqlang.
- `agents.defaults.models`: allowlist’ga kiritmoqchi bo‘lgan modellarga alias bering.
- `models.mode`: agar MiniMax’ni ichki (built‑in) modellar bilan birga qo‘shmoqchi bo‘lsangiz, `merge` holatida qoldiring.

## Eslatmalar

- Model havolalari `minimax/<model>` ko‘rinishida bo‘ladi.
- Coding Plan foydalanish API’si: `https://api.minimaxi.com/v1/api/openplatform/coding_plan/remains` (coding plan kalitini talab qiladi).
- Aniq xarajatlarni kuzatish kerak bo‘lsa, `models.json` dagi narx qiymatlarini yangilang.
- MiniMax Coding Plan uchun referal havola (10% chegirma): [https://platform.minimax.io/subscribe/coding-plan?code=DbXJTRClnb&source=link](https://platform.minimax.io/subscribe/coding-plan?code=DbXJTRClnb&source=link)
- Provayder qoidalari uchun [/concepts/model-providers](/concepts/model-providers) sahifasiga qarang.
- Almashtirish uchun `openclaw models list` va `openclaw models set minimax/MiniMax-M2.1` dan foydalaning.

## Nosozliklarni bartaraf etish

### “Noma’lum model: minimax/MiniMax-M2.1”

Bu odatda **MiniMax provayderi sozlanmaganini** anglatadi (provayder yozuvi yo‘q va MiniMax autentifikatsiya profili/muhit kaliti topilmadi). Ushbu aniqlash muammosiga tuzatish **2026.1.12** versiyasida mavjud (yozish vaqtida reliz qilinmagan). Tuzatish usullari:

- **2026.1.12** versiyasiga yangilang (yoki manbadan `main` ni ishga tushiring), so‘ng gateway’ni qayta ishga tushiring.
- `openclaw configure` ni ishga tushirib, **MiniMax M2.1** ni tanlang, yoki
- `models.providers.minimax` blokini qo‘lda qo‘shing, yoki
- Provayder kiritilishi uchun `MINIMAX_API_KEY` (yoki MiniMax auth profili) ni sozlang.

Model ID **katta‑kichik harflarga sezgir** ekanligiga ishonch hosil qiling:

- `minimax/MiniMax-M2.1`
- `minimax/MiniMax-M2.1-lightning`

So‘ng yana tekshiring:

```bash
openclaw models list
```
