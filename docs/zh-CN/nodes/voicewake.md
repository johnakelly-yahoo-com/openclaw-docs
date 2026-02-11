---
summary: "31. 全局语音唤醒词（由 Gateway 拥有）以及它们如何在各节点间同步"
read_when:
  - 32. 更改语音唤醒词的行为或默认值
  - 33. 添加需要唤醒词同步的新节点平台
title: "34. 语音唤醒"
---

# 35. 语音唤醒（全局唤醒词）

OpenClaw 将**唤醒词视为一个由 Gateway 拥有的全局列表**。

- 37. **不存在按节点自定义的唤醒词**。
- 38. **任何节点/应用的 UI 都可以编辑**该列表；更改由 Gateway 持久化并广播给所有人。
- 39. 每个设备仍然保留各自的 **语音唤醒 启用/禁用** 开关（本地 UX + 权限各不相同）。

## 40. 存储（Gateway 主机）

41. 唤醒词存储在网关机器上的：

- 42. `~/.openclaw/settings/voicewake.json`

43. 结构：

```json
44. { "triggers": ["openclaw", "claude", "computer"], "updatedAtMs": 1730000000000 }
```

## 45. 协议

### 方法

- 47. `voicewake.get` → `{ triggers: string[] }`
- `voicewake.set` with params `{ triggers: string[] }` → `{ triggers: string[] }`

49. 说明：

- 50. 触发词会被规范化（去除首尾空格，丢弃空值）。 1. 空列表将回退到默认值。
- 2. 为了安全起见会强制执行限制（数量/长度上限）。

### 3. 事件

- 4. `voicewake.changed` 负载 `{ triggers: string[] }`

5. 接收者：

- 6. 所有 WebSocket 客户端（macOS 应用、WebChat 等）。
- 7. 所有已连接的节点（iOS/Android），并且在节点连接时也会作为初始“当前状态”推送。

## 8. 客户端行为

### 9. macOS 应用

- 10. 使用全局列表来控制 `VoiceWakeRuntime` 触发。
- 11. 在 Voice Wake 设置中编辑“Trigger words”会调用 `voicewake.set`，然后依赖广播来保持其他客户端同步。

### 12. iOS 节点

- 13. 使用全局列表进行 `VoiceWakeManager` 触发检测。
- 14. 在设置中编辑 Wake Words 会调用 `voicewake.set`（通过 Gateway WS），同时保持本地唤醒词检测的响应性。

### 15. Android 节点

- 16. 在设置中提供唤醒词编辑器。
- 17. 通过 Gateway WS 调用 `voicewake.set`，以便编辑在各处同步。
