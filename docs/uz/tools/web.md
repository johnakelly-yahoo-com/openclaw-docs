---
summary: "Veb qidiruv + fetch vositalari (Brave Search API, Perplexity direct/OpenRouter)"
read_when:
  - Siz web_search yoki web_fetch ni yoqmoqchisiz
  - Sizga Brave Search API kalitini sozlash kerak
  - Siz veb qidiruv uchun Perplexity Sonar’dan foydalanmoqchisiz
title: "Veb vositalar"
---

# Veb vositalar

OpenClaw ikkita yengil veb vositani taqdim etadi:

- `web_search` — Brave Search API (standart) yoki Perplexity Sonar (toʻgʻridan-toʻgʻri yoki OpenRouter orqali) orqali vebni qidiradi.
- `web_fetch` — HTTP fetch + oʻqilishi qulay chiqarish (HTML → markdown/text).

Bular brauzer avtomatlashtirish vositalari **emas**. JS-ga boy saytlar yoki loginlar uchun
[Browser tool](/tools/browser) dan foydalaning.

## Qanday ishlaydi

- `web_search` sozlangan provayderingizni chaqiradi va natijalarni qaytaradi.
  - **Brave** (standart): tuzilgan natijalarni (sarlavha, URL, snippet) qaytaradi.
  - **Perplexity**: real vaqt veb qidiruviga asoslangan, iqtiboslar bilan AI tomonidan sintez qilingan javoblarni qaytaradi.
- Natijalar soʻrov boʻyicha 15 daqiqaga keshlanadi (sozlanishi mumkin).
- `web_fetch` oddiy HTTP GET bajaradi va oʻqilishi qulay kontentni ajratib oladi
  (HTML → markdown/text). U JavaScript’ni **bajarmaydi**.
- `web_fetch` standart holatda yoqilgan (agar aniq oʻchirib qoʻyilmagan boʻlsa).

## Qidiruv provayderini tanlash

| Provayder                               | Afzalliklar                                                  | Kamchiliklar                                       | API kaliti                                     |
| --------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------- | ---------------------------------------------- |
| **Brave** (standart) | Tezkor, tuzilgan natijalar, bepul tarif                      | Anʼanaviy qidiruv natijalari                       | `BRAVE_API_KEY`                                |
| **Perplexity**                          | AI tomonidan sintez qilingan javoblar, iqtiboslar, real vaqt | Perplexity yoki OpenRouter’ga kirish talab etiladi | `OPENROUTER_API_KEY` yoki `PERPLEXITY_API_KEY` |

Provayderga xos tafsilotlar uchun [Brave Search setup](/brave-search) va [Perplexity Sonar](/perplexity) sahifalariga qarang.

Provayderni konfiguratsiyada belgilang:

```json5
{
  tools: {
    web: {
      search: {
        provider: "brave", // or "perplexity"
      },
    },
  },
}
```

Misol: Perplexity Sonar’ga oʻtish (toʻgʻridan-toʻgʻri API):

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

## Brave API kalitini olish

1. [https://brave.com/search/api/](https://brave.com/search/api/) manzilida Brave Search API hisobini yarating
2. Boshqaruv panelida **Data for Search** rejasini tanlang (“Data for AI” emas) va API kalitini yarating.
3. Kalitni konfiguratsiyada saqlash uchun `openclaw configure --section web` buyrug‘ini ishga tushiring (tavsiya etiladi) yoki muhitda `BRAVE_API_KEY` ni o‘rnating.

Brave bepul darajani hamda pullik rejalarni taqdim etadi; joriy cheklovlar va narxlarni Brave API portalida tekshiring.

### Kalitni qayerga o‘rnatish (tavsiya etiladi)

**Tavsiya etiladi:** `openclaw configure --section web` buyrug‘ini ishga tushiring. U kalitni `~/.openclaw/openclaw.json` faylida `tools.web.search.apiKey` ostida saqlaydi.

**Muhit orqali muqobil:** Gateway jarayoni muhitida `BRAVE_API_KEY` ni o‘rnating. Gateway o‘rnatilishi uchun uni `~/.openclaw/.env` fayliga (yoki xizmat muhitingizga) joylashtiring. [Env vars](/help/faq#how-does-openclaw-load-environment-variables) sahifasiga qarang.

## Perplexity’dan foydalanish (to‘g‘ridan-to‘g‘ri yoki OpenRouter orqali)

Perplexity Sonar modellari ichki veb-qidiruv imkoniyatlariga ega va manbalar bilan AI tomonidan sintez qilingan javoblarni qaytaradi. Ularni OpenRouter orqali ishlatishingiz mumkin (kredit karta talab qilinmaydi — kripto/prepaid qo‘llab-quvvatlanadi).

### OpenRouter API kalitini olish

1. [https://openrouter.ai/](https://openrouter.ai/) manzilida hisob yarating
2. Hisobingizga kreditlar qo‘shing (kripto, prepaid yoki kredit karta qo‘llab-quvvatlanadi)
3. Hisob sozlamalarida API kalitini yarating

### Perplexity qidiruvini sozlash

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        provider: "perplexity",
        perplexity: {
          // API key (optional if OPENROUTER_API_KEY or PERPLEXITY_API_KEY is set)
          apiKey: "sk-or-v1-...",
          // Base URL (key-aware default if omitted)
          baseUrl: "https://openrouter.ai/api/v1",
          // Model (defaults to perplexity/sonar-pro)
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

**Muhit orqali muqobil:** Gateway muhitida `OPENROUTER_API_KEY` yoki `PERPLEXITY_API_KEY` ni o‘rnating. Gateway o‘rnatilishi uchun uni `~/.openclaw/.env` fayliga joylashtiring.

Agar base URL o‘rnatilmagan bo‘lsa, OpenClaw API kaliti manbasiga qarab standartni tanlaydi:

- `PERPLEXITY_API_KEY` yoki `pplx-...` → `https://api.perplexity.ai`
- `OPENROUTER_API_KEY` yoki `sk-or-...` → `https://openrouter.ai/api/v1`
- Noma’lum kalit formatlari → OpenRouter (xavfsiz zaxira variant)

### Mavjud Perplexity modellari

| Model                                                | Tavsif                                             | Eng mos keladi    |
| ---------------------------------------------------- | -------------------------------------------------- | ----------------- |
| `perplexity/sonar`                                   | Veb-qidiruv bilan tezkor savol-javob               | Tezkor qidiruvlar |
| `perplexity/sonar-pro` (standart) | Veb-qidiruv bilan ko‘p bosqichli mulohaza yuritish | Murakkab savollar |
| `perplexity/sonar-reasoning-pro`                     | Fikr zanjiri tahlili                               | Chuqur tadqiqot   |

## web_search

Sozlangan provayderingizdan foydalanib vebni qidiring.

### Talablar

- `tools.web.search.enabled` `false` bo‘lmasligi kerak (standart: yoqilgan)
- Tanlangan provayder uchun API kaliti:
  - **Brave**: `BRAVE_API_KEY` yoki `tools.web.search.apiKey`
  - **Perplexity**: `OPENROUTER_API_KEY`, `PERPLEXITY_API_KEY` yoki `tools.web.search.perplexity.apiKey`

### Konfiguratsiya

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        apiKey: "BRAVE_API_KEY_HERE", // optional if BRAVE_API_KEY is set
        maxResults: 5,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
      },
    },
  },
}
```

### Asbob parametrlari

- `query` (majburiy)
- `count` (1–10; konfiguratsiyadan standart qiymat)
- `country` (ixtiyoriy): mintaqaga xos natijalar uchun 2 harfli mamlakat kodi (masalan, "DE", "US", "ALL"). Agar ko‘rsatilmasa, Brave o‘zining standart mintaqasini tanlaydi.
- `search_lang` (ixtiyoriy): qidiruv natijalari uchun ISO til kodi (masalan, "de", "en", "fr")
- `ui_lang` (ixtiyoriy): UI elementlari uchun ISO til kodi
- `freshness` (ixtiyoriy, faqat Brave): topilgan vaqt bo‘yicha filtrlash (`pd`, `pw`, `pm`, `py` yoki `YYYY-MM-DDtoYYYY-MM-DD`)

**Misollar:**

```javascript
// German-specific search
await web_search({
  query: "TV online schauen",
  count: 10,
  country: "DE",
  search_lang: "de",
});

// French search with French UI
await web_search({
  query: "actualités",
  country: "FR",
  search_lang: "fr",
  ui_lang: "fr",
});

// Recent results (past week)
await web_search({
  query: "TMBG interview",
  freshness: "pw",
});
```

## web_fetch

URL manzilini olib, o‘qilishi qulay kontentni ajratib oling.

### web_fetch talablari

- `tools.web.fetch.enabled` `false` bo‘lmasligi kerak (standart: yoqilgan)
- Ixtiyoriy Firecrawl zaxira varianti: `tools.web.fetch.firecrawl.apiKey` yoki `FIRECRAWL_API_KEY` ni sozlang.

### web_fetch konfiguratsiyasi

```json5
{
  tools: {
    web: {
      fetch: {
        enabled: true,
        maxChars: 50000,
        maxCharsCap: 50000,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
        maxRedirects: 3,
        userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        readability: true,
        firecrawl: {
          enabled: true,
          apiKey: "FIRECRAWL_API_KEY_HERE", // optional if FIRECRAWL_API_KEY is set
          baseUrl: "https://api.firecrawl.dev",
          onlyMainContent: true,
          maxAgeMs: 86400000, // ms (1 day)
          timeoutSeconds: 60,
        },
      },
    },
  },
}
```

### web_fetch vositasi parametrlari

- `url` (majburiy, faqat http/https)
- `extractMode` (`markdown` | `text`)
- `maxChars` (uzun sahifalarni qisqartirish)

Eslatmalar:

- `web_fetch` avval Readability (asosiy kontentni ajratish) dan foydalanadi, so‘ng (agar sozlangan bo‘lsa) Firecrawl. Agar ikkalasi ham muvaffaqiyatsiz bo‘lsa, vosita xato qaytaradi.
- Firecrawl so‘rovlari botlardan himoyalanish rejimidan foydalanadi va natijalarni standart bo‘yicha keshlaydi.
- `web_fetch` standart bo‘yicha Chrome’ga o‘xshash User-Agent va `Accept-Language` yuboradi; kerak bo‘lsa `userAgent` ni o‘zgartiring.
- `web_fetch` xususiy/ichki xost nomlarini bloklaydi va yo‘naltirishlarni qayta tekshiradi (`maxRedirects` bilan cheklash).
- `maxChars` qiymati `tools.web.fetch.maxCharsCap` ga moslab cheklanadi.
- `web_fetch` eng yaxshi urinish asosida kontent ajratadi; ayrim saytlar uchun brauzer vositasi kerak bo‘ladi.
- Kalitni sozlash va xizmat tafsilotlari uchun [Firecrawl](/tools/firecrawl) ga qarang.
- Takroriy yuklab olishlarni kamaytirish uchun javoblar keshlanadi (standart 15 daqiqa).
- Agar vosita profillari/allowlistlardan foydalansangiz, `web_search`/`web_fetch` yoki `group:web` ni qo‘shing.
- Agar Brave kaliti yo‘q bo‘lsa, `web_search` hujjatlar havolasi bilan qisqa sozlash bo‘yicha ko‘rsatma qaytaradi.
