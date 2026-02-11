---
summary: "iOS 节点应用：连接到 Gateway、配对、画布以及故障排查"
read_when:
  - 配对或重新连接 iOS 节点
  - 从源码运行 iOS 应用
  - Debugging gateway discovery or canvas commands
title: "iOS 应用"
---

# iOS 应用（Node）

可用性：内部预览。 iOS 应用尚未公开分发。

## 功能说明

- Connects to a Gateway over WebSocket (LAN or tailnet).
- 暴露节点能力：Canvas、屏幕快照、相机捕获、位置、对讲模式、语音唤醒。
- 接收 `node.invoke` 命令并上报节点状态事件。

## 要求

- Gateway 运行在另一台设备上（macOS、Linux，或通过 WSL2 的 Windows）。
- 网络路径：
  - 同一 LAN（通过 Bonjour），**或**
  - Tailnet via unicast DNS-SD (example domain: `openclaw.internal.`), **or**
  - 手动主机/端口（回退方案）。

## 快速开始（配对 + 连接）

1. 启动 Gateway：

```bash
openclaw gateway --port 18789
```

2. In the iOS app, open Settings and pick a discovered gateway (or enable Manual Host and enter host/port).

3. 在 Gateway 主机上批准配对请求：

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
```

4. 验证连接：

```bash
openclaw nodes status
openclaw gateway call node.list --params "{}"
```

## 发现方式

### Bonjour（LAN）

Gateway 在 `local.` 上广播 `_openclaw-gw._tcp`。 iOS 应用会自动列出这些。

### Tailnet（跨网络）

如果 mDNS 被阻止，请使用单播 DNS-SD 区（选择一个域；示例：`openclaw.internal.`）以及 Tailscale 分离 DNS。
参见 [Bonjour](/gateway/bonjour) 获取 CoreDNS 示例。

### 手动主机/端口

在“设置”中启用 **手动主机**，并输入 Gateway 主机 + 端口（默认 `18789`）。

## Canvas + A2UI

The iOS node renders a WKWebView canvas. Use `node.invoke` to drive it:

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.navigate --params '{"url":"http://<gateway-host>:18793/__openclaw__/canvas/"}'
```

说明：

- Gateway 的画布主机提供 `/__openclaw__/canvas/` 和 `/__openclaw__/a2ui/`。
- 当连接时若广播了画布主机 URL，iOS 节点会自动导航到 A2UI。
- 使用 `canvas.navigate` 和 `{"url":""}` 返回内置脚手架。

### Canvas 执行 / 快照

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.eval --params '{"javaScript":"(() => { const {ctx} = window.__openclaw; ctx.clearRect(0,0,innerWidth,innerHeight); ctx.lineWidth=6; ctx.strokeStyle=\"#ff2d55\"; ctx.beginPath(); ctx.moveTo(40,40); ctx.lineTo(innerWidth-40, innerHeight-40); ctx.stroke(); return \"ok\"; })()"}'
```

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.snapshot --params '{"maxWidth":900,"format":"jpeg"}'
```

## 语音唤醒 + 对讲模式

- 语音唤醒和对讲模式可在“设置”中使用。
- iOS 可能会暂停后台音频；当应用未处于活跃状态时，请将语音功能视为尽力而为。

## 常见错误

- `NODE_BACKGROUND_UNAVAILABLE`：将 iOS 应用切换到前台（画布/相机/屏幕命令需要前台状态）。
- `A2UI_HOST_NOT_CONFIGURED`：Gateway 未公布画布主机 URL；请检查 [Gateway 配置](/gateway/configuration) 中的 `canvasHost`。
- 配对提示从未出现：运行 `openclaw nodes pending` 并手动批准。
- 重新安装后重连失败：钥匙串中的配对令牌已被清除；请重新配对节点。

## 相关文档

- [配对](/gateway/pairing)
- [发现](/gateway/discovery)
- [Bonjour](/gateway/bonjour)
