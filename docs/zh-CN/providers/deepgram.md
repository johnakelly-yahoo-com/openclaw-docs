---
summary: "用于入站语音备注的 Deepgram 转写"
read_when:
  - 你想为音频附件使用 Deepgram 语音转文本
  - 你需要一个快速的 Deepgram 配置示例
title: "Deepgram"
---

# Deepgram（音频转写）

Deepgram 是一个语音转文本 API。 在 OpenClaw 中，它通过 `tools.media.audio` 用于**入站音频/语音备注转写**。

启用后，OpenClaw 会将音频文件上传到 Deepgram，并将转写内容注入回复流水线（`{{Transcript}}` + `[Audio]` 块）。 这**不是流式**；
它使用预录音的转写端点。

网站：[https://deepgram.com](https://deepgram.com)  
文档：[https://developers.deepgram.com](https://developers.deepgram.com)

## 快速开始

1. 设置你的 API 密钥：

```
DEEPGRAM_API_KEY=dg_...
```

2. 启用提供商：

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "deepgram", model: "nova-3" }],
      },
    },
  },
}
```

## 选项

- `model`：Deepgram 模型 ID（默认：`nova-3`）
- `language`：语言提示（可选）
- `tools.media.audio.providerOptions.deepgram.detect_language`：启用语言检测（可选）
- `tools.media.audio.providerOptions.deepgram.punctuate`：启用标点（可选）
- `tools.media.audio.providerOptions.deepgram.smart_format`：启用智能格式化（可选）

包含语言的示例：

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "deepgram", model: "nova-3", language: "en" }],
      },
    },
  },
}
```

Example with Deepgram options:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        providerOptions: {
          deepgram: {
            detect_language: true,
            punctuate: true,
            smart_format: true,
          },
        },
        models: [{ provider: "deepgram", model: "nova-3" }],
      },
    },
  },
}
```

## Notes

- Authentication follows the standard provider auth order; `DEEPGRAM_API_KEY` is the simplest path.
- Override endpoints or headers with `tools.media.audio.baseUrl` and `tools.media.audio.headers` when using a proxy.
- Output follows the same audio rules as other providers (size caps, timeouts, transcript injection).
