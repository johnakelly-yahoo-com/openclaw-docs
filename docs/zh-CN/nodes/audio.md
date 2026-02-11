---
summary: "7. 入站音频/语音备注如何被下载、转录并注入到回复中"
read_when:
  - 8. 更改音频转录或媒体处理
title: "9. 音频和语音备注"
---

# 10. 音频 / 语音备注 — 2026-01-17

## 11. 可用功能

- 12. **媒体理解（音频）**：如果启用（或自动检测）音频理解，OpenClaw：
  1. 13. 定位第一个音频附件（本地路径或 URL），并在需要时下载。
  2. 14. 在发送到每个模型条目之前强制执行 `maxBytes`。
  3. 15. 按顺序运行第一个符合条件的模型条目（提供方或 CLI）。
  4. 16. 如果失败或跳过（大小/超时），则尝试下一个条目。
  5. 17. 成功后，将 `Body` 替换为 `[Audio]` 块并设置 `{{Transcript}}`。
- **命令解析**：当转录成功时，会将 `CommandBody`/`RawBody` 设置为转录文本，从而保证斜杠命令仍然可用。
- 19. **详细日志**：在 `--verbose` 模式下，我们会记录转录运行以及替换正文的时机。

## 20. 自动检测（默认）

21. 如果你**未配置模型**且未将 `tools.media.audio.enabled` 设置为 `false`，
    OpenClaw 将按以下顺序自动检测，并在找到第一个可用选项时停止：

1. 22. **本地 CLI**（如果已安装）
   - 23. `sherpa-onnx-offline`（需要包含 encoder/decoder/joiner/tokens 的 `SHERPA_ONNX_MODEL_DIR`）
   - 24. `whisper-cli`（来自 `whisper-cpp`；使用 `WHISPER_CPP_MODEL` 或随附的 tiny 模型）
   - 25. `whisper`（Python CLI；自动下载模型）
2. 26. **Gemini CLI**（`gemini`），使用 `read_many_files`
3. 27. **提供方密钥**（OpenAI → Groq → Deepgram → Google）

28) 要禁用自动检测，请设置 `tools.media.audio.enabled: false`。
29) 要进行自定义，请设置 `tools.media.audio.models`。
30) 注意：在 macOS/Linux/Windows 上的二进制检测为尽力而为；请确保 CLI 在 `PATH` 中（我们会展开 `~`），或使用包含完整命令路径的显式 CLI 模型。

## 31. 配置示例

### 32. 提供方 + CLI 回退（OpenAI + Whisper CLI）

```json5
33. {
  tools: {
    media: {
      audio: {
        enabled: true,
        maxBytes: 20971520,
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          {
            type: "cli",
            command: "whisper",
            args: ["--model", "base", "{{MediaPath}}"],
            timeoutSeconds: 45,
          },
        ],
      },
    },
  },
}
```

### 34. 仅提供方并带作用域控制

```json5
35. {
  tools: {
    media: {
      audio: {
        enabled: true,
        scope: {
          default: "allow",
          rules: [{ action: "deny", match: { chatType: "group" } }],
        },
        models: [{ provider: "openai", model: "gpt-4o-mini-transcribe" }],
      },
    },
  },
}
```

### 36. 仅提供方（Deepgram）

```json5
37. {
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

## 38. 说明与限制

- 39. 提供方认证遵循标准模型认证顺序（认证配置、环境变量、`models.providers.*.apiKey`）。
- 40. 当使用 `provider: "deepgram"` 时，Deepgram 会读取 `DEEPGRAM_API_KEY`。
- 41. Deepgram 设置详情：[Deepgram（音频转录）](/providers/deepgram)。
- 42. 音频提供方可以通过 `tools.media.audio` 覆盖 `baseUrl`、`headers` 和 `providerOptions`。
- 43. 默认大小上限为 20MB（`tools.media.audio.maxBytes`）。 44. 超出大小限制的音频会被该模型跳过，并尝试下一个条目。
- 45. 音频的默认 `maxChars` **未设置**（完整转录）。 46. 设置 `tools.media.audio.maxChars` 或每个条目的 `maxChars` 以裁剪输出。
- 47. OpenAI 的自动默认模型为 `gpt-4o-mini-transcribe`；如需更高准确率，请设置 `model: "gpt-4o-transcribe"`。
- 48. 使用 `tools.media.audio.attachments` 处理多个语音备注（`mode: "all"` + `maxAttachments`）。
- 49. 转录文本可在模板中通过 `{{Transcript}}` 使用。
- 50. CLI 的 stdout 有上限（5MB）；请保持 CLI 输出简洁。

## 注意事项

- 2. 作用域规则采用“先匹配者优先”。 3. `chatType` 会被规范化为 `direct`、`group` 或 `room`。
- 4. 确保你的 CLI 以 0 退出并输出纯文本；JSON 需要通过 `jq -r .text` 进行处理。
- 5. 保持超时时间合理（`timeoutSeconds`，默认 60s），以避免阻塞回复队列。
