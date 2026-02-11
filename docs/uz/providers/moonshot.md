---
summary: "Moonshot K2 va Kimi Coding’ni sozlash (alohida provayderlar + kalitlar)"
read_when:
  - Sizga Moonshot K2 (Moonshot Open Platform) va Kimi Coding sozlamalarini taqqoslash kerak
  - Alohida endpointlar, kalitlar va model havolalarini tushunishingiz kerak
  - Har ikkala provayder uchun copy/paste konfiguratsiya kerak
title: "Moonshot AI"
---

# Moonshot AI (Kimi)

Moonshot OpenAI’ga mos endpointlarga ega Kimi API’ni taqdim etadi. Provayderni sozlang va standart modelni `moonshot/kimi-k2.5` qilib belgilang yoki
`kimi-coding/k2p5` bilan Kimi Coding’dan foydalaning.

Joriy Kimi K2 model ID’lari:

{/_moonshot-kimi-k2-ids:start_/ && null}

- `kimi-k2.5`
- `kimi-k2-0905-preview`
- `kimi-k2-turbo-preview`
- `kimi-k2-thinking`
- `kimi-k2-thinking-turbo`
  {/_moonshot-kimi-k2-ids:end_/ && null}

```bash
openclaw onboard --auth-choice moonshot-api-key
```

Kimi Coding:

```bash
openclaw onboard --auth-choice kimi-code-api-key
```

Eslatma: Moonshot va Kimi Coding — alohida provayderlar. Kalitlar o‘zaro almashilmaydi, endpointlar farq qiladi va model havolalari ham boshqacha (Moonshot `moonshot/...` dan, Kimi Coding esa `kimi-coding/...` dan foydalanadi).

## Konfiguratsiya namunasi (Moonshot API)

```json5
{
  env: { MOONSHOT_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "moonshot/kimi-k2.5" },
      models: {
        // moonshot-kimi-k2-aliases:start
        "moonshot/kimi-k2.5": { alias: "Kimi K2.5" },
        "moonshot/kimi-k2-0905-preview": { alias: "Kimi K2" },
        "moonshot/kimi-k2-turbo-preview": { alias: "Kimi K2 Turbo" },
        "moonshot/kimi-k2-thinking": { alias: "Kimi K2 Thinking" },
        "moonshot/kimi-k2-thinking-turbo": { alias: "Kimi K2 Thinking Turbo" },
        // moonshot-kimi-k2-aliases:end
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [
          // moonshot-kimi-k2-models:start
          {
            id: "kimi-k2.5",
            name: "Kimi K2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-0905-preview",
            name: "Kimi K2 0905 Preview",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-turbo-preview",
            name: "Kimi K2 Turbo",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-thinking",
            name: "Kimi K2 Thinking",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-thinking-turbo",
            name: "Kimi K2 Thinking Turbo",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          // moonshot-kimi-k2-models:end
        ],
      },
    },
  },
}
```

## Kimi Coding

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "kimi-coding/k2p5" },
      models: {
        "kimi-coding/k2p5": { alias: "Kimi K2.5" },
      },
    },
  },
}
```

## Eslatmalar

- Moonshot model havolalari `moonshot/<modelId>` formatidan foydalanadi. Kimi Coding model havolalari `kimi-coding/<modelId>` formatidan foydalanadi.
- Agar kerak bo‘lsa, `models.providers` ichida narxlash va kontekst metama’lumotlarini o‘zgartiring.
- Agar Moonshot model uchun boshqa kontekst limitlarini e’lon qilsa,
  `contextWindow` qiymatini mos ravishda sozlang.
- Xalqaro endpoint uchun `https://api.moonshot.ai/v1`, Xitoy endpointi uchun esa `https://api.moonshot.cn/v1` dan foydalaning.
