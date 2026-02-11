---
summary: "44. `openclaw status` 的 CLI 参考（诊断、探测、使用情况快照）"
read_when:
  - 45. 你想快速诊断频道健康状况 + 最近的会话接收方
  - 46. 你想要一个可粘贴的“全部”状态用于调试
title: "47. status"
---

# 48. `openclaw status`

49. 用于频道 + 会话的诊断。

```bash
50. openclaw status
openclaw status --all
openclaw status --deep
openclaw status --usage
```

Notes:

- `--deep` runs live probes (WhatsApp Web + Telegram + Discord + Google Chat + Slack + Signal).
- Output includes per-agent session stores when multiple agents are configured.
- Overview includes Gateway + node host service install/runtime status when available.
- 30. 概览包含更新通道 + git SHA（用于源码检出）。
- Update info surfaces in the Overview; if an update is available, status prints a hint to run `openclaw update` (see [Updating](/install/updating)).
