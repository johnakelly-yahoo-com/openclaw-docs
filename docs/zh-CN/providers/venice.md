---
summary: "在 OpenClaw 中使用 Venice AI 的隐私优先模型"
read_when:
  - 你希望在 OpenClaw 中进行隐私优先的推理
  - 你希望获得 Venice AI 的设置指南
title: "Venice AI"
---

# Venice AI（Venice 高亮）

**Venice** 是我们重点推荐的 Venice 设置，用于隐私优先的推理，并可选择通过匿名方式访问专有模型。

Venice AI 提供以隐私为重点的 AI 推理，支持无审查模型，并可通过其匿名代理访问主流专有模型。 所有推理默认都是私密的——不使用你的数据进行训练，也不记录日志。

## 为什么在 OpenClaw 中选择 Venice

- **私密推理**：适用于开源模型（不记录日志）。
- **无审查模型**：在需要时使用。
- **匿名访问**：当质量很重要时，通过匿名方式访问专有模型（Opus/GPT/Gemini）。
- 兼容 OpenAI 的 `/v1` 端点。

## 隐私模式

Venice 提供两种隐私级别——理解这一点是选择模型的关键：

| 模式     | 描述                                                     | 模型                                       |
| ------ | ------------------------------------------------------ | ---------------------------------------- |
| **私密** | 完全私有。 提示/响应 **永不存储或记录**。 临时的。                          | Llama、Qwen、DeepSeek、Venice Uncensored 等。 |
| **匿名** | 通过 Venice 代理并去除元数据。 底层提供商（OpenAI、Anthropic）只会看到匿名化的请求。 | Claude、GPT、Gemini、Grok、Kimi、MiniMax      |

## 功能

- **以隐私为中心**：在“私密”（完全私密）和“匿名”（代理）模式之间选择
- **无审查模型**：访问不受内容限制的模型
- **主流模型访问**：通过 Venice 的匿名代理使用 Claude、GPT-5.2、Gemini、Grok
- **兼容 OpenAI 的 API**：标准 `/v1` 端点，便于集成
- **流式传输**：✅ 所有模型均支持
- **函数调用**：✅ 部分模型支持（请查看模型能力）
- **视觉**：✅ 具备视觉能力的模型支持
- **无硬性速率限制**：极端使用情况下可能会应用公平使用限流

## 设置

### 1. 获取 API 密钥

1. 在 [venice.ai](https://venice.ai) 注册
2. 前往 **Settings → API Keys → Create new key**
3. 复制你的 API 密钥（格式：`vapi_xxxxxxxxxxxx`）

### 2) 配置 OpenClaw

**Option A: Environment Variable**

```bash
export VENICE_API_KEY="vapi_xxxxxxxxxxxx"
```

**Option B: Interactive Setup (Recommended)**

```bash
openclaw onboard --auth-choice venice-api-key
```

This will:

1. Prompt for your API key (or use existing `VENICE_API_KEY`)
2. Show all available Venice models
3. Let you pick your default model
4. Configure the provider automatically

**Option C: Non-interactive**

```bash
openclaw onboard --non-interactive \
  --auth-choice venice-api-key \
  --venice-api-key "vapi_xxxxxxxxxxxx"
```

### 3. Verify Setup

```bash
openclaw chat --model venice/llama-3.3-70b "Hello, are you working?"
```

## Model Selection

After setup, OpenClaw shows all available Venice models. Pick based on your needs:

- **Default (our pick)**: `venice/llama-3.3-70b` for private, balanced performance.
- **最佳整体质量**：`venice/claude-opus-45` 适合高难度任务（Opus 仍然是最强的）。
- **隐私**：选择“private”模型以实现完全私有的推理。
- **Capability**: Choose "anonymized" models to access Claude, GPT, Gemini via Venice's proxy.

Change your default model anytime:

```bash
openclaw models set venice/claude-opus-45
openclaw models set venice/llama-3.3-70b
```

List all available models:

```bash
openclaw models list | grep venice
```

## Configure via `openclaw configure`

1. Run `openclaw configure`
2. Select **Model/auth**
3. Choose **Venice AI**

## Which Model Should I Use?

| Use Case                     | Recommended Model                | Why                                       |
| ---------------------------- | -------------------------------- | ----------------------------------------- |
| **General chat**             | `llama-3.3-70b`                  | Good all-around, fully private            |
| **Best overall quality**     | `claude-opus-45`                 | Opus remains the strongest for hard tasks |
| **Privacy + Claude quality** | `claude-opus-45`                 | Best reasoning via anonymized proxy       |
| **Coding**                   | `qwen3-coder-480b-a35b-instruct` | Code-optimized, 262k context              |
| **Vision tasks**             | `qwen3-vl-235b-a22b`             | Best private vision model                 |
| **Uncensored**               | `venice-uncensored`              | No content restrictions                   |
| **Fast + cheap**             | `qwen3-4b`                       | Lightweight, still capable                |
| **Complex reasoning**        | `deepseek-v3.2`                  | Strong reasoning, private                 |

## Available Models (25 Total)

### Private Models (15) — Fully Private, No Logging

| Model ID                                           | 名称                                                      | Context (tokens) | Features                          |
| -------------------------------------------------- | ------------------------------------------------------- | ----------------------------------- | --------------------------------- |
| `llama-3.3-70b`                                    | Llama 3.3 70B                           | 131k                                | General                           |
| `llama-3.2-3b`                                     | Llama 3.2 3B                            | 131k                                | Fast, lightweight                 |
| `hermes-3-llama-3.1-405b`                          | Hermes 3 Llama 3.1 405B                 | 131k                                | Complex tasks                     |
| `qwen3-235b-a22b-thinking-2507`                    | Qwen3 235B Thinking                                     | 131k                                | Reasoning                         |
| `qwen3-235b-a22b-instruct-2507`                    | Qwen3 235B Instruct                                     | 131k                                | General                           |
| `qwen3-coder-480b-a35b-instruct`                   | Qwen3 Coder 480B                                        | 262k                                | Code                              |
| `qwen3-next-80b`                                   | Qwen3 Next 80B                                          | 262k                                | General                           |
| `qwen3-vl-235b-a22b`                               | Qwen3 VL 235B                                           | 262k                                | Vision                            |
| `qwen3-4b`                                         | Venice Small (Qwen3 4B)              | 32k                                 | Fast, reasoning                   |
| `deepseek-v3.2`                                    | 1. DeepSeek V3.2 | 2. 163k      | 3. 推理      |
| 4. `venice-uncensored`      | 5. Venice Uncensored             | 6. 32k       | 7. 无审查     |
| 8. `mistral-31-24b`         | 9. Venice Medium（Mistral）        | 10. 131k     | 11. 视觉     |
| 12. `google-gemma-3-27b-it` | 13. Gemma 3 27B 指令版              | 14. 202k     | 15. 视觉     |
| 16. `openai-gpt-oss-120b`   | 17. OpenAI GPT OSS 120B          | 18. 131k     | 19. 通用     |
| 20. `zai-org-glm-4.7`       | 21. GLM 4.7      | 22. 202k     | 23. 推理，多语言 |

### 24. 匿名化模型（10）— 通过 Venice 代理

| 25. 模型 ID                    | 26. 原始                                | 27. 上下文（tokens） | 28. 功能    |
| --------------------------------------------------- | ------------------------------------------------------------ | -------------------------------------- | -------------------------------- |
| 29. `claude-opus-45`         | 30. Claude Opus 4.5   | 31. 202k        | 32. 推理，视觉 |
| 33. `claude-sonnet-45`       | 34. Claude Sonnet 4.5 | 35. 202k        | 36. 推理，视觉 |
| 37. `openai-gpt-52`          | 38. GPT-5.2           | 39. 262k        | 40. 推理    |
| 41. `openai-gpt-52-codex`    | 42. GPT-5.2 Codex     | 43. 262k        | 44. 推理，视觉 |
| 45. `gemini-3-pro-preview`   | 46. Gemini 3 Pro                      | 47. 202k        | 48. 推理，视觉 |
| 49. `gemini-3-flash-preview` | Gemini 3 Flash                                               | 262k                                   | Reasoning, vision                |
| `grok-41-fast`                                      | Grok 4.1 Fast                                | 262k                                   | Reasoning, vision                |
| `grok-code-fast-1`                                  | Grok Code Fast 1                                             | 262k                                   | Reasoning, code                  |
| `kimi-k2-thinking`                                  | Kimi K2 Thinking                                             | 262k                                   | 推理                               |
| `minimax-m21`                                       | MiniMax M2.1                                 | 202k                                   | Reasoning                        |

## Model Discovery

OpenClaw automatically discovers models from the Venice API when `VENICE_API_KEY` is set. If the API is unreachable, it falls back to a static catalog.

The `/models` endpoint is public (no auth needed for listing), but inference requires a valid API key.

## Streaming & Tool Support

| Feature              | Support                                                                   |
| -------------------- | ------------------------------------------------------------------------- |
| **Streaming**        | ✅ All models                                                              |
| **Function calling** | ✅ Most models (check `supportsFunctionCalling` in API) |
| **Vision/Images**    | ✅ Models marked with "Vision" feature                                     |
| **JSON mode**        | ✅ Supported via `response_format`                                         |

## 定价

Venice uses a credit-based system. Check [venice.ai/pricing](https://venice.ai/pricing) for current rates:

- **Private models**: Generally lower cost
- **Anonymized models**: Similar to direct API pricing + small Venice fee

## 对比：Venice vs 直连 API

| Aspect       | Venice (Anonymized) | Direct API          |
| ------------ | -------------------------------------- | ------------------- |
| **Privacy**  | Metadata stripped, anonymized          | Your account linked |
| **Latency**  | +10-50ms (proxy)    | Direct              |
| **Features** | Most features supported                | Full features       |
| **Billing**  | Venice credits                         | 提供方计费               |

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

The Venice model catalog updates dynamically. Run `openclaw models list` to see currently available models. Some models may be temporarily offline.

### Connection issues

Venice API is at `https://api.venice.ai/api/v1`. Ensure your network allows HTTPS connections.

## Config file example

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
