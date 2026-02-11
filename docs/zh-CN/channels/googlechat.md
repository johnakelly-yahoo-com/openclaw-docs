---
summary: "5. Google Chat 应用支持状态、功能与配置"
read_when:
  - 6. 正在开发 Google Chat 渠道功能
title: "7. Google Chat"
---

# 8. Google Chat（Chat API）

9. 状态：已就绪，可通过 Google Chat API Webhook（仅 HTTP）用于私信和空间。

## 10. 快速设置（新手）

1. 11. 创建一个 Google Cloud 项目并启用 **Google Chat API**。
   - 12. 前往：[Google Chat API 凭据](https://console.cloud.google.com/apis/api/chat.googleapis.com/credentials)
   - 13. 如果尚未启用，请启用该 API。
2. 14. 创建一个 **服务账号**：
   - 15. 点击 **创建凭据** > **服务账号**。
   - 16. 名称可随意（例如：`openclaw-chat`）。
   - 17. 权限留空（点击 **继续**）。
   - 18. 访问主体留空（点击 **完成**）。
3. 19. 创建并下载 **JSON 密钥**：
   - 20. 在服务账号列表中，点击你刚创建的账号。
   - 21. 前往 **密钥** 选项卡。
   - 22. 点击 **添加密钥** > **创建新密钥**。
   - 23. 选择 **JSON** 并点击 **创建**。
4. Store the downloaded JSON file on your gateway host (e.g., `~/.openclaw/googlechat-service-account.json`).
5. 25. 在 [Google Cloud Console Chat 配置](https://console.cloud.google.com/apis/api/chat.googleapis.com/hangouts-chat) 中创建一个 Google Chat 应用：
   - Fill in the **Application info**:
     - 27. **应用名称**：（例如：`OpenClaw`）
     - 28. **头像 URL**：（例如：`https://openclaw.ai/logo.png`）
     - 29. **描述**：（例如：`Personal AI Assistant`）
   - 30. 启用 **交互功能**。
   - 31. 在 **功能** 下，勾选 **加入空间和群组对话**。
   - 32. 在 **连接设置** 下，选择 **HTTP 端点 URL**。
   - 33. 在 **触发器** 下，选择 **对所有触发器使用通用的 HTTP 端点 URL**，并将其设置为你的网关公网 URL，后跟 `/googlechat`。
     - _Tip: Run `openclaw status` to find your gateway's public URL._
   - 35. 在 **可见性** 下，勾选 **使此 Chat 应用对 <Your Domain> 中的特定人员和群组可用**。
   - Enter your email address (e.g. `user@example.com`) in the text box.
   - 37. 点击底部的 **保存**。
6. 38. **启用应用状态**：
   - 39. 保存后，**刷新页面**。
   - 40. 查找 **应用状态** 部分（通常在保存后页面的顶部或底部）。
   - 41. 将状态更改为 **Live - available to users**。
   - 42. 再次点击 **保存**。
7. 43. 使用服务账号路径 + Webhook 受众配置 OpenClaw：
   - 44. 环境变量：`GOOGLE_CHAT_SERVICE_ACCOUNT_FILE=/path/to/service-account.json`
   - 45. 或配置：`channels.googlechat.serviceAccountFile: "/path/to/service-account.json"`。
8. 46. 设置 Webhook 受众类型和值（需与 Chat 应用配置匹配）。
9. 47. 启动网关。 48. Google Chat 将向你的 Webhook 路径发送 POST 请求。

## 49) 添加到 Google Chat

Once the gateway is running and your email is added to the visibility list:

1. 前往 [Google Chat](https://chat.google.com/)。
2. 点击 **Direct Messages** 旁边的 **+**（加号）图标。
3. 在搜索栏中（你平时添加联系人的地方），输入你在 Google Cloud Console 中配置的 **App name**。
   - **注意**：该机器人 **不会** 出现在“Marketplace”浏览列表中，因为它是一个私有应用。 你必须通过名称搜索它。
4. 从结果中选择你的机器人。
5. Click **Add** or **Chat** to start a 1:1 conversation.
6. 发送“Hello”以触发助手！

## 公共 URL（仅 Webhook）

Google Chat webhooks require a public HTTPS endpoint. 出于安全考虑，**只将 `/googlechat` 路径暴露到互联网**。 将 OpenClaw 仪表板和其他敏感端点保留在你的私有网络中。

### Option A: Tailscale Funnel (Recommended)

使用 Tailscale Serve 提供私有仪表板，并使用 Funnel 暴露公共 webhook 路径。 这样可以保持 `/` 为私有，仅暴露 `/googlechat`。

1. **检查你的网关绑定到的地址：**

   ```bash
   ss -tlnp | grep 18789
   ```

   记下 IP 地址（例如 `127.0.0.1`、`0.0.0.0`，或你的 Tailscale IP，如 `100.x.x.x`）。

2. **仅向 tailnet 暴露仪表板（端口 8443）：**

   ```bash
   # If bound to localhost (127.0.0.1 or 0.0.0.0):
   tailscale serve --bg --https 8443 http://127.0.0.1:18789

   # If bound to Tailscale IP only (e.g., 100.106.161.80):
   tailscale serve --bg --https 8443 http://100.106.161.80:18789
   ```

3. **仅公开暴露 webhook 路径：**

   ```bash
   # If bound to localhost (127.0.0.1 or 0.0.0.0):
   tailscale funnel --bg --set-path /googlechat http://127.0.0.1:18789/googlechat

   # If bound to Tailscale IP only (e.g., 100.106.161.80):
   tailscale funnel --bg --set-path /googlechat http://100.106.161.80:18789/googlechat
   ```

4. **Authorize the node for Funnel access:**
   If prompted, visit the authorization URL shown in the output to enable Funnel for this node in your tailnet policy.

5. **验证配置：**

   ```bash
   tailscale serve status
   tailscale funnel status
   ```

你的公共 webhook URL 将是：
`https://<node-name>.<tailnet>.ts.net/googlechat`

你的私有仪表板仍然只在 tailnet 内可访问：
`https://<node-name>.<tailnet>.ts.net:8443/`

在 Google Chat 应用配置中使用公共 URL（不带 `:8443`）。

> 注意：此配置在重启后仍然有效。 如需稍后移除，请运行 `tailscale funnel reset` 和 `tailscale serve reset`。

### 选项 B：反向代理（Caddy）

如果你使用像 Caddy 这样的反向代理，只代理特定路径：

```caddy
your-domain.com {
    reverse_proxy /googlechat* localhost:18789
}
```

使用此配置，对 `your-domain.com/` 的任何请求都会被忽略或返回 404，而 `your-domain.com/googlechat` 会被安全地路由到 OpenClaw。

### 选项 C：Cloudflare Tunnel

将你的隧道 ingress 规则配置为仅路由 webhook 路径：

- **路径**：`/googlechat` -> `http://localhost:18789/googlechat`
- **默认规则**：HTTP 404（Not Found）

## 工作原理

1. Google Chat 向网关发送 webhook POST 请求。 每个请求都包含一个 `Authorization: Bearer <token>` 头。
2. OpenClaw 会根据配置的 `audienceType` + `audience` 验证该令牌：
   - `audienceType: "app-url"` → audience 是你的 HTTPS webhook URL。
   - `audienceType: "project-number"` → audience 是 Cloud 项目编号。
3. 消息按空间进行路由：
   - DM 使用会话键 `agent:<agentId>:googlechat:dm:<spaceId>`。
   - Spaces 使用会话键 `agent:<agentId>:googlechat:group:<spaceId>`。
4. DM 访问默认需要配对。 未知发送者会收到一个配对码；使用以下命令批准：
   - `openclaw pairing approve googlechat <code>`
5. 群组空间默认需要 @ 提及。 如果提及检测需要应用的用户名，请使用 `botUser`。

## 目标

使用以下标识符进行投递和允许列表配置：

- 私信：`users/<userId>` 或 `users/<email>`（支持电子邮件地址）。
- 空间：`spaces/<spaceId>`。

## 配置要点

```json5
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountFile: "/path/to/service-account.json",
      audienceType: "app-url",
      audience: "https://gateway.example.com/googlechat",
      webhookPath: "/googlechat",
      botUser: "users/1234567890", // optional; helps mention detection
      dm: {
        policy: "pairing",
        allowFrom: ["users/1234567890", "name@example.com"],
      },
      groupPolicy: "allowlist",
      groups: {
        "spaces/AAAA": {
          allow: true,
          requireMention: true,
          users: ["users/1234567890"],
          systemPrompt: "Short answers only.",
        },
      },
      actions: { reactions: true },
      typingIndicator: "message",
      mediaMaxMb: 20,
    },
  },
}
```

注意：

- 服务账号凭据也可以通过 `serviceAccount`（JSON 字符串）以内联方式传递。
- 如果未设置 `webhookPath`，默认的 webhook 路径为 `/googlechat`。
- 当启用 `actions.reactions` 时，可通过 `reactions` 工具和 `channels action` 使用表情反应。
- `typingIndicator` 支持 `none`、`message`（默认）和 `reaction`（`reaction` 需要用户 OAuth）。
- 附件通过 Chat API 下载并存储在媒体管道中（大小受 `mediaMaxMb` 限制）。

## 故障排查

### 405 方法不允许

如果 Google Cloud Logs Explorer 显示如下错误：

```
status code: 405, reason phrase: HTTP error response: HTTP/1.1 405 Method Not Allowed
```

这表示 webhook 处理器尚未注册。 常见原因：

1. **渠道未配置**：你的配置中缺少 `channels.googlechat` 部分。 可通过以下命令验证：

   ```bash
   openclaw config get channels.googlechat
   ```

   如果返回“Config path not found”，请添加配置（参见 [Config highlights](#config-highlights)）。

2. **插件未启用**：检查插件状态：

   ```bash
   openclaw plugins list | grep googlechat
   ```

   如果显示为“disabled”，请在配置中添加 `plugins.entries.googlechat.enabled: true`。

3. **网关未重启**：添加配置后，重启网关：

   ```bash
   openclaw gateway restart
   ```

验证渠道是否正在运行：

```bash
openclaw channels status
# 应显示：Google Chat default: enabled, configured, ...
```

### 其他问题

- 检查 `openclaw channels status --probe` 以查看认证错误或缺失的 audience 配置。
- 如果未收到消息，请确认 Chat 应用的 webhook URL 和事件订阅。
- 如果提及门控阻止了回复，请将 `botUser` 设置为应用的用户资源名称，并验证 `requireMention`。
- 在发送测试消息时使用 `openclaw logs --follow`，查看请求是否到达网关。

相关文档：

- [Gateway configuration](/gateway/configuration)
- [Security](/gateway/security)
- [Reactions](/tools/reactions)
