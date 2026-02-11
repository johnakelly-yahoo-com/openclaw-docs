---
summary: "OpenClaw tomonidan qo‘llab‑quvvatlanadigan model provayderlari (LLMlar)"
read_when:
  - Siz model provayderini tanlamoqchisiz
  - LLM autentifikatsiyasi va model tanlash bo‘yicha tezkor sozlash misollarini xohlaysiz
title: "Model Provayderi Tezkor Boshlash"
---

# Model Provayderlari

OpenClaw ko‘plab LLM provayderlaridan foydalanishi mumkin. Birini tanlang, autentifikatsiya qiling, so‘ng standart modelni `provider/model` sifatida belgilang.

## Ajratib ko‘rsatish: Venice (Venice AI)

Venice — maxfiylikka yo‘naltirilgan inferens uchun tavsiya etiladigan Venice AI sozlamamiz bo‘lib, eng murakkab vazifalar uchun Opus’dan foydalanish imkoniyatiga ega.

- Standart: `venice/llama-3.3-70b`
- Eng yaxshisi: `venice/claude-opus-45` (Opus hanuz eng kuchlisi)

[Venice AI](/providers/venice) sahifasiga qarang.

## Tezkor boshlash (ikki qadam)

1. Provayder bilan autentifikatsiya qiling (odatda `openclaw onboard` orqali).
2. Standart modelni belgilang:

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

## Qo‘llab‑quvvatlanadigan provayderlar (boshlang‘ich to‘plam)

- [OpenAI (API + Codex)](/providers/openai)
- [Anthropic (API + Claude Code CLI)](/providers/anthropic)
- [OpenRouter](/providers/openrouter)
- [Vercel AI Gateway](/providers/vercel-ai-gateway)
- [Cloudflare AI Gateway](/providers/cloudflare-ai-gateway)
- [Moonshot AI (Kimi + Kimi Coding)](/providers/moonshot)
- [Synthetic](/providers/synthetic)
- [OpenCode Zen](/providers/opencode)
- [Z.AI](/providers/zai)
- [GLM modellari](/providers/glm)
- [MiniMax](/providers/minimax)
- [Venice (Venice AI)](/providers/venice)
- [Amazon Bedrock](/providers/bedrock)
- [Qianfan](/providers/qianfan)

To‘liq provayderlar katalogi uchun (xAI, Groq, Mistral va boshqalar) va kengaytirilgan sozlashlar uchun,
[Model provayderlari](/concepts/model-providers) sahifasiga qarang.
