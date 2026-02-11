---
summary: "Run OpenClaw with Ollama (local LLM runtime)"
read_when:
  - You want to run OpenClaw with local models via Ollama
  - You need Ollama setup and configuration guidance
title: "Ollama"
---

# Ollama

Ollama is a local LLM runtime that makes it easy to run open-source models on your machine. OpenClaw integrates with Ollama's OpenAI-compatible API and can **auto-discover tool-capable models** when you opt in with `OLLAMA_API_KEY` (or an auth profile) and do not define an explicit `models.providers.ollama` entry.

## Quick start

1. Install Ollama: [https://ollama.ai](https://ollama.ai)

2. Pull a model:

```bash
ollama pull gpt-oss:20b
# or
ollama pull llama3.3
# or
ollama pull qwen2.5-coder:32b
# or
ollama pull deepseek-r1:32b
```

3. Enable Ollama for OpenClaw (any value works; Ollama doesn't require a real key):

```bash
# 设置环境变量
export OLLAMA_API_KEY="ollama-local"

# 或在你的配置文件中进行配置
openclaw config set models.providers.ollama.apiKey "ollama-local"
```

4. 使用 Ollama 模型：

```json5
{
  agents: {
    defaults: {
      model: { primary: "ollama/gpt-oss:20b" },
    },
  },
}
```

## 模型发现（隐式提供方）

当你设置 `OLLAMA_API_KEY`（或认证配置文件）且**未**定义 `models.providers.ollama` 时，OpenClaw 会从本地 Ollama 实例 `http://127.0.0.1:11434` 发现模型：

- 查询 `/api/tags` 和 `/api/show`
- 仅保留报告具备 `tools` 能力的模型
- 当模型报告 `thinking` 时，将其标记为 `reasoning`
- 在可用时，从 `model_info["<arch>.context_length"]` 读取 `contextWindow`
- 49. 将 `maxTokens` 设置为上下文窗口的 10×
- 50. 将所有成本设置为 `0`

这避免了手动添加模型条目，同时保持模型目录与 Ollama 能力一致。

查看可用模型：

```bash
ollama list
openclaw models list
```

要添加新模型，只需使用 Ollama 拉取即可：

```bash
ollama pull mistral
```

新模型将被自动发现并可立即使用。

如果你显式设置了 `models.providers.ollama`，将跳过自动发现，你必须手动定义模型（见下文）。

## 配置

### 基础设置（隐式发现）

启用 Ollama 的最简单方式是通过环境变量：

```bash
export OLLAMA_API_KEY="ollama-local"
```

### 显式设置（手动模型）

在以下情况下使用显式配置：

- Ollama 运行在其他主机或端口上。
- 你想强制指定特定的上下文窗口或模型列表。
- 你希望包含那些未报告工具支持的模型。

```json5
{
  models: {
    providers: {
      ollama: {
        // 使用包含 /v1 的主机以兼容 OpenAI API
        baseUrl: "http://ollama-host:11434/v1",
        apiKey: "ollama-local",
        api: "openai-completions",
        models: [
          {
            id: "gpt-oss:20b",
            name: "GPT-OSS 20B",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 8192,
            maxTokens: 8192 * 10
          }
        ]
      }
    }
  }
}
```

如果设置了 `OLLAMA_API_KEY`，你可以在 provider 条目中省略 `apiKey`，OpenClaw 会在可用性检查时自动填充。

### 自定义基础 URL（显式配置）

如果 Ollama 运行在不同的主机或端口上（显式配置会禁用自动发现，因此需要手动定义模型）：

```json5
{
  models: {
    providers: {
      ollama: {
        apiKey: "ollama-local",
        baseUrl: "http://ollama-host:11434/v1",
      },
    },
  },
}
```

### 模型选择

配置完成后，所有 Ollama 模型都可用：

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "ollama/gpt-oss:20b",
        fallbacks: ["ollama/llama3.3", "ollama/qwen2.5-coder:32b"],
      },
    },
  },
}
```

## 高级

### 推理模型

当 Ollama 在 `/api/show` 中报告 `thinking` 时，OpenClaw 会将模型标记为具备推理能力：

```bash
ollama pull deepseek-r1:32b
```

### 模型成本

Ollama 免费且在本地运行，因此所有模型成本均设置为 $0。

### 流式配置

由于底层 SDK 与 Ollama 响应格式存在一个[已知问题](https://github.com/badlogic/pi-mono/issues/1205)，**默认情况下会为 Ollama 模型禁用流式传输**。 这可以防止在使用具备工具能力的模型时出现响应损坏。

当禁用流式传输时，响应将一次性返回（非流式模式），从而避免内容/推理增量交错导致的乱码输出问题。

#### 重新启用流式传输（高级）

如果你希望为 Ollama 重新启用流式传输（可能会导致具备工具能力的模型出现问题）：

```json5
{
  agents: {
    defaults: {
      models: {
        "ollama/gpt-oss:20b": {
          streaming: true,
        },
      },
    },
  },
}
```

#### 为其他提供方禁用流式传输

如有需要，你也可以为任何提供方禁用流式传输：

```json5
{
  agents: {
    defaults: {
      models: {
        "openai/gpt-4": {
          streaming: false,
        },
      },
    },
  },
}
```

### 上下文窗口

For auto-discovered models, OpenClaw uses the context window reported by Ollama when available, otherwise it defaults to `8192`. You can override `contextWindow` and `maxTokens` in explicit provider config.

## Troubleshooting

### Ollama not detected

Make sure Ollama is running and that you set `OLLAMA_API_KEY` (or an auth profile), and that you did **not** define an explicit `models.providers.ollama` entry:

```bash
ollama serve
```

And that the API is accessible:

```bash
curl http://localhost:11434/api/tags
```

### No models available

OpenClaw only auto-discovers models that report tool support. If your model isn't listed, either:

- Pull a tool-capable model, or
- Define the model explicitly in `models.providers.ollama`.

To add models:

```bash
ollama list  # See what's installed
ollama pull gpt-oss:20b  # Pull a tool-capable model
ollama pull llama3.3     # Or another model
```

### Connection refused

检查 Ollama 是否在正确的端口上运行：

```bash
# Check if Ollama is running
ps aux | grep ollama

# Or restart Ollama
ollama serve
```

### Corrupted responses or tool names in output

If you see garbled responses containing tool names (like `sessions_send`, `memory_get`) or fragmented text when using Ollama models, this is due to an upstream SDK issue with streaming responses. **This is fixed by default** in the latest OpenClaw version by disabling streaming for Ollama models.

If you manually enabled streaming and experience this issue:

1. Remove the `streaming: true` configuration from your Ollama model entries, or
2. Explicitly set `streaming: false` for Ollama models (see [Streaming Configuration](#streaming-configuration))

## See Also

- [模型提供方](/concepts/model-providers) - 所有提供方概览
- [Model Selection](/concepts/models) - How to choose models
- [Configuration](/gateway/configuration) - Full config reference
