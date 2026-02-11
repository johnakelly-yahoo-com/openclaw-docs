---
summary: "OpenClaw tomonidan qo‘llab-quvvatlanadigan model provayderlari (LLM’lar)"
read_when:
  - Siz model provayderini tanlamoqchisiz
  - Sizga qo‘llab-quvvatlanadigan LLM backendlari bo‘yicha tezkor umumiy ko‘rinish kerak
title: "Model provayderlari"
---

# Model provayderlari

OpenClaw ko‘plab LLM provayderlaridan foydalana oladi. Provayderni tanlang, autentifikatsiyadan o‘ting, so‘ngra
standart modelni `provider/model` ko‘rinishida belgilang.

Chat kanallari hujjatlarini qidiryapsizmi (WhatsApp/Telegram/Discord/Slack/Mattermost (plagin)/va boshqalar)? [Kanallar](/channels) sahifasiga qarang.

## Ajratilgan: Venice (Venice AI)

Venice — maxfiylikka yo‘naltirilgan inferensiya uchun tavsiya etilgan Venice AI sozlamamiz bo‘lib, murakkab vazifalar uchun Opus’dan foydalanish imkoniyatiga ega.

- Standart: `venice/llama-3.3-70b`
- Eng yaxshi umumiy tanlov: `venice/claude-opus-45` (Opus hanuz eng kuchlisi)

[Venice AI](/providers/venice) sahifasiga qarang.

## Tezkor boshlash

1. Provayder bilan autentifikatsiyadan o‘ting (odatda `openclaw onboard` orqali).
2. Standart modelni belgilang:

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

## Provayder hujjatlari

- [OpenAI (API + Codex)](/providers/openai)
- [Anthropic (API + Claude Code CLI)](/providers/anthropic)
- [Qwen (OAuth)](/providers/qwen)
- [OpenRouter](/providers/openrouter)
- [Vercel AI Gateway](/providers/vercel-ai-gateway)
- [Cloudflare AI Gateway](/providers/cloudflare-ai-gateway)
- [Moonshot AI (Kimi + Kimi Coding)](/providers/moonshot)
- [OpenCode Zen](/providers/opencode)
- [Amazon Bedrock](/providers/bedrock)
- [Z.AI](/providers/zai)
- [Xiaomi](/providers/xiaomi)
- [GLM modellari](/providers/glm)
- [MiniMax](/providers/minimax)
- [Venice (Venice AI, maxfiylikka yo‘naltirilgan)](/providers/venice)
- [Ollama (lokal modellar)](/providers/ollama)
- [Qianfan](/providers/qianfan)

## Transkripsiya provayderlari

- [Deepgram (audio transkripsiya)](/providers/deepgram)

## Hamjamiyat vositalari

- [Claude Max API Proxy](/providers/claude-max-api-proxy) - Claude Max/Pro obunasidan OpenAI’ga mos API endpoint sifatida foydalaning

Provayderlarning to‘liq katalogi (xAI, Groq, Mistral va boshqalar) uchun va ilg‘or sozlamalar uchun,
[Model provayderlari](/concepts/model-providers) sahifasiga qarang.
