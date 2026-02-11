---
summary: "Plugin manifest + JSON schema requirements (strict config validation)"
read_when:
  - You are building a OpenClaw plugin
  - 你需要提供一个插件配置模式，或调试插件验证错误
title: "插件清单"
---

# 插件清单（openclaw.plugin.json）

每个插件**必须**在**插件根目录**中提供一个 `openclaw.plugin.json` 文件。
OpenClaw 使用该清单在**不执行插件代码**的情况下验证配置。 缺失或无效的清单会被视为插件错误，并会阻止配置验证。

查看完整的插件系统指南：[Plugins](/tools/plugin)。

## 必需字段

```json
{
  "id": "voice-call",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

1. 必需的键：

- `id`（string）：规范化的插件 ID。
- `configSchema`（object）：插件配置的 JSON Schema（内联）。

可选键：

- `kind`（string）：插件类型（示例：`"memory"`）。
- `channels`（array）：该插件注册的通道 ID（示例：`["matrix"]`）。
- `providers`（array）：该插件注册的提供方 ID。
- 2. `skills`（数组）：要加载的技能目录（相对于插件根目录）。
- 3. `name`（字符串）：插件的显示名称。
- `description`（string）：插件的简要说明。
- `uiHints`（object）：用于 UI 渲染的配置字段标签/占位符/敏感标志。
- `version`（string）：插件版本（信息性）。

## JSON Schema 要求

- **每个插件都必须提供一个 JSON Schema**，即使它不接受任何配置。
- 可以接受空的 Schema（例如，`{ "type": "object", "additionalProperties": false }`）。
- 4. 架构在配置读/写时进行验证，而不是在运行时。

## 验证行为

- 未知的 `channels.*` 键被视为**错误**，除非该通道 ID 由某个插件清单声明。
- `plugins.entries.<id>`, `plugins.allow`, `plugins.deny` 和 `plugins.slots.*`
  必须引用**可发现的**插件 ID。 未知的 ID 会被视为**错误**。
- 如果插件已安装但其清单或 Schema 损坏或缺失，验证将失败，Doctor 会报告插件错误。
- 如果存在插件配置但插件被**禁用**，配置将被保留，并且 Doctor + 日志中会显示**警告**。

## 说明

- 清单对**所有插件都是必需的**，包括从本地文件系统加载的插件。
- 运行时仍会单独加载插件模块；清单仅用于发现 + 验证。
- 如果你的插件依赖原生模块，请记录构建步骤以及任何包管理器的允许列表要求（例如，pnpm `allow-build-scripts`
  - `pnpm rebuild <package>`）。
