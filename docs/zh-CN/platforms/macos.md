---
summary: "OpenClaw macOS companion app (menu bar + gateway broker)"
read_when:
  - Implementing macOS app features
  - Changing gateway lifecycle or node bridging on macOS
title: "macOS App"
---

# OpenClaw macOS Companion (menu bar + gateway broker)

macOS 应用是 OpenClaw 的**菜单栏伴侣**。 It owns permissions,
manages/attaches to the Gateway locally (launchd or manual), and exposes macOS
capabilities to the agent as a node.

## 它的功能

- Shows native notifications and status in the menu bar.
- Owns TCC prompts (Notifications, Accessibility, Screen Recording, Microphone,
  Speech Recognition, Automation/AppleScript).
- Runs or connects to the Gateway (local or remote).
- Exposes macOS‑only tools (Canvas, Camera, Screen Recording, `system.run`).
- Starts the local node host service in **remote** mode (launchd), and stops it in **local** mode.
- Optionally hosts **PeekabooBridge** for UI automation.
- Installs the global CLI (`openclaw`) via npm/pnpm on request (bun not recommended for the Gateway runtime).

## Local vs remote mode

- **Local** (default): the app attaches to a running local Gateway if present;
  otherwise it enables the launchd service via `openclaw gateway install`.
- **Remote**: the app connects to a Gateway over SSH/Tailscale and never starts
  a local process.
  The app starts the local **node host service** so the remote Gateway can reach this Mac.
  The app does not spawn the Gateway as a child process.

## Launchd control

The app manages a per‑user LaunchAgent labeled `bot.molt.gateway`
(or `bot.molt.<profile>` 在使用 `--profile`/`OPENCLAW_PROFILE` 时；旧版 `com.openclaw.*` 仍会卸载）。

```bash
launchctl kickstart -k gui/$UID/bot.molt.gateway
launchctl bootout gui/$UID/bot.molt.gateway
```

Replace the label with `bot.molt.<profile>` when running a named profile.

If the LaunchAgent isn’t installed, enable it from the app or run
`openclaw gateway install`.

## Node capabilities (mac)

The macOS app presents itself as a node. Common commands:

- Canvas: `canvas.present`, `canvas.navigate`, `canvas.eval`, `canvas.snapshot`, `canvas.a2ui.*`
- Camera: `camera.snap`, `camera.clip`
- Screen: `screen.record`
- System: `system.run`, `system.notify`

The node reports a `permissions` map so agents can decide what’s allowed.

Node service + app IPC:

- When the headless node host service is running (remote mode), it connects to the Gateway WS as a node.
- `system.run` executes in the macOS app (UI/TCC context) over a local Unix socket; prompts + output stay in-app.

Diagram (SCI):

```
Gateway -> Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + TCC + system.run)
```

## Exec approvals (system.run)

`system.run` is controlled by **Exec approvals** in the macOS app (Settings → Exec approvals).
Security + ask + allowlist are stored locally on the Mac in:

```
~/.openclaw/exec-approvals.json
```

Example:

```json
{
  "version": 1,
  "defaults": {
    "security": "deny",
    "ask": "on-miss"
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "allowlist": [{ "pattern": "/opt/homebrew/bin/rg" }]
    }
  }
}
```

Notes:

- `allowlist` entries are glob patterns for resolved binary paths.
- Choosing “Always Allow” in the prompt adds that command to the allowlist.
- `system.run` environment overrides are filtered (drops `PATH`, `DYLD_*`, `LD_*`, `NODE_OPTIONS`, `PYTHON*`, `PERL*`, `RUBYOPT`) and then merged with the app’s environment.

## 3. 深度链接

4. 该应用为本地操作注册了 `openclaw://` URL scheme。

### 5. `openclaw://agent`

Triggers a Gateway `agent` request.

```bash
7. open 'openclaw://agent?message=Hello%20from%20deep%20link'
```

8. 查询参数：

- 9. `message`（必需）
- 10. `sessionKey`（可选）
- 11. `thinking`（可选）
- 12. `deliver` / `to` / `channel`（可选）
- 13. `timeoutSeconds`（可选）
- 14. `key`（可选的无人值守模式密钥）

15. 安全性：

- 16. 没有 `key` 时，应用会提示确认。
- 17. 使用有效的 `key` 时，运行将为无人值守（适用于个人自动化）。

## 18. 引导流程（典型）

1. 19. 安装并启动 **OpenClaw.app**。
2. 20. 完成权限清单（TCC 提示）。
3. 21. 确保 **Local** 模式处于激活状态并且 Gateway 正在运行。
4. 22. 如果需要终端访问，请安装 CLI。

## 23) 构建与开发工作流（原生）

- 24. `cd apps/macos && swift build`
- 25. `swift run OpenClaw`（或使用 Xcode）
- 26. 打包应用：`scripts/package-mac-app.sh`

## 27. 调试 Gateway 连接（macOS CLI）

28. 使用调试 CLI，在不启动应用的情况下，执行与 macOS 应用相同的 Gateway WebSocket 握手和发现逻辑。

```bash
cd apps/macos
swift run openclaw-mac connect --json
swift run openclaw-mac discover --timeout 3000 --json
```

30. 连接选项：

- 31. `--url <ws://host:port>`：覆盖配置
- `--mode <local|remote>`: resolve from config (default: config or local)
- 33. `--probe`：强制进行一次新的健康探测
- 34. `--timeout <ms>`：请求超时（默认：`15000`）
- `--json`: structured output for diffing

36. 发现选项：

- `--include-local`: include gateways that would be filtered as “local”
- 38. `--timeout <ms>`：整体发现窗口（默认：`2000`）
- 39. `--json`：用于差异比较的结构化输出

Tip: compare against `openclaw gateway discover --json` to see whether the
macOS app’s discovery pipeline (NWBrowser + tailnet DNS‑SD fallback) differs from
the Node CLI’s `dns-sd` based discovery.

## Remote connection plumbing (SSH tunnels)

42. 当 macOS 应用在 **Remote** 模式下运行时，它会打开一个 SSH 隧道，使本地 UI 组件能够像在 localhost 上一样与远程 Gateway 通信。

### 43. 控制隧道（Gateway WebSocket 端口）

- 44. **用途：** 健康检查、状态、Web Chat、配置以及其他控制平面调用。
- 45. **本地端口：** Gateway 端口（默认 `18789`），始终稳定。
- 46. **远程端口：** 远程主机上的相同 Gateway 端口。
- 47. **行为：** 不使用随机本地端口；应用会复用现有的健康隧道，或在需要时重启它。
- 48. **SSH 形式：** `ssh -N -L <local>:127.0.0.1:<remote>`，并启用 BatchMode + ExitOnForwardFailure + keepalive 选项。
- 49. **IP 报告：** SSH 隧道使用回环地址，因此网关看到的节点 IP 将是 `127.0.0.1`。 50. 如果你希望显示真实的客户端 IP，请使用 **Direct（ws/wss）** 传输（参见 [macOS remote access](/platforms/mac/remote)）。

1. 有关设置步骤，请参阅 [macOS 远程访问](/platforms/mac/remote)。 2. 有关协议
   详情，请参阅 [Gateway 协议](/gateway/protocol)。

## 3. 相关文档

- 4. [Gateway 运行手册](/gateway)
- 5. [Gateway（macOS）](/platforms/mac/bundled-gateway)
- 6. [macOS 权限](/platforms/mac/permissions)
- 7. [Canvas](/platforms/mac/canvas)
