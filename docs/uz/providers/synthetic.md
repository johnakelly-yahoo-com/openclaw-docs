---
summary: "OpenClaw’da Synthetic’ning Anthropic-mos API’sidan foydalaning"
read_when:
  - Siz Synthetic’ni model provayderi sifatida ishlatmoqchisiz
  - Sizga Synthetic API kaliti yoki bazaviy URL sozlamasi kerak
title: "Synthetic"
---

# Synthetic

Synthetic Anthropic’ga mos endpointlarni taqdim etadi. OpenClaw uni
`synthetic` provayderi sifatida ro‘yxatdan o‘tkazadi va Anthropic Messages API’dan foydalanadi.

## Tezkor sozlash

1. `SYNTHETIC_API_KEY` ni o‘rnating (yoki quyidagi ustani ishga tushiring).
2. Onboarding’ni ishga tushiring:

```bash
openclaw onboard --auth-choice synthetic-api-key
```

Standart model quyidagiga o‘rnatiladi:

```
synthetic/hf:MiniMaxAI/MiniMax-M2.1
```

## Konfiguratsiya namunasi

```json5
{
  env: { SYNTHETIC_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.1" },
      models: { "synthetic/hf:MiniMaxAI/MiniMax-M2.1": { alias: "MiniMax M2.1" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "hf:MiniMaxAI/MiniMax-M2.1",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 192000,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

Eslatma: OpenClaw’ning Anthropic mijozi bazaviy URL’ga `/v1` qo‘shadi, shuning uchun
`https://api.synthetic.new/anthropic` dan foydalaning (`/anthropic/v1` emas). Agar Synthetic
bazaviy URL’ni o‘zgartirsa, `models.providers.synthetic.baseUrl` ni o‘zgartiring.

## Model katalogi

Quyidagi barcha modellar `0` xarajatdan foydalanadi (kirish/chiqish/kesh).

| Model ID                                               | Kontekst oynasi | Maksimal tokenlar | Mulohaza yuritish | Kirish      |
| ------------------------------------------------------ | --------------- | ----------------- | ----------------- | ----------- |
| `hf:MiniMaxAI/MiniMax-M2.1`                            | 192000          | 65536             | false             | matn        |
| `hf:moonshotai/Kimi-K2-Thinking`                       | 256000          | 8192              | true              | matn        |
| `hf:zai-org/GLM-4.7`                                   | 198000          | 128000            | false             | matn        |
| `hf:deepseek-ai/DeepSeek-R1-0528`                      | 128000          | 8192              | false             | matn        |
| `hf:deepseek-ai/DeepSeek-V3-0324`                      | 128000          | 8192              | false             | matn        |
| `hf:deepseek-ai/DeepSeek-V3.1`                         | 128000          | 8192              | false             | matn        |
| `hf:deepseek-ai/DeepSeek-V3.1-Terminus`                | 128000          | 8192              | false             | matn        |
| `hf:deepseek-ai/DeepSeek-V3.2`                         | 159000          | 8192              | false             | matn        |
| `hf:meta-llama/Llama-3.3-70B-Instruct`                 | 128000          | 8192              | yolg‘on           | matn        |
| `hf:meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` | 524000          | 8192              | yolg‘on           | matn        |
| `hf:moonshotai/Kimi-K2-Instruct-0905`                  | 256000          | 8192              | yolg‘on           | matn        |
| `hf:openai/gpt-oss-120b`                               | 128000          | 8192              | yolg‘on           | matn        |
| `hf:Qwen/Qwen3-235B-A22B-Instruct-2507`                | 256000          | 8192              | yolg‘on           | matn        |
| `hf:Qwen/Qwen3-Coder-480B-A35B-Instruct`               | 256000          | 8192              | yolg‘on           | matn        |
| `hf:Qwen/Qwen3-VL-235B-A22B-Instruct`                  | 250000          | 8192              | yolg‘on           | matn + rasm |
| `hf:zai-org/GLM-4.5`                                   | 128000          | 128000            | yolg‘on           | matn        |
| `hf:zai-org/GLM-4.6`                                   | 198000          | 128000            | yolg‘on           | matn        |
| `hf:deepseek-ai/DeepSeek-V3`                           | 128000          | 8192              | yolg‘on           | matn        |
| `hf:Qwen/Qwen3-235B-A22B-Thinking-2507`                | 256000          | 8192              | true              | text        |

## Notes

- Model refs use `synthetic/<modelId>`.
- If you enable a model allowlist (`agents.defaults.models`), add every model you
  plan to use.
- See [Model providers](/concepts/model-providers) for provider rules.
