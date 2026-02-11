---
summary: "通过 Gateway HTTP 端点直接调用单个工具"
read_when:
  - 在不运行完整 agent 回合的情况下调用工具
  - 构建需要工具策略强制执行的自动化
title: "Tools Invoke API"
---

# Tools Invoke（HTTP）

OpenClaw 的 Gateway 暴露了一个简单的 HTTP 端点，用于直接调用单个工具。 该端点始终启用，但受 Gateway 认证和工具策略的限制。

- `POST /tools/invoke`
- Same port as the Gateway (WS + HTTP multiplex): `http://<gateway-host>:<port>/tools/invoke`

默认最大负载大小为 2 MB。

## 认证

Uses the Gateway auth configuration. 发送 Bearer token：

- `Authorization: Bearer <token>`

注意：

- 1. 当 `gateway.auth.mode="token"` 时，使用 `gateway.auth.token`（或 `OPENCLAW_GATEWAY_TOKEN`）。
- When `gateway.auth.mode="password"`, use `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`).

## 3. 请求体

```json
4. {
  "tool": "sessions_list",
  "action": "json",
  "args": {},
  "sessionKey": "main",
  "dryRun": false
}
```

Fields:

- 6. `tool`（string，必需）：要调用的工具名称。
- 7. `action`（string，可选）：如果工具 schema 支持 `action` 且 args 载荷中未包含它，则会映射进 args。
- 8. `args`（object，可选）：工具特定的参数。
- 9. `sessionKey`（string，可选）：目标会话键。 10. 如果省略或为 `"main"`，Gateway 将使用配置的主会话键（遵循 `session.mainKey` 和默认 agent，或在全局作用域中使用 `global`）。
- 11. `dryRun`（boolean，可选）：为将来使用预留；当前会被忽略。

## 12. 策略 + 路由行为

13. 工具可用性会通过与 Gateway agents 使用的同一策略链进行过滤：

- 14. `tools.profile` / `tools.byProvider.profile`
- 15. `tools.allow` / `tools.byProvider.allow`
- 16. `agents.<id>`17. `.tools.allow` / `agents.<id>`18. `.tools.byProvider.allow`
- 19. 组策略（如果会话键映射到某个组或频道）
- 20. 子代理策略（当使用子代理会话键进行调用时）

If a tool is not allowed by policy, the endpoint returns **404**.

22. 为了帮助组策略解析上下文，你可以选择性地设置：

- 23. `x-openclaw-message-channel: <channel>`（示例：`slack`、`telegram`）
- 24. `x-openclaw-account-id: <accountId>`（当存在多个账户时）

## 25. 响应

- 26. `200` → `{ ok: true, result }`
- 27. `400` → `{ ok: false, error: { type, message } }`（无效请求或工具错误）
- 28. `401` → 未授权
- 29. `404` → 工具不可用（未找到或未在允许列表中）
- `405` → method not allowed

## 31. 示例

```bash
32. curl -sS http://127.0.0.1:18789/tools/invoke \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "tool": "sessions_list",
    "action": "json",
    "args": {}
  }'
```
