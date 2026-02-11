---
summary: "用于引导向导和配置 schema 的 RPC 协议说明"
read_when: "更改引导向导步骤或配置 schema 端点"
title: "Onboarding and Config Protocol"
---

# 引导 + 配置协议

Purpose: shared onboarding + config surfaces across CLI, macOS app, and Web UI.

## 组件

- 向导引擎（共享会话 + 提示 + 引导状态）。
- CLI 引导使用与 UI 客户端相同的向导流程。
- 网关 RPC 暴露向导和配置 schema 端点。
- macOS 引导使用向导步骤模型。
- Web UI 基于 JSON Schema + UI 提示渲染配置表单。

## 网关 RPC

- `wizard.start` 参数：`{ mode?: "local"|"remote", workspace?: string }`
- `wizard.next` 参数：`{ sessionId, answer?: { stepId, value? } }`
- `wizard.cancel` 参数：`{ sessionId }`
- `wizard.status` 参数：`{ sessionId }`
- `config.schema` 参数：`{}`

响应（结构）

- 向导：`{ sessionId, done, step?, status?, error? } }`
- 配置 schema：`{ schema, uiHints, version, generatedAt }`

## UI 提示

- `uiHints` 按路径作为键；可选元数据（label/help/group/order/advanced/sensitive/placeholder）。
- 敏感字段会渲染为密码输入；没有额外的脱敏层。
- 不受支持的 schema 节点将回退到原始 JSON 编辑器。

## 注意事项

- 本文档是跟踪引导/配置协议重构的唯一位置。
