---
summary: "Model provider overview with example configs + CLI flows"
read_when:
  - You need a provider-by-provider model setup reference
  - You want example configs or CLI onboarding commands for model providers
title: "Model Providers"
---

# Model providers

This page covers **LLM/model providers** (not chat channels like WhatsApp/Telegram).1) 有关模型选择规则，请参见 [/concepts/models](/concepts/models)。

## 2. 快速规则

- 3. 模型引用使用 `provider/model`（示例：`opencode/claude-opus-4-6`）。
- 4. 如果你设置了 `agents.defaults.models`，它将成为允许列表。
- 5. CLI 助手：`openclaw onboard`、`openclaw models list`、`openclaw models set <provider/model>`。

## 35. 内置提供方（pi-ai 目录）

7. OpenClaw 随附 pi‑ai 目录。 8. 这些提供方**不需要**
   `models.providers` 配置；只需设置鉴权并选择一个模型。

### 9. OpenAI

- 10. 提供方：`openai`
- 11. 鉴权：`OPENAI_API_KEY`
- 12. 示例模型：`openai/gpt-5.1-codex`
- 13. CLI：`openclaw onboard --auth-choice openai-api-key`

```json5
{
  agents: { defaults: { model: { primary: "openai/gpt-5.1-codex" } } },
}
```

### 15. Anthropic

- 16. 提供方：`anthropic`
- 17. 鉴权：`ANTHROPIC_API_KEY` 或 `claude setup-token`
- 18. 示例模型：`anthropic/claude-opus-4-6`
- 19. CLI：`openclaw onboard --auth-choice token`（粘贴 setup-token）或 `openclaw models auth paste-token --provider anthropic`

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

### 21. OpenAI Code（Codex）

- 22. 提供方：`openai-codex`
- 23. 鉴权：OAuth（ChatGPT）
- 24. 示例模型：`openai-codex/gpt-5.3-codex`
- 25. CLI：`openclaw onboard --auth-choice openai-codex` 或 `openclaw models auth login --provider openai-codex`

```json5
{
  agents: { defaults: { model: { primary: "openai-codex/gpt-5.3-codex" } } },
}
```

### 27. OpenCode Zen

- 28. 提供方：`opencode`
- 29. 鉴权：`OPENCODE_API_KEY`（或 `OPENCODE_ZEN_API_KEY`）
- 36. 示例模型：`opencode/claude-opus-4-6`
- 31. CLI：`openclaw onboard --auth-choice opencode-zen`

```json5
37. {
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-6" } } },
}
```

### 33. Google Gemini（API Key）

- 34. 提供方：`google`
- 35. 鉴权：`GEMINI_API_KEY`
- 36. 示例模型：`google/gemini-3-pro-preview`
- 37. CLI：`openclaw onboard --auth-choice gemini-api-key`

### 38. Google Vertex、Antigravity 和 Gemini CLI

- 39. 提供方：`google-vertex`、`google-antigravity`、`google-gemini-cli`
- 40. 鉴权：Vertex 使用 gcloud ADC；Antigravity/Gemini CLI 使用各自的鉴权流程
- 41. Antigravity OAuth 作为捆绑插件提供（`google-antigravity-auth`，默认禁用）。
  - 42. 启用：`openclaw plugins enable google-antigravity-auth`
  - 43. 登录：`openclaw models auth login --provider google-antigravity --set-default`
- 44. Gemini CLI OAuth 作为捆绑插件提供（`google-gemini-cli-auth`，默认禁用）。
  - 45. 启用：`openclaw plugins enable google-gemini-cli-auth`
  - 46. 登录：`openclaw models auth login --provider google-gemini-cli --set-default`
  - 47. 注意：你**不需要**将 client id 或 secret 粘贴到 `openclaw.json` 中。 48. CLI 登录流程会将
        令牌存储在网关主机上的鉴权配置文件中。

### 49. Z.AI（GLM）

- 50. 提供方：`zai`
- Auth: `ZAI_API_KEY`
- Example model: `zai/glm-4.7`
- CLI: `openclaw onboard --auth-choice zai-api-key`
  - Aliases: `z.ai/*` and `z-ai/*` normalize to `zai/*`

### Vercel AI Gateway

- Provider: `vercel-ai-gateway`
- Auth: `AI_GATEWAY_API_KEY`
- Example model: `vercel-ai-gateway/anthropic/claude-opus-4.6`
- CLI: `openclaw onboard --auth-choice ai-gateway-api-key`

### Other built-in providers

- OpenRouter: `openrouter` (`OPENROUTER_API_KEY`)
- Example model: `openrouter/anthropic/claude-sonnet-4-5`
- xAI: `xai` (`XAI_API_KEY`)
- Groq: `groq` (`GROQ_API_KEY`)
- Cerebras: `cerebras` (`CEREBRAS_API_KEY`)
  - GLM models on Cerebras use ids `zai-glm-4.7` and `zai-glm-4.6`.
  - OpenAI-compatible base URL: `https://api.cerebras.ai/v1`.
- 39. Mistral：`mistral`（`MISTRAL_API_KEY`）
- GitHub Copilot: `github-copilot` (`COPILOT_GITHUB_TOKEN` / `GH_TOKEN` / `GITHUB_TOKEN`)

## Providers via `models.providers` (custom/base URL)

Use `models.providers` (or `models.json`) to add **custom** providers or
OpenAI/Anthropic‑compatible proxies.

### 40. Moonshot AI（Kimi）

Moonshot uses OpenAI-compatible endpoints, so configure it as a custom provider:

- Provider: `moonshot`
- Auth: `MOONSHOT_API_KEY`
- Example model: `moonshot/kimi-k2.5`

Kimi K2 model IDs:

{/_moonshot-kimi-k2-model-refs:start_/ && null}

- `moonshot/kimi-k2.5`
- `moonshot/kimi-k2-0905-preview`
- `moonshot/kimi-k2-turbo-preview`
- `moonshot/kimi-k2-thinking`
- `moonshot/kimi-k2-thinking-turbo`
  {/_moonshot-kimi-k2-model-refs:end_/ && null}

```json5
{
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

### Kimi Coding

Kimi Coding uses Moonshot AI's Anthropic-compatible endpoint:

- Provider: `kimi-coding`
- Auth: `KIMI_API_KEY`
- Example model: `kimi-coding/k2p5`

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: { model: { primary: "kimi-coding/k2p5" } },
  },
}
```

### Qwen OAuth (free tier)

41. Qwen 通过设备码流程为 Qwen Coder + Vision 提供 OAuth 访问。
    Enable the bundled plugin, then log in:

```bash
openclaw plugins enable qwen-portal-auth
openclaw models auth login --provider qwen-portal --set-default
```

42. 模型引用：

- `qwen-portal/coder-model`
- 43. `qwen-portal/vision-model`

44. 设置详情和说明请参见 [/providers/qwen](/providers/qwen)。

### Synthetic

Synthetic provides Anthropic-compatible models behind the `synthetic` provider:

- Provider: `synthetic`
- Auth: `SYNTHETIC_API_KEY`
- 45. 示例模型：`synthetic/hf:MiniMaxAI/MiniMax-M2.1`
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

46. MiniMax 通过 `models.providers` 进行配置，因为它使用自定义端点：

- MiniMax (Anthropic‑compatible): `--auth-choice minimax-api`
- Auth: `MINIMAX_API_KEY`

See [/providers/minimax](/providers/minimax) for setup details, model options, and config snippets.

### Ollama

47. Ollama 是一个本地 LLM 运行时，提供与 OpenAI 兼容的 API：

- 48. 提供方：`ollama`
- 49. 认证：不需要（本地服务器）
- 50. 示例模型：`ollama/llama3.3`
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

1. 备注：

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
