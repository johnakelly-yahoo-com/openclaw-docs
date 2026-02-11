---
summary: "修复 Linux 上用于 OpenClaw 浏览器控制的 Chrome/Brave/Edge/Chromium CDP 启动问题"
read_when: "在 Linux 上浏览器控制失败，尤其是使用 snap Chromium 时"
title: "Browser Troubleshooting"
---

# 浏览器故障排查（Linux）

## 问题：“Failed to start Chrome CDP on port 18800”

OpenClaw 的浏览器控制服务器在启动 Chrome/Brave/Edge/Chromium 时失败，并出现以下错误：

```
{"error":"Error: Failed to start Chrome CDP on port 18800 for profile \"openclaw\"."}
```

### 根本原因

在 Ubuntu（以及许多 Linux 发行版）上，默认的 Chromium 安装是一个 **snap 包**。 Snap 的 AppArmor 隔离机制会干扰 OpenClaw 启动和监控浏览器进程的方式。

`apt install chromium` 命令安装的是一个会重定向到 snap 的占位包：

```
注意，选择的是“chromium-browser”而不是“chromium”
chromium-browser 已是最新版本（2:1snap1-0ubuntu2）。
```

这并不是真正的浏览器——它只是一个包装器。

### 解决方案 1：安装 Google Chrome（推荐）

安装官方的 Google Chrome `.deb` 包，该包不受 snap 沙箱限制：

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y  # if there are dependency errors
```

然后更新你的 OpenClaw 配置（`~/.openclaw/openclaw.json`）：

```json
{
  "browser": {
    "enabled": true,
    "executablePath": "/usr/bin/google-chrome-stable",
    "headless": true,
    "noSandbox": true
  }
}
```

### 解决方案 2：使用 Snap Chromium 的仅附加（Attach-Only）模式

如果你必须使用 snap Chromium，请将 OpenClaw 配置为附加到手动启动的浏览器：

1. 更新配置：

```json
{
  "browser": {
    "enabled": true,
    "attachOnly": true,
    "headless": true,
    "noSandbox": true
  }
}
```

2. Start Chromium manually:

```bash
chromium-browser --headless --no-sandbox --disable-gpu \
  --remote-debugging-port=18800 \
  --user-data-dir=$HOME/.openclaw/browser/openclaw/user-data \
  about:blank &
```

3. Optionally create a systemd user service to auto-start Chrome:

```ini
# ~/.config/systemd/user/openclaw-browser.service
[Unit]
Description=OpenClaw Browser (Chrome CDP)
After=network.target

[Service]
ExecStart=/snap/bin/chromium --headless --no-sandbox --disable-gpu --remote-debugging-port=18800 --user-data-dir=%h/.openclaw/browser/openclaw/user-data about:blank
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

Enable with: `systemctl --user enable --now openclaw-browser.service`

### Verifying the Browser Works

Check status:

```bash
curl -s http://127.0.0.1:18791/ | jq '{running, pid, chosenBrowser}'
```

Test browsing:

```bash
curl -s -X POST http://127.0.0.1:18791/start
curl -s http://127.0.0.1:18791/tabs
```

### Config Reference

| Option                   | Description                                                                             | Default                                                                        |
| ------------------------ | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `browser.enabled`        | 启用浏览器控制                                                                                 | `true`                                                                         |
| `browser.executablePath` | Path to a Chromium-based browser binary (Chrome/Brave/Edge/Chromium) | auto-detected (prefers default browser when Chromium-based) |
| `browser.headless`       | Run without GUI                                                                         | `false`                                                                        |
| `browser.noSandbox`      | 添加 `--no-sandbox` 标志（某些 Linux 设置需要）                                                     | `false`                                                                        |
| `browser.attachOnly`     | Don't launch browser, only attach to existing                                           | `false`                                                                        |
| `browser.cdpPort`        | Chrome DevTools Protocol port                                                           | `18800`                                                                        |

### Problem: "Chrome extension relay is running, but no tab is connected"

You’re using the `chrome` profile (extension relay). It expects the OpenClaw
browser extension to be attached to a live tab.

Fix options:

1. **Use the managed browser:** `openclaw browser start --browser-profile openclaw`
   (or set `browser.defaultProfile: "openclaw"`).
2. **Use the extension relay:** install the extension, open a tab, and click the
   OpenClaw extension icon to attach it.

说明：

- The `chrome` profile uses your **system default Chromium browser** when possible.
- 本地 `openclaw` 配置会自动分配 `cdpPort`/`cdpUrl`；仅在远程 CDP 时才设置这些。
