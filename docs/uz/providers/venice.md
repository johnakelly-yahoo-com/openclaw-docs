---
summary: "Use Venice AI privacy-focused models in OpenClaw"
read_when:
  - You want privacy-focused inference in OpenClaw
  - You want Venice AI setup guidance
title: "Venice AI"
---

# Venice AI (Venice highlight)

**Venice** is our highlight Venice setup for privacy-first inference with optional anonymized access to proprietary models.

Venice AI provides privacy-focused AI inference with support for uncensored models and access to major proprietary models through their anonymized proxy. All inference is private by default—no training on your data, no logging.

## Why Venice in OpenClaw

- **Private inference** for open-source models (no logging).
- **Uncensored models** when you need them.
- **Anonymized access** to proprietary models (Opus/GPT/Gemini) when quality matters.
- OpenAI-compatible `/v1` endpoints.

## Privacy Modes

Venice offers two privacy levels — understanding this is key to choosing your model:

| Mode           | Description                                                                                                                                                             | Models                                                         |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Private**    | Fully private. Prompts/responses are **never stored or logged**. Ephemeral.                                             | Llama, Qwen, DeepSeek, Venice Uncensored, etc. |
| **Anonymized** | Proxied through Venice with metadata stripped. The underlying provider (OpenAI, Anthropic) sees anonymized requests. | Claude, GPT, Gemini, Grok, Kimi, MiniMax                       |

## Features

- **Privacy-focused**: Choose between "private" (fully private) and "anonymized" (proxied) modes
- **Uncensored models**: Access to models without content restrictions
- **Major model access**: Use Claude, GPT-5.2, Gemini, Grok via Venice's anonymized proxy
- **OpenAI-compatible API**: Standard `/v1` endpoints for easy integration
- **Streaming**: ✅ Supported on all models
- **Function calling**: ✅ Supported on select models (check model capabilities)
- **Vision**: ✅ Supported on models with vision capability
- **No hard rate limits**: Fair-use throttling may apply for extreme usage

## Setup

### 1. Get API Key

1. Sign up at [venice.ai](https://venice.ai)
2. Go to **Settings → API Keys → Create new key**
3. Copy your API key (format: `vapi_xxxxxxxxxxxx`)

### 2) Configure OpenClaw

1. **Variant A: Muhit o‘zgaruvchisi**

```bash
2. export VENICE_API_KEY="vapi_xxxxxxxxxxxx"
```

3. **Variant B: Interaktiv sozlash (Tavsiya etiladi)**

```bash
4. openclaw onboard --auth-choice venice-api-key
```

5. Bu quyidagilarni amalga oshiradi:

1. 6. API kalitingizni so‘raydi (yoki mavjud `VENICE_API_KEY` dan foydalanadi)
2. 7. Mavjud barcha Venice modellarini ko‘rsatadi
3. 8. Standart modelingizni tanlashga imkon beradi
4. 9. Provayderni avtomatik sozlaydi

10) **Variant C: Interaktiv bo‘lmagan**

```bash
11. openclaw onboard --non-interactive \
  --auth-choice venice-api-key \
  --venice-api-key "vapi_xxxxxxxxxxxx"
```

### 12. 3. 13. Sozlashni tekshirish

```bash
openclaw chat --model venice/llama-3.3-70b "Hello, are you working?"
```

## 15. Model tanlash

16. Sozlashdan so‘ng, OpenClaw barcha mavjud Venice modellarini ko‘rsatadi. 17. Ehtiyojlaringizga qarab tanlang:

- **Sukut bo‘yicha (bizning tanlovimiz)**: shaxsiylik va muvozanatli unumdorlik uchun `venice/llama-3.3-70b`.
- 19. **Eng yuqori umumiy sifat**: `venice/claude-opus-45` — murakkab vazifalar uchun (Opus hanuzgacha eng kuchlisi).
- 20. **Maxfiylik**: To‘liq maxfiy inferensiya uchun "private" modellarni tanlang.
- 21. **Imkoniyat**: Venice’ning proksi xizmati orqali Claude, GPT, Gemini’dan foydalanish uchun "anonymized" modellarni tanlang.

22. Standart modelingizni istalgan vaqtda o‘zgartiring:

```bash
23. openclaw models set venice/claude-opus-45
openclaw models set venice/llama-3.3-70b
```

24. Barcha mavjud modellarni ro‘yxatlash:

```bash
25. openclaw models list | grep venice
```

## 26. `openclaw configure` orqali sozlash

1. 27. `openclaw configure` ni ishga tushiring
2. 28. **Model/auth** ni tanlang
3. 29. **Venice AI** ni tanlang

## 30) Qaysi modelni ishlatishim kerak?

| 31. Foydalanish holati            | 32. Tavsiya etilgan model            | 33. Sababi                                                      |
| -------------------------------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| 34. **Umumiy chat**               | 35. `llama-3.3-70b`                  | 36. Har tomonlama yaxshi, to‘liq maxfiy                         |
| 37. **Eng yuqori umumiy sifat**   | 38. `claude-opus-45`                 | 39. Opus murakkab vazifalar uchun hanuzgacha eng kuchlisi       |
| 40. **Maxfiylik + Claude sifati** | 41. `claude-opus-45`                 | 42. Anonimlashtirilgan proksi orqali eng yaxshi mantiqiy xulosa |
| 43. **Dasturlash**                | 44. `qwen3-coder-480b-a35b-instruct` | 45. Kodlash uchun optimallashtirilgan, 262k kontekst            |
| 46. **Ko‘rish vazifalari**        | 47. `qwen3-vl-235b-a22b`             | 48. Eng yaxshi xususiy ko‘rish modeli                           |
| 49. **Tsenzurasiz**               | 50. `venice-uncensored`              | No content restrictions                                                                |
| **Fast + cheap**                                         | `qwen3-4b`                                                  | Lightweight, still capable                                                             |
| **Complex reasoning**                                    | `deepseek-v3.2`                                             | Strong reasoning, private                                                              |

## Available Models (25 Total)

### Private Models (15) — Fully Private, No Logging

| Model ID                         | Name                                       | Context (tokens) | Features                      |
| -------------------------------- | ------------------------------------------ | ----------------------------------- | ----------------------------- |
| `llama-3.3-70b`                  | Llama 3.3 70B              | 131k                                | General                       |
| `llama-3.2-3b`                   | Llama 3.2 3B               | 131k                                | Fast, lightweight             |
| `hermes-3-llama-3.1-405b`        | Hermes 3 Llama 3.1 405B    | 131k                                | Complex tasks                 |
| `qwen3-235b-a22b-thinking-2507`  | Qwen3 235B Thinking                        | 131k                                | Reasoning                     |
| `qwen3-235b-a22b-instruct-2507`  | Qwen3 235B Instruct                        | 131k                                | General                       |
| `qwen3-coder-480b-a35b-instruct` | Qwen3 Coder 480B                           | 262k                                | Code                          |
| `qwen3-next-80b`                 | Qwen3 Next 80B                             | 262k                                | General                       |
| `qwen3-vl-235b-a22b`             | Qwen3 VL 235B                              | 262k                                | Vision                        |
| `qwen3-4b`                       | Venice Small (Qwen3 4B) | 32k                                 | Fast, reasoning               |
| `deepseek-v3.2`                  | DeepSeek V3.2              | 163k                                | Mantiqiy fikrlash             |
| `venice-uncensored`              | Venice Tsenzurasiz                         | 32k                                 | Tsenzurasiz                   |
| `mistral-31-24b`                 | Venice O‘rta (Mistral)  | 131k                                | Ko‘rish                       |
| `google-gemma-3-27b-it`          | Gemma 3 27B Instruct                       | 202k                                | Ko‘rish                       |
| `openai-gpt-oss-120b`            | OpenAI GPT OSS 120B                        | 131k                                | Umumiy                        |
| `zai-org-glm-4.7`                | GLM 4.7                    | 202k                                | Mantiqiy fikrlash, ko‘p tilli |

### Anonimlashtirilgan modellar (10) — Venice proksi orqali

| Model ID                 | Asl                               | Kontekst (tokenlar) | Xususiyatlar               |
| ------------------------ | --------------------------------- | -------------------------------------- | -------------------------- |
| `claude-opus-45`         | Claude Opus 4.5   | 202k                                   | Mantiqiy fikrlash, ko‘rish |
| `claude-sonnet-45`       | Claude Sonnet 4.5 | 202k                                   | Mantiqiy fikrlash, ko‘rish |
| `openai-gpt-52`          | GPT-5.2           | 262k                                   | Mantiqiy fikrlash          |
| `openai-gpt-52-codex`    | GPT-5.2 Codex     | 262k                                   | Mantiqiy fikrlash, ko‘rish |
| `gemini-3-pro-preview`   | Gemini 3 Pro                      | 202k                                   | Mantiqiy fikrlash, ko‘rish |
| `gemini-3-flash-preview` | Gemini 3 Flash                    | 262k                                   | Mantiqiy fikrlash, ko‘rish |
| `grok-41-fast`           | Grok 4.1 Fast     | 262k                                   | Mantiqiy fikrlash, ko‘rish |
| `grok-code-fast-1`       | Grok Code Fast 1                  | 262k                                   | Mantiqiy fikrlash, kod     |
| `kimi-k2-thinking`       | Kimi K2 Thinking                  | 262k                                   | Mantiqiy fikrlash          |
| `minimax-m21`            | MiniMax M2.1      | 202k                                   | Mantiqiy fikrlash          |

## Modelni aniqlash

OpenClaw `VENICE_API_KEY` o‘rnatilganda Venice API’dan modellarni avtomatik aniqlaydi. Agar API’ga ulanib bo‘lmasa, u statik katalogga qaytadi.

`/models` endpointi ommaviy (ro‘yxatlash uchun autentifikatsiya talab qilinmaydi), ammo inference uchun yaroqli API kaliti kerak.

## Streaming va vositalarni qo‘llab-quvvatlash

| Xususiyat                 | Qo‘llab-quvvatlash                                                                        |
| ------------------------- | ----------------------------------------------------------------------------------------- |
| **Streaming**             | ✅ Barcha modellar                                                                         |
| **Funksiya chaqiruvlari** | ✅ Ko‘pchilik modellar (`supportsFunctionCalling` ni API’da tekshiring) |
| **Ko‘rish/Rasmlar**       | ✅ "Vision" xususiyati bilan belgilangan modellar                                          |
| **JSON rejimi**           | ✅ `response_format` orqali qo‘llab-quvvatlanadi                                           |

## Narxlash

Venice kreditga asoslangan tizimdan foydalanadi. Joriy tariflar uchun [venice.ai/pricing](https://venice.ai/pricing) ni tekshiring:

- **Xususiy modellar**: Odatda arzonroq
- **Anonimlashtirilgan modellar**: To‘g‘ridan-to‘g‘ri API narxlariga o‘xshash + kichik Venice to‘lovi

## Taqqoslash: Venice va To‘g‘ridan-to‘g‘ri API

| Jihat            | Venice (Anonimlashtirilgan)      | To‘g‘ridan-to‘g‘ri API      |
| ---------------- | --------------------------------------------------- | --------------------------- |
| **Maxfiylik**    | Metama’lumotlar olib tashlanadi, anonimlashtiriladi | Hisobingiz bilan bog‘langan |
| **Kechikish**    | +10–50 ms (proksi)               | To‘g‘ridan-to‘g‘ri          |
| **Xususiyatlar** | Ko‘pchilik xususiyatlar qo‘llab-quvvatlanadi        | Full features               |
| **Billing**      | Venice credits                                      | Provider billing            |

## Usage Examples

```bash
# Use default private model
openclaw chat --model venice/llama-3.3-70b

# Use Claude via Venice (anonymized)
openclaw chat --model venice/claude-opus-45

# Use uncensored model
openclaw chat --model venice/venice-uncensored

# Use vision model with image
openclaw chat --model venice/qwen3-vl-235b-a22b

# Use coding model
openclaw chat --model venice/qwen3-coder-480b-a35b-instruct
```

## Troubleshooting

### API key not recognized

```bash
echo $VENICE_API_KEY
openclaw models list | grep venice
```

Ensure the key starts with `vapi_`.

### Model not available

The Venice model catalog updates dynamically. Run `openclaw models list` to see currently available models. Ba’zi modellar vaqtincha oflayn bo‘lishi mumkin.

### Connection issues

Venice API is at `https://api.venice.ai/api/v1`. Ensure your network allows HTTPS connections.

## Konfiguratsiya fayli namunasi

```json5
{
  env: { VENICE_API_KEY: "vapi_..." },
  agents: { defaults: { model: { primary: "venice/llama-3.3-70b" } } },
  models: {
    mode: "merge",
    providers: {
      venice: {
        baseUrl: "https://api.venice.ai/api/v1",
        apiKey: "${VENICE_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "llama-3.3-70b",
            name: "Llama 3.3 70B",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 131072,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Links

- [Venice AI](https://venice.ai)
- [API Documentation](https://docs.venice.ai)
- [Pricing](https://venice.ai/pricing)
- [Status](https://status.venice.ai)
