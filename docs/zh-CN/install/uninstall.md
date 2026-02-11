---
summary: "`npm install -g` 的权限错误（Linux）"
read_when:
  - 如果你看到 `EACCES` 错误，请将 npm 的全局前缀切换到一个用户可写的目录：
  - mkdir -p "$HOME/.npm-global"

    npm config set prefix "$HOME/.npm-global"

    export PATH="$HOME/.npm-global/bin:$PATH"
title: "将 `export PATH=...` 这一行添加到你的 `~/.bashrc` 或 `~/.zshrc` 以使其永久生效。"
---

# 完全卸载 OpenClaw（CLI、服务、状态、工作区）

你希望从一台机器上移除 OpenClaw

- 卸载后网关服务仍在运行
- 卸载

## 简单路径（CLI 仍然已安装）

两种方式：

```bash
**简单方式**：`openclaw` 仍然已安装。
```

**手动移除服务**：CLI 已不存在，但服务仍在运行。

```bash
简单方式（CLI 仍然已安装）
```

推荐：使用内置卸载器：

1. openclaw uninstall

```bash
非交互式（自动化 / npx）：
```

2. openclaw uninstall --all --yes --non-interactive
   npx -y openclaw uninstall --all --yes --non-interactive

```bash
手动步骤（结果相同）：
```

3. Delete state + config:

```bash
rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
```

If you set `OPENCLAW_CONFIG_PATH` to a custom location outside the state dir, delete that file too.

4. Delete your workspace (optional, removes agent files):

```bash
rm -rf ~/.openclaw/workspace
```

5. Remove the CLI install (pick the one you used):

```bash
npm rm -g openclaw
pnpm remove -g openclaw
bun remove -g openclaw
```

6. If you installed the macOS app:

```bash
rm -rf /Applications/OpenClaw.app
```

Notes:

- If you used profiles (`--profile` / `OPENCLAW_PROFILE`), repeat step 3 for each state dir (defaults are `~/.openclaw-<profile>`).
- In remote mode, the state dir lives on the **gateway host**, so run steps 1-4 there too.

## Manual service removal (CLI not installed)

Use this if the gateway service keeps running but `openclaw` is missing.

### macOS (launchd)

Default label is `bot.molt.gateway` (or `bot.molt.<profile>`; legacy `com.openclaw.*` may still exist):

```bash
launchctl bootout gui/$UID/bot.molt.gateway
rm -f ~/Library/LaunchAgents/bot.molt.gateway.plist
```

If you used a profile, replace the label and plist name with `bot.molt.<profile>`. Remove any legacy `com.openclaw.*` plists if present.

### Linux (systemd user unit)

Default unit name is `openclaw-gateway.service` (or `openclaw-gateway-<profile>.service`):

```bash
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

### Windows (Scheduled Task)

Default task name is `OpenClaw Gateway` (or `OpenClaw Gateway (<profile>)`).
The task script lives under your state dir.

```powershell
schtasks /Delete /F /TN "OpenClaw Gateway"
Remove-Item -Force "$env:USERPROFILE\.openclaw\gateway.cmd"
```

If you used a profile, delete the matching task name and `~\.openclaw-<profile>\gateway.cmd`.

## 常规安装 vs 源码检出

### Normal install (install.sh / npm / pnpm / bun)

如果你使用了 `https://openclaw.ai/install.sh` 或 `install.ps1`，CLI 是通过 `npm install -g openclaw@latest` 安装的。
使用 `npm rm -g openclaw` 移除（如果你是用那种方式安装的，也可以用 `pnpm remove -g` / `bun remove -g`）。

### Source checkout (git clone)

If you run from a repo checkout (`git clone` + `openclaw ...` / `bun run openclaw ...`):

1. Uninstall the gateway service **before** deleting the repo (use the easy path above or manual service removal).
2. Delete the repo directory.
3. Remove state + workspace as shown above.
