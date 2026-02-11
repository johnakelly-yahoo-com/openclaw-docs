---
summary: "用于查找网关的节点发现与传输（Bonjour、Tailscale、SSH）"
read_when:
  - 实现或更改 Bonjour 发现/广播
  - 调整远程连接模式（直连 vs SSH）
  - 为远程节点设计节点发现与配对
title: "发现与传输"
---

# 23. 发现与传输

OpenClaw 有两个在表面上看起来相似的不同问题：

1. **操作员远程控制**：macOS 菜单栏应用控制运行在其他位置的网关。
2. 24. **节点配对**：iOS/Android（以及未来的节点）发现网关并安全配对。

25) 设计目标是将所有网络发现/广告保留在 **Node Gateway**（`openclaw gateway`）中，并让客户端（Mac 应用、iOS）作为消费者。

## 26. 术语

- **Gateway**：一个长期运行的网关进程，拥有状态（会话、配对、节点注册表）并运行各个渠道。 大多数设置每台主机使用一个；也可以使用隔离的多网关设置。
- 27. **Gateway WS（控制平面）**：默认位于 `127.0.0.1:18789` 的 WebSocket 端点；可通过 `gateway.bind` 绑定到 LAN/尾网。
- **直连 WS 传输**：面向 LAN/tailnet 的 Gateway WS 端点（无 SSH）。
- **SSH 传输（回退）**：通过 SSH 转发 `127.0.0.1:18789` 进行远程控制。
- 28. **旧版 TCP 桥接（已弃用/移除）**：较早的节点传输方式（参见 [Bridge protocol](/gateway/bridge-protocol)）；不再用于发现广播。

协议详情：

- [Gateway protocol](/gateway/protocol)
- [Bridge protocol（旧版）](/gateway/bridge-protocol)

## 为何同时保留“直连”和 SSH

- 29. **Direct WS** 在同一网络和尾网内提供最佳用户体验：
  - 通过 Bonjour 在 LAN 上自动发现
  - 由网关拥有的配对令牌 + ACL
  - 无需 shell 访问；协议面可以保持紧凑且可审计
- **SSH** 仍然是通用的回退方案：
  - 在任何有 SSH 访问的地方都可工作（即使跨越不相关的网络）
  - 可应对组播/mDNS 问题
  - 除 SSH 外无需新的入站端口

## 发现输入（客户端如何得知网关位置）

### 1）Bonjour / mDNS（仅限 LAN）

Bonjour 是尽力而为的，且不跨网络。 它仅用于“同一 LAN”的便利性。

1. 目标方向：

- 2. **网关** 通过 Bonjour 广播其 WS 端点。
- 3. 客户端进行浏览并显示“选择一个网关”的列表，然后存储所选端点。

4. 故障排查和信标详情：[Bonjour](/gateway/bonjour)。

#### 5. 服务信标详情

- 6. 服务类型：
  - 7. `_openclaw-gw._tcp`（网关传输信标）
- 8. TXT 键（非机密）：
  - 9. `role=gateway`
  - 10. `lanHost=<hostname>.local`
  - 11. `sshPort=22`（或所广播的其他端口）
  - 12. `gatewayPort=18789`（网关 WS + HTTP）
  - 13. `gatewayTls=1`（仅在启用 TLS 时）
  - 14. `gatewayTlsSha256=<sha256>`（仅在启用 TLS 且指纹可用时）
  - 15. `canvasPort=18793`（默认画布主机端口；提供 `/__openclaw__/canvas/`）
  - 16. `cliPath=<path>`（可选；指向可运行的 `openclaw` 入口点或二进制文件的绝对路径）
  - 17. `tailnetDns=<magicdns>`（可选提示；当 Tailscale 可用时自动检测）

18. 禁用/覆盖：

- 19. `OPENCLAW_DISABLE_BONJOUR=1` 禁用广播。
- 20. `~/.openclaw/openclaw.json` 中的 `gateway.bind` 控制网关的绑定模式。
- 21. `OPENCLAW_SSH_PORT` 覆盖在 TXT 中广播的 SSH 端口（默认为 22）。
- 22. `OPENCLAW_TAILNET_DNS` 发布一个 `tailnetDns` 提示（MagicDNS）。
- 23. `OPENCLAW_CLI_PATH` 覆盖所广播的 CLI 路径。

### 24. 2. Tailnet（跨网络）

25. 对于伦敦/维也纳风格的部署，Bonjour 将无济于事。 26. 推荐的“直连”目标是：

- 27. Tailscale MagicDNS 名称（优先）或稳定的 tailnet IP。

28. 如果网关能检测到其运行在 Tailscale 下，它会将 `tailnetDns` 作为可选提示发布给客户端（包括广域信标）。

### 29. 3. 手动 / SSH 目标

30. 当没有直连路由（或直连被禁用）时，客户端始终可以通过转发回环网关端口的方式经由 SSH 连接。

31. 参见 [远程访问](/gateway/remote)。

## 32. 传输选择（客户端策略）

33. 推荐的客户端行为：

1. 34. 如果已配置并可达已配对的直连端点，则使用它。
2. 35. 否则，如果 Bonjour 在 LAN 上发现网关，提供一键“使用此网关”的选项，并将其保存为直连端点。
3. 36. 否则，如果已配置 tailnet DNS/IP，则尝试直连。
4. 37. 否则，回退到 SSH。

## 38) 配对 + 认证（直连传输）

39. 网关是节点/客户端准入的唯一事实来源。

- 40. 配对请求在网关中创建/批准/拒绝（参见 [网关配对](/gateway/pairing)）。
- 41. 网关强制执行：
  - 42. 认证（令牌 / 密钥对）
  - 43. 作用域/ACL（网关不是对每个方法的原始代理）
  - 44. 速率限制

## 45. 各组件的职责

- 46. **网关**：广播发现信标，拥有配对决策，并托管 WS 端点。
- 47. **macOS 应用**：帮助你选择网关，显示配对提示，并仅在回退时使用 SSH。
- 48. **iOS/Android 节点**：将 Bonjour 作为便利手段进行浏览，并连接到已配对的网关 WS。
