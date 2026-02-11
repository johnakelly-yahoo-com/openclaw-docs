---
summary: "43. mac 应用如何嵌入网关 WebChat 以及如何调试"
read_when:
  - 44. 调试 mac WebChat 视图或回环端口
title: "45. WebChat"
---

# 46. WebChat（macOS 应用）

47. macOS 菜单栏应用将 WebChat UI 作为原生 SwiftUI 视图嵌入。 48. 它
    连接到网关，并默认为所选代理的**主会话**（并提供用于其他会话的会话切换器）。

- 49. **本地模式**：直接连接到本地 Gateway WebSocket。
- 50. **远程模式**：通过 SSH 转发 Gateway 控制端口，并将该隧道用作数据平面。

## Launch & debugging

- Manual: Lobster menu → “Open Chat”.

- Auto‑open for testing:

  ```bash
  dist/OpenClaw.app/Contents/MacOS/OpenClaw --webchat
  ```

- Logs: `./scripts/clawlog.sh` (subsystem `bot.molt`, category `WebChatSwiftUI`).

## How it’s wired

- Data plane: Gateway WS methods `chat.history`, `chat.send`, `chat.abort`,
  `chat.inject` and events `chat`, `agent`, `presence`, `tick`, `health`.
- Session: defaults to the primary session (`main`, or `global` when scope is
  global). The UI can switch between sessions.
- 引导流程使用专用会话，以保持首次运行设置的独立性。

## 安全面

- 远程模式仅通过 SSH 转发 Gateway 的 WebSocket 控制端口。

## Known limitations

- The UI is optimized for chat sessions (not a full browser sandbox).
