---
summary: "Group chat behavior across surfaces (WhatsApp/Telegram/Discord/Slack/Signal/iMessage/Microsoft Teams)"
read_when:
  - Changing group chat behavior or mention gating
title: "Groups"
---

# Groups

OpenClaw treats group chats consistently across surfaces: WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Microsoft Teams.

## Beginner intro (2 minutes)

OpenClaw “lives” on your own messaging accounts. There is no separate WhatsApp bot user.
If **you** are in a group, OpenClaw can see that group and respond there.

Default behavior:

- Groups are restricted (`groupPolicy: "allowlist"`).
- Replies require a mention unless you explicitly disable mention gating.

Translation: allowlisted senders can trigger OpenClaw by mentioning it.

> TL;DR
>
> - **DM access** is controlled by `*.allowFrom`.
> - **Group access** is controlled by `*.groupPolicy` + allowlists (`*.groups`, `*.groupAllowFrom`).
> - **Reply triggering** is controlled by mention gating (`requireMention`, `/activation`).

Quick flow (what happens to a group message):

```
groupPolicy? disabled -> drop
groupPolicy? allowlist -> group allowed? no -> drop
requireMention? yes -> mentioned? no -> store for context only
otherwise -> reply
```

![Group message flow](/images/groups-flow.svg)

If you want...

| Goal                                                      | What to set                                                |
| --------------------------------------------------------- | ---------------------------------------------------------- |
| Allow all groups but only reply on @mentions | `groups: { "*": { requireMention: true } }`                |
| Disable all group replies                                 | `groupPolicy: "disabled"`                                  |
| Only specific groups                                      | `groups: { "<group-id>": { ... } }`（没有 `"*"` 键）            |
| 只有你可以在群组中触发                                               | `groupPolicy: "allowlist"`, `groupAllowFrom: ["+1555..."]` |

## 会话键

- 群组会话使用 `agent:<agentId>:<channel>:group:<id>` 会话键（房间/频道使用 `agent:<agentId>:<channel>:channel:<id>`）。
- Telegram 论坛主题会在群组 ID 中添加 `:topic:<threadId>`，因此每个主题都有自己的会话。
- 私聊使用主会话（或如果已配置，则按发送者区分）。
- 群组会话会跳过心跳。

## 模式：个人私聊 + 公共群组（单一代理）

是的——如果你的“个人”流量是 **私聊（DMs）**，而你的“公共”流量是 **群组**，这种方式效果很好。

原因：在单代理模式下，私聊通常落在 **主** 会话键（`agent:main:main`）中，而群组始终使用 **非主** 会话键（`agent:main:<channel>:group:<id>`）。 如果你启用 `mode: "non-main"` 的沙箱，这些群组会话将在 Docker 中运行，而你的主私聊会话仍然在宿主机上运行。

这样你就拥有一个代理“大脑”（共享工作区 + 记忆），但有两种执行姿态：

- **DMs**: full tools (host)
- **群组**：沙箱 + 受限工具（Docker）

> 如果你需要真正分离的工作区/人格（“个人”和“公共”绝不能混合），请使用第二个代理 + 绑定。 参见 [多代理路由](/concepts/multi-agent)。

示例（私聊在宿主机，群组沙箱化 + 仅消息工具）：

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // 群组/频道是 non-main -> 沙箱化
        scope: "session", // 最强隔离（每个群组/频道一个容器）
        workspaceAccess: "none",
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        // 如果 allow 非空，其它全部被阻止（deny 仍然优先生效）。
        allow: ["group:messaging", "group:sessions"],
        deny: ["group:runtime", "group:fs", "group:ui", "nodes", "cron", "gateway"],
      },
    },
  },
}
```

想要“群组只能看到文件夹 X”而不是“没有宿主机访问权限”？ 保持 `workspaceAccess: "none"`，并只将允许列表中的路径挂载到沙箱中：

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "none",
        docker: {
          binds: [
            // hostPath:containerPath:mode
            "~/FriendsShared:/data:ro",
          ],
        },
      },
    },
  },
}
```

相关：

- 配置键和值的默认值：[Gateway 配置](/gateway/configuration#agentsdefaultssandbox)
- 调试工具为何被阻止：[Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated)
- 1. 绑定挂载详情：[Sandboxing](/gateway/sandboxing#custom-bind-mounts)

## 显示标签

- UI 标签在可用时使用 `displayName`，格式为 `<channel>:<token>`。
- `#room` 保留用于房间/频道；群组聊天使用 `g-<slug>`（小写，空格 -> `-`，保留 `#@+._-`）。

## 群组策略

按渠道控制群组/房间消息的处理方式：

```json5
{
  channels: {
    whatsapp: {
      groupPolicy: "disabled", // "open" | "disabled" | "allowlist"
      groupAllowFrom: ["+15551234567"],
    },
    telegram: {
      groupPolicy: "disabled",
      groupAllowFrom: ["123456789", "@username"],
    },
    signal: {
      groupPolicy: "disabled",
      groupAllowFrom: ["+15551234567"],
    },
    imessage: {
      groupPolicy: "disabled",
      groupAllowFrom: ["chat_id:123"],
    },
    msteams: {
      groupPolicy: "disabled",
      groupAllowFrom: ["user@org.com"],
    },
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        GUILD_ID: { channels: { help: { allow: true } } },
      },
    },
    slack: {
      groupPolicy: "allowlist",
      channels: { "#general": { allow: true } },
    },
    matrix: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["@owner:example.org"],
      groups: {
        "!roomId:example.org": { allow: true },
        "#alias:example.org": { allow: true },
      },
    },
  },
}
```

| 策略            | 行为                   |
| ------------- | -------------------- |
| `"open"`      | 群组会绕过允许列表；提及门控仍然适用。  |
| `"disabled"`  | 完全阻止所有群组消息。          |
| `"allowlist"` | 只允许与配置的允许列表匹配的群组/房间。 |

注意：

- `groupPolicy` 与提及门控是分离的（提及门控需要 @ 提及）。
- WhatsApp/Telegram/Signal/iMessage/Microsoft Teams：使用 `groupAllowFrom`（回退：显式的 `allowFrom`）。
- Discord：允许列表使用 `channels.discord.guilds.<id>``.channels`。
- Slack：允许列表使用 `channels.slack.channels`。
- Matrix：允许列表使用 `channels.matrix.groups`（房间 ID、别名或名称）。 使用 `channels.matrix.groupAllowFrom` 来限制发送者；也支持按房间的 `users` 允许列表。
- 群组私聊单独控制（`channels.discord.dm.*`、`channels.slack.dm.*`）。
- Telegram 允许列表可以匹配用户 ID（`"123456789"`、`"telegram:123456789"`、`"tg:123456789"`）或用户名（`"@alice"` 或 `"alice"`）；前缀不区分大小写。
- 1. 默认是 `groupPolicy: "allowlist"`；如果你的群组白名单为空，群组消息将被阻止。

2. 快速心智模型（群组消息的评估顺序）：

1. 3. `groupPolicy`（open/disabled/allowlist）
2. 4. 群组白名单（`*.groups`、`*.groupAllowFrom`、按频道的白名单）
3. 5. 提及门控（`requireMention`、`/activation`）

## 6) 提及门控（默认）

7. 群组消息需要被提及，除非按群组单独覆盖。 8. 默认值按子系统存放在 `*.groups."*"` 下。

9. 回复机器人消息视为一次隐式提及（当频道支持回复元数据时）。 10. 适用于 Telegram、WhatsApp、Slack、Discord 和 Microsoft Teams。

```json5
11. {
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true },
        "123@g.us": { requireMention: false },
      },
    },
    telegram: {
      groups: {
        "*": { requireMention: true },
        "123456789": { requireMention: false },
      },
    },
    imessage: {
      groups: {
        "*": { requireMention: true },
        "123": { requireMention: false },
      },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          mentionPatterns: ["@openclaw", "openclaw", "\\+15555550123"],
          historyLimit: 50,
        },
      },
    ],
  },
}
```

12. 备注：

- 13. `mentionPatterns` 是不区分大小写的正则表达式。
- 14. 提供显式提及的界面仍然会通过；这些模式只是兜底。
- 15. 按代理覆盖：`agents.list[].groupChat.mentionPatterns`（当多个代理共享同一个群组时很有用）。
- 16. 只有在可以进行提及检测时才会强制执行提及门控（存在原生提及或已配置 `mentionPatterns`）。
- 17. Discord 的默认值位于 `channels.discord.guilds."*"`（可按公会/频道覆盖）。
- 18. 群组历史上下文在各频道中统一封装，且仅包含**待处理**消息（因提及门控而跳过的消息）；全局默认使用 `messages.groupChat.historyLimit`，覆盖使用 `channels.<channel>`19. `.historyLimit`（或 `channels.<channel>`.accounts.\*.historyLimit`) for overrides. 21. 设置为 `0\` 可禁用。

## 22. 群组/频道工具限制（可选）

23. 某些频道配置支持限制**特定群组/房间/频道内**可用的工具。

- 24. `tools`：为整个群组允许/拒绝工具。
- 25. `toolsBySender`：群组内按发送者的覆盖（键为发送者 ID/用户名/邮箱/电话号码，取决于频道）。 26. 使用 `"*"` 作为通配符。

27. 解析顺序（越具体优先级越高）：

1. 28. 群组/频道 `toolsBySender` 匹配
2. 29. 群组/频道 `tools`
3. 30. 默认（`"*"`）`toolsBySender` 匹配
4. 31. 默认（`"*"`）`tools`

32) 示例（Telegram）：

```json5
33. {
  channels: {
    telegram: {
      groups: {
        "*": { tools: { deny: ["exec"] } },
        "-1001234567890": {
          tools: { deny: ["exec", "read", "write"] },
          toolsBySender: {
            "123456789": { alsoAllow: ["exec"] },
          },
        },
      },
    },
  },
}
```

34. 备注：

- 3. 组/频道工具限制会在全局/代理工具策略之外生效（拒绝仍然优先生效）。
- 36. 某些频道对房间/频道使用不同的嵌套结构（例如 Discord `guilds.*.channels.*`、Slack `channels.*`、MS Teams `teams.*.channels.*`）。

## 37. 群组白名单

38. 当配置了 `channels.whatsapp.groups`、`channels.telegram.groups` 或 `channels.imessage.groups` 时，这些键即作为群组白名单。 39. 使用 `"*"` 以允许所有群组，同时仍可设置默认的提及行为。

40. 常见意图（复制/粘贴）：

1. 4. 禁用所有群组回复

```json5
42. {
  channels: { whatsapp: { groupPolicy: "disabled" } },
}
```

2. 43. 仅允许特定群组（WhatsApp）

```json5
44. {
  channels: {
    whatsapp: {
      groups: {
        "123@g.us": { requireMention: true },
        "456@g.us": { requireMention: false },
      },
    },
  },
}
```

3. 45. 允许所有群组但需要提及（显式）

```json5
46. {
  channels: {
    whatsapp: {
      groups: { "*": { requireMention: true } },
    },
  },
}
```

4. 47. 仅群主可以在群组中触发（WhatsApp）

```json5
48. {
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
      groups: { "*": { requireMention: true } },
    },
  },
}
```

## 49. 激活（仅限群主）

50. 群主可以按群组切换激活状态：

- 1. `/activation mention`
- 2. `/activation always`

3. 所有者由 `channels.whatsapp.allowFrom` 决定（未设置时为机器人的自身 E.164）。 4. 将该命令作为一条独立消息发送。 5. 其他界面目前会忽略 `/activation`。

## 6. 上下文字段

7. 群组入站负载设置：

- 8. `ChatType=group`
- 9. `GroupSubject`（如果已知）
- 10. `GroupMembers`（如果已知）
- 5. `WasMentioned`（提及门控结果）
- 12. Telegram 论坛主题还包含 `MessageThreadId` 和 `IsForum`。

13. 在新群组会话的首轮中，代理系统提示包含群组介绍。 14. 它会提醒模型像人类一样回复，避免 Markdown 表格，并避免输入字面的 `\n` 序列。

## 15. iMessage 细节

- 16. 在路由或加入允许列表时，优先使用 `chat_id:<id>`。
- 17. 列出聊天：`imsg chats --limit 20`。
- 6. 群组回复始终返回到同一个 `chat_id`。

## 7. WhatsApp 细节

20. 有关 WhatsApp 专有行为（历史注入、提及处理细节），请参见 [Group messages](/channels/group-messages)。
