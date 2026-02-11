---
summary: "Perplexity Sonar setup for web_search"
read_when:
  - Siz web qidiruv uchun Perplexity Sonar’dan foydalanmoqchisiz
  - Sizga PERPLEXITY_API_KEY yoki OpenRouter sozlamasi kerak
title: "Perplexity Sonar"
---

# Perplexity Sonar

OpenClaw `web_search` vositasi uchun Perplexity Sonar’dan foydalanishi mumkin. Siz Perplexity’ning to‘g‘ridan-to‘g‘ri API’si orqali yoki OpenRouter orqali ulanishingiz mumkin.

## API variantlari

### Perplexity (to‘g‘ridan-to‘g‘ri)

- Asosiy URL: [https://api.perplexity.ai](https://api.perplexity.ai)
- Muhit o‘zgaruvchisi: `PERPLEXITY_API_KEY`

### OpenRouter (muqobil)

- Asosiy URL: [https://openrouter.ai/api/v1](https://openrouter.ai/api/v1)
- Muhit o‘zgaruvchisi: `OPENROUTER_API_KEY`
- Oldindan to‘lov/kripto kreditlarini qo‘llab-quvvatlaydi.

## Konfiguratsiya namunasi

```json5
{
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...",
          baseUrl: "https://api.perplexity.ai",
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

## Brave’dan o‘tish

```json5
{
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...",
          baseUrl: "https://api.perplexity.ai",
        },
      },
    },
  },
}
```

Agar `PERPLEXITY_API_KEY` va `OPENROUTER_API_KEY` ikkalasi ham o‘rnatilgan bo‘lsa, aniqlashtirish uchun `tools.web.search.perplexity.baseUrl`ni (yoki `tools.web.search.perplexity.apiKey`ni) belgilang.

Agar asosiy URL o‘rnatilmagan bo‘lsa, OpenClaw API kaliti manbasiga qarab sukut bo‘yicha qiymatni tanlaydi:

- `PERPLEXITY_API_KEY` yoki `pplx-...` → to‘g‘ridan-to‘g‘ri Perplexity (`https://api.perplexity.ai`)
- `OPENROUTER_API_KEY` yoki `sk-or-...` → OpenRouter (`https://openrouter.ai/api/v1`)
- Noma’lum kalit formatlari → OpenRouter (xavfsiz zaxira)

## Modellar

- `perplexity/sonar` — veb qidiruv bilan tezkor savol-javob
- `perplexity/sonar-pro` (sukut bo‘yicha) — ko‘p bosqichli mulohaza + veb qidiruv
- `perplexity/sonar-reasoning-pro` — chuqur tadqiqot

To‘liq web_search konfiguratsiyasi uchun [Web tools](/tools/web) ga qarang.
