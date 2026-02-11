---
summary: "31. OpenClaw 可连接的消息平台"
read_when:
  - 32. 你想为 OpenClaw 选择一个聊天频道
  - 33. 你需要一个受支持消息平台的快速概览
title: "34. 聊天频道"
---

# 35. 聊天频道

36. OpenClaw 可以在你已经使用的任何聊天应用上与你交流。 37. 每个频道都通过 Gateway 连接。
37. 文本在所有平台都受支持；媒体和表情因频道而异。

## 39. 支持的频道

- 40. [WhatsApp](/channels/whatsapp) — 最受欢迎；使用 Baileys 并需要二维码配对。
- 41. [Telegram](/channels/telegram) — 通过 grammY 使用 Bot API；支持群组。
- 42. [Discord](/channels/discord) — Discord Bot API + Gateway；支持服务器、频道和私聊。
- 43. [Slack](/channels/slack) — Bolt SDK；工作区应用。
- 44. [Feishu](/channels/feishu) — 通过 WebSocket 的飞书/Lark 机器人（插件，需单独安装）。
- 45. [Google Chat](/channels/googlechat) — 通过 HTTP Webhook 的 Google Chat API 应用。
- 46. [Mattermost](/channels/mattermost) — Bot API + WebSocket；频道、群组、私聊（插件，需单独安装）。
- 47. [Signal](/channels/signal) — signal-cli；以隐私为重点。
- 48. [BlueBubbles](/channels/bluebubbles) — **iMessage 推荐**；使用 BlueBubbles macOS 服务器 REST API，提供完整功能支持（编辑、撤回、特效、反应、群管理——在 macOS 26 Tahoe 上编辑目前不可用）。
- 49. [iMessage（旧版）](/channels/imessage) — 通过 imsg CLI 的传统 macOS 集成（已弃用，新部署请使用 BlueBubbles）。
- 50. [Microsoft Teams](/channels/msteams) — Bot Framework；企业级支持（插件，需单独安装）。
- [LINE](/channels/line) — LINE Messaging API bot (plugin, installed separately).
- [Nextcloud Talk](/channels/nextcloud-talk) — Self-hosted chat via Nextcloud Talk (plugin, installed separately).
- [Matrix](/channels/matrix) — Matrix protocol (plugin, installed separately).
- [Nostr](/channels/nostr) — Decentralized DMs via NIP-04 (plugin, installed separately).
- [Tlon](/channels/tlon) — Urbit-based messenger (plugin, installed separately).
- [Twitch](/channels/twitch) — Twitch chat via IRC connection (plugin, installed separately).
- [Zalo](/channels/zalo) — Zalo Bot API; Vietnam's popular messenger (plugin, installed separately).
- [Zalo Personal](/channels/zalouser) — Zalo personal account via QR login (plugin, installed separately).
- [WebChat](/web/webchat) — Gateway WebChat UI over WebSocket.

## Notes

- Channels can run simultaneously; configure multiple and OpenClaw will route per chat.
- Fastest setup is usually **Telegram** (simple bot token). 13. WhatsApp 需要通过二维码配对，并且
  会在磁盘上存储更多状态。
- Group behavior varies by channel; see [Groups](/channels/groups).
- DM pairing and allowlists are enforced for safety; see [Security](/gateway/security).
- Telegram internals: [grammY notes](/channels/grammy).
- Troubleshooting: [Channel troubleshooting](/channels/troubleshooting).
- Model providers are documented separately; see [Model Providers](/providers/models).
