---
summary: "20. 入站图像/音频/视频理解（可选），支持提供商 + CLI 回退"
read_when:
  - 21. 设计或重构媒体理解
  - 22. 调优入站音频/视频/图像预处理
title: "23. 媒体理解"
---

# 24. 媒体理解（入站）— 2026-01-17

25. OpenClaw 可在回复流水线运行前 **汇总入站媒体**（图像/音频/视频）。 26. 它会自动检测本地工具或提供商密钥是否可用，并且可以被禁用或自定义。 27. 如果关闭理解，模型仍会像往常一样接收原始文件/URL。

## 28. 目标

- 29. 可选：将入站媒体预消化为简短文本，以实现更快路由 + 更好的命令解析。
- 30. 始终保留向模型交付原始媒体（始终）。
- 31. 支持 **提供商 API** 和 **CLI 回退**。
- 32. 允许多个模型并按顺序回退（错误/大小/超时）。

## 33. 高层行为

1. 34. 收集入站附件（`MediaPaths`、`MediaUrls`、`MediaTypes`）。
2. 35. 对于每个启用的能力（图像/音频/视频），按策略选择附件（默认：**第一个**）。
3. 36. 选择第一个符合条件的模型条目（大小 + 能力 + 鉴权）。
4. 37. 如果模型失败或媒体过大，**回退到下一个条目**。
5. 38. 成功时：
   - 39. `Body` 变为 `[Image]`、`[Audio]` 或 `[Video]` 块。
   - 40. 音频设置 `{{Transcript}}`；命令解析在存在字幕时使用字幕文本，否则使用转写文本。
   - 41. 字幕会作为 `User text:` 保留在块内。

42) 如果理解失败或被禁用，**回复流程将继续**，并使用原始正文 + 附件。

## 43. 配置概览

44. `tools.media` 支持 **共享模型** 以及按能力的覆盖：

- 45. `tools.media.models`：共享模型列表（使用 `capabilities` 进行门控）。
- 46. `tools.media.image` / `tools.media.audio` / `tools.media.video`：
  - 47. 默认项（`prompt`、`maxChars`、`maxBytes`、`timeoutSeconds`、`language`）
  - 48. 提供商覆盖（`baseUrl`、`headers`、`providerOptions`）
  - 49. 通过 `tools.media.audio.providerOptions.deepgram` 的 Deepgram 音频选项
  - 50. 可选的 **按能力 `models` 列表**（优先于共享模型）
  - `attachments` 策略（`mode`、`maxAttachments`、`prefer`）
  - `scope`（按 channel/chatType/session key 的可选门控）
- `tools.media.concurrency`：最大并发能力运行数（默认 **2**）。

```json5
{
  tools: {
    media: {
      models: [
        /* 共享列表 */
      ],
      image: {
        /* 可选覆盖 */
      },
      audio: {
        /* 可选覆盖 */
      },
      video: {
        /* 可选覆盖 */
      },
    },
  },
}
```

### 模型条目

每个 `models[]` 条目可以是 **provider** 或 **CLI**：

```json5
{
  type: "provider", // 若省略则为默认
  provider: "openai",
  model: "gpt-5.2",
  prompt: "Describe the image in <= 500 chars.",
  maxChars: 500,
  maxBytes: 10485760,
  timeoutSeconds: 60,
  capabilities: ["image"], // 可选，用于多模态条目
  profile: "vision-profile",
  preferredProfile: "vision-fallback",
}
```

```json5
{
  type: "cli",
  command: "gemini",
  args: [
    "-m",
    "gemini-3-flash",
    "--allowed-tools",
    "read_file",
    "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
  ],
  maxChars: 500,
  maxBytes: 52428800,
  timeoutSeconds: 120,
  capabilities: ["video", "image"],
}
```

CLI 模板还可以使用：

- `{{MediaDir}}`（包含媒体文件的目录）
- `{{OutputDir}}`（为本次运行创建的临时目录）
- `{{OutputBase}}`（临时文件基路径，无扩展名）

## 默认值与限制

推荐默认值：

- `maxChars`：用于图片/视频为 **500**（简短、便于命令行）
- `maxChars`：用于音频为 **未设置**（完整转写，除非你设置限制）
- `maxBytes`：
  - 图片：**10MB**
  - 音频：**20MB**
  - 视频：**50MB**

规则：

- 如果媒体超过 `maxBytes`，则跳过该模型并**尝试下一个模型**。
- 如果模型返回内容超过 `maxChars`，输出将被截断。
- `prompt` 默认是简单的“Describe the {media}.”，并附加 `maxChars` 指引（仅图片/视频）。
- 如果 `<capability>.enabled: true` 但未配置任何模型，当其提供方支持该能力时，OpenClaw 会尝试**当前回复模型**。

### 自动检测媒体理解（默认）

如果未将 `tools.media.<capability>
.enabled` 设置为 `false`，且你尚未配置模型，OpenClaw 会按以下顺序自动检测，并在**第一个可用选项**处停止：**本地 CLI**（仅音频；若已安装）

1. `sherpa-onnx-offline`（需要 `SHERPA_ONNX_MODEL_DIR`，包含 encoder/decoder/joiner/tokens）
   - `whisper-cli`（`whisper-cpp`；使用 `WHISPER_CPP_MODEL` 或内置的 tiny 模型）
   - `whisper`（Python CLI；自动下载模型）
   - **Gemini CLI**（`gemini`），使用 `read_many_files`
2. **提供方密钥**
3. 音频：OpenAI → Groq → Deepgram → Google
   - 图片：OpenAI → Anthropic → Google → MiniMax
   - 视频：Google
   - 要禁用自动检测，请设置：

{
tools: {
media: {
audio: {
enabled: false,
},
},
},
}

```json5
注意：二进制检测在 macOS/Linux/Windows 上尽力而为；请确保 CLI 位于 `PATH` 中（我们会展开 `~`），或使用带完整命令路径的显式 CLI 模型。
```

能力（可选）

## 如果你设置了 `capabilities`，该条目仅会针对这些媒体类型运行。

对于共享列表，OpenClaw 可以推断默认值： `openai`、`anthropic`、`minimax`：**image**

- `google`（Gemini API）：**image + audio + video**
- `groq`：**audio**
- `deepgram`：**audio**
- 对于 CLI 条目，**请显式设置 `capabilities`** 以避免意外匹配。

如果省略 `capabilities`，该条目将适用于其所在的列表。
提供方支持矩阵（OpenClaw 集成）

## Provider support matrix (OpenClaw integrations)

| Capability | Provider integration                             | Notes                                                                                |
| ---------- | ------------------------------------------------ | ------------------------------------------------------------------------------------ |
| Image      | OpenAI / Anthropic / Google / others via `pi-ai` | Any image-capable model in the registry works.                       |
| Audio      | OpenAI, Groq, Deepgram, Google                   | Provider transcription (Whisper/Deepgram/Gemini). |
| Video      | Google (Gemini API)           | Provider video understanding.                                        |

## Recommended providers

**Image**

- Prefer your active model if it supports images.
- Good defaults: `openai/gpt-5.2`, `anthropic/claude-opus-4-6`, `google/gemini-3-pro-preview`.

**Audio**

- `openai/gpt-4o-mini-transcribe`, `groq/whisper-large-v3-turbo`, or `deepgram/nova-3`.
- CLI fallback: `whisper-cli` (whisper-cpp) or `whisper`.
- Deepgram setup: [Deepgram (audio transcription)](/providers/deepgram).

**Video**

- `google/gemini-3-flash-preview` (fast), `google/gemini-3-pro-preview` (richer).
- CLI fallback: `gemini` CLI (supports `read_file` on video/audio).

## Attachment policy

Per‑capability `attachments` controls which attachments are processed:

- `mode`: `first` (default) or `all`
- `maxAttachments`：限制处理的数量（默认 **1**）。
- `prefer`: `first`, `last`, `path`, `url`

When `mode: "all"`, outputs are labeled `[Image 1/2]`, `[Audio 2/2]`, etc.

## Config examples

### 1. Shared models list + overrides

```json5
{
  tools: {
    media: {
      models: [
        { provider: "openai", model: "gpt-5.2", capabilities: ["image"] },
        {
          provider: "google",
          model: "gemini-3-flash-preview",
          capabilities: ["image", "audio", "video"],
        },
        {
          type: "cli",
          command: "gemini",
          args: [
            "-m",
            "gemini-3-flash",
            "--allowed-tools",
            "read_file",
            "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
          ],
          capabilities: ["image", "video"],
        },
      ],
      audio: {
        attachments: { mode: "all", maxAttachments: 2 },
      },
      video: {
        maxChars: 500,
      },
    },
  },
}
```

### 2. Audio + Video only (image off)

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          {
            type: "cli",
            command: "whisper",
            args: ["--model", "base", "{{MediaPath}}"],
          },
        ],
      },
      video: {
        enabled: true,
        maxChars: 500,
        models: [
          { provider: "google", model: "gemini-3-flash-preview" },
          {
            type: "cli",
            command: "gemini",
            args: [
              "-m",
              "gemini-3-flash",
              "--allowed-tools",
              "read_file",
              "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
            ],
          },
        ],
      },
    },
  },
}
```

### 3. Optional image understanding

```json5
{
  tools: {
    media: {
      image: {
        enabled: true,
        maxBytes: 10485760,
        maxChars: 500,
        models: [
          { provider: "openai", model: "gpt-5.2" },
          { provider: "anthropic", model: "claude-opus-4-6" },
          {
            type: "cli",
            command: "gemini",
            args: [
              "-m",
              "gemini-3-flash",
              "--allowed-tools",
              "read_file",
              "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
            ],
          },
        ],
      },
    },
  },
}
```

### 4. Multi‑modal single entry (explicit capabilities)

```json5
{
  tools: {
    media: {
      image: {
        models: [
          {
            provider: "google",
            model: "gemini-3-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
      audio: {
        models: [
          {
            provider: "google",
            model: "gemini-3-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
      video: {
        models: [
          {
            provider: "google",
            model: "gemini-3-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
    },
  },
}
```

## Status output

When media understanding runs, `/status` includes a short summary line:

```
📎 Media: image ok (openai/gpt-5.2) · audio skipped (maxBytes)
```

This shows per‑capability outcomes and the chosen provider/model when applicable.

## Notes

- Understanding is **best‑effort**. Errors do not block replies.
- Attachments are still passed to models even when understanding is disabled.
- Use `scope` to limit where understanding runs (e.g. only DMs).

## Related docs

- [Configuration](/gateway/configuration)
- [Image & Media Support](/nodes/images)
