---
summary: "36. 用于工作流的仅 JSON LLM 任务（可选插件工具）"
read_when:
  - 37. 你希望在工作流中加入一个仅 JSON 的 LLM 步骤
  - 38. 你需要用于自动化的、经过架构验证的 LLM 输出
title: "39. LLM 任务"
---

# 40. LLM 任务

41. `llm-task` 是一个**可选的插件工具**，用于运行仅 JSON 的 LLM 任务并返回结构化输出（可选地根据 JSON Schema 进行验证）。

42. 这非常适合像 Lobster 这样的工作流引擎：你可以添加一个单独的 LLM 步骤，而无需为每个工作流编写自定义 OpenClaw 代码。

## 43. 启用插件

1. 44. 启用插件：```
   {
     "plugins": {
       "entries": {
         "llm-task": { "enabled": true }
       }
     }
   }
   ```

````json
45. 将该工具加入允许列表（它以 `optional: true` 注册）：
```
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "allow": ["llm-task"] }
      }
    ]
  }
}
```
````

2. 46. 配置（可选）

````json
47. ```
{
  "plugins": {
    "entries": {
      "llm-task": {
        "enabled": true,
        "config": {
          "defaultProvider": "openai-codex",
          "defaultModel": "gpt-5.2",
          "defaultAuthProfileId": "main",
          "allowedModels": ["openai-codex/gpt-5.3-codex"],
          "maxTokens": 800,
          "timeoutMs": 30000
        }
      }
    }
  }
}
```
````

## 48. `allowedModels` 是由 `provider/model` 字符串组成的允许列表。

```json
{
  "plugins": {
    "entries": {
      "llm-task": {
        "enabled": true,
        "config": {
          "defaultProvider": "openai-codex",
          "defaultModel": "gpt-5.2",
          "defaultAuthProfileId": "main",
          "allowedModels": ["openai-codex/gpt-5.3-codex"],
          "maxTokens": 800,
          "timeoutMs": 30000
        }
      }
    }
  }
}
```

`allowedModels` is an allowlist of `provider/model` strings. 1. 如果设置，列表之外的任何请求都会被拒绝。

## 2. 工具参数

- 3. `prompt`（字符串，必填）
- 4. `input`（任意类型，可选）
- 5. `schema`（对象，可选的 JSON Schema）
- 6. `provider`（字符串，可选）
- 7. `model`（字符串，可选）
- 8. `authProfileId`（字符串，可选）
- 9. `temperature`（数字，可选）
- 10. `maxTokens`（数字，可选）
- 11. `timeoutMs`（数字，可选）

## 12. 输出

13. 返回包含解析后 JSON 的 `details.json`（如果提供了 `schema`，则会根据其进行校验）。

## 14. 示例：Lobster 工作流步骤

```lobster
15. openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
  "input": {
    "subject": "Hello",
    "body": "Can you help?"
  },
  "schema": {
    "type": "object",
    "properties": {
      "intent": { "type": "string" },
      "draft": { "type": "string" }
    },
    "required": ["intent", "draft"],
    "additionalProperties": false
  }
}'
```

## 16. 安全说明

- 17. 该工具为**仅 JSON**，并指示模型只输出 JSON（不使用代码围栏，不添加说明性文字）。
- 18. 本次运行不会向模型暴露任何工具。
- 19. 除非使用 `schema` 进行校验，否则应将输出视为不可信。
- 20. 在任何产生副作用的步骤（发送、发布、执行）之前放置审批。
