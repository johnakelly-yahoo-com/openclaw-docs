---
summary: "13. 会话修剪：裁剪工具结果以减少上下文膨胀"
read_when:
  - 14. 你希望减少来自工具输出的 LLM 上下文增长
  - 15. 你正在调优 agents.defaults.contextPruning
---

# 16. 会话修剪

17. 会话修剪会在每次 LLM 调用前，直接从内存上下文中裁剪**旧的工具结果**。 18. 它**不会**重写磁盘上的会话历史（`*.jsonl`）。

## 19. 运行时机

- 20. 当启用 `mode: "cache-ttl"` 且该会话上一次 Anthropic 调用早于 `ttl` 时。
- 21. 仅影响该请求发送给模型的消息。
- 22. 仅对 Anthropic API 调用（以及 OpenRouter 的 Anthropic 模型）生效。
- 23. 为获得最佳效果，将 `ttl` 与你的模型 `cacheControlTtl` 匹配。
- 24. 修剪后，TTL 窗口会重置，因此后续请求会在 `ttl` 再次过期前继续使用缓存。

## 25. 智能默认值（Anthropic）

- 26. **OAuth 或 setup-token** 配置：启用 `cache-ttl` 修剪，并将心跳设置为 `1h`。
- 27. **API key** 配置：启用 `cache-ttl` 修剪，将心跳设置为 `30m`，并在 Anthropic 模型上将默认 `cacheControlTtl` 设为 `1h`。
- 28. 如果你显式设置了其中任何值，OpenClaw **不会**覆盖它们。

## 29. 改进点（成本 + 缓存行为）

- 30. **为什么要修剪：** Anthropic 的提示缓存仅在 TTL 内生效。 31. 如果会话空闲超过 TTL，下一次请求将重新缓存完整提示，除非你先进行裁剪。
- 32. **哪些会更便宜：** 修剪会降低 TTL 过期后首次请求的 **cacheWrite** 大小。
- 33. **TTL 重置为何重要：** 一旦执行修剪，缓存窗口会重置，因此后续请求可以复用新近缓存的提示，而无需再次缓存完整历史。
- 34. **它不做什么：** 修剪不会增加 token 或产生“翻倍”的成本；它只会改变 TTL 过期后首次请求中被缓存的内容。

## 35. 可被修剪的内容

- 36. 仅 `toolResult` 消息。
- 37. 用户与助手消息**永不**修改。
- 38. 最后 `keepLastAssistants` 条助手消息会受到保护；该分界点之后的工具结果不会被修剪。
- 39. 如果没有足够的助手消息来确定分界点，将跳过修剪。
- 40. 包含**图像块**的工具结果会被跳过（永不裁剪/清除）。

## 41. 上下文窗口估算

42. 修剪使用估算的上下文窗口（字符数 ≈ token × 4）。 43. 基础窗口按以下顺序解析：

1. 44. `models.providers.*.models[].contextWindow` 覆盖值。
2. 45. 模型定义中的 `contextWindow`（来自模型注册表）。
3. 46. 默认 `200000` tokens。

47) 如果设置了 `agents.defaults.contextTokens`，则将其视为解析后窗口的上限（取最小值）。

## 48. 模式

### 49. cache-ttl

- 50. 仅当最后一次 Anthropic 调用早于 `ttl`（默认 `5m`）时才会运行修剪。
- When it runs: same soft-trim + hard-clear behavior as before.

## Soft vs hard pruning

- **Soft-trim**: only for oversized tool results.
  - Keeps head + tail, inserts `...`, and appends a note with the original size.
  - Skips results with image blocks.
- **Hard-clear**: replaces the entire tool result with `hardClear.placeholder`.

## Tool selection

- `tools.allow` / `tools.deny` support `*` wildcards.
- Deny wins.
- Matching is case-insensitive.
- Empty allow list => all tools allowed.

## 22. 与其他限制的交互

- Built-in tools already truncate their own output; session pruning is an extra layer that prevents long-running chats from accumulating too much tool output in the model context.
- Compaction is separate: compaction summarizes and persists, pruning is transient per request. See [/concepts/compaction](/concepts/compaction).

## Defaults (when enabled)

- `ttl`: `"5m"`
- `keepLastAssistants`: `3`
- `softTrimRatio`: `0.3`
- `hardClearRatio`: `0.5`
- `minPrunableToolChars`: `50000`
- `softTrim`: `{ maxChars: 4000, headChars: 1500, tailChars: 1500 }`
- `hardClear`: `{ enabled: true, placeholder: "[Old tool result content cleared]" }`

## Examples

Default (off):

```json5
{
  agent: {
    contextPruning: { mode: "off" },
  },
}
```

Enable TTL-aware pruning:

```json5
{
  agent: {
    contextPruning: { mode: "cache-ttl", ttl: "5m" },
  },
}
```

Restrict pruning to specific tools:

```json5
{
  agent: {
    contextPruning: {
      mode: "cache-ttl",
      tools: { allow: ["exec", "read"], deny: ["*image*"] },
    },
  },
}
```

See config reference: [Gateway Configuration](/gateway/configuration)
