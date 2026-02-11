---
summary: "38. macOS 应用如何报告 gateway / Baileys 的健康状态"
read_when:
  - 39. 调试 mac 应用的健康指示器
title: "40. 健康检查"
---

# 41. macOS 上的健康检查

42. 如何通过菜单栏应用查看已链接通道是否健康。

## 43. 菜单栏

- 44. 状态指示点现在反映 Baileys 的健康状态：
  - 45. 绿色：已链接 + 最近已打开 socket。
  - 46. 橙色：正在连接 / 重试中。
  - 47. 红色：已注销或探测失败。
- 48. 第二行显示 "linked · auth 12m" 或失败原因。
- 49. “Run Health Check” 菜单项会触发一次按需探测。

## 50. 设置

- General tab gains a Health card showing: linked auth age, session-store path/count, last check time, last error/status code, and buttons for Run Health Check / Reveal Logs.
- Uses a cached snapshot so the UI loads instantly and falls back gracefully when offline.
- **Channels 标签页**展示 WhatsApp/Telegram 的通道状态与控制（登录二维码、登出、探测、最近一次断开/错误）。

## 探测的工作原理

- 应用通过 `ShellExecutor` 每约 60 秒以及按需运行 `openclaw health --json`。 The probe loads creds and reports status without sending messages.
- Cache the last good snapshot and the last error separately to avoid flicker; show the timestamp of each.

## When in doubt

- You can still use the CLI flow in [Gateway health](/gateway/health) (`openclaw status`, `openclaw status --deep`, `openclaw health --json`) and tail `/tmp/openclaw/openclaw-*.log` for `web-heartbeat` / `web-reconnect`.
