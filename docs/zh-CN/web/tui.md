---
summary: "终端 UI（TUI）：从任意机器连接到 Gateway"
read_when:
  - 你想要一个适合初学者的 TUI 演练指南
  - 你需要完整的 TUI 功能、命令和快捷键列表
title: "TUI"
---

# TUI（终端 UI）

## 快速开始

1. 启动 Gateway。

```bash
openclaw gateway
```

2. 打开 TUI。

```bash
openclaw tui
```

3. 输入一条消息并按 Enter。

远程 Gateway：

```bash
openclaw tui --url ws://<host>:<port> --token <gateway-token>
```

如果你的 Gateway 使用密码认证，请使用 `--password`。

## 你将看到的内容

- 页眉：连接 URL、当前代理、当前会话。
- 聊天记录：用户消息、助手回复、系统通知、工具卡片。
- 状态行：连接/运行状态（connecting、running、streaming、idle、error）。
- 页脚：连接状态 + 代理 + 会话 + 模型 + think/verbose/reasoning + 令牌计数 + deliver。
- 输入区：带自动补全的文本编辑器。

## 心智模型：代理 + 会话

- 代理是唯一的 slug（例如 `main`、`research`）。 Gateway 会公开该列表。
- 会话属于当前代理。
- 会话键以 `agent:<agentId>:<sessionKey>` 的形式存储。
  - 如果你输入 `/session main`，TUI 会将其展开为 `agent:<currentAgent>:main`。
  - 如果你输入 `/session agent:other:main`，你会显式切换到该代理的会话。
- 会话作用域：
  - `per-sender`（默认）：每个代理都有多个会话。
  - `global`：TUI 始终使用 `global` 会话（选择器可能为空）。
- 当前代理 + 会话始终在页脚中可见。

## 发送与投递

- 消息会发送到 Gateway；默认情况下不会投递到提供方。
- 开启投递：
  - `/deliver on`
  - 1. 或“设置”面板
  - 2. 或使用 `openclaw tui --deliver` 启动

## 3. 选择器 + 覆盖层

- 4. 模型选择器：列出可用模型并设置会话级覆盖。
- 5. 代理选择器：选择不同的代理。
- 6. 会话选择器：仅显示当前代理的会话。
- 7. 设置：切换 deliver、工具输出展开以及思考可见性。

## 8. 键盘快捷键

- 9. Enter：发送消息
- 10. Esc：中止正在进行的运行
- 11. Ctrl+C：清空输入（按两次退出）
- 12. Ctrl+D：退出
- 13. Ctrl+L：模型选择器
- 14. Ctrl+G：代理选择器
- 15. Ctrl+P：会话选择器
- 16. Ctrl+O：切换工具输出展开
- 17. Ctrl+T：切换思考可见性（重新加载历史）

## 18. 斜杠命令

19. 核心：

- 20. `/help`
- 21. `/status`
- 22. `/agent <id>`（或 `/agents`）
- 23. `/session <key>`（或 `/sessions`）
- 24. `/model <provider/model>`（或 `/models`）

25. 会话控制：

- 26. `/think <off|minimal|low|medium|high>`
- 27. `/verbose <on|full|off>`
- 28. `/reasoning <on|off|stream>`
- 29. `/usage <off|tokens|full>`
- 30. `/elevated <on|off|ask|full>`（别名：`/elev`）
- 31. `/activation <mention|always>`
- 32. `/deliver <on|off>`

33. 会话生命周期：

- 34. `/new` 或 `/reset`（重置会话）
- 35. `/abort`（中止正在进行的运行）
- 36. `/settings`
- 37. `/exit`

38. 其他 Gateway 斜杠命令（例如 `/context`）会被转发到 Gateway，并以系统输出显示。 39. 参见 [斜杠命令](/tools/slash-commands)。

## 40. 本地 shell 命令

- 41. 以 `!` 前缀一行可在 TUI 主机上运行本地 shell 命令。
- 42. 每个会话中，TUI 会提示一次以允许本地执行；拒绝后将为该会话保持 `!` 禁用。
- 43. 命令在 TUI 工作目录中的全新、非交互式 shell 中运行（不保留 `cd`/环境）。
- 44. 单独的 `!` 会作为普通消息发送；行首空格不会触发本地执行。

## 45. 工具输出

- 46. 工具调用以卡片形式显示，包含参数和结果。
- 47. Ctrl+O 在折叠/展开视图之间切换。
- 48. 工具运行期间，部分更新会流式进入同一张卡片。

## 49. 历史 + 流式

- 50. 连接时，TUI 会加载最新的历史记录（默认 200 条消息）。
- 流式响应在最终确定前会原地更新。
- TUI 还会监听代理工具事件，以提供更丰富的工具卡片。

## 连接详情

- The TUI registers with the Gateway as `mode: "tui"`.
- 重连时会显示系统消息；事件间隙会在日志中呈现。

## Options

- `--url <url>`：Gateway WebSocket URL（默认为配置或 `ws://127.0.0.1:<port>`）
- `--token <token>`：Gateway 令牌（如需要）
- `--password <password>`：Gateway 密码（如需要）
- `--session <key>`: Session key (default: `main`, or `global` when scope is global)
- `--deliver`：将助手回复投递给提供方（默认关闭）
- `--thinking <level>`：覆盖发送时的思考级别
- `--timeout-ms <ms>`：代理超时时间（毫秒）（默认为 `agents.defaults.timeoutSeconds`）

注意：当你设置 `--url` 时，TUI 不会回退到配置或环境凭据。
请显式传递 `--token` 或 `--password`。 Missing explicit credentials is an error.

## 故障排查

发送消息后没有输出：

- 在 TUI 中运行 `/status` 以确认 Gateway 已连接且处于空闲/忙碌状态。
- 检查 Gateway 日志：`openclaw logs --follow`。
- 确认代理可以运行：`openclaw status` 和 `openclaw models status`。
- 如果你期望在聊天频道中看到消息，请启用投递（`/deliver on` 或 `--deliver`）。
- `--history-limit <n>`：要加载的历史条目数（默认 200）

## 连接故障排查

- `disconnected`：确保 Gateway 正在运行，并且你的 `--url/--token/--password` 正确。
- 选择器中没有代理：检查 `openclaw agents list` 以及你的路由配置。
- 会话选择器为空：你可能处于 global 作用域，或尚未有任何会话。
