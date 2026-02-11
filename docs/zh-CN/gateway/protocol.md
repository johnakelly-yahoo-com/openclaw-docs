---
summary: "15. Gateway WebSocket 协议：握手、帧、版本控制"
read_when:
  - 16. 实现或更新 Gateway WS 客户端
  - 17. 调试协议不匹配或连接失败
  - 18. 重新生成协议 schema / 模型
title: "19. Gateway 协议"
---

# 20. Gateway 协议（WebSocket）

21. Gateway WS 协议是 OpenClaw 的**单一控制平面 + 节点传输**。 22. 所有客户端（CLI、Web UI、macOS 应用、iOS/Android 节点、无头节点）都通过 WebSocket 连接，并在握手时声明其**角色** + **作用域**。

## 传输

- 24. WebSocket，使用带有 JSON 负载的文本帧。
- 25. 第一帧**必须**是一个 `connect` 请求。

## 26. 握手（connect）

27. Gateway → Client（预连接挑战）：

```json
{
  "type": "event",
  "event": "connect.challenge",
  "payload": { "nonce": "…", "ts": 1737264000000 }
}
```

29. Client → Gateway：

```json
{
  "type": "req",
  "id": "…",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 3,
    "client": {
      "id": "cli",
      "version": "1.2.3",
      "platform": "macos",
      "mode": "operator"
    },
    "role": "operator",
    "scopes": ["operator.read", "operator.write"],
    "caps": [],
    "commands": [],
    "permissions": {},
    "auth": { "token": "…" },
    "locale": "en-US",
    "userAgent": "openclaw-cli/1.2.3",
    "device": {
      "id": "device_fingerprint",
      "publicKey": "…",
      "signature": "…",
      "signedAt": 1737264000000,
      "nonce": "…"
    }
  }
}
```

31. Gateway → Client：

```json
{
  "type": "res",
  "id": "…",
  "ok": true,
  "payload": { "type": "hello-ok", "protocol": 3, "policy": { "tickIntervalMs": 15000 } }
}
```

33. 当设备令牌被签发时，`hello-ok` 还会包含：

```json
{
  "auth": {
    "deviceToken": "…",
    "role": "operator",
    "scopes": ["operator.read", "operator.write"]
  }
}
```

### 35. 节点示例

```json
{
  "type": "req",
  "id": "…",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 3,
    "client": {
      "id": "ios-node",
      "version": "1.2.3",
      "platform": "ios",
      "mode": "node"
    },
    "role": "node",
    "scopes": [],
    "caps": ["camera", "canvas", "screen", "location", "voice"],
    "commands": ["camera.snap", "canvas.navigate", "screen.record", "location.get"],
    "permissions": { "camera.capture": true, "screen.record": false },
    "auth": { "token": "…" },
    "locale": "en-US",
    "userAgent": "openclaw-ios/1.2.3",
    "device": {
      "id": "device_fingerprint",
      "publicKey": "…",
      "signature": "…",
      "signedAt": 1737264000000,
      "nonce": "…"
    }
  }
}
```

## 37. 帧格式

- **请求**：`{type:"req", id, method, params}`
- **响应**：`{type:"res", id, ok, payload|error}`
- 40. **事件**：`{type:"event", event, payload, seq?, stateVersion?}`

41. 具有副作用的方法需要 **幂等键**（参见 schema）。

## 42. 角色 + 作用域

### 43. 角色

- 44. `operator` = 控制平面客户端（CLI / UI / 自动化）。
- 45. `node` = 能力宿主（camera / screen / canvas / system.run）。

### 46. 作用域（operator）

47. 常用作用域：

- 48. `operator.read`
- 49. `operator.write`
- 50. `operator.admin`
- `operator.approvals`
- `operator.pairing`

### 功能/命令/权限（节点）

节点在连接时声明能力声明：

- `caps`：高层级能力类别。
- `commands`：可调用命令的允许列表。
- `permissions`：细粒度开关（例如 `screen.record`、`camera.capture`）。

Gateway 将这些视为**声明**并在服务器端强制执行允许列表。

## 在线状态

- `system-presence` 返回以设备身份为键的条目。
- 在线状态条目包含 `deviceId`、`roles` 和 `scopes`，以便 UI 即使设备同时以 **operator** 和 **node** 连接，也能为每个设备显示一行。

### 节点辅助方法

- 节点可以调用 `skills.bins` 来获取当前技能可执行文件列表，用于自动允许检查。

## 执行审批

- 当执行请求需要审批时，网关会广播 `exec.approval.requested`。
- Operator 客户端通过调用 `exec.approval.resolve` 进行处理（需要 `operator.approvals` scope）。

## 版本控制

- `PROTOCOL_VERSION` 位于 `src/gateway/protocol/schema.ts`。
- 客户端发送 `minProtocol` + `maxProtocol`；服务器会拒绝不匹配的情况。
- Schema + model 由 TypeBox 定义生成：
  - `pnpm protocol:gen`
  - `pnpm protocol:gen:swift`
  - `pnpm protocol:check`

## 认证

- 如果设置了 `OPENCLAW_GATEWAY_TOKEN`（或 `--token`），则 `connect.params.auth.token` 必须匹配，否则将关闭 socket。
- 配对完成后，Gateway 会签发一个**设备令牌**，其作用域限定为连接的角色 + scopes。 该令牌在 `hello-ok.auth.deviceToken` 中返回，客户端应将其持久化以供后续连接使用。
- 设备令牌可通过 `device.token.rotate` 和 `device.token.revoke` 进行轮换/吊销（需要 `operator.pairing` scope）。

## 设备身份 + 配对

- 节点应包含一个稳定的设备标识（`device.id`），该标识应来源于密钥对指纹。
- Gateway 会按设备 + 角色签发令牌。
- 除非启用了本地自动审批，否则新的设备 ID 需要配对审批。
- **本地**连接包括回环地址以及网关主机自身的 tailnet 地址（因此同主机的 tailnet 绑定仍可自动审批）。
- 所有 WS 客户端在 `connect` 期间都必须包含 `device` 身份（operator + node）。
  仅当启用 `gateway.controlUi.allowInsecureAuth`（或用于紧急情况的 `gateway.controlUi.dangerouslyDisableDeviceAuth`）时，控制 UI 才可省略。
- 非本地连接必须对服务器提供的 `connect.challenge` 随机数进行签名。

## TLS + 证书固定

- WS 连接支持 TLS。
- 客户端可以选择固定网关证书指纹（参见 `gateway.tls` 配置，以及 `gateway.remote.tlsFingerprint` 或 CLI `--tls-fingerprint`）。

## 作用域

该协议暴露**完整的网关 API**（状态、通道、模型、聊天、agent、会话、节点、审批等）。 确切的接口由 `src/gateway/protocol/schema.ts` 中的 TypeBox schema 定义。
