---
summary: "Chrome extension: let OpenClaw drive your existing Chrome tab"
read_when:
  - You want the agent to drive an existing Chrome tab (toolbar button)
  - You need remote Gateway + local browser automation via Tailscale
  - You want to understand the security implications of browser takeover
title: "Chrome Extension"
---

# Chrome extension (browser relay)

The OpenClaw Chrome extension lets the agent control your **existing Chrome tabs** (your normal Chrome window) instead of launching a separate openclaw-managed Chrome profile.

Attach/detach happens via a **single Chrome toolbar button**.

## What it is (concept)

There are three parts:

- **Browser control service** (Gateway or node): the API the agent/tool calls (via the Gateway)
- **Local relay server** (loopback CDP): bridges between the control server and the extension (`http://127.0.0.1:18792` by default)
- **Chrome MV3 extension**: attaches to the active tab using `chrome.debugger` and pipes CDP messages to the relay

OpenClaw then controls the attached tab through the normal `browser` tool surface (selecting the right profile).

## Install / load (unpacked)

1. Install the extension to a stable local path:

```bash
openclaw browser extension install
```

2. Print the installed extension directory path:

```bash
openclaw browser extension path
```

3. Chrome → `chrome://extensions`

- Enable “Developer mode”
- “Load unpacked” → select the directory printed above

4. Pin the extension.

## Updates (no build step)

The extension ships inside the OpenClaw release (npm package) as static files. There is no separate “build” step.

After upgrading OpenClaw:

- Re-run `openclaw browser extension install` to refresh the installed files under your OpenClaw state directory.
- Chrome → `chrome://extensions` → click “Reload” on the extension.

## Use it (no extra config)

OpenClaw ships with a built-in browser profile named `chrome` that targets the extension relay on the default port.

Use it:

- CLI: `openclaw browser --browser-profile chrome tabs`
- Agent tool: `browser` with `profile="chrome"`

If you want a different name or a different relay port, create your own profile:

```bash
openclaw browser create-profile \
  --name my-chrome \
  --driver extension \
  --cdp-url http://127.0.0.1:18792 \
  --color "#00AA00"
```

## Attach / detach (toolbar button)

- Open the tab you want OpenClaw to control.
- Click the extension icon.
  - 1. 连接后徽章显示为 `ON`。
- 2. 再次点击即可分离。

## 3. 它控制的是哪个标签页？

- 4. 它**不会**自动控制“你正在查看的任何标签页”。
- 5. 它**只控制你通过点击工具栏按钮明确附加的标签页**。
- 6. 切换方法：打开另一个标签页，并在该标签页中点击扩展图标。

## 7. 徽章 + 常见错误

- 8. `ON`：已附加；OpenClaw 可以驱动该标签页。
- 9. `…`：正在连接本地中继。
- 10. `!`：无法连接中继（最常见原因：此机器上未运行浏览器中继服务器）。

11. 如果你看到 `!`：

- 12. 确保 Gateway 在本地运行（默认设置），或者如果 Gateway 运行在别处，则在此机器上运行一个 node host。
- 13. 打开扩展的 Options 页面；它会显示中继是否可达。

## 14. 远程 Gateway（使用 node host）

### 15. 本地 Gateway（与 Chrome 在同一台机器上）——通常**无需额外步骤**

16. 如果 Gateway 与 Chrome 运行在同一台机器上，它会在回环地址上启动浏览器控制服务，并自动启动中继服务器。 17. 扩展与本地中继通信；CLI/工具调用会发送到 Gateway。

### 18. 远程 Gateway（Gateway 运行在别处）——**运行一个 node host**

19. 如果你的 Gateway 运行在另一台机器上，请在运行 Chrome 的机器上启动一个 node host。
20. Gateway 会将浏览器操作代理到该节点；扩展和中继仍然保持在浏览器所在的本地机器上。

21. 如果连接了多个节点，请使用 `gateway.nodes.browser.node` 固定一个，或设置 `gateway.nodes.browser.mode`。

## 22. 沙箱（工具容器）

23. 如果你的代理会话是沙箱化的（`agents.defaults.sandbox.mode != "off"`），`browser` 工具可能会受到限制：

- 24. 默认情况下，沙箱化会话通常指向**沙箱浏览器**（`target="sandbox"`），而不是你的主机 Chrome。
- 25. Chrome 扩展的中继接管需要控制**主机**浏览器控制服务器。

26. 选项：

- 27. 最简单：在**非沙箱化**的会话/代理中使用该扩展。
- 28. 或者允许沙箱化会话控制主机浏览器：

```json5
29. {
  agents: {
    defaults: {
      sandbox: {
        browser: {
          allowHostControl: true,
        },
      },
    },
  },
}
```

30. 然后确保该工具未被工具策略拒绝，并且（如有需要）使用 `target="host"` 调用 `browser`。

31. 调试：`openclaw sandbox explain`

## 32. 远程访问提示

- 33. 将 Gateway 和 node host 保持在同一个 tailnet 中；避免将中继端口暴露到局域网或公共互联网。
- 34. 有意地配对节点；如果你不希望远程控制，请禁用浏览器代理路由（`gateway.nodes.browser.mode="off"`）。

## 35. “extension path”的工作方式

36. `openclaw browser extension path` 会打印包含扩展文件的**已安装**磁盘目录。

37. CLI 有意**不会**打印 `node_modules` 路径。 38. 始终先运行 `openclaw browser extension install`，以将扩展复制到 OpenClaw 状态目录下的稳定位置。

39. 如果你移动或删除该安装目录，Chrome 将把该扩展标记为损坏，直到你从有效路径重新加载它。

## 40. 安全影响（请阅读）

41. 这很强大，也很有风险。 42. 把它当作给模型“直接操作你浏览器的手”。

- 43. 该扩展使用 Chrome 的调试器 API（`chrome.debugger`）。 44. 附加后，模型可以：
  - 45. 在该标签页中点击/输入/导航
  - 46. 读取页面内容
  - 47. 访问该标签页已登录会话能够访问的任何内容
- 48. **这并不像专用的 openclaw 管理的配置文件那样被隔离**。
  - 49. 如果你附加到日常使用的配置文件/标签页，你就是在授予对该账户状态的访问权限。

50. 建议：

- 1. 优先为扩展中继使用一个专用的 Chrome 配置文件（与个人浏览分开）。
- 2. 将 Gateway 和任何节点主机保持为仅 tailnet 可访问；依赖 Gateway 认证 + 节点配对。
- 3. 避免通过 LAN（`0.0.0.0`）暴露中继端口，并避免使用 Funnel（公网）。
- 4. 中继会阻止非扩展来源，并要求 CDP 客户端使用内部认证令牌。

5. 相关：

- 6. 浏览器工具概览：[Browser](/tools/browser)
- 7. 安全审计：[Security](/gateway/security)
- Tailscale setup: [Tailscale](/gateway/tailscale)
