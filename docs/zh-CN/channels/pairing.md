---
summary: "30. 配对概览：批准谁可以给你发私信 + 哪些节点可以加入"
read_when:
  - 31. 设置私信访问控制
  - 32. 配对新的 iOS/Android 节点
  - 33. 审查 OpenClaw 安全态势
title: "34. 配对"
---

# 35. 配对

36. “配对”是 OpenClaw 明确的**所有者批准**步骤。
37. 它用于两个地方：

1. 38. **私信配对**（谁被允许与机器人对话）
2. 39. **节点配对**（哪些设备/节点被允许加入网关网络）

40) 安全上下文：[Security](/gateway/security)

## 41. 1. 私信配对（入站聊天访问）

42. 当频道配置了私信策略 `pairing` 时，未知发送者会收到一个短码，其消息在你批准之前**不会被处理**。

43. 默认私信策略记录在：[Security](/gateway/security)

44. 配对码：

- 45. 8 个字符，大写，不含易混淆字符（`0O1I`）。
- 46. **1 小时后过期**。 47. 机器人仅在创建新的请求时发送配对消息（大约每个发送者每小时一次）。
- 48. 待处理的私信配对请求默认每个频道**最多 3 个**；在有请求过期或被批准之前，额外请求将被忽略。

### 49. 批准发送者

```bash
50. openclaw 配对列表 telegram
openclaw pairing approve telegram <CODE>
```

Supported channels: `telegram`, `whatsapp`, `signal`, `imessage`, `discord`, `slack`.

### Where the state lives

Stored under `~/.openclaw/credentials/`:

- Pending requests: `<channel>-pairing.json`
- Approved allowlist store: `<channel>-allowFrom.json`

Treat these as sensitive (they gate access to your assistant).

## 2. Node device pairing (iOS/Android/macOS/headless nodes)

Nodes connect to the Gateway as **devices** with `role: node`. The Gateway
creates a device pairing request that must be approved.

### Pair via Telegram (recommended for iOS)

If you use the `device-pair` plugin, you can do first-time device pairing entirely from Telegram:

1. In Telegram, message your bot: `/pair`
2. The bot replies with two messages: an instruction message and a separate **setup code** message (easy to copy/paste in Telegram).
3. On your phone, open the OpenClaw iOS app → Settings → Gateway.
4. Paste the setup code and connect.
5. Back in Telegram: `/pair approve`

The setup code is a base64-encoded JSON payload that contains:

- `url`: the Gateway WebSocket URL (`ws://...` or `wss://...`)
- `token`: a short-lived pairing token

Treat the setup code like a password while it is valid.

### Approve a node device

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
```

### Node pairing state storage

Stored under `~/.openclaw/devices/`:

- `pending.json` (short-lived; pending requests expire)
- `paired.json` (paired devices + tokens)

### Notes

- The legacy `node.pair.*` API (CLI: `openclaw nodes pending/approve`) is a
  separate gateway-owned pairing store. WS nodes still require device pairing.

## Related docs

- Security model + prompt injection: [Security](/gateway/security)
- Updating safely (run doctor): [Updating](/install/updating)
- Channel configs:
  - Telegram: [Telegram](/channels/telegram)
  - WhatsApp: [WhatsApp](/channels/whatsapp)
  - Signal: [Signal](/channels/signal)
  - BlueBubbles (iMessage): [BlueBubbles](/channels/bluebubbles)
  - iMessage (legacy): [iMessage](/channels/imessage)
  - Discord: [Discord](/channels/discord)
  - Slack: [Slack](/channels/slack)
