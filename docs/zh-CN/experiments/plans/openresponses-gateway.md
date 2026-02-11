---
summary: "Plan: Add OpenResponses /v1/responses endpoint and deprecate chat completions cleanly"
owner: "openclaw"
status: "draft"
last_updated: "2026-01-19"
title: "OpenResponses Gateway Plan"
---

# OpenResponses Gateway Integration Plan

## Context

OpenClaw Gateway currently exposes a minimal OpenAI-compatible Chat Completions endpoint at
`/v1/chat/completions` (see [OpenAI Chat Completions](/gateway/openai-http-api)).

Open Responses is an open inference standard based on the OpenAI Responses API. It is designed
for agentic workflows and uses item-based inputs plus semantic streaming events. The OpenResponses
spec defines `/v1/responses`, not `/v1/chat/completions`.

## Goals

- Add a `/v1/responses` endpoint that adheres to OpenResponses semantics.
- Keep Chat Completions as a compatibility layer that is easy to disable and eventually remove.
- Standardize validation and parsing with isolated, reusable schemas.

## Non-goals

- Full OpenResponses feature parity in the first pass (images, files, hosted tools).
- Replacing internal agent execution logic or tool orchestration.
- Changing the existing `/v1/chat/completions` behavior during the first phase.

## Research Summary

Sources: OpenResponses OpenAPI, OpenResponses specification site, and the Hugging Face blog post.

Key points extracted:

- `POST /v1/responses` accepts `CreateResponseBody` fields like `model`, `input` (string or
  `ItemParam[]`), `instructions`, `tools`, `tool_choice`, `stream`, `max_output_tokens`, and
  `max_tool_calls`.
- `ItemParam` is a discriminated union of:
  - `message` items with roles `system`, `developer`, `user`, `assistant`
  - `function_call` and `function_call_output`
  - `reasoning`
  - `item_reference`
- Successful responses return a `ResponseResource` with `object: "response"`, `status`, and
  `output` items.
- Streaming uses semantic events such as:
  - `response.created`, `response.in_progress`, `response.completed`, `response.failed`
  - `response.output_item.added`, `response.output_item.done`
  - `response.content_part.added`, `response.content_part.done`
  - `response.output_text.delta`, `response.output_text.done`
- The spec requires:
  - `Content-Type: text/event-stream`
  - 2. 终止事件必须是字面量 `[DONE]`
  - 3. 推理项可以暴露 `content`、`encrypted_content` 和 `summary`。
- 4. HF 示例在请求中包含 `OpenResponses-Version: latest`（可选请求头）。
- 5. 拟议架构

## 6. 添加仅包含 Zod schema 的 `src/gateway/open-responses.schema.ts`（不引入 gateway 相关内容）。

- 7. 为 `/v1/responses` 添加 `src/gateway/openresponses-http.ts`（或 `open-responses-http.ts`）。
- 8. 保持 `src/gateway/openai-http.ts` 不变，作为遗留兼容适配器。
- 9. 添加配置 `gateway.http.endpoints.responses.enabled`（默认 `false`）。
- 10. 保持 `gateway.http.endpoints.chatCompletions.enabled` 相互独立；允许两个端点分别
      单独切换。
- 11. 当启用 Chat Completions 时，在启动时发出警告以提示其遗留状态。
- 12. Chat Completions 的弃用路径

## 13. 维持严格的模块边界：Responses 与 Chat Completions 之间不共享 schema 类型。

- 14. 通过配置将 Chat Completions 设为可选启用，以便无需代码变更即可禁用。
- 15. 在 `/v1/responses` 稳定后，更新文档将 Chat Completions 标注为遗留。
- 16. 可选的未来步骤：将 Chat Completions 请求映射到 Responses 处理器，以简化
      移除路径。
- 17. 第 1 阶段支持子集

## 18. 接受 `input` 为字符串或 `ItemParam[]`，包含消息角色和 `function_call_output`。

- 19. 将 system 和 developer 消息提取到 `extraSystemPrompt` 中。
- 20. 使用最近的 `user` 或 `function_call_output` 作为 agent 运行的当前消息。
- 21. 对不支持的内容部分（image/file）以 `invalid_request_error` 拒绝。
- 22. 返回单条包含 `output_text` 内容的 assistant 消息。
- 23. 在令牌计数接入之前，返回数值为零的 `usage`。
- 24. 校验策略（无 SDK）

## 25. 为以下受支持子集实现 Zod schemas：

- 26. `CreateResponseBody`
  - 27. `ItemParam` + 消息内容部分联合类型
  - 28. `ResponseResource`
  - 29. 网关使用的流式事件形状
  - 30. 将 schemas 保持在单一、隔离的模块中，以避免漂移并支持未来代码生成。
- 31. 流式实现（第 1 阶段）

## 32. SSE 行同时包含 `event:` 和 `data:`。

- 33. 所需顺序（最小可行）：
- 34. `response.created`
  - 35. `response.output_item.added`
  - 36. `response.content_part.added`
  - 37. `response.output_text.delta`（按需重复）
  - 38. `response.output_text.done`
  - 39. `response.content_part.done`
  - 40. `response.completed`
  - 41. `[DONE]`
  - 42. 测试与验证计划

## 43. 为 `/v1/responses` 添加 e2e 覆盖：

- 44. 需要鉴权
  - 45. 非流式响应形状
  - 46. 流事件顺序与 `[DONE]`
  - 47. 通过请求头和 `user` 进行会话路由
  - 48. 保持 `src/gateway/openai-http.e2e.test.ts` 不变。
- 49. 手动：使用 curl 请求 `/v1/responses` 并设置 `stream: true`，验证事件顺序以及终止
      `[DONE]`。
- 50. 文档更新（后续）

## Doc Updates (Follow-up)

- Add a new docs page for `/v1/responses` usage and examples.
- Update `/gateway/openai-http-api` with a legacy note and pointer to `/v1/responses`.
