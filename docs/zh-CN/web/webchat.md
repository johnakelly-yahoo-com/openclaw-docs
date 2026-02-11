---
summary: "用于聊天 UI 的回环 WebChat 静态主机与 Gateway WS 用法"
read_when:
  - 调试或配置 WebChat 访问
title: "WebChat"
---

# WebChat (Gateway WebSocket UI)

状态：macOS/iOS 的 SwiftUI 聊天 UI 直接与 Gateway WebSocket 通信。

## 它是什么

- 一个用于 Gateway 的原生聊天 UI（无内嵌浏览器，也无本地静态服务器）。
- 使用与其他通道相同的会话和路由规则。
- 确定性路由：回复始终返回到 WebChat。

## 快速开始

1. 启动 Gateway。
2. Open the WebChat UI (macOS/iOS app) or the Control UI chat tab.
3. 确保已配置 Gateway 认证（默认需要，即使在回环模式下）。

## 工作原理（行为）

- UI 连接到 Gateway WebSocket，并使用 `chat.history`、`chat.send` 和 `chat.inject`。
- `chat.inject` 会将一条助手备注直接追加到对话记录并广播到 UI（不运行代理）。
- 历史始终从 Gateway 获取（不进行本地文件监视）。
- 如果 Gateway 无法访问，WebChat 将为只读。

## 远程使用

- 远程模式通过 SSH/Tailscale 隧道转发 Gateway WebSocket。
- 你无需运行单独的 WebChat 服务器。

## 配置参考（WebChat）

完整配置：[Configuration](/gateway/configuration)

Channel options:

- No dedicated `webchat.*` block. WebChat uses the gateway endpoint + auth settings below.

Related global options:

- `gateway.port`, `gateway.bind`: WebSocket host/port.
- `gateway.auth.mode`, `gateway.auth.token`, `gateway.auth.password`: WebSocket auth.
- `gateway.remote.url`, `gateway.remote.token`, `gateway.remote.password`: remote gateway target.
- `session.*`: session storage and main key defaults.
