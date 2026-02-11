---
summary: "Web 搜索 + 抓取工具（Brave Search API、Perplexity 直连/OpenRouter）"
read_when:
  - 你想启用 web_search 或 web_fetch
  - 你需要设置 Brave Search API 密钥
  - 你想使用 Perplexity Sonar 进行 Web 搜索
title: "Web 工具"
---

# Web 工具

OpenClaw 提供两个轻量级 Web 工具：

- `web_search` — 通过 Brave Search API（默认）或 Perplexity Sonar（直连或通过 OpenRouter）进行 Web 搜索。
- `web_fetch` — HTTP 抓取 + 可读内容提取（HTML → markdown/text）。

这些**不是**浏览器自动化。 对于 JS 密集型网站或需要登录的场景，请使用
[Browser tool](/tools/browser)。

## 工作原理

- `web_search` 调用你配置的提供商并返回结果。
  - **Brave**（默认）：返回结构化结果（标题、URL、摘要）。
  - **Perplexity**：返回基于实时 Web 搜索的 AI 综合答案，并附带引用。
- 结果会按查询缓存 15 分钟（可配置）。
- `web_fetch` 执行普通的 HTTP GET 并提取可读内容
  （HTML → markdown/text）。 它**不会**执行 JavaScript。
- `web_fetch` 默认启用（除非显式禁用）。

## 选择搜索提供商

| 提供商            | Pros          | 缺点                              | API 密钥                                      |
| -------------- | ------------- | ------------------------------- | ------------------------------------------- |
| **Brave**（默认）  | 快速、结构化结果、免费套餐 | 传统搜索结果                          | `BRAVE_API_KEY`                             |
| **Perplexity** | AI 综合答案、引用、实时 | 需要 Perplexity 或 OpenRouter 访问权限 | `OPENROUTER_API_KEY` 或 `PERPLEXITY_API_KEY` |

有关提供商的具体细节，请参阅 [Brave Search setup](/brave-search) 和 [Perplexity Sonar](/perplexity)。

在配置中设置提供商：

```json5
{
  tools: {
    web: {
      search: {
        provider: "brave", // 或 "perplexity"
      },
    },
  },
}
```

示例：切换到 Perplexity Sonar（直连 API）：

```json5
1. {
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

## 2. 获取 Brave API 密钥

1. 3. 在 [https://brave.com/search/api/](https://brave.com/search/api/) 创建一个 Brave Search API 账户
2. In the dashboard, choose the **Data for Search** plan (not “Data for AI”) and generate an API key.
3. 5. 运行 `openclaw configure --section web` 将密钥存储到配置中（推荐），或者在你的环境中设置 `BRAVE_API_KEY`。

Brave provides a free tier plus paid plans; check the Brave API portal for the
current limits and pricing.

### 7. 在哪里设置密钥（推荐）

8. **推荐：** 运行 `openclaw configure --section web`。 9. 它会将密钥存储在
   `~/.openclaw/openclaw.json` 中的 `tools.web.search.apiKey`。

10. **环境变量替代方案：** 在 Gateway 进程的环境中设置 `BRAVE_API_KEY`。 For a gateway install, put it in `~/.openclaw/.env` (or your
    service environment). 12. 请参阅 [Env vars](/help/faq#how-does-openclaw-load-environment-variables)。

## 13. 使用 Perplexity（直接或通过 OpenRouter）

14. Perplexity Sonar 模型内置了网页搜索能力，并返回带有引用的 AI 综合答案。 You can use them via OpenRouter (no credit card required - supports
    crypto/prepaid).

### 16. 获取 OpenRouter API 密钥

1. 17. 在 [https://openrouter.ai/](https://openrouter.ai/) 创建一个账户
2. 18. 添加余额（支持加密货币、预付费或信用卡）
3. 19. 在账户设置中生成一个 API 密钥

### Setting up Perplexity search

```json5
21. {
  tools: {
    web: {
      search: {
        enabled: true,
        provider: "perplexity",
        perplexity: {
          // API key (optional if OPENROUTER_API_KEY or PERPLEXITY_API_KEY is set)
          apiKey: "sk-or-v1-...",
          // Base URL (key-aware default if omitted)
          baseUrl: "https://openrouter.ai/api/v1",
          // Model (defaults to perplexity/sonar-pro)
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

22. **环境变量替代方案：** 在 Gateway 环境中设置 `OPENROUTER_API_KEY` 或 `PERPLEXITY_API_KEY`。 23. 对于 gateway 安装，将其放在 `~/.openclaw/.env` 中。

24. 如果未设置 base URL，OpenClaw 会根据 API 密钥来源选择默认值：

- 25. `PERPLEXITY_API_KEY` 或 `pplx-...` → `https://api.perplexity.ai`
- 26. `OPENROUTER_API_KEY` 或 `sk-or-...` → `https://openrouter.ai/api/v1`
- 27. 未知的密钥格式 → OpenRouter（安全回退）

### 28. 可用的 Perplexity 模型

| 29. 模型                               | 30. 描述         | 31. 最适合  |
| ----------------------------------------------------------- | ------------------------------------- | ------------------------------- |
| 32. `perplexity/sonar`               | 33. 带网页搜索的快速问答 | 34. 快速查询 |
| 35. `perplexity/sonar-pro`（默认）       | 36. 带网页搜索的多步推理 | 37. 复杂问题 |
| 38. `perplexity/sonar-reasoning-pro` | 39. 思维链分析      | 40. 深度研究 |

## 41. web_search

42. 使用你配置的提供商搜索网页。

### 43. 要求

- 44. `tools.web.search.enabled` 不能为 `false`（默认：启用）
- 45. 你所选提供商的 API 密钥：
  - 46. **Brave**：`BRAVE_API_KEY` 或 `tools.web.search.apiKey`
  - 47. **Perplexity**：`OPENROUTER_API_KEY`、`PERPLEXITY_API_KEY`，或 `tools.web.search.perplexity.apiKey`

### 48. 配置

```json5
49. {
  tools: {
    web: {
      search: {
        enabled: true,
        apiKey: "BRAVE_API_KEY_HERE", // optional if BRAVE_API_KEY is set
        maxResults: 5,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
      },
    },
  },
}
```

### 50. 工具参数

- 1. `query`（必需）
- 2. `count`（1–10；默认来自配置）
- 3. `country`（可选）：用于区域特定结果的 2 字母国家代码（例如 "DE"、"US"、"ALL"）。 4. 如果省略，Brave 会选择其默认区域。
- 5. `search_lang`（可选）：搜索结果的 ISO 语言代码（例如 "de"、"en"、"fr"）
- 6. `ui_lang`（可选）：UI 元素的 ISO 语言代码
- 7. `freshness`（可选，仅 Brave）：按发现时间过滤（`pd`、`pw`、`pm`、`py`，或 `YYYY-MM-DDtoYYYY-MM-DD`）

8. **示例：**

```javascript
9. // German-specific search
await web_search({
  query: "TV online schauen",
  count: 10,
  country: "DE",
  search_lang: "de",
});

// French search with French UI
await web_search({
  query: "actualités",
  country: "FR",
  search_lang: "fr",
  ui_lang: "fr",
});

// Recent results (past week)
await web_search({
  query: "TMBG interview",
  freshness: "pw",
});
```

## 10. web_fetch

11. 获取一个 URL 并提取可读内容。

### 12. web_fetch 要求

- 13. `tools.web.fetch.enabled` 不得为 `false`（默认：启用）
- 14. 可选的 Firecrawl 回退：设置 `tools.web.fetch.firecrawl.apiKey` 或 `FIRECRAWL_API_KEY`。

### 15. web_fetch 配置

```json5
16. {
  tools: {
    web: {
      fetch: {
        enabled: true,
        maxChars: 50000,
        maxCharsCap: 50000,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
        maxRedirects: 3,
        userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        readability: true,
        firecrawl: {
          enabled: true,
          apiKey: "FIRECRAWL_API_KEY_HERE", // optional if FIRECRAWL_API_KEY is set
          baseUrl: "https://api.firecrawl.dev",
          onlyMainContent: true,
          maxAgeMs: 86400000, // ms (1 day)
          timeoutSeconds: 60,
        },
      },
    },
  },
}
```

### 17. web_fetch 工具参数

- 18. `url`（必需，仅限 http/https）
- `extractMode` (`markdown` | `text`)
- 20. `maxChars`（截断过长页面）

21. 说明：

- 22. `web_fetch` 会先使用 Readability（主内容提取），然后使用 Firecrawl（如果已配置）。 23. 如果两者都失败，工具将返回错误。
- 24. Firecrawl 请求默认使用反机器人规避模式并缓存结果。
- 25. `web_fetch` 默认发送类似 Chrome 的 User-Agent 和 `Accept-Language`；如有需要可覆盖 `userAgent`。
- 26. `web_fetch` 会阻止私有/内部主机名并重新检查重定向（可通过 `maxRedirects` 限制）。
- 27. `maxChars` 会被限制在 `tools.web.fetch.maxCharsCap` 范围内。
- 28. `web_fetch` 是尽力而为的提取；某些网站需要使用浏览器工具。
- 29. 有关密钥设置和服务详情，请参见 [Firecrawl](/tools/firecrawl)。
- 30. 响应会被缓存（默认 15 分钟），以减少重复抓取。
- 31. 如果你使用工具配置文件/允许列表，请添加 `web_search`/`web_fetch` 或 `group:web`。
- 32. 如果缺少 Brave 密钥，`web_search` 会返回简短的设置提示并附带文档链接。
