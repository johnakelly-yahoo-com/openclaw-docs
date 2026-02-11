---
summary: "33. 用于外发回复的文本转语音（TTS）"
read_when:
  - 34. 为回复启用文本转语音
  - 35. 配置 TTS 提供商或限制
  - 36. 使用 /tts 命令
title: "37. 文本转语音"
---

# 38. 文本转语音（TTS）

39. OpenClaw 可以使用 ElevenLabs、OpenAI 或 Edge TTS 将外发回复转换为音频。
40. 它可在 OpenClaw 能发送音频的任何地方使用；Telegram 会显示为圆形语音消息气泡。

## 41. 支持的服务

- 42. **ElevenLabs**（主提供商或回退提供商）
- 43. **OpenAI**（主提供商或回退提供商；也用于摘要）
- 44. **Edge TTS**（主提供商或回退提供商；使用 `node-edge-tts`，在没有 API 密钥时为默认）

### 45. Edge TTS 说明

46. Edge TTS 通过 `node-edge-tts` 库使用 Microsoft Edge 的在线神经 TTS 服务。 47. 它是托管服务（非本地），使用微软的端点，且不需要 API 密钥。 48. `node-edge-tts` 提供语音配置选项和输出格式，但并非所有选项都受 Edge 服务支持。 49. citeturn2search0

50. 由于 Edge TTS 是没有公开 SLA 或配额的公共 Web 服务，请将其视为尽力而为。 如果你需要有保障的限额和支持，请使用 OpenAI 或 ElevenLabs。
    Microsoft 的 Speech REST API 文档记录了每个请求 10 分钟的音频限制；Edge TTS
    未公布限制，因此应假设限制相同或更低。 citeturn0search3

## 可选密钥

如果你要使用 OpenAI 或 ElevenLabs：

- `ELEVENLABS_API_KEY`（或 `XI_API_KEY`）
- `OPENAI_API_KEY`

Edge TTS **不**需要 API 密钥。 如果未找到任何 API 密钥，OpenClaw 默认
使用 Edge TTS（除非通过 `messages.tts.edge.enabled=false` 禁用）。

如果配置了多个提供商，将优先使用所选提供商，其余作为回退选项。
自动摘要使用已配置的 `summaryModel`（或 `agents.defaults.model.primary`），
因此如果启用摘要，该提供商也必须完成身份验证。

## 服务链接

- [OpenAI 文本转语音指南](https://platform.openai.com/docs/guides/text-to-speech)
- [OpenAI 音频 API 参考](https://platform.openai.com/docs/api-reference/audio)
- [ElevenLabs 文本转语音](https://elevenlabs.io/docs/api-reference/text-to-speech)
- [ElevenLabs 身份验证](https://elevenlabs.io/docs/api-reference/authentication)
- [node-edge-tts](https://github.com/SchneeHertz/node-edge-tts)
- [Microsoft Speech 输出格式](https://learn.microsoft.com/azure/ai-services/speech-service/rest-text-to-speech#audio-outputs)

## 是否默认启用？

否。 自动 TTS 默认 **关闭**。 在配置中通过
`messages.tts.auto` 启用，或在每个会话中使用 `/tts always`（别名：`/tts on`）。

一旦开启 TTS，Edge TTS **默认启用**，并且在没有可用的 OpenAI 或 ElevenLabs API 密钥时会自动使用。

## 配置

TTS 配置位于 `openclaw.json` 中的 `messages.tts` 下。
完整的 schema 位于 [Gateway configuration](/gateway/configuration)。

### 最小配置（启用 + 提供商）

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "elevenlabs",
    },
  },
}
```

### OpenAI 为主，ElevenLabs 为回退

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "openai",
      summaryModel: "openai/gpt-4.1-mini",
      modelOverrides: {
        enabled: true,
      },
      openai: {
        apiKey: "openai_api_key",
        model: "gpt-4o-mini-tts",
        voice: "alloy",
      },
      elevenlabs: {
        apiKey: "elevenlabs_api_key",
        baseUrl: "https://api.elevenlabs.io",
        voiceId: "voice_id",
        modelId: "eleven_multilingual_v2",
        seed: 42,
        applyTextNormalization: "auto",
        languageCode: "en",
        voiceSettings: {
          stability: 0.5,
          similarityBoost: 0.75,
          style: 0.0,
          useSpeakerBoost: true,
          speed: 1.0,
        },
      },
    },
  },
}
```

### Edge TTS 为主（无需 API 密钥）

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "edge",
      edge: {
        enabled: true,
        voice: "en-US-MichelleNeural",
        lang: "en-US",
        outputFormat: "audio-24khz-48kbitrate-mono-mp3",
        rate: "+10%",
        pitch: "-5%",
      },
    },
  },
}
```

### 禁用 Edge TTS

```json5
{
  messages: {
    tts: {
      edge: {
        enabled: false,
      },
    },
  },
}
```

### 自定义限制 + 偏好路径

```json5
{
  messages: {
    tts: {
      auto: "always",
      maxTextLength: 4000,
      timeoutMs: 30000,
      prefsPath: "~/.openclaw/settings/tts.json",
    },
  },
}
```

### 仅在收到语音消息后才用音频回复

```json5
{
  messages: {
    tts: {
      auto: "inbound",
    },
  },
}
```

### 为长回复禁用自动摘要

```json5
{
  messages: {
    tts: {
      auto: "always",
    },
  },
}
```

然后运行：

```
/tts summary off
```

### 字段说明

- `auto`：自动 TTS 模式（`off`、`always`、`inbound`、`tagged`）。
  - `inbound` 仅在收到语音消息后才发送音频。
  - `tagged` 仅当回复中包含 `[[tts]]` 标签时才发送音频。
- `enabled`：旧版开关（doctor 会将其迁移到 `auto`）。
- `mode`：`"final"`（默认）或 `"all"`（包含工具/区块回复）。
- `provider`：`"elevenlabs"`、`"openai"` 或 `"edge"`（回退自动）。
- 如果 `provider` **未设置**，OpenClaw 会优先选择 `openai`（如果有密钥），其次 `elevenlabs`（如果有密钥），
  否则使用 `edge`。
- `summaryModel`：用于自动摘要的可选低成本模型；默认使用 `agents.defaults.model.primary`。
  - 接受 `provider/model` 或已配置的模型别名。
- `modelOverrides`：允许模型输出 TTS 指令（默认开启）。
- `maxTextLength`：TTS 输入的硬性上限（字符数）。 `/tts audio`：超出限制时会失败。
- `timeoutMs`：请求超时时间（毫秒）。
- `prefsPath`：覆盖本地偏好设置 JSON 路径（provider/limit/summary）。
- `apiKey` 的值会回退到环境变量（`ELEVENLABS_API_KEY`/`XI_API_KEY`、`OPENAI_API_KEY`）。
- `elevenlabs.baseUrl`：覆盖 ElevenLabs API 基础 URL。
- `elevenlabs.voiceSettings`：
  - `stability`、`similarityBoost`、`style`：`0..1`
  - `useSpeakerBoost`：`true|false`
  - `speed`：`0.5..2.0`（1.0 = 正常）
- `elevenlabs.applyTextNormalization`：`auto|on|off`
- `elevenlabs.languageCode`：2 位 ISO 639-1（例如 `en`、`de`）
- `elevenlabs.seed`：整数 `0..4294967295`（尽力保证确定性）
- `edge.enabled`：允许使用 Edge TTS（默认 `true`；无需 API key）。
- `edge.voice`：Edge 神经语音名称（例如 `en-US-MichelleNeural`）。
- `edge.lang`：语言代码（例如 `en-US`）。
- `edge.outputFormat`：Edge 输出格式（例如 `audio-24khz-48kbitrate-mono-mp3`）。
  - 有效值请参见 Microsoft Speech 输出格式；并非所有格式都受 Edge 支持。
- `edge.rate` / `edge.pitch` / `edge.volume`：百分比字符串（例如 `+10%`、`-5%`）。
- `edge.saveSubtitles`：在音频文件旁写入 JSON 字幕。
- `edge.proxy`：用于 Edge TTS 请求的代理 URL。
- `edge.timeoutMs`：请求超时覆盖（毫秒）。

## 模型驱动的覆盖（默认开启）

默认情况下，模型**可以**为单个回复输出 TTS 指令。
当 `messages.tts.auto` 为 `tagged` 时，需要这些指令才能触发音频。

启用后，模型可以输出 `[[tts:...]]` 指令来为单个回复覆盖语音，并可选地使用 `[[tts:text]]...[[/tts:text]]` 块提供仅应出现在音频中的表现性标签（笑声、歌唱提示等）。

示例回复载荷：

```
给你。
```

[[tts:provider=elevenlabs voiceId=pMsXgVXv3BLzUgSXRplE model=eleven_v3 speed=1.1]]
[[tts:text]](laughs) Read the song once more.[[/tts:text]]

- 可用的指令键（启用时）：
- `provider`（`openai` | `elevenlabs` | `edge`）
- `voice`（OpenAI 语音）或 `voiceId`（ElevenLabs）
- `model`（OpenAI TTS 模型或 ElevenLabs 模型 ID）
- `stability`、`similarityBoost`、`style`、`speed`、`useSpeakerBoost`
- `applyTextNormalization`（`auto|on|off`）
- `languageCode`（ISO 639-1）

`seed`

```json5
禁用所有模型覆盖：
```

{
messages: {
tts: {
modelOverrides: {
enabled: false,
},
},
},
}

```json5
可选允许列表（在保持标签启用的同时禁用特定覆盖）：
```

{
messages: {
tts: {
modelOverrides: {
enabled: true,
allowProvider: false,
allowSeed: false,
},
},
},
}
-

按用户偏好设置

斜杠命令会将本地覆盖写入 `prefsPath`（默认：
`~/.openclaw/settings/tts.json`，可通过 `OPENCLAW_TTS_PREFS` 或
`messages.tts.prefsPath` 覆盖）。

- 存储的字段：
- `enabled`
- `provider`
- `maxLength`（摘要阈值；默认 1500 字符）

These override `messages.tts.*` for that host.

## Output formats (fixed)

- **Telegram**: Opus voice note (`opus_48000_64` from ElevenLabs, `opus` from OpenAI).
  - 48kHz / 64kbps is a good voice-note tradeoff and required for the round bubble.
- **Other channels**: MP3 (`mp3_44100_128` from ElevenLabs, `mp3` from OpenAI).
  - 44.1kHz / 128kbps is the default balance for speech clarity.
- **Edge TTS**: uses `edge.outputFormat` (default `audio-24khz-48kbitrate-mono-mp3`).
  - `node-edge-tts` accepts an `outputFormat`, but not all formats are available
    from the Edge service. citeturn2search0
  - Output format values follow Microsoft Speech output formats (including Ogg/WebM Opus). citeturn1search0
  - Telegram `sendVoice` accepts OGG/MP3/M4A; use OpenAI/ElevenLabs if you need
    guaranteed Opus voice notes. citeturn1search1
  - If the configured Edge output format fails, OpenClaw retries with MP3.

OpenAI/ElevenLabs formats are fixed; Telegram expects Opus for voice-note UX.

## Auto-TTS behavior

When enabled, OpenClaw:

- skips TTS if the reply already contains media or a `MEDIA:` directive.
- skips very short replies (< 10 chars).
- summarizes long replies when enabled using `agents.defaults.model.primary` (or `summaryModel`).
- attaches the generated audio to the reply.

If the reply exceeds `maxLength` and summary is off (or no API key for the
summary model), audio
is skipped and the normal text reply is sent.

## Flow diagram

```
Reply -> TTS enabled?
  no  -> send text
  yes -> has media / MEDIA: / short?
          yes -> send text
          no  -> length > limit?
                   no  -> TTS -> attach audio
                   yes -> summary enabled?
                            no  -> send text
                            yes -> summarize (summaryModel or agents.defaults.model.primary)
                                      -> TTS -> attach audio
```

## Slash command usage

There is a single command: `/tts`.
See [Slash commands](/tools/slash-commands) for enablement details.

Discord note: `/tts` is a built-in Discord command, so OpenClaw registers
`/voice` as the native command there. Text `/tts ...` still works.

```
/tts off
/tts always
/tts inbound
/tts tagged
/tts status
/tts provider openai
/tts limit 2000
/tts summary off
/tts audio Hello from OpenClaw
```

Notes:

- Commands require an authorized sender (allowlist/owner rules still apply).
- `commands.text` or native command registration must be enabled.
- `off|always|inbound|tagged` are per‑session toggles (`/tts on` is an alias for `/tts always`).
- `limit` and `summary` are stored in local prefs, not the main config.
- `/tts audio` generates a one-off audio reply (does not toggle TTS on).

## Agent tool

The `tts` tool converts text to speech and returns a `MEDIA:` path. When the
result is Telegram-compatible, the tool includes `[[audio_as_voice]]` so
Telegram sends a voice bubble.

## Gateway RPC

Gateway methods:

- `tts.status`
- `tts.enable`
- `tts.disable`
- `tts.convert`
- `tts.setProvider`
- `tts.providers`
