---
summary: "适用于 iOS 和其他远程节点的网关所有节点配对（选项 B）"
read_when:
  - 在没有 macOS UI 的情况下实现节点配对审批
  - 添加用于批准远程节点的 CLI 流程
  - 通过节点管理扩展网关协议
title: "网关所有的配对"
---

# 网关所有的配对（选项 B）

在网关所有的配对中，**网关** 是决定哪些节点
允许加入的唯一真实来源。 UI（macOS 应用、未来的客户端）只是前端，
用于批准或拒绝待处理的请求。

**重要：** WS 节点在 `connect` 期间使用 **设备配对**（角色为 `node`）。
`node.pair.*` 是一个独立的配对存储，并且 **不会** 控制 WS 握手。
只有显式调用 `node.pair.*` 的客户端才会使用该流程。

## 概念

- **待处理请求**：节点请求加入；需要批准。
- **已配对节点**：已批准并获得授权令牌的节点。
- **传输**：网关 WS 端点转发请求，但不决定
  成员资格。 （旧版 TCP 桥接支持已弃用/移除。）

## 配对的工作方式

1. 节点连接到网关 WS 并请求配对。
2. 网关存储一个 **待处理请求** 并发出 `node.pair.requested`。
3. 你批准或拒绝该请求（CLI 或 UI）。
4. 批准后，网关会签发一个 **新令牌**（重新配对时令牌会轮换）。
5. 节点使用该令牌重新连接，现在即为“已配对”。

待处理请求会在 **5 分钟** 后自动过期。

## CLI 工作流（适合无界面环境）

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes reject <requestId>
openclaw nodes status
openclaw nodes rename --node <id|name|ip> --name "Living Room iPad"
```

`nodes status` 显示已配对/已连接的节点及其能力。

## API 表面（网关协议）

事件：

- `node.pair.requested` — 在创建新的待处理请求时发出。
- `node.pair.resolved` — 在请求被批准/拒绝/过期时发出。

方法：

- `node.pair.request` — 创建或复用一个待处理请求。
- `node.pair.list` — 列出待处理节点和已配对节点。
- `node.pair.approve` — 批准一个待处理请求（签发令牌）。
- `node.pair.reject` — 拒绝一个待处理请求。
- `node.pair.verify` — 验证 `{ nodeId, token }`。

说明：

- `node.pair.request` 对每个节点是幂等的：重复调用会返回相同的
  待处理请求。
- 批准 **始终** 会生成一个新的令牌；绝不会从
  `node.pair.request` 返回令牌。
- 请求可以包含 `silent: true`，作为自动批准流程的提示。

## 自动批准（macOS 应用）

在以下情况下，macOS 应用可以选择尝试 **静默批准**：

- 请求被标记为 `silent`，并且
- 1. 应用可以使用相同的用户验证到网关主机的 SSH 连接。

2. 如果静默批准失败，则回退到常规的“批准/拒绝”提示。

## 3. 存储（本地，私有）

4. 配对状态存储在 Gateway 状态目录下（默认 `~/.openclaw`）：

- 5. `~/.openclaw/nodes/paired.json`
- 6. `~/.openclaw/nodes/pending.json`

7. 如果你覆盖了 `OPENCLAW_STATE_DIR`，`nodes/` 文件夹会随之移动。

8. 安全说明：

- 9. 令牌是机密；请将 `paired.json` 视为敏感文件。
- 10. 轮换令牌需要重新批准（或删除节点条目）。

## 11. 传输行为

- 12. 该传输是**无状态**的；它不存储成员关系。
- 13. 如果 Gateway 离线或禁用了配对，节点将无法配对。
- 14. 如果 Gateway 处于远程模式，配对仍然针对远程 Gateway 的存储进行。
