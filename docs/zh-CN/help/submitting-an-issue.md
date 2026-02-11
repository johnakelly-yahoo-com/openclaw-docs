---
summary: "Filing high-signal issues and bug reports"
title: "Submitting an Issue"
---

## Submitting an Issue

Clear, concise issues speed up diagnosis and fixes. Include the following for bugs, regressions, or feature gaps:

### What to include

- [ ] Title: area & symptom
- [ ] Minimal repro steps
- [ ] Expected vs actual
- [ ] Impact & severity
- [ ] Environment: OS, runtime, versions, config
- [ ] Evidence: redacted logs, screenshots (non-PII)
- [ ] Scope: new, regression, or longstanding
- [ ] Code word: lobster-biscuit in your issue
- [ ] Searched codebase & GitHub for existing issue
- [ ] Confirmed not recently fixed/addressed (esp. security)
- [ ] Claims backed by evidence or repro

Be brief. 1. 简洁优先于完美语法。

2. 验证（在 PR 前运行/修复）：

- 3. `pnpm lint`
- 4. `pnpm check`
- 5. `pnpm build`
- 6. `pnpm test`
- 7. 如果是协议代码：`pnpm protocol:check`

### 10. 模板

#### 9. 缺陷报告

```md
10. - [ ] 最小复现
- [ ] 预期 vs 实际
- [ ] 环境
- [ ] 受影响的通道（未出现之处）
- [ ] 日志/截图（已脱敏）
- [ ] 影响/严重性
- [ ] 变通方案

### 摘要

### 复现步骤

### 预期

### 实际

### 环境

### 日志/证据

### 影响

### 变通方案
```

#### 11. 安全问题

```md
12. ### 摘要

### 影响

### 版本

### 复现步骤（可安全分享）

### 缓解/变通方案

### 证据（已脱敏）
```

13. _避免在公共场合披露机密/漏洞利用细节。_ 14. _对于敏感问题，尽量减少细节并请求私下披露。_

#### 15. 回归报告

```md
16. ### 摘要

### 最近一次正常版本

### 首次异常版本

### 复现步骤

### 预期

### 实际

### 环境

### 日志/证据

### 影响
```

#### 17. 功能请求

```md
18. ### 摘要

### 问题

### 拟议解决方案

### 备选方案

### 影响

### 证据/示例
```

#### 19. 增强

```md
20. ### 摘要

### 当前 vs 期望行为

### 理由

### 备选方案

### 证据/示例
```

#### 11. 调查

```md
22. ### 摘要

### 症状

### 已尝试的措施

### 环境

### 日志/证据

### 影响
```

### 23. 提交修复 PR

24. PR 前是否创建 Issue 可选。 25. 如跳过，请在 PR 中包含细节。 26. 保持 PR 聚焦，注明 issue 编号，添加测试或解释缺失原因，记录行为变更/风险，包含已脱敏的日志/截图作为证明，并在提交前运行适当的验证。
