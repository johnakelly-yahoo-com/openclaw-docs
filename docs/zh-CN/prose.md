---
summary: "OpenProse: .prose workflows, slash commands, and state in OpenClaw"
read_when:
  - You want to run or write .prose workflows
  - You want to enable the OpenProse plugin
  - You need to understand state storage
title: "OpenProse"
---

# OpenProse

10. OpenProse 是一种可移植、以 Markdown 为先的工作流格式，用于编排 AI 会话。 11. 在 OpenClaw 中，它以插件形式提供，安装一个 OpenProse 技能包并附带一个 `/prose` 斜杠命令。 Programs live in `.prose` files and can spawn multiple sub-agents with explicit control flow.

Official site: [https://www.prose.md](https://www.prose.md)

## What it can do

- Multi-agent research + synthesis with explicit parallelism.
- Repeatable approval-safe workflows (code review, incident triage, content pipelines).
- 12. 可复用的 `.prose` 程序，可在受支持的代理运行时中运行。

## Install + enable

Bundled plugins are disabled by default. Enable OpenProse:

```bash
openclaw plugins enable open-prose
```

Restart the Gateway after enabling the plugin.

Dev/local checkout: `openclaw plugins install ./extensions/open-prose`

Related docs: [Plugins](/tools/plugin), [Plugin manifest](/plugins/manifest), [Skills](/tools/skills).

## Slash command

OpenProse registers `/prose` as a user-invocable skill command. It routes to the OpenProse VM instructions and uses OpenClaw tools under the hood.

Common commands:

```
/prose help
/prose run <file.prose>
/prose run <handle/slug>
/prose run <https://example.com/file.prose>
/prose compile <file.prose>
/prose examples
/prose update
```

## Example: a simple `.prose` file

```prose
# Research + synthesis with two agents running in parallel.

input topic: "What should we research?"

agent researcher:
  model: sonnet
  prompt: "You research thoroughly and cite sources."

agent writer:
  model: opus
  prompt: "You write a concise summary."

parallel:
  findings = session: researcher
    prompt: "Research {topic}."
  draft = session: writer
    prompt: "Summarize {topic}."

session "Merge the findings + draft into a final answer."
context: { findings, draft }
```

## File locations

OpenProse keeps state under `.prose/` in your workspace:

```
.prose/
├── .env
├── runs/
│   └── {YYYYMMDD}-{HHMMSS}-{random}/
│       ├── program.prose
│       ├── state.md
│       ├── bindings/
│       └── agents/
└── agents/
```

User-level persistent agents live at:

```
~/.prose/agents/
```

## State modes

OpenProse supports multiple state backends:

- **filesystem** (default): `.prose/runs/...`
- **in-context**: transient, for small programs
- **sqlite** (experimental): requires `sqlite3` binary
- **postgres** (experimental): requires `psql` and a connection string

Notes:

- sqlite/postgres are opt-in and experimental.
- postgres credentials flow into subagent logs; use a dedicated, least-privileged DB.

## Remote programs

13. `/prose run <handle/slug>` 会解析为 `https://p.prose.md/<handle>/<slug>`。
    Direct URLs are fetched as-is. This uses the `web_fetch` tool (or `exec` for POST).

## OpenClaw runtime mapping

OpenProse programs map to OpenClaw primitives:

| OpenProse concept                         | OpenClaw tool                          |
| ----------------------------------------- | -------------------------------------- |
| 14. 生成会话 / Task 工具 | `sessions_spawn`                       |
| File read/write                           | `read` / `write`                       |
| Web fetch                                 | 15. `web_fetch` |

If your tool allowlist blocks these tools, OpenProse programs will fail. 16. 请参阅 [Skills config](/tools/skills-config)。

## 17. 安全性 + 审批

18. 将 `.prose` 文件视为代码来对待。 Review before running. 19. 使用 OpenClaw 工具白名单和审批门控来控制副作用。

20. 对于确定性、需审批门控的工作流，可与 [Lobster](/tools/lobster) 进行对比。
