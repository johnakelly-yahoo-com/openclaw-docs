---
summary: "`openclaw browser` 的 CLI 参考（配置文件、标签页、操作、扩展中继）"
read_when:
  - 你正在使用 `openclaw browser`，并希望查看常见任务的示例
  - 你希望通过节点主机控制运行在另一台机器上的浏览器
  - 你希望使用 Chrome 扩展中继（通过工具栏按钮进行附加/分离）
title: "browser"
---

# `openclaw browser`

管理 OpenClaw 的浏览器控制服务器并运行浏览器操作（标签页、快照、截图、导航、点击、输入）。

相关：

- 浏览器工具 + API：[Browser tool](/tools/browser)
- Chrome 扩展中继：[Chrome extension](/tools/chrome-extension)

## Common flags

- `--url <gatewayWsUrl>`：网关 WebSocket URL（默认为配置中的值）。
- `--token <token>`：网关令牌（如果需要）。
- `--timeout <ms>`：请求超时时间（毫秒）。
- `--browser-profile <name>`：选择浏览器配置文件（默认使用配置中的值）。
- `--json`：机器可读输出（在支持的地方）。

## 快速开始（本地）

```bash
openclaw browser --browser-profile chrome tabs
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

## 配置文件

配置文件是命名的浏览器路由配置。 在实践中：

- `openclaw`：启动/附加到一个由 OpenClaw 管理的专用 Chrome 实例（隔离的用户数据目录）。
- `chrome`：通过 Chrome 扩展中继控制你现有的 Chrome 标签页。

```bash
openclaw browser profiles
openclaw browser create-profile --name work --color "#FF5A36"
openclaw browser delete-profile --name work
```

使用特定配置文件：

```bash
openclaw browser --browser-profile work tabs
```

## 标签页

```bash
openclaw browser tabs
openclaw browser open https://docs.openclaw.ai
openclaw browser focus <targetId>
openclaw browser close <targetId>
```

## 快照 / 截图 / 操作

快照：

```bash
openclaw browser snapshot
```

截图：

```bash
openclaw 浏览器截图
```

导航/点击/输入（基于 ref 的 UI 自动化）：

```bash
openclaw browser navigate https://example.com
openclaw browser click <ref>
openclaw browser type <ref> "hello"
```

## Chrome 扩展中继（通过工具栏按钮附加）

此模式允许代理控制你手动附加的现有 Chrome 标签页（不会自动附加）。

将未打包的扩展安装到一个稳定路径：

```bash
openclaw browser extension install
openclaw browser extension path
```

然后 Chrome → `chrome://extensions` → 启用“开发者模式”→“加载已解压的扩展程序”→ 选择打印出的文件夹。

完整指南：[Chrome extension](/tools/chrome-extension)

## 远程浏览器控制（node 主机代理）

如果 Gateway 运行在与浏览器不同的机器上，请在拥有 Chrome/Brave/Edge/Chromium 的机器上运行一个 **node 主机**。 Gateway 将把浏览器操作代理到该 node（无需单独的浏览器控制服务器）。

使用 `gateway.nodes.browser.mode` 控制自动路由，并在连接多个节点时使用 `gateway.nodes.browser.node` 固定到特定节点。

安全 + 远程设置：[Browser tool](/tools/browser)、[Remote access](/gateway/remote)、[Tailscale](/gateway/tailscale)、[Security](/gateway/security)
