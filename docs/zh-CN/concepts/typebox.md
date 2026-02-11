---
summary: "9. 将 TypeBox schemas 作为网关协议的唯一事实来源"
read_when:
  - 10. 更新协议 schemas 或代码生成
title: "11. TypeBox"
---

# 12. TypeBox 作为协议的事实来源

13. 最后更新：2026-01-10

14. TypeBox 是一个以 TypeScript 为先的 schema 库。 15. 我们使用它来定义 **Gateway
    WebSocket 协议**（握手、请求/响应、服务器事件）。 16. 这些 schemas
    驱动 **运行时校验**、**JSON Schema 导出** 以及 macOS 应用的 **Swift 代码生成**。 17. 单一事实来源；其余一切均由此生成。

18. 如果你想了解更高层级的协议背景，请从
    [Gateway architecture](/concepts/architecture) 开始。

## 19. 心智模型（30 秒）

20. 每条 Gateway WS 消息都是以下三种帧之一：

- 21. **Request**：`{ type: "req", id, method, params }`
- 22. **Response**：`{ type: "res", id, ok, payload | error }`
- 23. **Event**：\`{ type: "event", event, payload, seq?, stateVersion?
  24. }`25. 第一帧**必须**是一个`connect\` 请求。

26. 之后，客户端可以调用
    方法（例如 `health`、`send`、`chat.send`）并订阅事件（例如
    `presence`、`tick`、`agent`）。 27. 连接流程（最小）：

28. Client                    Gateway
    \|---- req:connect -------->|
    |<---- res:hello-ok --------|
    |<---- event:tick ----------|
    \|---- req:health ---------->|
    |<---- res:health ----------|

```
29. 常用方法 + 事件：
```

30. 分类

| 31. 示例                                                    | 32. 说明                         | 33. 核心 |
| -------------------------------------------------------------------------------- | ----------------------------------------------------- | ----------------------------- |
| 34. `connect`、`health`、`status`                           | 35. `connect` 必须首先调用           | 36. 消息 |
| 37. `send`、`poll`、`agent`、`agent.wait`                    | 38. 有副作用的操作需要 `idempotencyKey` | 39. 聊天 |
| 40. `chat.history`、`chat.send`、`chat.abort`、`chat.inject` | 41. WebChat 使用这些               | 42. 会话 |
| 43. `sessions.list`、`sessions.patch`、`sessions.delete`    | 44. 会话管理                       | 45. 节点 |
| 46. `node.list`、`node.invoke`、`node.pair.*`               | 47. Gateway WS + 节点操作          | 48. 事件 |
| 49. `tick`、`presence`、`agent`、`chat`、`health`、`shutdown`  | 50. 服务器推送                      | server push                   |

权威列表位于 `src/gateway/server.ts`（`METHODS`、`EVENTS`）。

## 模式所在的位置

- Source: `src/gateway/protocol/schema.ts`
- 运行时校验器（AJV）：`src/gateway/protocol/index.ts`
- 服务器握手 + 方法分发：`src/gateway/server.ts`
- Node 客户端：`src/gateway/client.ts`
- 生成的 JSON Schema：`dist/protocol.schema.json`
- 生成的 Swift 模型：`apps/macos/Sources/OpenClawProtocol/GatewayModels.swift`

## 当前流水线

- `pnpm protocol:gen`
  - 将 JSON Schema（draft‑07）写入 `dist/protocol.schema.json`
- `pnpm protocol:gen:swift`
  - 生成 Swift 网关模型
- `pnpm protocol:check`
  - 运行两个生成器并验证输出已提交

## 运行时如何使用这些模式

- **服务器端**：每个入站帧都会使用 AJV 进行校验。 握手阶段只
  接受其 params 匹配 `ConnectParams` 的 `connect` 请求。
- **Client side**: the JS client validates event and response frames before
  using them.
- **方法面**：Gateway 会在 `hello-ok` 中公布支持的 `methods` 和
  `events`。

## 示例帧

连接（第一条消息）：

```json
{
  "type": "req",
  "id": "c1",
  "method": "connect",
  "params": {
    "minProtocol": 2,
    "maxProtocol": 2,
    "client": {
      "id": "openclaw-macos",
      "displayName": "macos",
      "version": "1.0.0",
      "platform": "macos 15.1",
      "mode": "ui",
      "instanceId": "A1B2"
    }
  }
}
```

Hello-ok response:

```json
{
  "type": "res",
  "id": "c1",
  "ok": true,
  "payload": {
    "type": "hello-ok",
    "protocol": 2,
    "server": { "version": "dev", "connId": "ws-1" },
    "features": { "methods": ["health"], "events": ["tick"] },
    "snapshot": {
      "presence": [],
      "health": {},
      "stateVersion": { "presence": 0, "health": 0 },
      "uptimeMs": 0
    },
    "policy": { "maxPayload": 1048576, "maxBufferedBytes": 1048576, "tickIntervalMs": 30000 }
  }
}
```

请求 + 响应：

```json
{ "type": "req", "id": "r1", "method": "health" }
```

```json
{ "type": "res", "id": "r1", "ok": true, "payload": { "ok": true } }
```

事件：

```json
{ "type": "event", "event": "tick", "payload": { "ts": 1730000000 }, "seq": 12 }
```

## 最小客户端（Node.js）

最小但有用的流程：connect + health。

```ts
import { WebSocket } from "ws";

const ws = new WebSocket("ws://127.0.0.1:18789");

ws.on("open", () => {
  ws.send(
    JSON.stringify({
      type: "req",
      id: "c1",
      method: "connect",
      params: {
        minProtocol: 3,
        maxProtocol: 3,
        client: {
          id: "cli",
          displayName: "example",
          version: "dev",
          platform: "node",
          mode: "cli",
        },
      },
    }),
  );
});

ws.on("message", (data) => {
  const msg = JSON.parse(String(data));
  if (msg.type === "res" && msg.id === "c1" && msg.ok) {
    ws.send(JSON.stringify({ type: "req", id: "h1", method: "health" }));
  }
  if (msg.type === "res" && msg.id === "h1") {
    console.log("health:", msg.payload);
    ws.close();
  }
});
```

## 完整示例：端到端新增一个方法

示例：新增一个 `system.echo` 请求，返回 `{ ok: true, text }`。

1. **Schema（事实来源）**

添加到 `src/gateway/protocol/schema.ts`：

```ts
export const SystemEchoParamsSchema = Type.Object(
  { text: NonEmptyString },
  { additionalProperties: false },
);

export const SystemEchoResultSchema = Type.Object(
  { ok: Type.Boolean(), text: NonEmptyString },
  { additionalProperties: false },
);
```

将二者加入 `ProtocolSchemas` 并导出类型：

```ts
  SystemEchoParams: SystemEchoParamsSchema,
  SystemEchoResult: SystemEchoResultSchema,
```

```ts
export type SystemEchoParams = Static<typeof SystemEchoParamsSchema>;
export type SystemEchoResult = Static<typeof SystemEchoResultSchema>;
```

2. **校验**

In `src/gateway/protocol/index.ts`, export an AJV validator:

```ts
export const validateSystemEchoParams = ajv.compile<SystemEchoParams>(SystemEchoParamsSchema);
```

3. **服务器行为**

在 `src/gateway/server-methods/system.ts` 中添加一个处理器：

```ts
export const systemHandlers: GatewayRequestHandlers = {
  "system.echo": ({ params, respond }) => {
    const text = String(params.text ?? "");
    respond(true, { ok: true, text });
  },
};
```

在 `src/gateway/server-methods.ts` 中注册它（该文件已合并 `systemHandlers`），
然后在 `src/gateway/server.ts` 的 `METHODS` 中添加 `"system.echo"`。

4. **Regenerate**

```bash
pnpm protocol:check
```

5. **Tests + docs**

Add a server test in `src/gateway/server.*.test.ts` and note the method in docs.

## Swift codegen behavior

The Swift generator emits:

- `GatewayFrame` enum with `req`, `res`, `event`, and `unknown` cases
- Strongly typed payload structs/enums
- `ErrorCode` values and `GATEWAY_PROTOCOL_VERSION`

Unknown frame types are preserved as raw payloads for forward compatibility.

## Versioning + compatibility

- `PROTOCOL_VERSION` lives in `src/gateway/protocol/schema.ts`.
- Clients send `minProtocol` + `maxProtocol`; the server rejects mismatches.
- The Swift models keep unknown frame types to avoid breaking older clients.

## Schema patterns and conventions

- Most objects use `additionalProperties: false` for strict payloads.
- `NonEmptyString` is the default for IDs and method/event names.
- The top-level `GatewayFrame` uses a **discriminator** on `type`.
- Methods with side effects usually require an `idempotencyKey` in params
  (example: `send`, `poll`, `agent`, `chat.send`).

## Live schema JSON

Generated JSON Schema is in the repo at `dist/protocol.schema.json`. The
published raw file is typically available at:

- [https://raw.githubusercontent.com/openclaw/openclaw/main/dist/protocol.schema.json](https://raw.githubusercontent.com/openclaw/openclaw/main/dist/protocol.schema.json)

## When you change schemas

1. Update the TypeBox schemas.
2. Run `pnpm protocol:check`.
3. Commit the regenerated schema + Swift models.
