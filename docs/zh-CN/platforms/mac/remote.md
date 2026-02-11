---
summary: "macOS app flow for controlling a remote OpenClaw gateway over SSH"
read_when:
  - Setting up or debugging remote mac control
title: "Remote Control"
---

# Remote OpenClaw (macOS ⇄ remote host)

This flow lets the macOS app act as a full remote control for a OpenClaw gateway running on another host (desktop/server). It’s the app’s **Remote over SSH** (remote run) feature. All features—health checks, Voice Wake forwarding, and Web Chat—reuse the same remote SSH configuration from _Settings → General_.

## Modes

- **Local (this Mac)**: Everything runs on the laptop. No SSH involved.
- **Remote over SSH (default)**: OpenClaw commands are executed on the remote host. The mac app opens an SSH connection with `-o BatchMode` plus your chosen identity/key and a local port-forward.
- **Remote direct (ws/wss)**: No SSH tunnel. The mac app connects to the gateway URL directly (for example, via Tailscale Serve or a public HTTPS reverse proxy).

## Remote transports

Remote mode supports two transports:

- **SSH tunnel** (default): Uses `ssh -N -L ...` to forward the gateway port to localhost. The gateway will see the node’s IP as `127.0.0.1` because the tunnel is loopback.
- **Direct (ws/wss)**: Connects straight to the gateway URL. The gateway sees the real client IP.

## Prereqs on the remote host

1. Install Node + pnpm and build/install the OpenClaw CLI (`pnpm install && pnpm build && pnpm link --global`).
2. Ensure `openclaw` is on PATH for non-interactive shells (symlink into `/usr/local/bin` or `/opt/homebrew/bin` if needed).
3. Open SSH with key auth. We recommend **Tailscale** IPs for stable reachability off-LAN.

## macOS app setup

1. 1. 打开 _设置 → 通用_。
2. 2. 在 **OpenClaw runs** 下，选择 **Remote over SSH** 并设置：
   - 3. **Transport**：**SSH tunnel** 或 **Direct (ws/wss)**。
   - 4. **SSH target**：`user@host`（可选 `:port`）。
     - 5. 如果网关在同一局域网并通过 Bonjour 广播，可从发现列表中选择以自动填充此字段。
   - 6. **Gateway URL**（仅 Direct）：`wss://gateway.example.ts.net`（本地/局域网可用 `ws://...`）。
   - 7. **Identity file**（高级）：你的密钥路径。
   - 8. **Project root**（高级）：用于执行命令的远程检出路径。
   - 9. **CLI path**（高级）：可运行的 `openclaw` 入口/二进制的可选路径（在被广播时会自动填充）。
3. 10. 点击 **Test remote**。 11. 成功表示远程 `openclaw status --json` 能正确运行。 12. 失败通常意味着 PATH/CLI 问题；退出码 127 表示远程找不到 CLI。
4. 13. 健康检查和 Web Chat 现在都会自动通过该 SSH 隧道运行。

## 14) Web Chat

- 15. **SSH tunnel**：Web Chat 通过转发的 WebSocket 控制端口（默认 18789）连接到网关。
- 16. **Direct (ws/wss)**：Web Chat 直接连接到配置的网关 URL。
- 17. 现在不再有单独的 WebChat HTTP 服务器。

## 18. 权限

- 19. 远程主机需要与本地相同的 TCC 批准（自动化、辅助功能、屏幕录制、麦克风、语音识别、通知）。 20. 在那台机器上运行一次引导流程以一次性授予这些权限。
- 21. 节点通过 `node.list` / `node.describe` 广播其权限状态，以便代理了解可用能力。

## 22. 安全说明

- 23. 优先在远程主机上使用回环地址绑定，并通过 SSH 或 Tailscale 连接。
- 24. 如果将网关绑定到非回环接口，请要求使用令牌/密码认证。
- 25. 参见 [Security](/gateway/security) 和 [Tailscale](/gateway/tailscale)。

## 26. WhatsApp 登录流程（远程）

- 27. **在远程主机上**运行 `openclaw channels login --verbose`。 28. 用手机上的 WhatsApp 扫描二维码。
- 29. 如果认证过期，请在该主机上重新运行登录。 30. 健康检查会提示链接问题。

## 31. 故障排查

- 32. **exit 127 / not found**：`openclaw` 不在非登录 shell 的 PATH 中。 33. 将其添加到 `/etc/paths`、你的 shell rc，或链接到 `/usr/local/bin`/`/opt/homebrew/bin`。
- 34. **Health probe failed**：检查 SSH 可达性、PATH，以及 Baileys 是否已登录（`openclaw status --json`）。
- 35. **Web Chat 卡住**：确认网关正在远程主机上运行，且转发端口与网关 WS 端口一致；UI 需要健康的 WS 连接。
- 36. **Node IP 显示 127.0.0.1**：在使用 SSH 隧道时这是预期行为。 37. 如果希望网关看到真实客户端 IP，请将 **Transport** 切换为 **Direct (ws/wss)**。
- 38. **Voice Wake**：在远程模式下，触发短语会自动转发；不需要单独的转发器。

## 39. 通知声音

40. 可使用 `openclaw` 和 `node.invoke` 从脚本中为每个通知选择声音，例如：

```bash
41. openclaw nodes notify --node <id> --title "Ping" --body "Remote gateway ready" --sound Glass
```

42. 应用中已不再有全局“默认声音”开关；调用方需为每个请求选择一种声音（或不选择）。
