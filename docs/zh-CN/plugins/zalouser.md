---
summary: "26. Zalo Personal 插件：通过 zca-cli 实现二维码登录 + 消息收发（插件安装 + 渠道配置 + CLI + 工具）"
read_when:
  - 27. 你希望在 OpenClaw 中支持 Zalo Personal（非官方）。
  - 28. 你正在配置或开发 zalouser 插件。
title: "29. Zalo Personal 插件"
---

# 30. Zalo Personal（插件）

31. 通过插件为 OpenClaw 提供 Zalo Personal 支持，使用 `zca-cli` 自动化一个普通的 Zalo 用户账号。

> 32. **警告：** 非官方自动化可能导致账号被暂停或封禁。 33. 使用风险自负。

## 34. 命名

35. 渠道 id 为 `zalouser`，以明确这是在自动化一个 **个人 Zalo 用户账号**（非官方）。 36. 我们保留 `zalo`，用于未来可能的官方 Zalo API 集成。

## 37. 运行位置

38. 此插件运行在 **Gateway 进程内部**。

39. 如果你使用远程 Gateway，请在 **运行 Gateway 的机器** 上安装并配置该插件，然后重启 Gateway。

## 40. 安装

### 41. 选项 A：从 npm 安装

```bash
42. openclaw plugins install @openclaw/zalouser
```

43. 随后重启 Gateway。

### 44. 选项 B：从本地文件夹安装（开发）

```bash
45. openclaw plugins install ./extensions/zalouser
cd ./extensions/zalouser && pnpm install
```

46. 随后重启 Gateway。

## 47. 前置条件：zca-cli

48. Gateway 所在机器必须在 `PATH` 中包含 `zca`：

```bash
49. zca --version
```

## 50. 配置

Channel config lives under `channels.zalouser` (not `plugins.entries.*`):

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

## CLI

```bash
openclaw channels login --channel zalouser
openclaw channels logout --channel zalouser
openclaw channels status --probe
openclaw message send --channel zalouser --target <threadId> --message "Hello from OpenClaw"
openclaw directory peers list --channel zalouser --query "name"
```

## Agent tool

Tool name: `zalouser`

Actions: `send`, `image`, `link`, `friends`, `groups`, `me`, `status`
