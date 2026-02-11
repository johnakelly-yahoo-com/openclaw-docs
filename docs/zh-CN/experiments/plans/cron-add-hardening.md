---
summary: "加强 cron.add 输入处理、对齐 schema，并改进 cron UI/agent 工具。"
owner: "openclaw"
status: "完成"
last_updated: "2026-01-05"
title: "Cron 添加加固"
---

# Cron 添加加固与架构对齐

## 背景

最近的网关日志显示多次 `cron.add` 失败，原因是参数无效（缺少 `sessionTarget`、`wakeMode`、`payload`，以及格式错误的 `schedule`）。 这表明至少有一个客户端（很可能是代理工具调用路径）正在发送被包装或部分指定的作业负载。 另外，TypeScript 中的 cron 提供方枚举、网关架构、CLI 标志以及 UI 表单类型之间存在漂移；同时 `cron.status` 在 UI 中也存在不匹配（期望 `jobCount`，而网关返回 `jobs`）。

## 目标

- 通过规范化常见的包装负载并推断缺失的 `kind` 字段，停止 `cron.add` 的 INVALID_REQUEST 垃圾错误。
- 在网关架构、cron 类型、CLI 文档和 UI 表单之间对齐 cron 提供方列表。
- 使代理 cron 工具架构显式化，以便 LLM 生成正确的作业负载。
- 修复 Control UI 中 cron 状态的作业计数显示。
- Add tests to cover normalization and tool behavior.

## 非目标

- 更改 cron 调度语义或作业执行行为。
- 添加新的调度类型或 cron 表达式解析。
- 除必要的字段修复外，不对 cron 的 UI/UX 进行全面改造。

## Findings (current gaps)

- 网关中的 `CronPayloadSchema` 排除了 `signal` 和 `imessage`，而 TS 类型中包含它们。
- Control UI 的 CronStatus 期望 `jobCount`，但网关返回 `jobs`。
- Agent cron tool schema allows arbitrary `job` objects, enabling malformed inputs.
- 网关对 `cron.add` 进行严格校验且不做规范化，因此被包装的负载会失败。

## 变更内容

- `cron.add` 和 `cron.update` 现在会规范化常见的包装形态并推断缺失的 `kind` 字段。
- 代理 cron 工具架构与网关架构一致，从而减少无效负载。
- Provider enums are aligned across gateway, CLI, UI, and macOS picker.
- Control UI 使用网关返回的 `jobs` 计数字段来显示状态。

## Current behavior

- **Normalization:** wrapped `data`/`job` payloads are unwrapped; `schedule.kind` and `payload.kind` are inferred when safe.
- **默认值：** 在缺失时为 `wakeMode` 和 `sessionTarget` 应用安全默认值。
- **提供方：** Discord/Slack/Signal/iMessage 现在在 CLI/UI 中一致呈现。

请参阅 [Cron jobs](/automation/cron-jobs) 了解规范化后的结构和示例。

## 验证

- 观察网关日志，确认 `cron.add` 的 INVALID_REQUEST 错误减少。
- 刷新后确认 Control UI 的 cron 状态显示作业计数。

## 可选后续

- 手动进行 Control UI 冒烟测试：为每个提供方添加一个 cron 作业并验证状态作业计数。

## Open Questions

- `cron.add` 是否应接受来自客户端的显式 `state`（目前架构不允许）？
- 是否应允许 `webchat` 作为显式投递提供方（当前在投递解析中被过滤）？
