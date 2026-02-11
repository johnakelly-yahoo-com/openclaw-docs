---
summary: "18. 用于 web_search 的 Perplexity Sonar 设置"
read_when:
  - 19. 你想使用 Perplexity Sonar 进行网页搜索
  - 20. 你需要 PERPLEXITY_API_KEY 或 OpenRouter 设置
title: "21. Perplexity Sonar"
---

# 22. Perplexity Sonar

23. OpenClaw 可以将 Perplexity Sonar 用于 `web_search` 工具。 24. 你可以通过 Perplexity 的直连 API 或通过 OpenRouter 进行连接。

## 25. API 选项

### 26. Perplexity（直连）

- 27. Base URL: [https://api.perplexity.ai](https://api.perplexity.ai)
- 28. 环境变量：`PERPLEXITY_API_KEY`

### 29. OpenRouter（替代方案）

- 30. Base URL: [https://openrouter.ai/api/v1](https://openrouter.ai/api/v1)
- 31. 环境变量：`OPENROUTER_API_KEY`
- 32. 支持预付费/加密货币积分。

## 33. 配置示例

```json5
34. {
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...",
          baseUrl: "https://api.perplexity.ai",
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

## 35. 从 Brave 切换

```json5
36. {
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...",
          baseUrl: "https://api.perplexity.ai",
        },
      },
    },
  },
}
```

37. 如果同时设置了 `PERPLEXITY_API_KEY` 和 `OPENROUTER_API_KEY`，请设置
    `tools.web.search.perplexity.baseUrl`（或 `tools.web.search.perplexity.apiKey`）以消除歧义。

38. 如果未设置 base URL，OpenClaw 会根据 API key 来源选择默认值：

- 39. `PERPLEXITY_API_KEY` 或 `pplx-...` → 直连 Perplexity（`https://api.perplexity.ai`）
- 40. `OPENROUTER_API_KEY` 或 `sk-or-...` → OpenRouter（`https://openrouter.ai/api/v1`）
- 41. 未知的 key 格式 → OpenRouter（安全回退）

## 42. 模型

- 43. `perplexity/sonar` — 快速问答 + 网页搜索
- 44. `perplexity/sonar-pro`（默认）— 多步推理 + 网页搜索
- 45. `perplexity/sonar-reasoning-pro` — 深度研究

46. 完整的 web_search 配置请参见 [Web tools](/tools/web)。
