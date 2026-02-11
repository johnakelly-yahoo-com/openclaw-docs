---
summary: "Skills: managed vs workspace, gating rules, and config/env wiring"
read_when:
  - Adding or modifying skills
  - Changing skill gating or load rules
title: "Skills"
---

# Skills (OpenClaw)

OpenClaw uses **[AgentSkills](https://agentskills.io)-compatible** skill folders to teach the agent how to use tools. Each skill is a directory containing a `SKILL.md` with YAML frontmatter and instructions. OpenClaw **biriktirilgan ko‘nikmalarni** hamda ixtiyoriy mahalliy override’larni yuklaydi va ularni yuklash vaqtida muhit, konfiguratsiya va binar mavjudligiga qarab filtrlaydi.

## Joylashuvlar va ustuvorlik

Skills are loaded from **three** places:

1. **Biriktirilgan ko‘nikmalar**: o‘rnatish bilan birga yetkaziladi (npm paketi yoki OpenClaw.app)
2. **Managed/local skills**: `~/.openclaw/skills`
3. **Workspace ko‘nikmalari**: `<workspace>/skills`

Agar ko‘nikma nomi to‘qnashsa, ustuvorlik quyidagicha:

`<workspace>/skills` (eng yuqori) → `~/.openclaw/skills` → biriktirilgan ko‘nikmalar (eng past)

Bundan tashqari, qo‘shimcha ko‘nikma papkalarini (eng past ustuvorlik) `~/.openclaw/openclaw.json` dagi
`skills.load.extraDirs` orqali sozlashingiz mumkin.

## Agentga xos va umumiy ko‘nikmalar

In **multi-agent** setups, each agent has its own workspace. Bu shuni anglatadiki:

- **Agentga xos ko‘nikmalar** faqat o‘sha agent uchun `<workspace>/skills` da joylashadi.
- **Umumiy ko‘nikmalar** `~/.openclaw/skills` (boshqariladigan/mahalliy) da joylashadi va
  bir xil mashinadagi **barcha agentlar** uchun ko‘rinadi.
- Agar bir nechta agentlar foydalanadigan umumiy ko‘nikmalar to‘plamini xohlasangiz,
  **umumiy papkalar**ni ham `skills.load.extraDirs` orqali (eng past ustuvorlik)
  qo‘shish mumkin.

Agar bir xil ko‘nikma nomi bir nechta joyda mavjud bo‘lsa, odatdagi ustuvorlik qo‘llanadi:
workspace yutadi, keyin boshqariladigan/mahalliy, so‘ng biriktirilgan.

## Plaginlar + ko‘nikmalar

Plaginlar `openclaw.plugin.json` faylida `skills` kataloglarini
(plagin ildiziga nisbatan yo‘llar) ko‘rsatish orqali o‘z ko‘nikmalarini yetkazishi mumkin. Plugin skills load
when the plugin is enabled and participate in the normal skill precedence rules.
You can gate them via `metadata.openclaw.requires.config` on the plugin’s config
entry. Kashf qilish/sozlash uchun [Plugins](/tools/plugin) va ushbu ko‘nikmalar o‘rgatadigan vositalar yuzasi uchun [Tools](/tools) ga qarang.

## ClawHub (o‘rnatish + sinxronlash)

ClawHub — OpenClaw uchun ommaviy ko‘nikmalar reyestri. Ko‘rib chiqing:
[https://clawhub.com](https://clawhub.com). Undan ko‘nikmalarni topish, o‘rnatish, yangilash va zaxiralash uchun foydalaning.
To‘liq qo‘llanma: [ClawHub](/tools/clawhub).

Ommabop oqimlar:

- Workspace’ingizga ko‘nikma o‘rnatish:
  - `clawhub install <skill-slug>`
- O‘rnatilgan barcha ko‘nikmalarni yangilash:
  - `clawhub update --all`
- Sinxronlash (skanlash + yangilanishlarni e’lon qilish):
  - `clawhub sync --all`

Odatiy holatda `clawhub` joriy ishchi katalogingiz ostidagi `./skills` ga o‘rnatadi
(yoki sozlangan OpenClaw workspace’iga qaytadi). OpenClaw keyingi sessiyada
buni `<workspace>/skills` sifatida aniqlaydi.

## Xavfsizlik eslatmalari

- Uchinchi tomon ko‘nikmalarini **ishonchsiz kod** sifatida qabul qiling. Yoqishdan oldin ularni o‘qing.
- Ishonchsiz kiritmalar va xavfli vositalar uchun sandboxlangan ishga tushirishni afzal ko‘ring. [Sandboxing](/gateway/sandboxing) ga qarang.
- `skills.entries.*.env` va `skills.entries.*.apiKey` sirlarni **host** jarayoniga
  o‘sha agent navbati uchun (sandbox’ga emas) yuboradi. Sirlarni promptlar va loglardan uzoq tuting.
- Kengroq tahdid modeli va tekshiruv ro‘yxatlari uchun [Security](/gateway/security) ga qarang.

## Format (AgentSkills + Pi-mos)

`SKILL.md` kamida quyidagilarni o‘z ichiga olishi kerak:

```markdown
---
name: nano-banana-pro
description: Gemini 3 Pro Image orqali tasvirlarni yaratish yoki tahrirlash
---
```

Eslatmalar:

- Joylashuv/maqsad uchun AgentSkills spetsifikatsiyasiga amal qilamiz.
- Ichki agent tomonidan ishlatiladigan parser **faqat bir qatorli** frontmatter kalitlarini qo‘llab-quvvatlaydi.
- `metadata` **bir qatorli JSON obyekt** bo‘lishi kerak.
- Use `{baseDir}` in instructions to reference the skill folder path.
- Optional frontmatter keys:
  - `homepage` — URL surfaced as “Website” in the macOS Skills UI (also supported via `metadata.openclaw.homepage`).
  - `user-invocable` — `true|false` (default: `true`). When `true`, the skill is exposed as a user slash command.
  - `disable-model-invocation` — `true|false` (default: `false`). When `true`, the skill is excluded from the model prompt (still available via user invocation).
  - `command-dispatch` — `tool` (optional). When set to `tool`, the slash command bypasses the model and dispatches directly to a tool.
  - `command-tool` — tool name to invoke when `command-dispatch: tool` is set.
  - `command-arg-mode` — `raw` (default). For tool dispatch, forwards the raw args string to the tool (no core parsing).

    The tool is invoked with params:
    `{ command: "<raw args>", commandName: "<slash command>", skillName: "<skill name>" }`.

## Gating (load-time filters)

OpenClaw **filters skills at load time** using `metadata` (single-line JSON):

```markdown
---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["uv"], "env": ["GEMINI_API_KEY"], "config": ["browser.enabled"] },
        "primaryEnv": "GEMINI_API_KEY",
      },
  }
---
```

Fields under `metadata.openclaw`:

- `always: true` — always include the skill (skip other gates).
- `emoji` — optional emoji used by the macOS Skills UI.
- `homepage` — optional URL shown as “Website” in the macOS Skills UI.
- `os` — optional list of platforms (`darwin`, `linux`, `win32`). If set, the skill is only eligible on those OSes.
- `requires.bins` — list; each must exist on `PATH`.
- `requires.anyBins` — list; at least one must exist on `PATH`.
- `requires.env` — list; env var must exist **or** be provided in config.
- `requires.config` — list of `openclaw.json` paths that must be truthy.
- `primaryEnv` — env var name associated with `skills.entries.<name>.apiKey`.
- `install` — optional array of installer specs used by the macOS Skills UI (brew/node/go/uv/download).

Note on sandboxing:

- `requires.bins` is checked on the **host** at skill load time.
- If an agent is sandboxed, the binary must also exist **inside the container**.
  Install it via `agents.defaults.sandbox.docker.setupCommand` (or a custom image).
  `setupCommand` runs once after the container is created.
  Package installs also require network egress, a writable root FS, and a root user in the sandbox.
  Example: the `summarize` skill (`skills/summarize/SKILL.md`) needs the `summarize` CLI
  in the sandbox container to run there.

Installer example:

```markdown
---
name: gemini
description: Use Gemini CLI for coding assistance and Google search lookups.
metadata:
  {
    "openclaw":
      {
        "emoji": "♊️",
        "requires": { "bins": ["gemini"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gemini-cli",
              "bins": ["gemini"],
              "label": "Install Gemini CLI (brew)",
            },
          ],
      },
  }
---
```

Notes:

- If multiple installers are listed, the gateway picks a **single** preferred option (brew when available, otherwise node).
- If all installers are `download`, OpenClaw lists each entry so you can see the available artifacts.
- Installer specs can include `os: ["darwin"|"linux"|"win32"]` to filter options by platform.
- Node installs honor `skills.install.nodeManager` in `openclaw.json` (default: npm; options: npm/pnpm/yarn/bun).
  This only affects **skill installs**; the Gateway runtime should still be Node
  (Bun is not recommended for WhatsApp/Telegram).
- Go installs: if `go` is missing and `brew` is available, the gateway installs Go via Homebrew first and sets `GOBIN` to Homebrew’s `bin` when possible.
- Download installs: `url` (required), `archive` (`tar.gz` | `tar.bz2` | `zip`), `extract` (default: auto when archive detected), `stripComponents`, `targetDir` (default: `~/.openclaw/tools/<skillKey>`).

If no `metadata.openclaw` is present, the skill is always eligible (unless
disabled in config or blocked by `skills.allowBundled` for bundled skills).

## Config overrides (`~/.openclaw/openclaw.json`)

Bundled/managed skills can be toggled and supplied with env values:

```json5
{
  skills: {
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: "GEMINI_KEY_HERE",
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
        config: {
          endpoint: "https://example.invalid",
          model: "nano-pro",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

Note: if the skill name contains hyphens, quote the key (JSON5 allows quoted keys).

Config keys match the **skill name** by default. If a skill defines
`metadata.openclaw.skillKey`, use that key under `skills.entries`.

Rules:

- `enabled: false` disables the skill even if it’s bundled/installed.
- `env`: injected **only if** the variable isn’t already set in the process.
- `apiKey`: convenience for skills that declare `metadata.openclaw.primaryEnv`.
- `config`: optional bag for custom per-skill fields; custom keys must live here.
- `allowBundled`: optional allowlist for **bundled** skills only. If set, only
  bundled skills in the list are eligible (managed/workspace skills unaffected).

## Environment injection (per agent run)

When an agent run starts, OpenClaw:

1. Reads skill metadata.
2. Applies any `skills.entries.<key>.env` or `skills.entries.<key>.apiKey` to
   `process.env`.
3. Builds the system prompt with **eligible** skills.
4. Restores the original environment after the run ends.

This is **scoped to the agent run**, not a global shell environment.

## Session snapshot (performance)

OpenClaw snapshots the eligible skills **when a session starts** and reuses that list for subsequent turns in the same session. Changes to skills or config take effect on the next new session.

Skills can also refresh mid-session when the skills watcher is enabled or when a new eligible remote node appears (see below). Think of this as a **hot reload**: the refreshed list is picked up on the next agent turn.

## Remote macOS nodes (Linux gateway)

If the Gateway is running on Linux but a **macOS node** is connected **with `system.run` allowed** (Exec approvals security not set to `deny`), OpenClaw can treat macOS-only skills as eligible when the required binaries are present on that node. The agent should execute those skills via the `nodes` tool (typically `nodes.run`).

This relies on the node reporting its command support and on a bin probe via `system.run`. If the macOS node goes offline later, the skills remain visible; invocations may fail until the node reconnects.

## Skills watcher (auto-refresh)

By default, OpenClaw watches skill folders and bumps the skills snapshot when `SKILL.md` files change. Configure this under `skills.load`:

```json5
{
  skills: {
    load: {
      watch: true,
      watchDebounceMs: 250,
    },
  },
}
```

## Token impact (skills list)

When skills are eligible, OpenClaw injects a compact XML list of available skills into the system prompt (via `formatSkillsForPrompt` in `pi-coding-agent`). The cost is deterministic:

- **Base overhead (only when ≥1 skill):** 195 characters.
- **Per skill:** 97 characters + the length of the XML-escaped `<name>`, `<description>`, and `<location>` values.

Formula (characters):

```
total = 195 + Σ (97 + len(name_escaped) + len(description_escaped) + len(location_escaped))
```

Notes:

- XML escaping expands `& < > " '` into entities (`&amp;`, `&lt;`, etc.), increasing length.
- Token counts vary by model tokenizer. A rough OpenAI-style estimate is ~4 chars/token, so **97 chars ≈ 24 tokens** per skill plus your actual field lengths.

## Managed skills lifecycle

OpenClaw ships a baseline set of skills as **bundled skills** as part of the
install (npm package or OpenClaw.app). `~/.openclaw/skills` exists for local
overrides (for example, pinning/patching a skill without changing the bundled
copy). Workspace skills are user-owned and override both on name conflicts.

## Config reference

See [Skills config](/tools/skills-config) for the full configuration schema.

## Looking for more skills?

Browse [https://clawhub.com](https://clawhub.com).

---
