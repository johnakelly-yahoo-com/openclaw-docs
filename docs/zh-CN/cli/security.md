---
summary: "1. `openclaw security` 的 CLI 参考（审计并修复常见的安全隐患）"
read_when:
  - 2. 你想对配置/状态运行一次快速的安全审计
  - 3. 你想应用安全的“修复”建议（chmod、收紧默认设置）
title: "4. security"
---

# 23. `openclaw security`

24. 安全工具（审计 + 可选修复）。

7. 相关：

- 8. 安全指南：[Security](/gateway/security)

## 25. 审计

```bash
10. openclaw security audit
openclaw security audit --deep
openclaw security audit --fix
```

11. 当多个 DM 发送者共享主会话时，审计会发出警告，并为共享收件箱推荐 **安全 DM 模式**：`session.dmScope="per-channel-peer"`（或用于多账号频道的 `per-account-channel-peer`）。
12. 当在未启用沙箱的情况下使用小模型（`<=300B`）且启用了 Web/浏览器工具时，也会发出警告。
