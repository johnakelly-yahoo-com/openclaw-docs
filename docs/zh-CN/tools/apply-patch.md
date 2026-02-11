---
summary: "使用 apply_patch 工具应用多文件补丁"
read_when:
  - 你需要跨多个文件的结构化文件编辑
  - 你想要记录或调试基于补丁的编辑
title: "apply_patch 工具"
---

# apply_patch 工具

使用结构化补丁格式应用文件更改。 这非常适合多文件
或多补丁块的编辑，在这种情况下单个 `edit` 调用会很脆弱。

该工具接受一个单一的 `input` 字符串，用于封装一个或多个文件操作：

```
*** Begin Patch
*** Add File: path/to/file.txt
+line 1
+line 2
*** Update File: src/app.ts
@@
-old line
+new line
*** Delete File: obsolete.txt
*** End Patch
```

## 参数

- `input`（必需）：完整的补丁内容，包括 `*** Begin Patch` 和 `*** End Patch`。

## 说明

- 路径相对于工作区根目录解析。
- 在 `*** Update File:` 补丁块中使用 `*** Move to:` 来重命名文件。
- 在需要时，`*** End of File` 用于标记仅在 EOF 处插入。
- 实验性功能，默认禁用。 通过 `tools.exec.applyPatch.enabled` 启用。
- 仅限 OpenAI（包括 OpenAI Codex）。 可选地按模型进行限制：
  `tools.exec.applyPatch.allowModels`。
- 配置仅位于 `tools.exec` 下。

## 示例

```json
{
  "tool": "apply_patch",
  "input": "*** Begin Patch\n*** Update File: src/index.ts\n@@\n-const foo = 1\n+const foo = 2\n*** End Patch"
}
```
