---
summary: "日志输出层面、文件日志、WS 日志样式以及控制台格式"
read_when:
  - 更改日志输出或格式
  - 调试 CLI 或网关输出
title: "日志"
---

# 日志

如需面向用户的概览（CLI + Control UI + 配置），请参见 [/logging](/logging)。

OpenClaw 有两个日志“层面”：

- **控制台输出**（你在终端 / 调试 UI 中看到的内容）。
- **文件日志**（JSON Lines），由网关日志器写入。

## 基于文件的日志器

- 默认的滚动日志文件位于 `/tmp/openclaw/`（每天一个文件）：`openclaw-YYYY-MM-DD.log`
  - 日期使用网关主机的本地时区。
- 日志文件路径和级别可通过 `~/.openclaw/openclaw.json` 配置：
  - `logging.file`
  - `logging.level`

文件格式为每行一个 JSON 对象。

Control UI 的 Logs 标签页通过网关（`logs.tail`）实时跟踪该文件。
CLI 也可以做到同样的事情：

```bash
openclaw logs --follow
```

**详细模式 vs. 日志级别**

- **文件日志** 完全由 `logging.level` 控制。
- `--verbose` 只影响 **控制台详细程度**（以及 WS 日志样式）；它**不会**提高文件日志级别。
- 若要在文件日志中捕获仅在详细模式下才有的细节，请将 `logging.level` 设置为 `debug` 或 `trace`。

## 控制台捕获

CLI 会捕获 `console.log/info/warn/error/debug/trace` 并将其写入文件日志，同时仍然输出到 stdout/stderr。

你可以通过以下方式独立调整控制台详细程度：

- `logging.consoleLevel`（默认 `info`）
- `logging.consoleStyle`（`pretty` | `compact` | `json`）

## 工具摘要脱敏

详细的工具摘要（例如 `🛠️ Exec: ...`）在进入控制台流之前可以掩盖敏感令牌。 这**仅作用于工具**，不会改变文件日志。

- `logging.redactSensitive`：`off` | `tools`（默认：`tools`）
- `logging.redactPatterns`：正则字符串数组（覆盖默认值）
  - 使用原始正则字符串（自动 `gi`），或在需要自定义标志时使用 `/pattern/flags`。
  - 匹配内容将被掩盖：保留前 6 位 + 后 4 位字符（长度 >= 18），否则显示为 `***`。
  - 默认规则覆盖常见的键赋值、CLI 标志、JSON 字段、Bearer 头、PEM 块以及常见的令牌前缀。

## 网关 WebSocket 日志

网关以两种模式打印 WebSocket 协议日志：

- **普通模式（无 `--verbose`）**：仅打印“有意义的” RPC 结果：
  - 错误（`ok=false`）
  - 慢调用（默认阈值：`>= 50ms`）
  - 解析错误
- **详细模式（`--verbose`）**：打印所有 WS 请求/响应流量。

### WS 日志样式

`openclaw gateway` 支持按网关切换样式：

- `--ws-log auto`（默认）：普通模式下进行优化；详细模式使用紧凑输出
- `--ws-log compact`：详细模式下使用紧凑输出（成对的请求/响应）
- `--ws-log full`：详细模式下使用完整的逐帧输出
- `--compact`：`--ws-log compact` 的别名

示例：

```bash
# 已优化（仅错误/慢）
openclaw gateway

# 显示所有 WS 流量（已配对）
openclaw gateway --verbose --ws-log compact

# 显示所有 WS 流量（完整元数据）
openclaw gateway --verbose --ws-log full
```

## 控制台格式化（子系统日志）

控制台格式化器**感知 TTY**，并打印一致的、带前缀的行。
子系统日志器使输出保持分组且易于扫描。

行为：

- 每一行都有**子系统前缀**（例如 `[gateway]`、`[canvas]`、`[tailscale]`）
- **Subsystem colors** (stable per subsystem) plus level coloring
- 当输出为 TTY 或环境看起来像富终端时启用颜色（`TERM`/`COLORTERM`/`TERM_PROGRAM`），并遵循 `NO_COLOR`
- **缩短的子系统前缀**：移除前导 `gateway/` + `channels/`，保留最后 2 个段（例如 `whatsapp/outbound`）
- **按子系统的子日志器**（自动前缀 + 结构化字段 `{ subsystem }`）
- **`logRaw()`** 用于 QR/UX 输出（无前缀、无格式）
- **控制台样式**（例如 `pretty | compact | json`）
- **控制台日志级别** 与 **文件日志级别** 分离（当 `logging.level` 设为 `debug`/`trace` 时，文件保留完整细节）
- **WhatsApp 消息正文** 以 `debug` 级别记录（使用 `--verbose` 可查看）

This keeps existing file logs stable while making interactive output scannable.
