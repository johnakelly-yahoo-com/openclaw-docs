---
summary: "监控模型提供商的 OAuth 过期情况"
read_when:
  - 设置身份验证过期监控或告警
  - 自动化 Claude Code / Codex OAuth 刷新检查
title: "身份验证监控"
---

# 身份验证监控

OpenClaw 通过 `openclaw models status` 暴露 OAuth 过期健康状态。 将其用于
自动化和告警；脚本是面向手机工作流的可选附加项。

## 首选：CLI 检查（可移植）

```bash
openclaw models status --check
```

退出码：

- `0`：正常
- `1`：凭据已过期或缺失
- `2`：即将过期（24 小时内）

这可在 cron/systemd 中运行且无需任何额外脚本。

## 可选脚本（运维 / 手机工作流）

这些位于 `scripts/` 下，且是**可选的**。 它们假设可以通过 SSH 访问网关主机，并针对 systemd + Termux 进行了调优。

- `scripts/claude-auth-status.sh` 现在使用 `openclaw models status --json` 作为
  权威数据源（当 CLI 不可用时回退到直接读取文件），
  因此请确保 `openclaw` 在定时器的 `PATH` 中。
- `scripts/auth-monitor.sh`：cron/systemd 定时器目标；发送告警（ntfy 或手机）。
- `scripts/systemd/openclaw-auth-monitor.{service,timer}`：systemd 用户定时器。
- `scripts/claude-auth-status.sh`: Claude Code + OpenClaw auth checker (full/json/simple).
- `scripts/mobile-reauth.sh`：通过 SSH 的引导式重新认证流程。
- `scripts/termux-quick-auth.sh`：一键小组件状态 + 打开认证 URL。
- `scripts/termux-auth-widget.sh`：完整的引导式小组件流程。
- `scripts/termux-sync-widget.sh`：同步 Claude Code 凭据 → OpenClaw。

如果你不需要手机自动化或 systemd 定时器，可以跳过这些脚本。
