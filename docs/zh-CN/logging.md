---
summary: "Logging overview: file logs, console output, CLI tailing, and the Control UI"
read_when:
  - You need a beginner-friendly overview of logging
  - 你希望配置日志级别或格式
  - 你正在排查问题，需要快速找到日志
title: "日志"
---

# 日志

OpenClaw 在两个位置记录日志：

- **文件日志**（JSON 行）由 Gateway 写入。
- **控制台输出**：显示在终端和控制 UI 中。

本页面说明日志的位置、如何读取它们，以及如何配置日志级别和格式。

## 日志位置

默认情况下，Gateway 会在以下路径写入滚动日志文件：

/tmp/openclaw/openclaw-YYYY-MM-DD.log

日期使用 Gateway 主机的本地时区。

你可以在 `~/.openclaw/openclaw.json` 中覆盖此设置：

```json
{
  "logging": {
    "file": "/path/to/openclaw.log"
  }
}
```

## 如何读取日志

### CLI：实时 tail（推荐）

使用 CLI 通过 RPC 对 Gateway 日志文件进行 tail：

```bash
openclaw logs --follow
```

输出模式：

- **TTY 会话**：美观、彩色、结构化的日志行。
- **非 TTY 会话**：纯文本。
- `--json`：行分隔的 JSON（每行一个日志事件）。
- `--plain`：在 TTY 会话中强制使用纯文本。
- `--no-color`: disable ANSI colors.

在 JSON 模式下，CLI 会输出带有 `type` 标签的对象：

- `meta`：流元数据（文件、游标、大小）
- `log`：已解析的日志条目
- `notice`：截断/轮转提示
- `raw`：未解析的日志行

如果 Gateway 无法访问，CLI 会打印一个简短提示，建议运行：

```bash
openclaw doctor
```

### 控制 UI（Web）

Control UI 的 **Logs** 选项卡使用 `logs.tail` 对同一文件进行 tail。
有关如何打开它，请参见 [/web/control-ui](/web/control-ui)。

### 仅频道日志

要过滤频道活动（WhatsApp/Telegram 等），请使用：

```bash
openclaw channels logs --channel whatsapp
```

## 日志格式

### 文件日志（JSONL）

日志文件中的每一行都是一个 JSON 对象。 CLI 和 Control UI 会解析这些条目，以渲染结构化输出（时间、级别、子系统、消息）。

### 控制台输出

控制台日志 **感知 TTY**，并针对可读性进行格式化：

- 子系统前缀（例如 `gateway/channels/whatsapp`）
- 级别着色（info/warn/error）
- 可选的紧凑或 JSON 模式

控制台格式由 `logging.consoleStyle` 控制。

## 配置日志

所有日志配置都位于 `~/.openclaw/openclaw.json` 中的 `logging` 下。

```json
{
  "logging": {
    "level": "info",
    "file": "/tmp/openclaw/openclaw-YYYY-MM-DD.log",
    "consoleLevel": "info",
    "consoleStyle": "pretty",
    "redactSensitive": "tools",
    "redactPatterns": ["sk-.*"]
  }
}
```

### Log levels

- `logging.level`: **file logs** (JSONL) level.
- `logging.consoleLevel`：**控制台**的详细级别。

`--verbose` only affects console output; it does not change file log levels.

### Console styles

`logging.consoleStyle`：

- `pretty`: human-friendly, colored, with timestamps.
- `compact`: tighter output (best for long sessions).
- `json`: JSON per line (for log processors).

### Redaction

Tool summaries can redact sensitive tokens before they hit the console:

- `logging.redactSensitive`: `off` | `tools` (default: `tools`)
- `logging.redactPatterns`: list of regex strings to override the default set

Redaction affects **console output only** and does not alter file logs.

## Diagnostics + OpenTelemetry

Diagnostics are structured, machine-readable events for model runs **and**
message-flow telemetry (webhooks, queueing, session state). They do **not**
replace logs; they exist to feed metrics, traces, and other exporters.

Diagnostics events are emitted in-process, but exporters only attach when
diagnostics + the exporter plugin are enabled.

### OpenTelemetry vs OTLP

- **OpenTelemetry (OTel)**: the data model + SDKs for traces, metrics, and logs.
- **OTLP**: the wire protocol used to export OTel data to a collector/backend.
- OpenClaw exports via **OTLP/HTTP (protobuf)** today.

### Signals exported

- **Metrics**: counters + histograms (token usage, message flow, queueing).
- **Traces**: spans for model usage + webhook/message processing.
- **Logs**: exported over OTLP when `diagnostics.otel.logs` is enabled. Log
  volume can be high; keep `logging.level` and exporter filters in mind.

### Diagnostic event catalog

Model usage:

- `model.usage`: tokens, cost, duration, context, provider/model/channel, session ids.

Message flow:

- `webhook.received`: webhook ingress per channel.
- `webhook.processed`: webhook handled + duration.
- `webhook.error`: webhook handler errors.
- `message.queued`: message enqueued for processing.
- `message.processed`: outcome + duration + optional error.

Queue + session:

- `queue.lane.enqueue`: command queue lane enqueue + depth.
- `queue.lane.dequeue`: command queue lane dequeue + wait time.
- `session.state`: session state transition + reason.
- `session.stuck`: session stuck warning + age.
- `run.attempt`: run retry/attempt metadata.
- `diagnostic.heartbeat`: aggregate counters (webhooks/queue/session).

### Enable diagnostics (no exporter)

Use this if you want diagnostics events available to plugins or custom sinks:

```json
{
  "diagnostics": {
    "enabled": true
  }
}
```

### Diagnostics flags (targeted logs)

Use flags to turn on extra, targeted debug logs without raising `logging.level`.
Flags are case-insensitive and support wildcards (e.g. `telegram.*` or `*`).

```json
{
  "diagnostics": {
    "flags": ["telegram.http"]
  }
}
```

Env override (one-off):

```
2. OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload
```

3. 说明：

- 4. 标志日志会写入标准日志文件（与 `logging.file` 相同）。
- 5. 输出仍会按照 `logging.redactSensitive` 进行脱敏。
- 6. 完整指南：[/diagnostics/flags](/diagnostics/flags)。

### 导出到 OpenTelemetry

8. 诊断信息可以通过 `diagnostics-otel` 插件导出（OTLP/HTTP）。 9. 这
   适用于任何接受 OTLP/HTTP 的 OpenTelemetry 收集器/后端。

```json
10. {
  "plugins": {
    "allow": ["diagnostics-otel"],
    "entries": {
      "diagnostics-otel": {
        "enabled": true
      }
    }
  },
  "diagnostics": {
    "enabled": true,
    "otel": {
      "enabled": true,
      "endpoint": "http://otel-collector:4318",
      "protocol": "http/protobuf",
      "serviceName": "openclaw-gateway",
      "traces": true,
      "metrics": true,
      "logs": true,
      "sampleRate": 0.2,
      "flushIntervalMs": 60000
    }
  }
}
```

11. 说明：

- 12. 你也可以使用 `openclaw plugins enable diagnostics-otel` 启用该插件。
- 13. `protocol` 目前仅支持 `http/protobuf`。 `grpc` 会被忽略。
- 15. 指标包括令牌用量、成本、上下文大小、运行时长，以及消息流
      计数器/直方图（webhook、队列、会话状态、队列深度/等待）。
- 16. 可通过 `traces` / `metrics` 切换追踪/指标（默认：开启）。 17. 追踪
      在启用时包括模型使用跨度以及 webhook/消息处理跨度。
- 18. 当你的收集器需要鉴权时，请设置 `headers`。
- 支持的环境变量：`OTEL_EXPORTER_OTLP_ENDPOINT`、`OTEL_SERVICE_NAME`、`OTEL_EXPORTER_OTLP_PROTOCOL`。

### 20. 导出的指标（名称 + 类型）

21. 模型使用：

- 22. `openclaw.tokens`（计数器，属性：`openclaw.token`、`openclaw.channel`、
      `openclaw.provider`、`openclaw.model`）
- 23. `openclaw.cost.usd`（计数器，属性：`openclaw.channel`、`openclaw.provider`、
      `openclaw.model`）
- 24. `openclaw.run.duration_ms`（直方图，属性：`openclaw.channel`、
      `openclaw.provider`、`openclaw.model`）
- 25. `openclaw.context.tokens`（直方图，属性：`openclaw.context`、
      `openclaw.channel`、`openclaw.provider`、`openclaw.model`）

26. 消息流：

- 27. `openclaw.webhook.received`（计数器，属性：`openclaw.channel`、
      `openclaw.webhook`）
- 28. `openclaw.webhook.error`（计数器，属性：`openclaw.channel`、
      `openclaw.webhook`）
- 29. `openclaw.webhook.duration_ms`（直方图，属性：`openclaw.channel`、
      `openclaw.webhook`）
- 30. `openclaw.message.queued`（计数器，属性：`openclaw.channel`、
      `openclaw.source`）
- 31. `openclaw.message.processed`（计数器，属性：`openclaw.channel`、
      `openclaw.outcome`）
- 32. `openclaw.message.duration_ms`（直方图，属性：`openclaw.channel`、
      `openclaw.outcome`）

33. 队列 + 会话：

- 34. `openclaw.queue.lane.enqueue`（计数器，属性：`openclaw.lane`）
- 35. `openclaw.queue.lane.dequeue`（计数器，属性：`openclaw.lane`）
- 36. `openclaw.queue.depth`（直方图，属性：`openclaw.lane` 或
      `openclaw.channel=heartbeat`）
- 37. `openclaw.queue.wait_ms`（直方图，属性：`openclaw.lane`）
- 38. `openclaw.session.state`（计数器，属性：`openclaw.state`、`openclaw.reason`）
- 39. `openclaw.session.stuck`（计数器，属性：`openclaw.state`）
- 40. `openclaw.session.stuck_age_ms`（直方图，属性：`openclaw.state`）
- 41. `openclaw.run.attempt`（计数器，属性：`openclaw.attempt`）

### 42. 导出的跨度（名称 + 关键属性）

- 43. `openclaw.model.usage`
  - 44. `openclaw.channel`、`openclaw.provider`、`openclaw.model`
  - 45. `openclaw.sessionKey`、`openclaw.sessionId`
  - 46. `openclaw.tokens.*`（input/output/cache_read/cache_write/total）
- 47. `openclaw.webhook.processed`
  - 48. `openclaw.channel`、`openclaw.webhook`、`openclaw.chatId`
- 49. `openclaw.webhook.error`
  - 50. `openclaw.channel`、`openclaw.webhook`、`openclaw.chatId`、
        `openclaw.error`
- `openclaw.message.processed`
  - `openclaw.channel`, `openclaw.outcome`, `openclaw.chatId`,
    `openclaw.messageId`, `openclaw.sessionKey`, `openclaw.sessionId`,
    `openclaw.reason`
- `openclaw.session.stuck`
  - `openclaw.state`, `openclaw.ageMs`, `openclaw.queueDepth`,
    `openclaw.sessionKey`, `openclaw.sessionId`

### Sampling + flushing

- Trace sampling: `diagnostics.otel.sampleRate` (0.0–1.0, root spans only).
- Metric export interval: `diagnostics.otel.flushIntervalMs` (min 1000ms).

### Protocol notes

- OTLP/HTTP endpoints can be set via `diagnostics.otel.endpoint` or
  `OTEL_EXPORTER_OTLP_ENDPOINT`.
- If the endpoint already contains `/v1/traces` or `/v1/metrics`, it is used as-is.
- If the endpoint already contains `/v1/logs`, it is used as-is for logs.
- `diagnostics.otel.logs` enables OTLP log export for the main logger output.

### Log export behavior

- OTLP logs use the same structured records written to `logging.file`.
- Respect `logging.level` (file log level). Console redaction does **not** apply
  to OTLP logs.
- High-volume installs should prefer OTLP collector sampling/filtering.

## Troubleshooting tips

- **Gateway not reachable?** Run `openclaw doctor` first.
- **Logs empty?** Check that the Gateway is running and writing to the file path
  in `logging.file`.
- **Need more detail?** Set `logging.level` to `debug` or `trace` and retry.
