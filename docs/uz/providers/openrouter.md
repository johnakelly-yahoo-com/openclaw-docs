---
summary: "22. OpenClaw’da ko‘plab modellarga kirish uchun OpenRouter’ning yagona API’sidan foydalaning"
read_when:
  - 23. Ko‘plab LLM’lar uchun bitta API kalitini xohlaysiz
  - 24. OpenClaw’da OpenRouter orqali modellarni ishga tushirmoqchisiz
title: "25. OpenRouter"
---

# 26. OpenRouter

27. OpenRouter **yagona API** taqdim etadi, u bitta
    endpoint va API kaliti ortida ko‘plab modellarga so‘rovlarni yo‘naltiradi. 28. U OpenAI bilan mos keladi, shuning uchun ko‘pchilik OpenAI SDK’lari bazaviy URL’ni almashtirish orqali ishlaydi.

## 29. CLI sozlash

```bash
openclaw onboard --auth-choice apiKey --token-provider openrouter --token "$OPENROUTER_API_KEY"
```

## 31. Konfiguratsiya parchasi

```json5
{
  env: { OPENROUTER_API_KEY: "sk-or-..." },
  agents: {
    defaults: {
      model: { primary: "openrouter/anthropic/claude-sonnet-4-5" },
    },
  },
}
```

## 33. Eslatmalar

- 34. Model havolalari `openrouter/<provider>/<model>` formatida bo‘ladi.
- 35. Ko‘proq model/provayder variantlari uchun [/concepts/model-providers](/concepts/model-providers) sahifasiga qarang.
- 36. OpenRouter ichki tomondan API kalitingiz bilan Bearer tokenidan foydalanadi.
