---
summary: "PeekabooBridge integration for macOS UI automation"
read_when:
  - Hosting PeekabooBridge in OpenClaw.app
  - Integrating Peekaboo via Swift Package Manager
  - Changing PeekabooBridge protocol/paths
title: "Peekaboo Bridge"
---

# Peekaboo Bridge (macOS UI automation)

OpenClaw can host **PeekabooBridge** as a local, permission‑aware UI automation
broker. This lets the `peekaboo` CLI drive UI automation while reusing the
macOS app’s TCC permissions.

## What this is (and isn’t)

- **Host**: OpenClaw.app can act as a PeekabooBridge host.
- **Client**: use the `peekaboo` CLI (no separate `openclaw ui ...` surface).
- **UI**: visual overlays stay in Peekaboo.app; OpenClaw is a thin broker host.

## Enable the bridge

In the macOS app:

- Settings → **Enable Peekaboo Bridge**

When enabled, OpenClaw starts a local UNIX socket server. If disabled, the host
is stopped and `peekaboo` will fall back to other available hosts.

## Client discovery order

Peekaboo clients typically try hosts in this order:

1. Peekaboo.app (full UX)
2. Claude.app (if installed)
3. OpenClaw.app (thin broker)

Use `peekaboo bridge status --verbose` to see which host is active and which
socket path is in use. You can override with:

```bash
export PEEKABOO_BRIDGE_SOCKET=/path/to/bridge.sock
```

## Security & permissions

- The bridge validates **caller code signatures**; an allowlist of TeamIDs is
  enforced (Peekaboo host TeamID + OpenClaw app TeamID).
- 1. 请求在约 10 秒后超时。
- 2. 如果缺少所需权限，bridge 会返回清晰的错误消息，而不是启动“系统设置”。

## 3. 快照行为（自动化）

4. 快照存储在内存中，并在短时间窗口后自动过期。
5. 如果需要更长的保留时间，请从客户端重新捕获。

## 6. 故障排查

- 7. 如果 `peekaboo` 报告“bridge client is not authorized”，请确保客户端已正确签名，或仅在 **debug** 模式下使用 `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` 运行主机。
- 8. 如果未找到任何主机，请打开其中一个主机应用（Peekaboo.app 或 OpenClaw.app），并确认已授予权限。
