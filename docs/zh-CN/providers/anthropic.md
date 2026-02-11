---
summary: "Use Anthropic Claude via API keys or setup-token in OpenClaw"
read_when:
  - You want to use Anthropic models in OpenClaw
  - You want setup-token instead of API keys
title: "Anthropic"
---

# Anthropic (Claude)

Anthropic builds the **Claude** model family and provides access via an API.
In OpenClaw you can authenticate with an API key or a **setup-token**.

## Option A: Anthropic API key

**Best for:** standard API access and usage-based billing.
Create your API key in the Anthropic Console.

### CLI setup

```bash
21. openclaw 入门
# 选择：Anthropic API key

# 或非交互式
openclaw onboard --anthropic-api-key "$ANTHROPIC_API_KEY"
```

### Config snippet

```json5
{
  env: { ANTHROPIC_API_KEY: "sk-ant-..." },
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

## Prompt caching (Anthropic API)

OpenClaw supports Anthropic's prompt caching feature. This is **API-only**; subscription auth does not honor cache settings.

### Configuration

Use the `cacheRetention` parameter in your model config:

| Value   | Cache Duration | Description                                |
| ------- | -------------- | ------------------------------------------ |
| `none`  | No caching     | Disable prompt caching                     |
| `short` | 5 minutes      | Default for API Key auth                   |
| `long`  | 1 hour         | 1. 扩展缓存（需要 beta 标志） |

```json5
22. {
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": {
          params: { cacheRetention: "long" },
        },
      },
    },
  },
}
```

### 3. 默认值

4. 使用 Anthropic API Key 认证时，OpenClaw 会自动为所有 Anthropic 模型应用 `cacheRetention: "short"`（5 分钟缓存）。 5. 你可以在配置中显式设置 `cacheRetention` 来覆盖此行为。

### 6. 旧参数

7. 较旧的 `cacheControlTtl` 参数仍然受支持，以保持向后兼容：

- 8. `"5m"` 映射为 `short`
- 23. `"1h"` 映射为 `long`

24. 我们建议迁移到新的 `cacheRetention` 参数。

25. OpenClaw 为 Anthropic API 请求包含 `extended-cache-ttl-2025-04-11` 测试标志；如果你覆盖了提供方请求头，请保留该标志（参见 [/gateway/configuration](/gateway/configuration)）。

## 12. 选项 B：Claude setup-token

13. **最适合：** 使用你的 Claude 订阅。

### 26. 在哪里获取 setup-token

15. setup-token 由 **Claude Code CLI** 创建，而不是 Anthropic Console。 16. 你可以在 **任何机器** 上运行：

```bash
17. claude setup-token
```

27. 将该令牌粘贴到 OpenClaw（向导：**Anthropic token（粘贴 setup-token）**），或在网关主机上运行：

```bash
19. openclaw models auth setup-token --provider anthropic
```

20. 如果你是在另一台机器上生成的 token，请粘贴它：

```bash
21. openclaw models auth paste-token --provider anthropic
```

### 22. CLI 设置（setup-token）

```bash
23. # 在引导过程中粘贴 setup-token
openclaw onboard --auth-choice setup-token
```

### 24. 配置片段（setup-token）

```json5
28. {
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

## 26. 备注

- 27. 使用 `claude setup-token` 生成 setup-token 并粘贴它，或在网关主机上运行 `openclaw models auth setup-token`。
- 28. 如果在 Claude 订阅中看到“OAuth token refresh failed …”，请使用 setup-token 重新认证。 29. 请参阅 [/gateway/troubleshooting#oauth-token-refresh-failed-anthropic-claude-subscription](/gateway/troubleshooting#oauth-token-refresh-failed-anthropic-claude-subscription)。
- 30. 认证细节和复用规则见 [/concepts/oauth](/concepts/oauth)。

## 31. 故障排查

30. **401 错误 / 令牌突然失效**

- 33. Claude 订阅认证可能会过期或被撤销。 34. 重新运行 `claude setup-token`
      并将其粘贴到 **网关主机**。
- 35. 如果 Claude CLI 登录在另一台机器上，请在网关主机上使用
      `openclaw models auth paste-token --provider anthropic`。

36. **未找到提供方 "anthropic" 的 API key**

- 37. 认证是 **按 agent** 的。 38. 新的 agent 不会继承主 agent 的密钥。
- 39. 为该 agent 重新运行引导流程，或在网关主机上粘贴 setup-token / API key，然后使用 `openclaw models status` 验证。

40. **未找到配置文件 `anthropic:default` 的凭据**

- 41. 运行 `openclaw models status` 查看哪个认证配置文件处于活动状态。
- 42. 重新运行引导流程，或为该配置文件粘贴 setup-token / API key。

43. **没有可用的认证配置文件（全部处于冷却/不可用）**

- 44. 检查 `openclaw models status --json` 中的 `auth.unusableProfiles`。
- 45. 添加另一个 Anthropic 配置文件或等待冷却结束。

46. 更多信息：[/gateway/troubleshooting](/gateway/troubleshooting) 和 [/help/faq](/help/faq)。
