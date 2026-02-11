---
summary: "30. 严格的配置校验 + 仅 doctor 运行的迁移"
read_when:
  - 31. 设计或实现配置校验行为
  - 32. 处理配置迁移或 doctor 工作流
  - 33. 处理插件配置 schema 或插件加载门控
title: "Strict Config Validation"
---

# 35. 严格配置校验（仅 doctor 迁移）

## 36. 目标

- 37. **在所有位置拒绝未知的配置键**（根级 + 嵌套）。
- 38. **拒绝没有 schema 的插件配置**；不要加载该插件。
- 39. **移除加载时的遗留自动迁移**；迁移仅通过 doctor 运行。
- 40. **启动时自动运行 doctor（dry-run）**；如无效，则阻止非诊断命令。

## 41. 非目标

- 42. 加载时的向后兼容（遗留键不会自动迁移）。
- 43. 静默丢弃无法识别的键。

## Strict validation rules

- 45. 配置必须在每一层级都与 schema 完全匹配。
- 46. 未知键属于校验错误（根级或嵌套均不允许透传）。
- 47. `plugins.entries.<id>48. .config` 必须由该插件的 schema 进行校验。
  - 49. 如果插件缺少 schema，**拒绝加载插件**并显示清晰的错误。
- 50. 未知的 \`channels.<id>\`\` keys are errors unless a plugin manifest declares the channel id.
- Plugin manifests (`openclaw.plugin.json`) are required for all plugins.

## Plugin schema enforcement

- Each plugin provides a strict JSON Schema for its config (inline in the manifest).
- Plugin load flow:
  1. Resolve plugin manifest + schema (`openclaw.plugin.json`).
  2. Validate config against the schema.
  3. If missing schema or invalid config: block plugin load, record error.
- Error message includes:
  - Plugin id
  - Reason (missing schema / invalid config)
  - Path(s) that failed validation
- Disabled plugins keep their config, but Doctor + logs surface a warning.

## Doctor flow

- Doctor runs **every time** config is loaded (dry-run by default).
- If config invalid:
  - Print a summary + actionable errors.
  - Instruct: `openclaw doctor --fix`.
- `openclaw doctor --fix`:
  - Applies migrations.
  - Removes unknown keys.
  - Writes updated config.

## Command gating (when config is invalid)

Allowed (diagnostic-only):

- `openclaw doctor`
- `openclaw logs`
- `openclaw health`
- `openclaw help`
- `openclaw status`
- `openclaw gateway status`

Everything else must hard-fail with: “Config invalid. Run `openclaw doctor --fix`.”

## Error UX format

- Single summary header.
- Grouped sections:
  - Unknown keys (full paths)
  - Legacy keys / migrations needed
  - Plugin load failures (plugin id + reason + path)

## Implementation touchpoints

- `src/config/zod-schema.ts`: remove root passthrough; strict objects everywhere.
- `src/config/zod-schema.providers.ts`: ensure strict channel schemas.
- `src/config/validation.ts`: fail on unknown keys; do not apply legacy migrations.
- `src/config/io.ts`: remove legacy auto-migrations; always run doctor dry-run.
- `src/config/legacy*.ts`: move usage to doctor only.
- `src/plugins/*`: add schema registry + gating.
- CLI command gating in `src/cli`.

## Tests

- Unknown key rejection (root + nested).
- Plugin missing schema → plugin load blocked with clear error.
- Invalid config → gateway startup blocked except diagnostic commands.
- Doctor 干运行自动；`doctor --fix` 会写入修正后的配置。
