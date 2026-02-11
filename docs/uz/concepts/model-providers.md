---
summary: "45. Misol konfiguratsiyalar + CLI oqimlari bilan model provayderlari sharhi"
read_when:
  - 46. Sizga provayderlar bo‘yicha model sozlamalari uchun ma’lumotnoma kerak
  - 47. Sizga model provayderlari uchun misol konfiguratsiyalar yoki CLI onboarding buyruqlari kerak
title: "48. Model Provayderlari"
---

# 49. Model provayderlari

50. Bu sahifa **LLM/model provayderlari**ni qamrab oladi (WhatsApp/Telegram kabi chat kanallari emas).
51. Modelni tanlash qoidalari uchun qarang: [/concepts/models](/concepts/models).

## 2. Tezkor qoidalar

- 3. Model havolalari `provider/model` formatidan foydalanadi (misol: `opencode/claude-opus-4-6`).
- 4. Agar `agents.defaults.models` ni o‘rnatsangiz, u ruxsat etilgan ro‘yxatga (allowlist) aylanadi.
- 5. CLI yordamchilari: `openclaw onboard`, `openclaw models list`, `openclaw models set <provider/model>`.

## 6. Ichki provayderlar (pi‑ai katalogi)

7. OpenClaw pi‑ai katalogi bilan birga yetkazib beriladi. 8. Ushbu provayderlar **hech qanday** `models.providers` konfiguratsiyasini talab qilmaydi; faqat autentifikatsiyani sozlab, modelni tanlang.

### 9. OpenAI

- 10. Provayder: `openai`
- 11. Autentifikatsiya: `OPENAI_API_KEY`
- 12. Namuna model: `openai/gpt-5.1-codex`
- 13. CLI: `openclaw onboard --auth-choice openai-api-key`

```json5
14. {
  agents: { defaults: { model: { primary: "openai/gpt-5.1-codex" } } },
}
```

### 15. Anthropic

- 16. Provayder: `anthropic`
- 17. Autentifikatsiya: `ANTHROPIC_API_KEY` yoki `claude setup-token`
- 18. Namuna model: `anthropic/claude-opus-4-6`
- 19. CLI: `openclaw onboard --auth-choice token` (setup-tokenni joylashtiring) yoki `openclaw models auth paste-token --provider anthropic`

```json5
20. {
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

### 21. OpenAI Code (Codex)

- 22. Provayder: `openai-codex`
- 23. Autentifikatsiya: OAuth (ChatGPT)
- 24. Namuna model: `openai-codex/gpt-5.3-codex`
- 25. CLI: `openclaw onboard --auth-choice openai-codex` yoki `openclaw models auth login --provider openai-codex`

```json5
26. {
  agents: { defaults: { model: { primary: "openai-codex/gpt-5.3-codex" } } },
}
```

### 27. OpenCode Zen

- 28. Provayder: `opencode`
- 29. Autentifikatsiya: `OPENCODE_API_KEY` (yoki `OPENCODE_ZEN_API_KEY`)
- 30. Namuna model: `opencode/claude-opus-4-6`
- 31. CLI: `openclaw onboard --auth-choice opencode-zen`

```json5
32. {
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-6" } } },
}
```

### 33. Google Gemini (API kalit)

- 34. Provayder: `google`
- 35. Autentifikatsiya: `GEMINI_API_KEY`
- 36. Namuna model: `google/gemini-3-pro-preview`
- 37. CLI: `openclaw onboard --auth-choice gemini-api-key`

### 38. Google Vertex, Antigravity va Gemini CLI

- 39. Provayderlar: `google-vertex`, `google-antigravity`, `google-gemini-cli`
- 40. Autentifikatsiya: Vertex gcloud ADC’dan foydalanadi; Antigravity/Gemini CLI esa o‘ziga xos autentifikatsiya jarayonlaridan foydalanadi
- 41. Antigravity OAuth biriktirilgan plagin sifatida yetkazib beriladi (`google-antigravity-auth`, sukut bo‘yicha o‘chirilgan).
  - 42. Yoqish: `openclaw plugins enable google-antigravity-auth`
  - 43. Kirish: `openclaw models auth login --provider google-antigravity --set-default`
- 44. Gemini CLI OAuth biriktirilgan plagin sifatida yetkazib beriladi (`google-gemini-cli-auth`, sukut bo‘yicha o‘chirilgan).
  - 45. Yoqish: `openclaw plugins enable google-gemini-cli-auth`
  - 46. Kirish: `openclaw models auth login --provider google-gemini-cli --set-default`
  - 47. Eslatma: `openclaw.json` ichiga mijoz identifikatori (client id) yoki maxfiy kalitni (secret) **kiritmaysiz**. 48. CLI orqali kirish jarayoni tokenlarni shlyuz xostidagi autentifikatsiya profillarida saqlaydi.

### 49. Z.AI (GLM)

- 50. Provayder: `zai`
- 1. Avtorizatsiya: `ZAI_API_KEY`
- 2. Namunaviy model: `zai/glm-4.7`
- 3. CLI: `openclaw onboard --auth-choice zai-api-key`
  - 4. Aliaslar: `z.ai/*` va `z-ai/*` `zai/*` ga normallashtiriladi

### 5. Vercel AI Gateway

- 6. Provayder: `vercel-ai-gateway`
- 7. Avtorizatsiya: `AI_GATEWAY_API_KEY`
- 8. Namunaviy model: `vercel-ai-gateway/anthropic/claude-opus-4.6`
- 9. CLI: `openclaw onboard --auth-choice ai-gateway-api-key`

### 10. Boshqa ichki (built-in) provayderlar

- 11. OpenRouter: `openrouter` (`OPENROUTER_API_KEY`)
- 12. Namunaviy model: `openrouter/anthropic/claude-sonnet-4-5`
- 13. xAI: `xai` (`XAI_API_KEY`)
- 14. Groq: `groq` (`GROQ_API_KEY`)
- 15. Cerebras: `cerebras` (`CEREBRAS_API_KEY`)
  - 16. Cerebras’dagi GLM modellari `zai-glm-4.7` va `zai-glm-4.6` identifikatorlaridan foydalanadi.
  - 17. OpenAI-mos asosiy URL: `https://api.cerebras.ai/v1`.
- 18. Mistral: `mistral` (`MISTRAL_API_KEY`)
- 19. GitHub Copilot: `github-copilot` (`COPILOT_GITHUB_TOKEN` / `GH_TOKEN` / `GITHUB_TOKEN`)

## 20. `models.providers` orqali provayderlar (custom/base URL)

21. **Maxsus** provayderlarni yoki OpenAI/Anthropic‑mos proksilarni qo‘shish uchun `models.providers` (yoki `models.json`) dan foydalaning.

### 22. Moonshot AI (Kimi)

23. Moonshot OpenAI-mos endpointlardan foydalanadi, shuning uchun uni maxsus provayder sifatida sozlang:

- 24. Provayder: `moonshot`
- 25. Avtorizatsiya: `MOONSHOT_API_KEY`
- 26. Namunaviy model: `moonshot/kimi-k2.5`

27. Kimi K2 model IDlari:

28. {/_moonshot-kimi-k2-model-refs:start_/ && null}

- 29. `moonshot/kimi-k2.5`
- 30. `moonshot/kimi-k2-0905-preview`
- 31. `moonshot/kimi-k2-turbo-preview`
- 32. `moonshot/kimi-k2-thinking`
- 33. `moonshot/kimi-k2-thinking-turbo`
      {/_moonshot-kimi-k2-model-refs:end_/ && null}

```json5
34. {
  agents: {
    defaults: { model: { primary: "moonshot/kimi-k2.5" } },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [{ id: "kimi-k2.5", name: "Kimi K2.5" }],
      },
    },
  },
}
```

### 35. Kimi Coding

36. Kimi Coding Moonshot AI’ning Anthropic-mos endpointidan foydalanadi:

- 37. Provayder: `kimi-coding`
- 38. Avtorizatsiya: `KIMI_API_KEY`
- 39. Namunaviy model: `kimi-coding/k2p5`

```json5
40. {
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: { model: { primary: "kimi-coding/k2p5" } },
  },
}
```

### 41. Qwen OAuth (bepul daraja)

42. Qwen Qwen Coder + Vision uchun qurilma-kod (device-code) oqimi orqali OAuth kirishni taqdim etadi.
43. Biriktirilgan plaginini yoqing, so‘ng tizimga kiring:

```bash
44. openclaw plugins enable qwen-portal-auth
openclaw models auth login --provider qwen-portal --set-default
```

45. Model havolalari:

- 46. `qwen-portal/coder-model`
- 47. `qwen-portal/vision-model`

48. Sozlash tafsilotlari va eslatmalar uchun [/providers/qwen](/providers/qwen) ga qarang.

### 49. Synthetic

50. Synthetic `synthetic` provayderi ortida Anthropic-mos modellalarni taqdim etadi:

- Provider: `synthetic`
- Auth: `SYNTHETIC_API_KEY`
- Example model: `synthetic/hf:MiniMaxAI/MiniMax-M2.1`
- CLI: `openclaw onboard --auth-choice synthetic-api-key`

```json5
{
  agents: {
    defaults: { model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.1" } },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [{ id: "hf:MiniMaxAI/MiniMax-M2.1", name: "MiniMax M2.1" }],
      },
    },
  },
}
```

### MiniMax

MiniMax is configured via `models.providers` because it uses custom endpoints:

- MiniMax (Anthropic‑compatible): `--auth-choice minimax-api`
- Auth: `MINIMAX_API_KEY`

See [/providers/minimax](/providers/minimax) for setup details, model options, and config snippets.

### Ollama

Ollama is a local LLM runtime that provides an OpenAI-compatible API:

- Provider: `ollama`
- Auth: None required (local server)
- Example model: `ollama/llama3.3`
- Installation: [https://ollama.ai](https://ollama.ai)

```bash
# Install Ollama, then pull a model:
ollama pull llama3.3
```

```json5
{
  agents: {
    defaults: { model: { primary: "ollama/llama3.3" } },
  },
}
```

Ollama is automatically detected when running locally at `http://127.0.0.1:11434/v1`. See [/providers/ollama](/providers/ollama) for model recommendations and custom configuration.

### Local proxies (LM Studio, vLLM, LiteLLM, etc.)

Example (OpenAI‑compatible):

```json5
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/minimax-m2.1-gs32" },
      models: { "lmstudio/minimax-m2.1-gs32": { alias: "Minimax" } },
    },
  },
  models: {
    providers: {
      lmstudio: {
        baseUrl: "http://localhost:1234/v1",
        apiKey: "LMSTUDIO_KEY",
        api: "openai-completions",
        models: [
          {
            id: "minimax-m2.1-gs32",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Notes:

- For custom providers, `reasoning`, `input`, `cost`, `contextWindow`, and `maxTokens` are optional.
  When omitted, OpenClaw defaults to:
  - `reasoning: false`
  - `input: ["text"]`
  - `cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }`
  - `contextWindow: 200000`
  - `maxTokens: 8192`
- Recommended: set explicit values that match your proxy/model limits.

## CLI examples

```bash
openclaw onboard --auth-choice opencode-zen
openclaw models set opencode/claude-opus-4-6
openclaw models list
```

See also: [/gateway/configuration](/gateway/configuration) for full configuration examples.
