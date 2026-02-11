---
summary: "OpenClaw logging: rolling diagnostics file log + unified log privacy flags"
read_when:
  - Capturing macOS logs or investigating private data logging
  - Debugging voice wake/session lifecycle issues
title: "macOS Logging"
---

# Logging (macOS)

## Rolling diagnostics file log (Debug pane)

OpenClaw routes macOS app logs through swift-log (unified logging by default) and can write a local, rotating file log to disk when you need a durable capture.

- Verbosity: **Debug pane → Logs → App logging → Verbosity**
- Enable: **Debug pane → Logs → App logging → “Write rolling diagnostics log (JSONL)”**
- Location: `~/Library/Logs/OpenClaw/diagnostics.jsonl` (rotates automatically; old files are suffixed with `.1`, `.2`, …)
- Clear: **Debug pane → Logs → App logging → “Clear”**

Notes:

- This is **off by default**. Enable only while actively debugging.
- Treat the file as sensitive; don’t share it without review.

## Unified logging private data on macOS

Unified logging redacts most payloads unless a subsystem opts into `privacy -off`. Per Peter's write-up on macOS [logging privacy shenanigans](https://steipete.me/posts/2025/logging-privacy-shenanigans) (2025) this is controlled by a plist in `/Library/Preferences/Logging/Subsystems/` keyed by the subsystem name. 2. 为 OpenClaw（`bot.molt`）启用

## 3. 先将 plist 写入临时文件，然后以 root 身份原子性地安装：

- 4. cat <<'EOF' >/tmp/bot.molt.plist<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0">
  <dict>
      <key>DEFAULT-OPTIONS</key>
      <dict>
          <key>Enable-Private-Data</key>
          <true/>
      </dict>
  </dict>
  </plist>
  EOF
  sudo install -m 644 -o root -g wheel /tmp/bot.molt.plist /Library/Preferences/Logging/Subsystems/bot.molt.plist

```bash
5. 无需重启；logd 会很快注意到该文件，但只有新的日志行才会包含私有负载。
```

- 6. 使用现有的辅助工具查看更丰富的输出，例如：`./scripts/clawlog.sh --category WebChat --last 5m`。
- 7. 调试完成后禁用

## 8. 移除覆盖：`sudo rm /Library/Preferences/Logging/Subsystems/bot.molt.plist`。

- 9. 可选地运行 `sudo log config --reload`，以强制 logd 立即丢弃该覆盖。
- 10. 请记住，该暴露面可能包含电话号码和消息正文；仅在你确实需要额外细节时才保留该 plist。
- 11. 菜单栏状态逻辑以及向用户展示的内容
