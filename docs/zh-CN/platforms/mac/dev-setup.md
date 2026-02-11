---
summary: "Setup guide for developers working on the OpenClaw macOS app"
read_when:
  - Setting up the macOS development environment
title: "macOS Dev Setup"
---

# macOS Developer Setup

This guide covers the necessary steps to build and run the OpenClaw macOS application from source.

## Prerequisites

Before building the app, ensure you have the following installed:

1. **Xcode 26.2+**: Required for Swift development.
2. **Node.js 22+ & pnpm**: Required for the gateway, CLI, and packaging scripts.

## 1) Install Dependencies

Install the project-wide dependencies:

```bash
pnpm install
```

## 1. 2. 2. 构建并打包应用

3. 要构建 macOS 应用并将其打包到 `dist/OpenClaw.app`，请运行：

```bash
./scripts/package-mac-app.sh
```

如果你没有 Apple Developer ID 证书，脚本将自动使用**临时签名**（`-`）。

关于开发运行模式、签名标志以及 Team ID 故障排除，请参阅 macOS 应用 README：
[https://github.com/openclaw/openclaw/blob/main/apps/macos/README.md](https://github.com/openclaw/openclaw/blob/main/apps/macos/README.md)

> 7. **注意**：使用临时签名的应用可能会触发安全提示。 8. 如果应用启动后立即因 "Abort trap 6" 崩溃，请参阅 [Troubleshooting](#troubleshooting) 部分。

## 9. 3. 10. 安装 CLI

11. macOS 应用需要全局安装的 `openclaw` CLI 来管理后台任务。

12. **安装方式（推荐）：**

1. 13. 打开 OpenClaw 应用。
2. 14. 前往 **General** 设置选项卡。
3. 15. 点击 **"Install CLI"**。

16) 或者，手动安装：

```bash
17. npm install -g openclaw@<version>
```

## 故障排除

### 构建失败：工具链或 SDK 不匹配

20. macOS 应用构建需要最新的 macOS SDK 和 Swift 6.2 工具链。

21. **系统依赖（必需）：**

- 22. **通过“软件更新”可获得的最新 macOS 版本**（Xcode 26.2 SDK 所需）
- 23. **Xcode 26.2**（Swift 6.2 工具链）

24. **检查：**

```bash
25. xcodebuild -version
xcrun swift --version
```

26. 如果版本不匹配，请更新 macOS/Xcode 并重新运行构建。

### 27. 授权时应用崩溃

28. 如果在尝试允许 **语音识别** 或 **麦克风** 访问时应用崩溃，可能是由于 TCC 缓存损坏或签名不匹配导致。

29. **解决方法：**

1. 30. 重置 TCC 权限：

   ```bash
   31. tccutil reset All bot.molt.mac.debug
   ```

2. 32. 如果仍然失败，请暂时修改 [`scripts/package-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/package-mac-app.sh) 中的 `BUNDLE_ID`，以强制 macOS 重新建立一个“干净状态”。

### 33) Gateway 一直显示 "Starting..."

34. 如果 gateway 状态一直停留在 "Starting..."，请检查是否有僵尸进程占用了端口：

```bash
35. openclaw gateway status
openclaw gateway stop

# 如果你未使用 LaunchAgent（开发模式 / 手动运行），查找监听进程：
lsof -nP -iTCP:18789 -sTCP:LISTEN
```

36. 如果是手动运行的进程占用了端口，请停止该进程（Ctrl+C）。 37. 作为最后手段，杀掉你在上面找到的 PID。
