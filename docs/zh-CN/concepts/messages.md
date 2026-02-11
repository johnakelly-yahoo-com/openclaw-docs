---
summary: "36. 消息流、会话、队列以及推理可见性"
read_when:
  - 37. 解释入站消息如何生成回复
  - Clarifying sessions, queueing modes, or streaming behavior
  - 39. 记录推理可见性及其使用影响
title: "40. 消息"
---

# 23. 消息

42. 本页面将 OpenClaw 如何处理入站消息、会话、队列、
    流式传输以及推理可见性整合在一起。

## 43. 消息流（高层级）

```
24. 入站消息
  -> 路由/绑定 -> 会话键
  -> 队列（如果有正在运行的任务）
  -> 代理运行（流式 + 工具）
  -> 出站回复（通道限制 + 分块）
```

45. 关键调节项位于配置中：

- 46. `messages.*` 用于前缀、队列以及分组行为。
- 47. `agents.defaults.*` 用于块级流式传输和分块的默认设置。
- 48. 通道覆盖（`channels.whatsapp.*`、`channels.telegram.*` 等） 49. 用于容量上限和流式开关。

50. 完整架构请参见 [Configuration](/gateway/configuration)。

## 25. 入站去重

渠道在重新连接后可能会重新投递同一条消息。 OpenClaw 维护一个短生命周期的缓存，以 channel/account/peer/session/message id 为键，因此重复投递不会再次触发代理运行。

## 入站防抖

来自**同一发送者**的快速连续消息可以通过 `messages.inbound` 合并为一次代理轮次。 Debouncing is scoped per channel + conversation
and uses the most recent message for reply threading/IDs.

配置（全局默认 + 按渠道覆盖）：

```json5
{
  messages: {
    inbound: {
      debounceMs: 2000,
      byChannel: {
        whatsapp: 5000,
        slack: 1500,
        discord: 1500,
      },
    },
  },
}
```

备注：

- 防抖仅适用于**纯文本**消息；媒体/附件会立即触发刷新。
- 控制命令会绕过防抖，以保持其独立性。

## 会话与设备

会话由网关拥有，而不是由客户端拥有。

- 私聊会折叠到代理的主会话键中。
- 群组/频道拥有各自的会话键。
- 会话存储和对话记录保存在网关主机上。

27. 多个设备/通道可以映射到同一会话，但历史不会完全
    同步回每个客户端。 28. 建议：长对话使用一个主设备，
    以避免上下文分歧。 Control UI 和 TUI 始终显示基于网关的会话记录，因此它们是事实来源。

详情：[会话管理](/concepts/session)。

## 入站内容与历史上下文

OpenClaw 将**提示内容**与**命令内容**分离：

- `Body`：发送给代理的提示文本。 其中可能包含渠道信封以及可选的历史包装。
- `CommandBody`：用于指令/命令解析的原始用户文本。
- `RawBody`：`CommandBody` 的旧别名（为兼容性保留）。

When a channel supplies history, it uses a shared wrapper:

- `[Chat messages since your last reply - for context]`
- `[Current message - respond to this]`

30. 对于 **非直接聊天**（群组/频道/房间），**当前消息正文** 会在前面加上
    发送者标签（与历史条目使用的样式相同）。 这使实时消息与排队/历史消息在代理提示中保持一致。

历史缓冲区是**仅待处理**的：它们包含未触发运行的群消息（例如受提及门控的消息），并**排除**已进入会话记录的消息。

指令剥离仅适用于**当前消息**部分，因此历史保持完整。 封装历史的渠道应将 `CommandBody`（或 `RawBody`）设置为原始消息文本，并将 `Body` 保持为组合后的提示。
历史缓冲区可通过 `messages.groupChat.historyLimit`（全局默认）以及按渠道覆盖（如 `channels.slack.historyLimit` 或 `channels.telegram.accounts.<id>`
36. .historyLimit`（设置为 `0\` 以禁用））进行配置。排队与跟进

## 如果已有运行处于活动状态，入站消息可以被排队、引导进入当前运行，或收集用于后续轮次。

通过 `messages.queue`（以及 `messages.queue.byChannel`）进行配置。

- 模式：`interrupt`、`steer`、`followup`、`collect`，以及其 backlog 变体。
- 详情：[排队](/concepts/queue)。

流式、分块与批处理

## 块流式发送会在模型生成文本块时发送部分回复。

分块会遵循渠道的文本长度限制，并避免拆分围栏代码。
关键设置：

`agents.defaults.blockStreamingDefault`（`on|off`，默认 off）

- `agents.defaults.blockStreamingBreak`（`text_end|message_end`）
- `agents.defaults.blockStreamingChunk`（`minChars|maxChars|breakPreference`）
- `agents.defaults.blockStreamingCoalesce`（基于空闲的批处理）
- `agents.defaults.humanDelay`（块回复之间的类人停顿）
- `agents.defaults.humanDelay` (human-like pause between block replies)
- 1. 通道覆盖：`*.blockStreaming` 和 `*.blockStreamingCoalesce`（非 Telegram 通道需要显式设置 `*.blockStreaming: true`）

2. 详情：[Streaming + chunking](/concepts/streaming)。

## Reasoning visibility and tokens

OpenClaw can expose or hide model reasoning:

- 5. `/reasoning on|off|stream` 控制可见性。
- 6. 当模型生成推理内容时，推理内容仍计入令牌使用量。
- 7. Telegram 支持将推理流式输出到草稿气泡中。

8. 详情：[Thinking + reasoning directives](/tools/thinking) 和 [Token use](/reference/token-use)。

## 9. 前缀、线程与回复

10. 出站消息格式集中在 `messages` 中：

- 11. `messages.responsePrefix`、`channels.<channel>12. .responsePrefix`，以及 `channels.<channel>13. .accounts.<id>14. .responsePrefix`（出站前缀级联），以及 `channels.whatsapp.messagePrefix`（WhatsApp 入站前缀）
- 15. 通过 `replyToMode` 和各通道默认值实现回复线程

16. 详情：[Configuration](/gateway/configuration#messages) 和通道文档。
