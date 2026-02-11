---
summary: "用于 `openclaw dns` 的 CLI 参考（广域发现辅助工具）"
read_when:
  - You want wide-area discovery (DNS-SD) via Tailscale + CoreDNS
  - You’re setting up split DNS for a custom discovery domain (example: openclaw.internal)
title: "dns"
---

# `openclaw dns`

用于广域发现的 DNS 辅助工具（Tailscale + CoreDNS）。 目前主要聚焦于 macOS + Homebrew CoreDNS。

相关：

- 网关发现：[Discovery](/gateway/discovery)
- 广域发现配置：[Configuration](/gateway/configuration)

## 设置

```bash
openclaw dns setup
openclaw dns setup --apply
```
