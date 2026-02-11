---
summary: "OpenProse: .prose workflows, slash commands, and state in OpenClaw"
read_when:
  - You want to run or write .prose workflows
  - You want to enable the OpenProse plugin
  - You need to understand state storage
title: "OpenProse"
---

# OpenProse

OpenProse is a portable, markdown-first workflow format for orchestrating AI sessions. In OpenClaw it ships as a plugin that installs an OpenProse skill pack plus a `/prose` slash command. Programs live in `.prose` files and can spawn multiple sub-agents with explicit control flow.

Official site: [https://www.prose.md](https://www.prose.md)

## What it can do

- Multi-agent research + synthesis with explicit parallelism.
- Repeatable approval-safe workflows (code review, incident triage, content pipelines).
- Reusable `.prose` programs you can run across supported agent runtimes.

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

`/prose run <handle/slug>` `https://p.prose.md/<handle>/<slug>` manziliga yo‘naltiriladi.
To‘g‘ridan-to‘g‘ri URL’lar qanday bo‘lsa, shundayicha olinadi. Bu `web_fetch` vositasidan foydalanadi (yoki POST uchun `exec`).

## OpenClaw runtime moslashtirishi

OpenProse dasturlari OpenClaw primitivlariga mos keladi:

| OpenProse tushunchasi            | OpenClaw vositasi |
| -------------------------------- | ----------------- |
| Sessiya yaratish / Task vositasi | `sessions_spawn`  |
| Faylni o‘qish/yozish             | `read` / `write`  |
| Vebdan olish                     | `web_fetch`       |

Agar vositalar allowlist’ingiz bu vositalarni bloklasa, OpenProse dasturlari ishlamaydi. [Skills config](/tools/skills-config) sahifasiga qarang.

## Xavfsizlik + tasdiqlashlar

`.prose` fayllarini kod kabi ko‘ring. Ishga tushirishdan oldin ko‘rib chiqing. Yon ta’sirlarni boshqarish uchun OpenClaw vositalari allowlist’lari va tasdiqlash darvozalaridan foydalaning.

Deterministik, tasdiqlash bilan cheklangan ish jarayonlari uchun [Lobster](/tools/lobster) bilan solishtiring.
