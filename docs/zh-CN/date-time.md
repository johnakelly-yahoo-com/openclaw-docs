---
summary: "跨信封、提示、工具和连接器的日期与时间处理"
read_when:
  - 你正在更改向模型或用户显示时间戳的方式
  - 你正在调试消息或系统提示输出中的时间格式
title: "Date and Time"
---

# 日期 & 时间

OpenClaw 默认**传输时间戳使用主机本地时间**，而**仅在系统提示中使用用户时区**。
提供方时间戳会被保留，以便工具保持其原生语义（当前时间可通过 `session_status` 获取）。

## 消息信封（默认本地）

入站消息会被包裹上一个时间戳（分钟精度）：

```
[Provider ... 2026-01-05 16:26 PST] message text
```

该信封时间戳**默认使用主机本地时间**，与提供方时区无关。

你可以覆盖此行为：

```json5
{
  agents: {
    defaults: {
      envelopeTimezone: "local", // "utc" | "local" | "user" | IANA timezone
      envelopeTimestamp: "on", // "on" | "off"
      envelopeElapsed: "on", // "on" | "off"
    },
  },
}
```

- `envelopeTimezone: "utc"` 使用 UTC。
- `envelopeTimezone: "local"` 使用主机时区。
- `envelopeTimezone: "user"` uses `agents.defaults.userTimezone` (falls back to host timezone).
- 使用显式的 IANA 时区（例如，`"America/Chicago"`）以固定时区。
- `envelopeTimestamp: "off"` 会从信封头中移除绝对时间戳。
- `envelopeElapsed: "off"` 会移除经过时间后缀（`+2m` 样式）。

### Examples

1. **本地（默认）：**

```
[WhatsApp +1555 2026-01-18 00:19 PST] hello
```

3. **用户时区：**

```
4. [WhatsApp +1555 2026-01-18 00:19 CST] hello
```

**Elapsed time enabled:**

```
6. [WhatsApp +1555 +30s 2026-01-18T05:19Z] follow-up
```

## 7. 系统提示：当前日期与时间

8. 如果已知用户时区，系统提示会包含一个专用的
   **当前日期与时间** 部分，并且**仅包含时区**（不包含具体时钟/时间格式），
   以保持提示缓存的稳定性：

```
9. 时区：America/Chicago
```

10. 当代理需要当前时间时，使用 `session_status` 工具；该状态
    卡片包含一行时间戳。

## System event lines (local by default)

12. 插入到代理上下文中的排队系统事件，会使用与消息信封相同的时区选择来添加时间戳前缀（默认：主机本地）。

```
System: [2026-01-12 12:19:17 PST] Model switched.
```

### Configure user timezone + format

```json5
15. {
  agents: {
    defaults: {
      userTimezone: "America/Chicago",
      timeFormat: "auto", // auto | 12 | 24
    },
  },
}
```

- `userTimezone` sets the **user-local timezone** for prompt context.
- `timeFormat` controls **12h/24h display** in the prompt. 18. `auto` 遵循操作系统偏好设置。

## 19. 时间格式检测（auto）

20. 当 `timeFormat: "auto"` 时，OpenClaw 会检查操作系统偏好（macOS/Windows），
    并在需要时回退到基于区域设置的格式。 21. 检测到的值会**按进程缓存**，
    以避免重复的系统调用。

## 22. 工具负载 + 连接器（原始提供方时间 + 规范化字段）

23. Channel 工具返回**提供方原生时间戳**，并添加规范化字段以保持一致性：

- 24. `timestampMs`：纪元毫秒（UTC）
- 25. `timestampUtc`：ISO 8601 UTC 字符串

26. 会保留原始提供方字段，确保不丢失任何信息。

- 27. Slack：来自 API 的类纪元字符串
- 28. Discord：UTC ISO 时间戳
- Telegram/WhatsApp: provider-specific numeric/ISO timestamps

30. 如果需要本地时间，请使用已知时区在下游进行转换。

## 31. 相关文档

- [System Prompt](/concepts/system-prompt)
- 33. [时区](/concepts/timezone)
- 34. [消息](/concepts/messages)
