---
summary: "Use OpenCode Zen (curated models) with OpenClaw"
read_when:
  - You want OpenCode Zen for model access
  - You want a curated list of coding-friendly models
title: "OpenCode Zen"
---

# OpenCode Zen

OpenCode Zen is a **curated list of models** recommended by the OpenCode team for coding agents.
It is an optional, hosted model access path that uses an API key and the `opencode` provider.
Zen 目前处于测试版。

## CLI setup

```bash
openclaw onboard --auth-choice opencode-zen
# or non-interactive
openclaw onboard --opencode-zen-api-key "$OPENCODE_API_KEY"
```

## Config snippet

```json5
{
  env: { OPENCODE_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-6" } } },
}
```

## Notes

- `OPENCODE_ZEN_API_KEY` is also supported.
- 你登录 Zen，添加计费信息，并复制你的 API 密钥。
- OpenCode Zen bills per request; check the OpenCode dashboard for details.
