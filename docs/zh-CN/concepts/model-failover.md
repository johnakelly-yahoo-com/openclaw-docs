---
summary: "17. OpenClaw 如何轮换鉴权配置并在模型之间回退"
read_when:
  - 18. 诊断鉴权配置轮换、冷却或模型回退行为
  - 33. 更新认证配置或模型的故障转移规则
title: "20. 模型故障切换"
---

# 21. 模型故障切换

34. OpenClaw 分两个阶段处理失败：

1. 23. **鉴权配置轮换**（在当前提供方内）。
2. 24. **模型回退** 到 `agents.defaults.model.fallbacks` 中的下一个模型。

25) 本文档解释运行时规则以及支撑这些规则的数据。

## 26. 鉴权存储（密钥 + OAuth）

27. OpenClaw 对 API 密钥和 OAuth 令牌都使用 **鉴权配置（auth profiles）**。

- 28. 密钥存储在 `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`（旧版：`~/.openclaw/agent/auth-profiles.json`）。
- 29. 配置 `auth.profiles` / `auth.order` 仅用于 **元数据 + 路由**（不包含密钥）。
- 30. 仅用于旧版导入的 OAuth 文件：`~/.openclaw/credentials/oauth.json`（首次使用时导入到 `auth-profiles.json`）。

31. 更多详情：[/concepts/oauth](/concepts/oauth)

32. 凭据类型：

- 33. `type: "api_key"` → `{ provider, key }`
- 34. `type: "oauth"` → `{ provider, access, refresh, expires, email? 35. }`（部分提供方还需要 `projectId`/`enterpriseUrl`）

## 36. 配置文件 ID

37. OAuth 登录会创建不同的配置文件，以便多个账号共存。

- 38. 默认值：当没有可用邮箱时使用 `provider:default`。
- 39. 带邮箱的 OAuth：`provider:<email>`（例如 `google-antigravity:user@gmail.com`）。

40. 配置文件位于 `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` 的 `profiles` 下。

## 41. 轮换顺序

42. 当某个提供方有多个配置文件时，OpenClaw 按如下顺序选择：

1. 43. **显式配置**：`auth.order[provider]`（如果已设置）。
2. 44. **已配置的配置文件**：按提供方筛选的 `auth.profiles`。
3. 45. **已存储的配置文件**：`auth-profiles.json` 中该提供方的条目。

46) 如果未配置显式顺序，OpenClaw 使用轮询（round‑robin）顺序：

- 47. **主键：** 配置文件类型（**OAuth 优先于 API 密钥**）。
- 48. **次键：** `usageStats.lastUsed`（每种类型内按最早使用优先）。
- 49. **处于冷却/已禁用的配置文件** 会被移到末尾，并按最早到期时间排序。

### 50. 会话粘性（缓存友好）

OpenClaw **pins the chosen auth profile per session** to keep provider caches warm.
It does **not** rotate on every request. The pinned profile is reused until:

- the session is reset (`/new` / `/reset`)
- a compaction completes (compaction count increments)
- the profile is in cooldown/disabled

Manual selection via `/model …@<profileId>` sets a **user override** for that session
and is not auto‑rotated until a new session starts.

Auto‑pinned profiles (selected by the session router) are treated as a **preference**:
they are tried first, but OpenClaw may rotate to another profile on rate limits/timeouts.
User‑pinned profiles stay locked to that profile; if it fails and model fallbacks
are configured, OpenClaw moves to the next model instead of switching profiles.

### Why OAuth can “look lost”

If you have both an OAuth profile and an API key profile for the same provider, round‑robin can switch between them across messages unless pinned. To force a single profile:

- Pin with `auth.order[provider] = ["provider:profileId"]`, or
- Use a per-session override via `/model …` with a profile override (when supported by your UI/chat surface).

## Cooldowns

When a profile fails due to auth/rate‑limit errors (or a timeout that looks
like rate limiting), OpenClaw marks it in cooldown and moves to the next profile.
Format/invalid‑request errors (for example Cloud Code Assist tool call ID
validation failures) are treated as failover‑worthy and use the same cooldowns.

Cooldowns use exponential backoff:

- 1 minute
- 5 minutes
- 25 minutes
- 1 hour (cap)

State is stored in `auth-profiles.json` under `usageStats`:

```json
{
  "usageStats": {
    "provider:profile": {
      "lastUsed": 1736160000000,
      "cooldownUntil": 1736160600000,
      "errorCount": 2
    }
  }
}
```

## Billing disables

Billing/credit failures (for example “insufficient credits” / “credit balance too low”) are treated as failover‑worthy, but they’re usually not transient. Instead of a short cooldown, OpenClaw marks the profile as **disabled** (with a longer backoff) and rotates to the next profile/provider.

State is stored in `auth-profiles.json`:

```json
{
  "usageStats": {
    "provider:profile": {
      "disabledUntil": 1736178000000,
      "disabledReason": "billing"
    }
  }
}
```

Defaults:

- Billing backoff starts at **5 hours**, doubles per billing failure, and caps at **24 hours**.
- Backoff counters reset if the profile hasn’t failed for **24 hours** (configurable).

## Model fallback

If all profiles for a provider fail, OpenClaw moves to the next model in
`agents.defaults.model.fallbacks`. This applies to auth failures, rate limits, and
timeouts that exhausted profile rotation (other errors do not advance fallback).

When a run starts with a model override (hooks or CLI), fallbacks still end at
`agents.defaults.model.primary` after trying any configured fallbacks.

## Related config

See [Gateway configuration](/gateway/configuration) for:

- `auth.profiles` / `auth.order`
- `auth.cooldowns.billingBackoffHours` / `auth.cooldowns.billingBackoffHoursByProvider`
- `auth.cooldowns.billingMaxHours` / `auth.cooldowns.failureWindowHours`
- `agents.defaults.model.primary` / `agents.defaults.model.fallbacks`
- `agents.defaults.imageModel` routing

See [Models](/concepts/models) for the broader model selection and fallback overview.
