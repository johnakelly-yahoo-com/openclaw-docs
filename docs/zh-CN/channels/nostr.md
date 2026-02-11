---
summary: "Nostr DM channel via NIP-04 encrypted messages"
read_when:
  - You want OpenClaw to receive DMs via Nostr
  - You're setting up decentralized messaging
title: "Nostr"
---

# Nostr

**Status:** Optional plugin (disabled by default).

Nostr is a decentralized protocol for social networking. This channel enables OpenClaw to receive and respond to encrypted direct messages (DMs) via NIP-04.

## Install (on demand)

### Onboarding (recommended)

- The onboarding wizard (`openclaw onboard`) and `openclaw channels add` list optional channel plugins.
- Selecting Nostr prompts you to install the plugin on demand.

Install defaults:

- **Dev channel + git checkout available:** uses the local plugin path.
- **Stable/Beta:** downloads from npm.

You can always override the choice in the prompt.

### Manual install

```bash
openclaw plugins install @openclaw/nostr
```

Use a local checkout (dev workflows):

```bash
openclaw plugins install --link <path-to-openclaw>/extensions/nostr
```

Restart the Gateway after installing or enabling plugins.

## Quick setup

1. Generate a Nostr keypair (if needed):

```bash
# Using nak
nak key generate
```

2. Add to config:

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}"
    }
  }
}
```

3. Export the key:

```bash
export NOSTR_PRIVATE_KEY="nsec1..."
```

4. Restart the Gateway.

## Configuration reference

| Key          | Type                                                         | Default                                     | Description                               |
| ------------ | ------------------------------------------------------------ | ------------------------------------------- | ----------------------------------------- |
| `privateKey` | string                                                       | required                                    | Private key in `nsec` or hex format       |
| `relays`     | string[] | `['wss://relay.damus.io', 'wss://nos.lol']` | Relay URLs (WebSocket) |
| `dmPolicy`   | string                                                       | `pairing`                                   | DM access policy                          |
| `allowFrom`  | string[] | `[]`                                        | Allowed sender pubkeys                    |
| `enabled`    | boolean                                                      | `true`                                      | Enable/disable channel                    |
| `name`       | string                                                       | -                                           | Display name                              |
| `profile`    | object                                                       | -                                           | NIP-01 profile metadata                   |

## Profile metadata

Profile data is published as a NIP-01 `kind:0` event. You can manage it from the Control UI (Channels -> Nostr -> Profile) or set it directly in config.

Example:

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "profile": {
        "name": "openclaw",
        "displayName": "OpenClaw",
        "about": "Personal assistant DM bot",
        "picture": "https://example.com/avatar.png",
        "banner": "https://example.com/banner.png",
        "website": "https://example.com",
        "nip05": "openclaw@example.com",
        "lud16": "openclaw@example.com"
      }
    }
  }
}
```

Notes:

- Profile URLs must use `https://`.
- Importing from relays merges fields and preserves local overrides.

## Access control

### DM policies

- **pairing** (default): unknown senders get a pairing code.
- **allowlist**: only pubkeys in `allowFrom` can DM.
- **open**: public inbound DMs (requires `allowFrom: ["*"]`).
- **disabled**: ignore inbound DMs.

### Allowlist example

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "dmPolicy": "allowlist",
      "allowFrom": ["npub1abc...", "npub1xyz..."]
    }
  }
}
```

## Key formats

Accepted formats:

- **Private key:** `nsec...` or 64-char hex
- **Pubkeys (`allowFrom`):** `npub...` or hex

## Relays

Defaults: `relay.damus.io` and `nos.lol`.

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "relays": ["wss://relay.damus.io", "wss://relay.primal.net", "wss://nostr.wine"]
    }
  }
}
```

Tips:

- Use 2-3 relays for redundancy.
- Avoid too many relays (latency, duplication).
- Paid relays can improve reliability.
- Local relays are fine for testing (`ws://localhost:7777`).

## Protocol support

| NIP    | Status    | Description                                 |
| ------ | --------- | ------------------------------------------- |
| NIP-01 | Supported | Basic event format + profile metadata       |
| NIP-04 | Supported | Encrypted DMs (`kind:4`) |
| NIP-17 | Planned   | Gift-wrapped DMs                            |
| NIP-44 | Planned   | Versioned encryption                        |

## Testing

### 1. 本地中继

```bash
2. # 启动 strfry
docker run -p 7777:7777 ghcr.io/hoytech/strfry
```

```json
3. {
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "relays": ["ws://localhost:7777"]
    }
  }
}
```

### 4. 手动测试

1. 5. 从日志中记录机器人公钥（npub）。
2. 6. 打开一个 Nostr 客户端（Damus、Amethyst 等）。
3. 7. 向机器人公钥发送私信。
4. 8. 验证响应。

## 9) 故障排查

### 10. 未收到消息

- 11. 验证私钥是否有效。
- 12. 确保中继 URL 可达，并使用 `wss://`（本地使用 `ws://`）。
- 13. 确认 `enabled` 不是 `false`。
- 14. 检查 Gateway 日志中的中继连接错误。

### 15. 未发送响应

- 16. 检查中继是否接受写入。
- 17. 验证出站连接。
- 18. 留意中继速率限制。

### 19. 重复响应

- 20. 使用多个中继时属于预期行为。
- 21. 消息按事件 ID 去重；只有第一次投递会触发响应。

## 22. 安全

- 23. 切勿提交私钥。
- 24. 使用环境变量存储密钥。
- 25. 生产环境机器人请考虑使用 `allowlist`。

## 26. 限制（MVP）

- 27. 仅支持私信（不支持群聊）。
- 28. 不支持媒体附件。
- 29. 仅支持 NIP-04（计划支持 NIP-17 gift-wrap）。
