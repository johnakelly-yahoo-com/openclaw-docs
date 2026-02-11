---
summary: "macOS 权限持久化（TCC）与签名要求"
read_when:
  - 10. 调试缺失或卡住的 macOS 权限提示
  - 11. 打包或签名 macOS 应用
  - 12. 更改 bundle ID 或应用安装路径
title: "macOS 权限"
---

# 14. macOS 权限（TCC）

15. macOS 的权限授权非常脆弱。 16. TCC 会将权限授权与应用的代码签名、bundle identifier 以及磁盘上的路径关联起来。 17. 如果其中任何一项发生变化，macOS 会将该应用视为新应用，并可能丢弃或隐藏权限提示。

## 18. 稳定权限的要求

- 19. 相同路径：从固定位置运行应用（对于 OpenClaw，为 `dist/OpenClaw.app`）。
- 20. 相同的 bundle identifier：更改 bundle ID 会创建新的权限身份。
- 21. 已签名的应用：未签名或 ad-hoc 签名的构建不会持久保存权限。
- 22. 一致的签名：使用真实的 Apple Development 或 Developer ID 证书，以便签名在多次重建之间保持稳定。

23. Ad-hoc 签名会在每次构建时生成新的身份。 24. macOS 会忘记之前的授权，并且在清理陈旧条目之前，权限提示可能会完全消失。

## 25. 当权限提示消失时的恢复检查清单

1. 26. 退出应用。
2. 27. 在“系统设置 -> 隐私与安全性”中移除该应用条目。
3. 从相同路径重新启动应用并重新授予权限。
4. 29. 如果提示仍未出现，请使用 `tccutil` 重置 TCC 条目并重试。
5. 30. 某些权限只有在完整重启 macOS 后才会再次出现。

31) 示例重置（根据需要替换 bundle ID）：

```bash
32. sudo tccutil reset Accessibility bot.molt.mac
sudo tccutil reset ScreenCapture bot.molt.mac
sudo tccutil reset AppleEvents
```

## 33. 文件与文件夹权限（桌面/文稿/下载）

34. macOS 也可能会对终端或后台进程访问桌面、文稿和下载文件夹进行限制。 35. 如果文件读取或目录列出操作卡住，请向执行文件操作的同一进程上下文授予访问权限（例如 Terminal/iTerm、由 LaunchAgent 启动的应用，或 SSH 进程）。

36. 解决方法：如果想避免逐个文件夹授权，可将文件移动到 OpenClaw 工作区（`~/.openclaw/workspace`）。

37. 在测试权限时，始终使用真实证书进行签名。 38. Ad-hoc 构建仅适用于权限无关的快速本地运行。
