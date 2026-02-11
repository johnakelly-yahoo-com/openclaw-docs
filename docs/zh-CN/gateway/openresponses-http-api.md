---
summary: "Expose an OpenResponses-compatible /v1/responses HTTP endpoint from the Gateway"
read_when:
  - Integrating clients that speak the OpenResponses API
  - You want item-based inputs, client tool calls, or SSE events
title: "OpenResponses API"
---

# OpenResponses API (HTTP)

OpenClaw’s Gateway can serve an OpenResponses-compatible `POST /v1/responses` endpoint.

This endpoint is **disabled by default**. Enable it in config first.

- `POST /v1/responses`
- Same port as the Gateway (WS + HTTP multiplex): `http://<gateway-host>:<port>/v1/responses`

Under the hood, requests are executed as a normal Gateway agent run (same codepath as
`openclaw agent`), so routing/permissions/config match your Gateway.

## Authentication

Uses the Gateway auth configuration. Send a bearer token:

- `Authorization: Bearer <token>`

Notes:

- When `gateway.auth.mode="token"`, use `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`).
- When `gateway.auth.mode="password"`, use `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`).

## Choosing an agent

No custom headers required: encode the agent id in the OpenResponses `model` field:

- `model: "openclaw:<agentId>"`（示例：`"openclaw:main"`、`"openclaw:beta"`）
- `model: "agent:<agentId>"` (alias)

或者通过请求头指定特定的 OpenClaw agent：

- `x-openclaw-agent-id: <agentId>`（默认：`main`）

Advanced:

- `x-openclaw-session-key: <sessionKey>` to fully control session routing.

## 1. 启用端点

2. 将 `gateway.http.endpoints.responses.enabled` 设置为 `true`：

```json5
3. {
  gateway: {
    http: {
      endpoints: {
        responses: { enabled: true },
      },
    },
  },
}
```

## 禁用该端点

5. 将 `gateway.http.endpoints.responses.enabled` 设置为 `false`：

```json5
6. {
  gateway: {
    http: {
      endpoints: {
        responses: { enabled: false },
      },
    },
  },
}
```

## 7. 会话行为

默认情况下，该端点是**按请求无状态的**（每次调用都会生成一个新的会话密钥）。

9. 如果请求包含 OpenResponses 的 `user` 字符串，Gateway 会从中派生一个稳定的会话键，因此重复调用可以共享同一个代理会话。

## 10. 请求结构（支持）

该请求遵循 OpenResponses API，并使用基于 item 的输入。 当前支持：

- 13. `input`：字符串或 item 对象数组。
- 14. `instructions`：合并到系统提示中。
- `tools`：客户端工具定义（函数工具）。
- 16. `tool_choice`：过滤或强制使用客户端工具。
- 17. `stream`：启用 SSE 流式传输。
- 18. `max_output_tokens`：尽力而为的输出长度限制（取决于提供方）。
- 19. `user`：稳定的会话路由。

20. 接受但**当前被忽略**：

- 21. `max_tool_calls`
- 22. `reasoning`
- 23. `metadata`
- 24. `store`
- 25. `previous_response_id`
- 26. `truncation`

## 27. Items（输入）

### 28. `message`

29. 角色：`system`、`developer`、`user`、`assistant`。

- 30. `system` 和 `developer` 会被追加到系统提示中。
- The most recent `user` or `function_call_output` item becomes the “current message.”
- 32. 更早的 user/assistant 消息会作为历史记录包含在上下文中。

### 33. `function_call_output`（回合制工具）

34. 将工具结果发送回模型：

```json
35. {
  "type": "function_call_output",
  "call_id": "call_123",
  "output": "{\"temperature\": \"72F\"}"
}
```

### 36. `reasoning` 和 `item_reference`

37. 为了模式兼容性而接受，但在构建提示时会被忽略。

## 38. 工具（客户端函数工具）

39. 使用 \`tools: [{ type: "function", function: { name, description?, parameters?
40. } }]`提供工具。 41. 如果代理决定调用工具，响应将返回一个`function_call\` 输出 item。

42. 然后你需要发送一个包含 `function_call_output` 的后续请求以继续该回合。
43. 图像（`input_image`）

## 44. 支持 base64 或 URL 来源：

45. {
    "type": "input_image",
    "source": { "type": "url", "url": "https://example.com/image.png" }
    }

```json
46. 允许的 MIME 类型（当前）：`image/jpeg`、`image/png`、`image/gif`、`image/webp`。
```

47. 最大大小（当前）：10MB。
48. 文件（`input_file`）

## 49. 支持 base64 或 URL 来源：

50. {
    "type": "input_file",
    "source": {
    "type": "base64",
    "media_type": "text/plain",
    "data": "SGVsbG8gV29ybGQh",
    "filename": "hello.txt"
    }
    }

```json
{
  "type": "input_file",
  "source": {
    "type": "base64",
    "media_type": "text/plain",
    "data": "SGVsbG8gV29ybGQh",
    "filename": "hello.txt"
  }
}
```

1. 允许的 MIME 类型（当前）：`text/plain`、`text/markdown`、`text/html`、`text/csv`，
   `application/json`、`application/pdf`。

2. 最大大小（当前）：5MB。

Current behavior:

- 4. 文件内容会被解码并添加到 **system prompt** 中，而不是用户消息中，
     因此它是临时的（不会持久化到会话历史中）。
- 5. 会对 PDF 进行文本解析。 6. 如果检测到的文本较少，则会将前几页栅格化为图像并传递给模型。

7. PDF 解析使用对 Node 友好的 `pdfjs-dist` 旧版构建（无 worker）。 现代版的 PDF.js 构建依赖浏览器 worker/DOM 全局对象，因此在 Gateway 中未使用。

9. URL 获取默认设置：

- `files.allowUrl`：`true`
- 11. `images.allowUrl`: `true`
- 12. 请求受到防护（DNS 解析、私有 IP 阻止、重定向上限、超时）。

## 13. 文件 + 图片限制（配置）

14. 默认值可在 `gateway.http.endpoints.responses` 下进行调整：

```json5
15. {
  gateway: {
    http: {
      endpoints: {
        responses: {
          enabled: true,
          maxBodyBytes: 20000000,
          files: {
            allowUrl: true,
            allowedMimes: [
              "text/plain",
              "text/markdown",
              "text/html",
              "text/csv",
              "application/json",
              "application/pdf",
            ],
            maxBytes: 5242880,
            maxChars: 200000,
            maxRedirects: 3,
            timeoutMs: 10000,
            pdf: {
              maxPages: 4,
              maxPixels: 4000000,
              minTextChars: 200,
            },
          },
          images: {
            allowUrl: true,
            allowedMimes: ["image/jpeg", "image/png", "image/gif", "image/webp"],
            maxBytes: 10485760,
            maxRedirects: 3,
            timeoutMs: 10000,
          },
        },
      },
    },
  },
}
```

16. 省略时的默认值：

- 17. `maxBodyBytes`: 20MB
- 18. `files.maxBytes`: 5MB
- 19. `files.maxChars`: 200k
- 20. `files.maxRedirects`: 3
- 21. `files.timeoutMs`: 10s
- 22. `files.pdf.maxPages`: 4
- 23. `files.pdf.maxPixels`: 4,000,000
- `files.pdf.minTextChars`：200
- 25. `images.maxBytes`: 10MB
- 26. `images.maxRedirects`: 3
- 27. `images.timeoutMs`: 10s

## 28. 流式传输（SSE）

29. 设置 `stream: true` 以接收 Server-Sent Events（SSE）：

- 30. `Content-Type: text/event-stream`
- 31. 每一行事件为 `event: <type>` 和 `data: <json>`
- 32. 流以 `data: [DONE]` 结束

33. 当前会发出的事件类型：

- 34. `response.created`
- 35. `response.in_progress`
- 36. `response.output_item.added`
- 37. `response.content_part.added`
- 38. `response.output_text.delta`
- 39. `response.output_text.done`
- 40. `response.content_part.done`
- 41. `response.output_item.done`
- 42. `response.completed`
- 43. `response.failed`（发生错误时）

## 44. 用量

45. 当底层提供方报告 token 计数时，会填充 `usage`。

## 46. 错误

47. 错误使用如下形式的 JSON 对象：

```json
48. { "error": { "message": "...", "type": "invalid_request_error" } }
```

49. 常见情况：

- 50. `401` 缺少/无效的认证
- `400` 无效的请求体
- `405` 错误的方法

## 示例

非流式：

```bash
curl -sS http://127.0.0.1:18789/v1/responses \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "input": "hi"
  }'
```

流式：

```bash
curl -N http://127.0.0.1:18789/v1/responses \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "stream": true,
    "input": "hi"
  }'
```
