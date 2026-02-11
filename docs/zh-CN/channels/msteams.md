---
summary: "Microsoft Teams bot support status, capabilities, and configuration"
read_when:
  - Working on MS Teams channel features
title: "Microsoft Teams"
---

# Microsoft Teams (plugin)

> 39. “进入此地者，放弃一切希望。”

Updated: 2026-01-21

Status: text + DM attachments are supported; channel/group file sending requires `sharePointSiteId` + Graph permissions (see [Sending files in group chats](#sending-files-in-group-chats)). Polls are sent via Adaptive Cards.

## Plugin required

Microsoft Teams ships as a plugin and is not bundled with the core install.

**Breaking change (2026.1.15):** MS Teams moved out of core. If you use it, you must install the plugin.

Explainable: keeps core installs lighter and lets MS Teams dependencies update independently.

Install via CLI (npm registry):

```bash
openclaw plugins install @openclaw/msteams
```

Local checkout (when running from a git repo):

```bash
openclaw plugins install ./extensions/msteams
```

If you choose Teams during configure/onboarding and a git checkout is detected,
OpenClaw will offer the local install path automatically.

40. 详情：[Plugins](/tools/plugin)

## 快速设置（新手）

1. 41. 安装 Microsoft Teams 插件。
2. 创建一个 **Azure Bot**（App ID + 客户端密钥 + 租户 ID）。
3. 使用这些凭据配置 OpenClaw。
4. 通过公共 URL 或隧道暴露 `/api/messages`（默认端口 3978）。
5. 安装 Teams 应用包并启动网关。

最小配置：

```json5
{
  channels: {
    msteams: {
      enabled: true,
      appId: "<APP_ID>",
      appPassword: "<APP_PASSWORD>",
      tenantId: "<TENANT_ID>",
      webhook: { port: 3978, path: "/api/messages" },
    },
  },
}
```

注意：群聊默认被阻止（`channels.msteams.groupPolicy: "allowlist"`）。 要允许群聊回复，请设置 `channels.msteams.groupAllowFrom`（或使用 `groupPolicy: "open"` 以允许任何成员，但需要提及）。

## 42. 目标

- 通过 Teams 私聊、群聊或频道与 OpenClaw 对话。
- 保持路由确定性：回复始终返回到其到达的频道。
- 默认采用安全的频道行为（除非另行配置，否则需要提及）。

## 配置写入

默认情况下，Microsoft Teams 允许写入由 `/config set|unset` 触发的配置更新（需要 `commands.config: true`）。

43. 使用以下方式禁用：

```json5
{
  channels: { msteams: { configWrites: false } },
}
```

## 访问控制（私聊 + 群组）

**私聊访问**

- 默认值：`channels.msteams.dmPolicy = "pairing"`。 未知发送者在获得批准之前会被忽略。
- `channels.msteams.allowFrom` 接受 AAD 对象 ID、UPN 或显示名称。 当凭据允许时，向导会通过 Microsoft Graph 将名称解析为 ID。

**群组访问**

- 默认值：`channels.msteams.groupPolicy = "allowlist"`（除非添加 `groupAllowFrom`，否则会被阻止）。 44. 当未设置时，使用 `channels.defaults.groupPolicy` 覆盖默认值。
- `channels.msteams.groupAllowFrom` 控制哪些发送者可以在群聊/频道中触发（回退到 `channels.msteams.allowFrom`）。
- 设置 `groupPolicy: "open"` 以允许任何成员（默认仍需要提及）。
- 45. 若要**不允许任何频道**，请设置 `channels.msteams.groupPolicy: "disabled"`。

示例：

```json5
{
  channels: {
    msteams: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["user@org.com"],
    },
  },
}
```

**Teams + 频道允许列表**

- 通过在 `channels.msteams.teams` 下列出团队和频道来限定群组/频道回复范围。
- 键可以是团队 ID 或名称；频道键可以是会话 ID 或名称。
- 当 `groupPolicy="allowlist"` 且存在团队允许列表时，只接受列出的团队/频道（需要提及）。
- 配置向导接受 `Team/Channel` 条目并为你存储它们。
- 启动时，OpenClaw 会将团队/频道和用户允许列表中的名称解析为 ID（当 Graph 权限允许时）
  并记录映射；无法解析的条目会按原样保留。

示例：

```json5
{
  channels: {
    msteams: {
      groupPolicy: "allowlist",
      teams: {
        "My Team": {
          channels: {
            General: { requireMention: true },
          },
        },
      },
    },
  },
}
```

## 工作原理

1. 安装 Microsoft Teams 插件。
2. 创建一个 **Azure Bot**（App ID + 密钥 + 租户 ID）。
3. 构建一个 **Teams 应用包**，引用该机器人并包含以下 RSC 权限。
4. 将 Teams 应用上传/安装到某个团队（或用于私聊的个人范围）。
5. 在 `~/.openclaw/openclaw.json`（或环境变量）中配置 `msteams` 并启动网关。
6. 网关默认在 `/api/messages` 上监听 Bot Framework 的 webhook 流量。

## Azure Bot 设置（先决条件）

在配置 OpenClaw 之前，你需要创建一个 Azure Bot 资源。

### 1. 第 1 步：创建 Azure Bot

1. 2. 前往 [创建 Azure Bot](https://portal.azure.com/#create/Microsoft.AzureBot)
2. 3. 填写 **Basics** 选项卡：

   | 4. 字段                  | 5. 值                                   |
   | --------------------------------------------- | ------------------------------------------------------------- |
   | 6. **Bot handle**      | 7. 你的机器人名称，例如 `openclaw-msteams`（必须唯一） |
   | 8. **Subscription**    | 9. 选择你的 Azure 订阅                       |
   | 10. **Resource group** | 11. 创建新的或使用现有的                         |
   | 12. **Pricing tier**   | 13. 开发/测试使用 **Free**                   |
   | 14. **Type of App**    | 15. **Single Tenant**（推荐——见下方说明）       |
   | 16. **Creation type**  | 17. **Create new Microsoft App ID**    |

> 18) **弃用通知：** 自 2025-07-31 之后，已弃用创建新的多租户机器人。 19. 新机器人请使用 **Single Tenant**。

3. 20. 点击 **Review + create** → **Create**（等待约 1-2 分钟）

### 21) 第 2 步：获取凭据

1. 22. 前往你的 Azure Bot 资源 → **Configuration**
2. 23. 复制 **Microsoft App ID** → 这就是你的 `appId`
3. 24. 点击 **Manage Password** → 前往应用注册（App Registration）
4. 25. 在 **Certificates & secrets** 下 → **New client secret** → 复制 **Value** → 这就是你的 `appPassword`
5. 26. 前往 **Overview** → 复制 **Directory (tenant) ID** → 这就是你的 `tenantId`

### 27) 第 3 步：配置消息终结点

1. 28. 在 Azure Bot → **Configuration**
2. 29. 将 **Messaging endpoint** 设置为你的 webhook URL：
   - 30. 生产环境：`https://your-domain.com/api/messages`
   - 31. 本地开发：使用隧道（见下方 [本地开发](#local-development-tunneling)）

### 32) 第 4 步：启用 Teams 渠道

1. 33. 在 Azure Bot → **Channels**
2. 34. 点击 **Microsoft Teams** → Configure → Save
3. 35. 接受服务条款

## 36) 本地开发（隧道）

37. Teams 无法访问 `localhost`。 38. 本地开发请使用隧道：

39. **选项 A：ngrok**

```bash
40. ngrok http 3978
```

# 复制 https URL，例如 https://abc123.ngrok.io

```bash
# 将消息终结点设置为：https://abc123.ngrok.io/api/messages
```

## 41. **选项 B：Tailscale Funnel**

42. tailscale funnel 3978

1. # 使用你的 Tailscale funnel URL 作为消息终结点
2. 43. Teams 开发者门户（替代方案）
3. 44. 你也可以使用 [Teams 开发者门户](https://dev.teams.microsoft.com/apps) 而不是手动创建清单 ZIP：
4. 45. 点击 **+ New app**
5. 46. 填写基本信息（名称、描述、开发者信息）
6. 47. 前往 **App features** → **Bot**
7. 1. 在 Teams 中：**应用** → **管理你的应用** → **上传自定义应用** → 选择 ZIP

2) 这通常比手动编辑 JSON 清单更简单。

## 46. 测试机器人

4. **选项 A：Azure Web Chat（先验证 webhook）**

1. 5. 在 Azure 门户 → 你的 Azure Bot 资源 → **在 Web Chat 中测试**
2. 6. 发送一条消息——你应该能看到响应
3. 7. 这可在进行 Teams 设置之前确认你的 webhook 端点可用

8) **选项 B：Teams（应用安装后）**

1. 9. 安装 Teams 应用（旁加载或组织应用目录）
2. 10. 在 Teams 中找到该 Bot 并发送一条私信
3. 11. 检查网关日志以查看传入的活动

## 12) 设置（最小化，仅文本）

1. 13. **安装 Microsoft Teams 插件**
   - 14. 通过 npm：`openclaw plugins install @openclaw/msteams`
   - 15. 从本地检出：`openclaw plugins install ./extensions/msteams`

2. 16. **Bot 注册**
   - 17. 创建一个 Azure Bot（见上文）并记录：
     - 18. 应用 ID
     - 19. 客户端密钥（应用密码）
     - 20. 租户 ID（单租户）

3. 21. **Teams 应用清单**
   - 22. 包含一个 `bot` 条目，并设置 `botId = <App ID>`。
   - 23. 作用域：`personal`、`team`、`groupChat`。
   - 24. `supportsFiles: true`（个人作用域文件处理所必需）。
   - 25. 添加 RSC 权限（如下）。
   - 26. 创建图标：`outline.png`（32x32）和 `color.png`（192x192）。
   - 27. 将这三个文件一起打包为 zip：`manifest.json`、`outline.png`、`color.png`。

4. 28. **配置 OpenClaw**

   ```json
   {
     "msteams": {
       "enabled": true,
       "appId": "<APP_ID>",
       "appPassword": "<APP_PASSWORD>",
       "tenantId": "<TENANT_ID>",
       "webhook": { "port": 3978, "path": "/api/messages" }
     }
   }
   ```

   30. 你也可以使用环境变量代替配置键：

   - 31. `MSTEAMS_APP_ID`
   - 32. `MSTEAMS_APP_PASSWORD`
   - 33. `MSTEAMS_TENANT_ID`

5. 34. **Bot 端点**
   - 35. 将 Azure Bot 消息传递端点设置为：
     - 36. `https://<host>:3978/api/messages`（或你选择的路径/端口）。

6. 37. **运行网关**
   - 38. 当插件安装且存在包含凭据的 `msteams` 配置时，Teams 通道会自动启动。

## 39) 历史上下文

- 40. `channels.msteams.historyLimit` 控制在提示中包含多少最近的频道/群聊消息。
- 41. 若未设置，则回退到 `messages.groupChat.historyLimit`。 42. 设置为 `0` 可禁用（默认 50）。
- 43. 可通过 `channels.msteams.dmHistoryLimit`（按用户轮次）限制私信历史。 44. 按用户覆盖：`channels.msteams.dms["<user_id>"].historyLimit`。

## 45. 当前 Teams RSC 权限（清单）

46. 这些是我们 Teams 应用清单中**现有的 resourceSpecific 权限**。 47. 它们仅适用于安装了该应用的团队/聊天内部。

48. **用于频道（团队作用域）：**

- 49. `ChannelMessage.Read.Group`（应用）- 无需 @ 提及即可接收所有频道消息
- 50. `ChannelMessage.Send.Group`（应用）
- `Member.Read.Group`（应用）
- `Owner.Read.Group`（应用）
- `ChannelSettings.Read.Group`（应用）
- `TeamMember.Read.Group`（应用）
- `TeamSettings.Read.Group`（应用）

47. **对于群聊：**

- `ChatMessage.Read.Chat`（应用）- 无需 @提及即可接收所有群聊消息

## 示例 Teams 清单（已脱敏）

包含所需字段的最小且有效示例。 替换 ID 和 URL。

```json
{
  "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.23/MicrosoftTeams.schema.json",
  "manifestVersion": "1.23",
  "version": "1.0.0",
  "id": "00000000-0000-0000-0000-000000000000",
  "name": { "short": "OpenClaw" },
  "developer": {
    "name": "Your Org",
    "websiteUrl": "https://example.com",
    "privacyUrl": "https://example.com/privacy",
    "termsOfUseUrl": "https://example.com/terms"
  },
  "description": { "short": "OpenClaw in Teams", "full": "OpenClaw in Teams" },
  "icons": { "outline": "outline.png", "color": "color.png" },
  "accentColor": "#5B6DEF",
  "bots": [
    {
      "botId": "11111111-1111-1111-1111-111111111111",
      "scopes": ["personal", "team", "groupChat"],
      "isNotificationOnly": false,
      "supportsCalling": false,
      "supportsVideo": false,
      "supportsFiles": true
    }
  ],
  "webApplicationInfo": {
    "id": "11111111-1111-1111-1111-111111111111"
  },
  "authorization": {
    "permissions": {
      "resourceSpecific": [
        { "name": "ChannelMessage.Read.Group", "type": "Application" },
        { "name": "ChannelMessage.Send.Group", "type": "Application" },
        { "name": "Member.Read.Group", "type": "Application" },
        { "name": "Owner.Read.Group", "type": "Application" },
        { "name": "ChannelSettings.Read.Group", "type": "Application" },
        { "name": "TeamMember.Read.Group", "type": "Application" },
        { "name": "TeamSettings.Read.Group", "type": "Application" },
        { "name": "ChatMessage.Read.Chat", "type": "Application" }
      ]
    }
  }
}
```

### 清单注意事项（必填字段）

- `bots[].botId` **必须** 与 Azure Bot App ID 一致。
- `webApplicationInfo.id` **必须** 与 Azure Bot App ID 一致。
- `bots[].scopes` 必须包含你计划使用的界面（`personal`、`team`、`groupChat`）。
- `bots[].supportsFiles: true` 是在个人作用域中进行文件处理的必需项。
- `authorization.permissions.resourceSpecific` 若需要频道流量，必须包含频道读取/发送权限。

### 更新现有应用

要更新已安装的 Teams 应用（例如添加 RSC 权限）：

1. 使用新设置更新你的 `manifest.json`
2. **递增 `version` 字段**（例如 `1.0.0` → `1.1.0`）
3. **重新打包 zip**，包含图标（`manifest.json`、`outline.png`、`color.png`）
4. 上传新的 zip：
   - **选项 A（Teams 管理中心）：** Teams 管理中心 → Teams 应用 → 管理应用 → 找到你的应用 → 上传新版本
   - **选项 B（旁加载）：** 在 Teams → 应用 → 管理你的应用 → 上传自定义应用
5. **用于团队频道：** 在每个团队中重新安装应用以使新权限生效
6. **完全退出并重新启动 Teams**（不只是关闭窗口）以清除缓存的应用元数据

## 功能：仅 RSC vs Graph

### 仅使用 **Teams RSC**（应用已安装，无 Graph API 权限）

可用：

- 读取频道消息**文本**内容。
- 发送频道消息**文本**内容。
- 接收\*\*个人（DM）\*\*文件附件。

不可用：

- 48. 频道/群组的**图片或文件内容**（负载仅包含 HTML 占位）。
- 下载存储在 SharePoint/OneDrive 中的附件。
- 读取消息历史（超出实时 webhook 事件）。

### 使用 **Teams RSC + Microsoft Graph 应用权限**

新增：

- 下载托管内容（粘贴到消息中的图片）。
- 下载存储在 SharePoint/OneDrive 中的文件附件。
- 通过 Graph 读取频道/聊天消息历史。

### RSC vs Graph API

| 能力                   | RSC 权限                                  | Graph API                              |
| -------------------- | --------------------------------------- | -------------------------------------- |
| **实时消息**             | 是（通过 webhook）                           | 否（仅轮询）                                 |
| **历史消息**             | No                                      | 49. 是（可以查询历史记录） |
| **Setup complexity** | App manifest only                       | Requires admin consent + token flow    |
| **Works offline**    | No (must be running) | Yes (query anytime) |

**Bottom line:** RSC is for real-time listening; Graph API is for historical access. For catching up on missed messages while offline, you need Graph API with `ChannelMessage.Read.All` (requires admin consent).

## Graph-enabled media + history (required for channels)

If you need images/files in **channels** or want to fetch **message history**, you must enable Microsoft Graph permissions and grant admin consent.

1. 50. 在 Entra ID（Azure AD）的**应用注册**中，添加 Microsoft Graph 的**应用程序权限**：
   - `ChannelMessage.Read.All` (channel attachments + history)
   - `Chat.Read.All` or `ChatMessage.Read.All` (group chats)
2. **Grant admin consent** for the tenant.
3. Bump the Teams app **manifest version**, re-upload, and **reinstall the app in Teams**.
4. **Fully quit and relaunch Teams** to clear cached app metadata.

## Known Limitations

### Webhook timeouts

Teams delivers messages via HTTP webhook. If processing takes too long (e.g., slow LLM responses), you may see:

- Gateway timeouts
- Teams retrying the message (causing duplicates)
- Dropped replies

OpenClaw handles this by returning quickly and sending replies proactively, but very slow responses may still cause issues.

### Formatting

Teams markdown is more limited than Slack or Discord:

- Basic formatting works: **bold**, _italic_, `code`, links
- Complex markdown (tables, nested lists) may not render correctly
- Adaptive Cards are supported for polls and arbitrary card sends (see below)

## Configuration

Key settings (see `/gateway/configuration` for shared channel patterns):

- `channels.msteams.enabled`: enable/disable the channel.
- `channels.msteams.appId`, `channels.msteams.appPassword`, `channels.msteams.tenantId`: bot credentials.
- `channels.msteams.webhook.port` (default `3978`)
- `channels.msteams.webhook.path` (default `/api/messages`)
- `channels.msteams.dmPolicy`: `pairing | allowlist | open | disabled` (default: pairing)
- `channels.msteams.allowFrom`: allowlist for DMs (AAD object IDs, UPNs, or display names). The wizard resolves names to IDs during setup when Graph access is available.
- `channels.msteams.textChunkLimit`: outbound text chunk size.
- `channels.msteams.chunkMode`: `length` (default) or `newline` to split on blank lines (paragraph boundaries) before length chunking.
- `channels.msteams.mediaAllowHosts`: allowlist for inbound attachment hosts (defaults to Microsoft/Teams domains).
- `channels.msteams.mediaAuthAllowHosts`: allowlist for attaching Authorization headers on media retries (defaults to Graph + Bot Framework hosts).
- `channels.msteams.requireMention`: require @mention in channels/groups (default true).
- `channels.msteams.replyStyle`: `thread | top-level` (see [Reply Style](#reply-style-threads-vs-posts)).
- `channels.msteams.teams.<teamId>.replyStyle`: per-team override.
- `channels.msteams.teams.<teamId>.requireMention`: per-team override.
- `channels.msteams.teams.<teamId>.tools`: default per-team tool policy overrides (`allow`/`deny`/`alsoAllow`) used when a channel override is missing.
- `channels.msteams.teams.<teamId>.toolsBySender`: default per-team per-sender tool policy overrides (`"*"` wildcard supported).
- `channels.msteams.teams.<teamId>.channels.<conversationId>.replyStyle`: per-channel override.
- `channels.msteams.teams.<teamId>.channels.<conversationId>.requireMention`: per-channel override.
- `channels.msteams.teams.<teamId>.channels.<conversationId>.tools`: per-channel tool policy overrides (`allow`/`deny`/`alsoAllow`).
- `channels.msteams.teams.<teamId>.channels.<conversationId>.toolsBySender`: per-channel per-sender tool policy overrides (`"*"` wildcard supported).
- `channels.msteams.sharePointSiteId`: SharePoint site ID for file uploads in group chats/channels (see [Sending files in group chats](#sending-files-in-group-chats)).

## Routing & Sessions

- Session keys follow the standard agent format (see [/concepts/session](/concepts/session)):
  - Direct messages share the main session (`agent:<agentId>:<mainKey>`).
  - Channel/group messages use conversation id:
    - `agent:<agentId>:msteams:channel:<conversationId>`
    - `agent:<agentId>:msteams:group:<conversationId>`

## Reply Style: Threads vs Posts

Teams recently introduced two channel UI styles over the same underlying data model:

| Style                                       | Description                                               | Recommended `replyStyle`              |
| ------------------------------------------- | --------------------------------------------------------- | ------------------------------------- |
| **Posts** (classic)      | Messages appear as cards with threaded replies underneath | `thread` (default) |
| **Threads** (Slack-like) | Messages flow linearly, more like Slack                   | `top-level`                           |

**The problem:** The Teams API does not expose which UI style a channel uses. If you use the wrong `replyStyle`:

- `thread` in a Threads-style channel → replies appear nested awkwardly
- `top-level` in a Posts-style channel → replies appear as separate top-level posts instead of in-thread

**Solution:** Configure `replyStyle` per-channel based on how the channel is set up:

```json
{
  "msteams": {
    "replyStyle": "thread",
    "teams": {
      "19:abc...@thread.tacv2": {
        "channels": {
          "19:xyz...@thread.tacv2": {
            "replyStyle": "top-level"
          }
        }
      }
    }
  }
}
```

## Attachments & Images

**Current limitations:**

- **DMs:** Images and file attachments work via Teams bot file APIs.
- **Channels/groups:** Attachments live in M365 storage (SharePoint/OneDrive). The webhook payload only includes an HTML stub, not the actual file bytes. **Graph API permissions are required** to download channel attachments.

Without Graph permissions, channel messages with images will be received as text-only (the image content is not accessible to the bot).
By default, OpenClaw only downloads media from Microsoft/Teams hostnames. Override with `channels.msteams.mediaAllowHosts` (use `["*"]` to allow any host).
Authorization headers are only attached for hosts in `channels.msteams.mediaAuthAllowHosts` (defaults to Graph + Bot Framework hosts). 保持此列表严格（避免多租户后缀）。

## 在群聊中发送文件

机器人可以在私聊（DM）中使用 FileConsentCard 流程（内置）发送文件。 但是，**在群聊/频道中发送文件** 需要额外配置：

| 背景            | How files are sent             | Setup needed                     |
| ------------- | ------------------------------ | -------------------------------- |
| **私聊（DMs）**   | FileConsentCard → 用户接受 → 机器人上传 | 开箱即用                             |
| **群聊/频道**     | 上传到 SharePoint → 分享链接          | 需要 `sharePointSiteId` + Graph 权限 |
| **图片（任何上下文）** | Base64 编码内联                    | 开箱即用                             |

### 为什么群聊需要 SharePoint

Bots don't have a personal OneDrive drive (the `/me/drive` Graph API endpoint doesn't work for application identities). 要在群聊/频道中发送文件，机器人会上传到 **SharePoint 站点** 并创建共享链接。

### 配置

1. 在 Entra ID（Azure AD）→ 应用注册 中 **添加 Graph API 权限**：
   - `Sites.ReadWrite.All`（应用）- 上传文件到 SharePoint
   - `Chat.Read.All`（应用）- 可选，用于启用按用户的共享链接

2. **Grant admin consent** for the tenant.

3. **获取你的 SharePoint 站点 ID：**

   ```bash
   # 通过 Graph Explorer 或使用有效令牌的 curl：
   curl -H "Authorization: Bearer $TOKEN" \
     "https://graph.microsoft.com/v1.0/sites/{hostname}:/{site-path}"

   # 示例：站点位于 "contoso.sharepoint.com/sites/BotFiles"
   curl -H "Authorization: Bearer $TOKEN" \
     "https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/BotFiles"

   # 响应包含："id": "contoso.sharepoint.com,guid1,guid2"
   ```

4. **配置 OpenClaw：**

   ```json5
   {
     channels: {
       msteams: {
         // ... other config ...
         sharePointSiteId: "contoso.sharepoint.com,guid1,guid2",
       },
     },
   }
   ```

### Sharing behavior

| 权限                                      | 共享行为                 |
| --------------------------------------- | -------------------- |
| 仅 `Sites.ReadWrite.All`                 | 组织范围共享链接（组织内任何人都可访问） |
| `Sites.ReadWrite.All` + `Chat.Read.All` | 按用户共享链接（仅聊天成员可访问）    |

按用户共享更安全，因为只有聊天参与者才能访问该文件。 如果缺少 `Chat.Read.All` 权限，机器人将回退到组织范围共享。

### 回退行为

| 场景                               | 结果                                     |
| -------------------------------- | -------------------------------------- |
| 群聊 + 文件 + 已配置 `sharePointSiteId` | 上传到 SharePoint，发送共享链接                  |
| 群聊 + 文件 + 未配置 `sharePointSiteId` | 尝试 OneDrive 上传（可能失败），仅发送文本             |
| 个人聊天 + 文件                        | FileConsentCard 流程（无需 SharePoint 也可使用） |
| 任何上下文 + 图片                       | Base64 编码内联（无需 SharePoint 也可使用）        |

### 文件存储位置

上传的文件存储在已配置 SharePoint 站点的默认文档库中的 `/OpenClawShared/` 文件夹内。

## Polls (Adaptive Cards)

2. OpenClaw 通过 Adaptive Cards 发送 Teams 投票（Teams 没有原生投票 API）。

- 3. CLI：`openclaw message poll --channel msteams --target conversation:<id> ...`
- 4. 投票由网关记录在 `~/.openclaw/msteams-polls.json` 中。
- 5. 网关必须保持在线才能记录投票。
- 6. 投票目前不会自动发布结果摘要（如有需要请检查存储文件）。

## 7. Adaptive Cards（任意）

8. 使用 `message` 工具或 CLI 将任意 Adaptive Card JSON 发送给 Teams 用户或会话。

9. `card` 参数接受一个 Adaptive Card JSON 对象。 10. 提供 `card` 时，消息文本是可选的。

11. **Agent 工具：**

```json
12. {
  "action": "send",
  "channel": "msteams",
  "target": "user:<id>",
  "card": {
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [{ "type": "TextBlock", "text": "Hello!" }]
  }
}
```

13. **CLI：**

```bash
14. openclaw message send --channel msteams \
  --target "conversation:19:abc...@thread.tacv2" \
  --card '{"type":"AdaptiveCard","version":"1.5","body":[{"type":"TextBlock","text":"Hello!"}]}'
```

See [Adaptive Cards documentation](https://adaptivecards.io/) for card schema and examples. 16. 有关目标格式的详细信息，请参阅下面的 [Target formats](#target-formats)。

## 17. 目标格式

18. MSTeams 目标使用前缀来区分用户和会话：

| 19. 目标类型      | 20. 格式                               | 21. 示例                                          |
| ------------------------------------ | ----------------------------------------------------------- | ---------------------------------------------------------------------- |
| 22. 用户（按 ID）  | 23. `user:<aad-object-id>`           | 24. `user:40a1a0ed-4ff2-4164-a219-55518990c197` |
| 25. 用户（按名称）   | `user:<display-name>`                                       | 27. `user:John Smith`（需要 Graph API）             |
| Group/channel                        | 29. `conversation:<conversation-id>` | 30. `conversation:19:abc123...@thread.tacv2`    |
| 31. 群组/频道（原始） | 32. `<conversation-id>`              | `19:abc123...@thread.tacv2` (if contains `@thread`) |

34. **CLI 示例：**

```bash
35. # 通过 ID 发送给用户
openclaw message send --channel msteams --target "user:40a1a0ed-..." --message "Hello"

# 通过显示名称发送给用户（触发 Graph API 查询）
openclaw message send --channel msteams --target "user:John Smith" --message "Hello"

# 发送到群聊或频道
openclaw message send --channel msteams --target "conversation:19:abc...@thread.tacv2" --message "Hello"

# 向会话发送 Adaptive Card
openclaw message send --channel msteams --target "conversation:19:abc...@thread.tacv2" \
  --card '{"type":"AdaptiveCard","version":"1.5","body":[{"type":"TextBlock","text":"Hello"}]}'
```

36. **Agent 工具示例：**

```json
37. {
  "action": "send",
  "channel": "msteams",
  "target": "user:John Smith",
  "message": "Hello!"
}
```

```json
38. {
  "action": "send",
  "channel": "msteams",
  "target": "conversation:19:abc...@thread.tacv2",
  "card": {
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [{ "type": "TextBlock", "text": "Hello" }]
  }
}
```

39. 注意：如果没有 `user:` 前缀，名称默认解析为群组/团队。 40. 通过显示名称定位人员时，始终使用 `user:`。

## 41. 主动消息

- 42. 只有在用户**之后**与系统交互过，才可以发送主动消息，因为我们会在那时存储会话引用。
- 43. 有关 `dmPolicy` 和允许列表控制，请参阅 `/gateway/configuration`。

## 44. 团队和频道 ID（常见陷阱）

45. Teams URL 中的 `groupId` 查询参数**不是**用于配置的团队 ID。 46. 请改为从 URL 路径中提取 ID：

47. **团队 URL：**

```
48. https://teams.microsoft.com/l/team/19%3ABk4j...%40thread.tacv2/conversations?groupId=...
                                    └────────────────────────────┘
                                    团队 ID（对其进行 URL 解码）
```

49. **频道 URL：**

```
50. https://teams.microsoft.com/l/channel/19%3A15bc...%40thread.tacv2/ChannelName?groupId=...
                                      └─────────────────────────┘
                                      频道 ID（对其进行 URL 解码）
```

**For config:**

- Team ID = path segment after `/team/` (URL-decoded, e.g., `19:Bk4j...@thread.tacv2`)
- Channel ID = path segment after `/channel/` (URL-decoded)
- **Ignore** the `groupId` query parameter

## Private Channels

Bots have limited support in private channels:

| Feature                                         | Standard Channels | Private Channels                          |
| ----------------------------------------------- | ----------------- | ----------------------------------------- |
| Bot installation                                | Yes               | Limited                                   |
| Real-time messages (webhook) | Yes               | May not work                              |
| RSC permissions                                 | Yes               | May behave differently                    |
| @mentions                          | Yes               | If bot is accessible                      |
| Graph API history                               | Yes               | Yes (with permissions) |

**Workarounds if private channels don't work:**

1. Use standard channels for bot interactions
2. Use DMs - users can always message the bot directly
3. Use Graph API for historical access (requires `ChannelMessage.Read.All`)

## Troubleshooting

### Common issues

- **Images not showing in channels:** Graph permissions or admin consent missing. Reinstall the Teams app and fully quit/reopen Teams.
- **No responses in channel:** mentions are required by default; set `channels.msteams.requireMention=false` or configure per team/channel.
- **Version mismatch (Teams still shows old manifest):** remove + re-add the app and fully quit Teams to refresh.
- **401 Unauthorized from webhook:** Expected when testing manually without Azure JWT - means endpoint is reachable but auth failed. Use Azure Web Chat to test properly.

### Manifest upload errors

- **"Icon file cannot be empty":** The manifest references icon files that are 0 bytes. Create valid PNG icons (32x32 for `outline.png`, 192x192 for `color.png`).
- **"webApplicationInfo.Id already in use":** The app is still installed in another team/chat. Find and uninstall it first, or wait 5-10 minutes for propagation.
- **"Something went wrong" on upload:** Upload via [https://admin.teams.microsoft.com](https://admin.teams.microsoft.com) instead, open browser DevTools (F12) → Network tab, and check the response body for the actual error.
- **Sideload failing:** Try "Upload an app to your org's app catalog" instead of "Upload a custom app" - this often bypasses sideload restrictions.

### RSC permissions not working

1. Verify `webApplicationInfo.id` matches your bot's App ID exactly
2. Re-upload the app and reinstall in the team/chat
3. Check if your org admin has blocked RSC permissions
4. Confirm you're using the right scope: `ChannelMessage.Read.Group` for teams, `ChatMessage.Read.Chat` for group chats

## References

- [Create Azure Bot](https://learn.microsoft.com/en-us/azure/bot-service/bot-service-quickstart-registration) - Azure Bot setup guide
- [Teams Developer Portal](https://dev.teams.microsoft.com/apps) - create/manage Teams apps
- [Teams app manifest schema](https://learn.microsoft.com/en-us/microsoftteams/platform/resources/schema/manifest-schema)
- [Receive channel messages with RSC](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/conversations/channel-messages-with-rsc)
- [RSC permissions reference](https://learn.microsoft.com/en-us/microsoftteams/platform/graph-api/rsc/resource-specific-consent)
- [Teams bot file handling](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/bots-filesv4) (channel/group requires Graph)
- [Proactive messaging](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/conversations/send-proactive-messages)
