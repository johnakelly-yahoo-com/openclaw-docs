---
summary: "Bonjour/mDNS discovery + debugging (Gateway beacons, clients, and common failure modes)"
read_when:
  - 32. 在 macOS/iOS 上调试 Bonjour 发现问题
  - Changing mDNS service types, TXT records, or discovery UX
title: "34. Bonjour 发现"
---

# 35. Bonjour / mDNS 发现

36. OpenClaw 使用 Bonjour（mDNS / DNS‑SD）作为**仅限局域网的便捷方式**来发现
    一个活动的 Gateway（WebSocket 端点）。 37. 这是尽力而为的机制，**不能**替代 SSH 或
    基于 Tailnet 的连接。

## 38. 通过 Tailscale 的广域 Bonjour（单播 DNS‑SD）

39. 如果节点和 Gateway 位于不同网络，多播 mDNS 无法跨越该
    边界。 40. 你可以通过切换到 **单播 DNS‑SD**（“广域 Bonjour”）并结合 Tailscale 来保持相同的发现 UX。

41. 高级步骤：

1. 42. 在 Gateway 主机上运行一个 DNS 服务器（可通过 Tailnet 访问）。
2. 43. 在一个专用域下发布 `_openclaw-gw._tcp` 的 DNS‑SD 记录
       （示例：`openclaw.internal.`）。
3. 44. 配置 Tailscale **拆分 DNS**，使客户端（包括 iOS）通过该 DNS 服务器解析你选择的域。

45) OpenClaw 支持任何发现域；`openclaw.internal.` 只是一个示例。
46) iOS/Android 节点会同时浏览 `local.` 以及你配置的广域域。

### 47. Gateway 配置（推荐）

```json5
48. {
  gateway: { bind: "tailnet" }, // 仅限 tailnet（推荐）
  discovery: { wideArea: { enabled: true } }, // 启用广域 DNS‑SD 发布
}
```

### 49. 一次性的 DNS 服务器设置（Gateway 主机）

```bash
50. openclaw dns setup --apply
```

1. 这将安装 CoreDNS 并将其配置为：

- 2. 仅在网关的 Tailscale 接口上监听 53 端口
- 3. 从 `~/.openclaw/dns/<domain>.db` 提供你选择的域（示例：`openclaw.internal.`）

Validate from a tailnet‑connected machine:

```bash
5. dns-sd -B _openclaw-gw._tcp openclaw.internal.
```

### dig @<TAILNET_IPV4> -p 53 _openclaw-gw._tcp.openclaw.internal PTR +short

6. Tailscale DNS 设置

- 7. 在 Tailscale 管理控制台中：
- Add split DNS so your discovery domain uses that nameserver.

9. 添加拆分 DNS，使你的发现域使用该名称服务器。

### 10. 一旦客户端接受 tailnet DNS，iOS 节点即可在你的发现域中浏览&#xA;`_openclaw-gw._tcp`，无需多播。

11. 网关监听器安全性（推荐） 12. 网关 WS 端口（默认 `18789`）默认绑定到回环地址。

13. 对于 LAN/tailnet
    访问，请显式绑定并保持启用认证。

- 14. 对于仅 tailnet 的设置：
- 15. 在 `~/.openclaw/openclaw.json` 中设置 `gateway.bind: "tailnet"`。

## 16. 重启网关（或重启 macOS 菜单栏应用）。

17. 广播内容

## 18. 只有网关会广播 `_openclaw-gw._tcp`。

- 19. 服务类型

## 20. `_openclaw-gw._tcp` — 网关传输信标（由 macOS/iOS/Android 节点使用）。

21. TXT 键（非机密提示）

- 22. 网关会广播一些小的非机密提示，以便 UI 流程更加便捷：
- `displayName=<friendly name>`
- 24. `displayName=<friendly name>`
- 25. `lanHost=<hostname>.local`
- 26. `gatewayPort=<port>`（网关 WS + HTTP）
- 27. `gatewayTls=1`（仅在启用 TLS 时）
- 28. `gatewayTlsSha256=<sha256>`（仅在启用 TLS 且指纹可用时）
- 29. `canvasPort=<port>`（仅在启用画布主机时；默认 `18793`）
- 30. `sshPort=<port>`（未覆盖时默认为 22）
- 31. `transport=gateway`
- 32. `cliPath=<path>`（可选；指向可运行的 `openclaw` 入口点的绝对路径）

## 33. `tailnetDns=<magicdns>`（可选；当 Tailnet 可用时的提示）

34. 在 macOS 上调试

- 35. 有用的内置工具：

  ```bash
  36. 浏览实例：
  ```

- 37. dns-sd -B _openclaw-gw._tcp local.

  ```bash
  38. 解析某个实例（替换 `<instance>`）：
  ```

If browsing works but resolving fails, you’re usually hitting a LAN policy or
mDNS resolver issue.

40. 如果浏览正常但解析失败，通常是遇到了 LAN 策略或
    mDNS 解析器问题。
---------------

The Gateway writes a rolling log file (printed on startup as
`gateway log file: ...`). 42. 网关会写入一个滚动日志文件（在启动时打印为
`gateway log file: ...`）。

- 43. 查找 `bonjour:` 行，尤其是：
- 44. `bonjour: advertise failed ...` 45. \`bonjour: ...
- 46. name conflict resolved`/`hostname conflict resolved\`

## 47. `bonjour: watchdog detected non-announced service ...`

48. 在 iOS 节点上调试

49. iOS 节点使用 `NWBrowser` 来发现 `_openclaw-gw._tcp`。

- Settings → Gateway → Advanced → **Discovery Debug Logs**
- Settings → Gateway → Advanced → **Discovery Logs** → reproduce → **Copy**

The log includes browser state transitions and result‑set changes.

## Common failure modes

- **Bonjour doesn’t cross networks**: use Tailnet or SSH.
- **Multicast blocked**: some Wi‑Fi networks disable mDNS.
- **Sleep / interface churn**: macOS may temporarily drop mDNS results; retry.
- **Browse works but resolve fails**: keep machine names simple (avoid emojis or
  punctuation), then restart the Gateway. The service instance name derives from
  the host name, so overly complex names can confuse some resolvers.

## Escaped instance names (`\032`)

Bonjour/DNS‑SD often escapes bytes in service instance names as decimal `\DDD`
sequences (e.g. spaces become `\032`).

- This is normal at the protocol level.
- UIs should decode for display (iOS uses `BonjourEscapes.decode`).

## Disabling / configuration

- `OPENCLAW_DISABLE_BONJOUR=1` disables advertising (legacy: `OPENCLAW_DISABLE_BONJOUR`).
- `gateway.bind` in `~/.openclaw/openclaw.json` controls the Gateway bind mode.
- `OPENCLAW_SSH_PORT` overrides the SSH port advertised in TXT (legacy: `OPENCLAW_SSH_PORT`).
- `OPENCLAW_TAILNET_DNS` publishes a MagicDNS hint in TXT (legacy: `OPENCLAW_TAILNET_DNS`).
- `OPENCLAW_CLI_PATH` overrides the advertised CLI path (legacy: `OPENCLAW_CLI_PATH`).

## Related docs

- Discovery policy and transport selection: [Discovery](/gateway/discovery)
- Node pairing + approvals: [Gateway pairing](/gateway/pairing)
