---
summary: "Reaction semantics shared across channels"
read_when:
  - Working on reactions in any channel
title: "Reactions"
---

# Reaction tooling

Shared reaction semantics across channels:

- `emoji` is required when adding a reaction.
- 2. 在支持的平台上，`emoji=""` 会移除机器人的反应。
- 3. 在支持的平台上，`remove: true` 会移除指定的表情（需要 `emoji`）。

4. 频道说明：

- 5. **Discord/Slack**：空的 `emoji` 会移除该消息上机器人的所有反应；`remove: true` 只会移除该表情。
- 6. **Google Chat**：空的 `emoji` 会移除该消息上应用的反应；`remove: true` 只会移除该表情。
- 7. **Telegram**：空的 `emoji` 会移除机器人的反应；`remove: true` 也会移除反应，但工具校验仍要求提供非空的 `emoji`。
- 8. **WhatsApp**：空的 `emoji` 会移除机器人反应；`remove: true` 会映射为空的 emoji（仍然需要提供 `emoji`）。
- 9. **Signal**：当启用 `channels.signal.reactionNotifications` 时，入站反应通知会触发系统事件。
