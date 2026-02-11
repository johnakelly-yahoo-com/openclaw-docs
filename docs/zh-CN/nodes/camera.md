---
summary: "6. 供代理使用的相机采集（iOS 节点 + macOS 应用）：照片（jpg）和短视频片段（mp4）"
read_when:
  - 7. 在 iOS 节点或 macOS 上添加或修改相机采集
  - 8. 扩展代理可访问的 MEDIA 临时文件工作流
title: "9. 相机采集"
---

# 10. 相机采集（代理）

11. OpenClaw 支持用于代理工作流的**相机采集**：

- 12. **iOS 节点**（通过 Gateway 配对）：通过 `node.invoke` 捕获**照片**（`jpg`）或**短视频片段**（`mp4`，可选音频）。
- 13. **Android 节点**（通过 Gateway 配对）：通过 `node.invoke` 捕获**照片**（`jpg`）或**短视频片段**（`mp4`，可选音频）。
- 14. **macOS 应用**（通过 Gateway 的节点）：通过 `node.invoke` 捕获**照片**（`jpg`）或**短视频片段**（`mp4`，可选音频）。

15. 所有相机访问均受**用户可控设置**限制。

## 16. iOS 节点

### 17. 用户设置（默认开启）

- 18. iOS 设置页 → **相机** → **允许相机**（`camera.enabled`）
  - 19. 默认：**开启**（缺少该键视为已启用）。
  - 20. 关闭时：`camera.*` 命令返回 `CAMERA_DISABLED`。

### 21. 命令（通过 Gateway 的 `node.invoke`）

- 22. `camera.list`
  - 23. 响应负载：
    - 24. `devices`：由 `{ id, name, position, deviceType }` 组成的数组

- 25. `camera.snap`
  - 26. 参数：
    - 27. `facing`：`front|back`（默认：`front`）
    - 28. `maxWidth`：number（可选；iOS 节点默认 `1600`）
    - 29. `quality`：`0..1`（可选；默认 `0.9`）
    - 30. `format`：当前为 `jpg`
    - 31. `delayMs`：number（可选；默认 `0`）
    - 32. `deviceId`：string（可选；来自 `camera.list`）
  - 33. 响应负载：
    - 34. `format: "jpg"`
    - 35. `base64: "<...>"`
    - 36. `width`、`height`
  - 37. 负载限制：照片会被重新压缩，以将 base64 负载保持在 5 MB 以下。

- 38. `camera.clip`
  - 39. 参数：
    - 40. `facing`：`front|back`（默认：`front`）
    - 41. `durationMs`：number（默认 `3000`，上限钳制为 `60000`）
    - 42. `includeAudio`：boolean（默认 `true`）
    - 43. `format`：当前为 `mp4`
    - 44. `deviceId`：string（可选；来自 `camera.list`）
  - 45. 响应负载：
    - 46. `format: "mp4"`
    - 47. `base64: "<...>"`
    - 48. `durationMs`
    - 49. `hasAudio`

### 50. 前台要求

Like `canvas.*`, the iOS node only allows `camera.*` commands in the **foreground**. Background invocations return `NODE_BACKGROUND_UNAVAILABLE`.

### CLI helper (temp files + MEDIA)

The easiest way to get attachments is via the CLI helper, which writes decoded media to a temp file and prints `MEDIA:<path>`.

Examples:

```bash
openclaw nodes camera snap --node <id>               # default: both front + back (2 MEDIA lines)
openclaw nodes camera snap --node <id> --facing front
openclaw nodes camera clip --node <id> --duration 3000
openclaw nodes camera clip --node <id> --no-audio
```

Notes:

- `nodes camera snap` defaults to **both** facings to give the agent both views.
- Output files are temporary (in the OS temp directory) unless you build your own wrapper.

## Android node

### Android user setting (default on)

- Android Settings sheet → **Camera** → **Allow Camera** (`camera.enabled`)
  - Default: **on** (missing key is treated as enabled).
  - When off: `camera.*` commands return `CAMERA_DISABLED`.

### Permissions

- Android requires runtime permissions:
  - `CAMERA` for both `camera.snap` and `camera.clip`.
  - `RECORD_AUDIO` for `camera.clip` when `includeAudio=true`.

If permissions are missing, the app will prompt when possible; if denied, `camera.*` requests fail with a
`*_PERMISSION_REQUIRED` error.

### Android foreground requirement

Like `canvas.*`, the Android node only allows `camera.*` commands in the **foreground**. Background invocations return `NODE_BACKGROUND_UNAVAILABLE`.

### Payload guard

Photos are recompressed to keep the base64 payload under 5 MB.

## macOS app

### User setting (default off)

The macOS companion app exposes a checkbox:

- **Settings → General → Allow Camera** (`openclaw.cameraEnabled`)
  - Default: **off**
  - When off: camera requests return “Camera disabled by user”.

### CLI helper (node invoke)

Use the main `openclaw` CLI to invoke camera commands on the macOS node.

Examples:

```bash
openclaw nodes camera list --node <id>            # list camera ids
openclaw nodes camera snap --node <id>            # prints MEDIA:<path>
openclaw nodes camera snap --node <id> --max-width 1280
openclaw nodes camera snap --node <id> --delay-ms 2000
openclaw nodes camera snap --node <id> --device-id <id>
openclaw nodes camera clip --node <id> --duration 10s          # prints MEDIA:<path>
openclaw nodes camera clip --node <id> --duration-ms 3000      # prints MEDIA:<path> (legacy flag)
openclaw nodes camera clip --node <id> --device-id <id>
openclaw nodes camera clip --node <id> --no-audio
```

Notes:

- `openclaw nodes camera snap` defaults to `maxWidth=1600` unless overridden.
- On macOS, `camera.snap` waits `delayMs` (default 2000ms) after warm-up/exposure settle before capturing.
- Photo payloads are recompressed to keep base64 under 5 MB.

## Safety + practical limits

- Camera and microphone access trigger the usual OS permission prompts (and require usage strings in Info.plist).
- Video clips are capped (currently `<= 60s`) to avoid oversized node payloads (base64 overhead + message limits).

## macOS screen video (OS-level)

For _screen_ video (not camera), use the macOS companion:

```bash
openclaw nodes screen record --node <id> --duration 10s --fps 15   # prints MEDIA:<path>
```

Notes:

- Requires macOS **Screen Recording** permission (TCC).
