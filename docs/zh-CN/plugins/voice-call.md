---
summary: "语音通话插件：通过 Twilio/Telnyx/Plivo 进行外呼 + 来呼（插件安装 + 配置 + CLI）"
read_when:
  - 你想从 OpenClaw 发起一次外呼语音通话
  - 你正在配置或开发 voice-call 插件
title: "语音通话插件"
---

# 语音通话（插件）

通过插件为 OpenClaw 提供语音通话。 支持外呼通知以及
具备来电策略的多轮对话。

当前提供方：

- `twilio`（Programmable Voice + Media Streams）
- `telnyx`（Call Control v2）
- `plivo`（Voice API + XML transfer + GetInput speech）
- `mock`（开发/无网络）

快速心智模型：

- Install plugin
- Restart Gateway
- Configure under `plugins.entries.voice-call.config`
- Use `openclaw voicecall ...` or the `voice_call` tool

## Where it runs (local vs remote)

The Voice Call plugin runs **inside the Gateway process**.

If you use a remote Gateway, install/configure the plugin on the **machine running the Gateway**, then restart the Gateway to load it.

## 5. 安装

### Option A: install from npm (recommended)

```bash
openclaw plugins install @openclaw/voice-call
```

Restart the Gateway afterwards.

### Option B: install from a local folder (dev, no copying)

```bash
openclaw plugins install ./extensions/voice-call
cd ./extensions/voice-call && pnpm install
```

Restart the Gateway afterwards.

## Config

Set config under `plugins.entries.voice-call.config`:

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        enabled: true,
        config: {
          provider: "twilio", // or "telnyx" | "plivo" | "mock"
          fromNumber: "+15550001234",
          toNumber: "+15550005678",

          twilio: {
            accountSid: "ACxxxxxxxx",
            authToken: "...",
          },

          plivo: {
            authId: "MAxxxxxxxxxxxxxxxxxxxx",
            authToken: "...",
          },

          // Webhook server
          serve: {
            port: 3334,
            path: "/voice/webhook",
          },

          // Webhook security (recommended for tunnels/proxies)
          webhookSecurity: {
            allowedHosts: ["voice.example.com"],
            trustedProxyIPs: ["100.64.0.1"],
          },

          // Public exposure (pick one)
          // publicUrl: "https://example.ngrok.app/voice/webhook",
          // tunnel: { provider: "ngrok" },
          // tailscale: { mode: "funnel", path: "/voice/webhook" }

          outbound: {
            defaultMode: "notify", // notify | conversation
          },

          streaming: {
            enabled: true,
            streamPath: "/voice/stream",
          },
        },
      },
    },
  },
}
```

Notes:

- Twilio/Telnyx require a **publicly reachable** webhook URL.
- 6. Plivo 需要一个**可公开访问的** webhook URL。
- `mock` is a local dev provider (no network calls).
- `skipSignatureVerification` is for local testing only.
- If you use ngrok free tier, set `publicUrl` to the exact ngrok URL; signature verification is always enforced.
- `tunnel.allowNgrokFreeTierLoopbackBypass: true` allows Twilio webhooks with invalid signatures **only** when `tunnel.provider="ngrok"` and `serve.bind` is loopback (ngrok local agent). Use for local dev only.
- Ngrok free tier URLs can change or add interstitial behavior; if `publicUrl` drifts, Twilio signatures will fail. For production, prefer a stable domain or Tailscale funnel.

## Webhook Security

When a proxy or tunnel sits in front of the Gateway, the plugin reconstructs the
public URL for signature verification. These options control which forwarded
headers are trusted.

`webhookSecurity.allowedHosts` allowlists hosts from forwarding headers.

`webhookSecurity.trustForwardingHeaders` trusts forwarded headers without an allowlist.

`webhookSecurity.trustedProxyIPs` only trusts forwarded headers when the request
remote IP matches the list.

Example with a stable public host:

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          publicUrl: "https://voice.example.com/voice/webhook",
          webhookSecurity: {
            allowedHosts: ["voice.example.com"],
          },
        },
      },
    },
  },
}
```

## TTS for calls

Voice Call uses the core `messages.tts` configuration (OpenAI or ElevenLabs) for
streaming speech on calls. You can override it under the plugin config with the
**same shape** — it deep‑merges with `messages.tts`.

```json5
{
  tts: {
    provider: "elevenlabs",
    elevenlabs: {
      voiceId: "pMsXgVXv3BLzUgSXRplE",
      modelId: "eleven_multilingual_v2",
    },
  },
}
```

Notes:

- **Edge TTS is ignored for voice calls** (telephony audio needs PCM; Edge output is unreliable).
- Core TTS is used when Twilio media streaming is enabled; otherwise calls fall back to provider native voices.

### More examples

Use core TTS only (no override):

```json5
{
  messages: {
    tts: {
      provider: "openai",
      openai: { voice: "alloy" },
    },
  },
}
```

Override to ElevenLabs just for calls (keep core default elsewhere):

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          tts: {
            provider: "elevenlabs",
            elevenlabs: {
              apiKey: "elevenlabs_key",
              voiceId: "pMsXgVXv3BLzUgSXRplE",
              modelId: "eleven_multilingual_v2",
            },
          },
        },
      },
    },
  },
}
```

Override only the OpenAI model for calls (deep‑merge example):

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          tts: {
            openai: {
              model: "gpt-4o-mini-tts",
              voice: "marin",
            },
          },
        },
      },
    },
  },
}
```

## Inbound calls

1. 入站策略默认设置为 `disabled`。 2. 要启用入站呼叫，请设置：

```json5
7. {
  inboundPolicy: "allowlist",
  allowFrom: ["+15550001234"],
  inboundGreeting: "Hello! How can I help?",
}
```

4. 自动回复使用代理系统。 5. 可通过以下参数进行调优：

- 6. `responseModel`
- 7. `responseSystemPrompt`
- 8. `responseTimeoutMs`

## 9. CLI

```bash
10. openclaw voicecall call --to "+15555550123" --message "Hello from OpenClaw"
openclaw voicecall continue --call-id <id> --message "Any questions?"
openclaw voicecall speak --call-id <id> --message "One moment"
openclaw voicecall end --call-id <id>
openclaw voicecall status --call-id <id>
openclaw voicecall tail
openclaw voicecall expose --mode funnel
```

## 11. 代理工具

12. 工具名称：`voice_call`

13. 操作：

- 14. `initiate_call`（message，to?，mode?）
- 15. `continue_call`（callId，message）
- 16. `speak_to_user`（callId，message）
- 17. `end_call`（callId）
- 9. `get_status`（callId）

19. 此仓库在 `skills/voice-call/SKILL.md` 中提供了对应的技能文档。

## 20. 网关 RPC

- 21. `voicecall.initiate`（`to?`，`message`，`mode?`）
- 22. `voicecall.continue`（`callId`，`message`）
- 23. `voicecall.speak`（`callId`，`message`）
- 24. `voicecall.end`（`callId`）
- 25. `voicecall.status`（`callId`）
