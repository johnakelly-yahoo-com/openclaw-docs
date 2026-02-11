---
summary: "45. 使用 Nix 以声明式方式安装 OpenClaw"
read_when:
  - 46. 你希望安装是可复现、可回滚的
  - 47. 你已经在使用 Nix/NixOS/Home Manager
  - 48. 你希望一切都被固定版本并以声明式方式管理
title: "49. Nix"
---

# 50. Nix 安装

运行 OpenClaw 并配合 Nix 的推荐方式是通过 **[nix-openclaw](https://github.com/openclaw/nix-openclaw)** —— 一个开箱即用的 Home Manager 模块。

## 快速开始

将以下内容粘贴给你的 AI 代理（Claude、Cursor 等）：

```text
我想在我的 Mac 上设置 nix-openclaw。
仓库：github:openclaw/nix-openclaw

我需要你帮我做的事情：
1. 检查是否已安装 Determinate Nix（如果没有，请安装）
2. 使用 templates/agent-first/flake.nix 在 ~/code/openclaw-local 创建一个本地 flake
3. 帮我创建一个 Telegram 机器人（@BotFather）并获取我的 chat ID（@userinfobot）
4. 设置密钥（bot token、Anthropic key）—— 使用 ~/.secrets/ 下的普通文件即可
5. 填充模板占位符并运行 home-manager switch
6. 验证：launchd 正在运行，机器人能响应消息

请参考 nix-openclaw README 获取模块选项。
```

> **📦 完整指南：[github.com/openclaw/nix-openclaw](https://github.com/openclaw/nix-openclaw)**
>
> nix-openclaw 仓库是 Nix 安装的唯一可信来源。 本页面只是一个快速概览。

## 你将获得什么

- 网关 + macOS 应用 + 工具（whisper、spotify、摄像头）—— 全部固定版本
- 可在重启后持续运行的 Launchd 服务
- 具有声明式配置的插件系统
- 即时回滚：`home-manager switch --rollback`

---

## Nix 模式运行时行为

当设置 `OPENCLAW_NIX_MODE=1` 时（使用 nix-openclaw 会自动设置）：

OpenClaw 支持一种 **Nix 模式**，使配置具备确定性并禁用自动安装流程。
你可以通过导出以下变量来启用：

```bash
OPENCLAW_NIX_MODE=1
```

在 macOS 上，GUI 应用不会自动继承 shell 的环境变量。 你也可以
通过 defaults 启用 Nix 模式：

```bash
defaults write bot.molt.mac openclaw.nixMode -bool true
```

### 配置 + 状态路径

OpenClaw 从 `OPENCLAW_CONFIG_PATH` 读取 JSON5 配置，并将可变数据存储在 `OPENCLAW_STATE_DIR` 中。
在需要时，你也可以设置 `OPENCLAW_HOME` 来控制用于内部路径解析的基础主目录。

- `OPENCLAW_HOME`（默认优先级：`HOME` / `USERPROFILE` / `os.homedir()`）
- `OPENCLAW_STATE_DIR`（默认：`~/.openclaw`）
- `OPENCLAW_CONFIG_PATH`（默认值：`$OPENCLAW_STATE_DIR/openclaw.json`）

在 Nix 环境下运行时，请将这些路径显式设置为由 Nix 管理的位置，以便运行时状态和配置
不进入不可变的 store。

### Nix 模式下的运行时行为

- 自动安装和自我修改流程被禁用
- 缺失的依赖项会显示 Nix 特有的修复提示信息
- 当存在时，UI 会显示只读的 Nix 模式横幅

## 打包说明（macOS）

macOS 打包流程期望在以下位置有一个稳定的 Info.plist 模板：

```
apps/macos/Sources/OpenClaw/Resources/Info.plist
```

[`scripts/package-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/package-mac-app.sh) 会将该模板复制到应用包中，并填充动态字段
（bundle ID、版本/构建号、Git SHA、Sparkle 密钥）。 这使得 plist 对 SwiftPM
打包以及 Nix 构建（不依赖完整的 Xcode 工具链）保持确定性。

## 相关内容

- [nix-openclaw](https://github.com/openclaw/nix-openclaw) — full setup guide
- [Wizard](/start/wizard) —— 非 Nix 的 CLI 设置
- [Docker](/install/docker) — 容器化设置
