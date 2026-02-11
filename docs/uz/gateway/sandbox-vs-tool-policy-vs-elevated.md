---
title: Sandbox vs Tool Policy vs Elevated
summary: "Nega tool bloklangan: sandbox runtime, tool allow/deny siyosati va elevated exec gate’lar."
read_when: "Siz “sandbox jail”ga tushdingiz yoki tool/elevated rad etilishini ko‘ryapsiz va o‘zgartirish kerak bo‘lgan aniq config kalitini xohlaysiz."
status: faol
---

# Sandbox vs Tool Policy vs Elevated

OpenClaw’da uchta bog‘liq (lekin turli) boshqaruv mavjud:

1. **Sandbox** (`agents.defaults.sandbox.*` / `agents.list[].sandbox.*`) **tool’lar qayerda ishlashini** belgilaydi (Docker vs host).
2. **Tool policy** (`tools.*`, `tools.sandbox.tools.*`, `agents.list[].tools.*`) **qaysi tool’lar mavjud/ruxsat etilganini** belgilaydi.
3. **Elevated** (`tools.elevated.*`, `agents.list[].tools.elevated.*`) sandbox holatida host’da ishga tushirish uchun **faqat exec’ga oid chiqish yo‘li**dir.

## Tezkor debug

Inspector’dan OpenClaw **aslida** nima qilayotganini ko‘rish uchun foydalaning:

```bash
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work
openclaw sandbox explain --json
```

U quyidagilarni chiqaradi:

- samarali sandbox rejimi/doirasi/workspace kirishi
- sessiya hozir sandboxlanganmi (main vs non-main)
- samarali sandbox tool allow/deny (va u agent/global/default’dan kelgan-kelmaganini)
- elevated gate’lar va tuzatish uchun kalit yo‘llari

## Sandbox: tool’lar qayerda ishlaydi

Sandboxing `agents.defaults.sandbox.mode` orqali boshqariladi:

- `"off"`: hammasi host’da ishlaydi.
- `"non-main"`: faqat non-main sessiyalar sandboxlanadi (guruhlar/kanallar uchun keng tarqalgan “kutilmagan holat”).
- `"all"`: hammasi sandboxlanadi.

To‘liq matritsa (scope, workspace mount’lar, image’lar) uchun [Sandboxing](/gateway/sandboxing) ga qarang.

### Bind mount’lar (xavfsizlik uchun tezkor tekshiruv)

- `docker.binds` sandbox fayl tizimini _teshib o‘tadi_: siz mount qilgan hamma narsa konteyner ichida belgilagan rejimingiz bilan (`:ro` yoki `:rw`) ko‘rinadi.
- Agar rejimni ko‘rsatmasangiz, standart holat o‘qish-yozishdir; manba/kirish ma’lumotlari uchun `:ro` ni afzal ko‘ring.
- `scope: "shared"` per-agent bind’larni e’tiborsiz qoldiradi (faqat global bind’lar qo‘llanadi).
- `/var/run/docker.sock` ni bind qilish amalda host boshqaruvini sandbox’ga topshiradi; buni faqat ongli ravishda bajaring.
- Workspace kirishi (`workspaceAccess: "ro"`/`"rw"`) bind rejimlaridan mustaqil.

## Tool policy: qaysi tool’lar mavjud/chaqirilishi mumkin

Two layers matter:

- **Tool profile**: `tools.profile` and `agents.list[].tools.profile` (base allowlist)
- **Provider tool profile**: `tools.byProvider[provider].profile` and `agents.list[].tools.byProvider[provider].profile`
- **Global/per-agent tool policy**: `tools.allow`/`tools.deny` and `agents.list[].tools.allow`/`agents.list[].tools.deny`
- **Provider tool policy**: `tools.byProvider[provider].allow/deny` and `agents.list[].tools.byProvider[provider].allow/deny`
- **Sandbox tool policy** (only applies when sandboxed): `tools.sandbox.tools.allow`/`tools.sandbox.tools.deny` and `agents.list[].tools.sandbox.tools.*`

Rules of thumb:

- `deny` always wins.
- If `allow` is non-empty, everything else is treated as blocked.
- Tool policy is the hard stop: `/exec` cannot override a denied `exec` tool.
- `/exec` only changes session defaults for authorized senders; it does not grant tool access.
  Provider tool keys accept either `provider` (e.g. `google-antigravity`) or `provider/model` (e.g. `openai/gpt-5.2`).

### Tool groups (shorthands)

Tool policies (global, agent, sandbox) support `group:*` entries that expand to multiple tools:

```json5
{
  tools: {
    sandbox: {
      tools: {
        allow: ["group:runtime", "group:fs", "group:sessions", "group:memory"],
      },
    },
  },
}
```

Available groups:

- `group:runtime`: `exec`, `bash`, `process`
- `group:fs`: `read`, `write`, `edit`, `apply_patch`
- `group:sessions`: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
- `group:memory`: `memory_search`, `memory_get`
- `group:ui`: `browser`, `canvas`
- `group:automation`: `cron`, `gateway`
- `group:messaging`: `message`
- `group:nodes`: `nodes`
- `group:openclaw`: all built-in OpenClaw tools (excludes provider plugins)

## Elevated: exec-only “run on host”

Elevated does **not** grant extra tools; it only affects `exec`.

- If you’re sandboxed, `/elevated on` (or `exec` with `elevated: true`) runs on the host (approvals may still apply).
- Use `/elevated full` to skip exec approvals for the session.
- If you’re already running direct, elevated is effectively a no-op (still gated).
- Elevated is **not** skill-scoped and does **not** override tool allow/deny.
- `/exec` is separate from elevated. It only adjusts per-session exec defaults for authorized senders.

Gates:

- Enablement: `tools.elevated.enabled` (and optionally `agents.list[].tools.elevated.enabled`)
- Sender allowlists: `tools.elevated.allowFrom.<provider>` (and optionally `agents.list[].tools.elevated.allowFrom.<provider>`)

See [Elevated Mode](/tools/elevated).

## Common “sandbox jail” fixes

### “Tool X blocked by sandbox tool policy”

Fix-it keys (pick one):

- Disable sandbox: `agents.defaults.sandbox.mode=off` (or per-agent `agents.list[].sandbox.mode=off`)
- Allow the tool inside sandbox:
  - remove it from `tools.sandbox.tools.deny` (or per-agent `agents.list[].tools.sandbox.tools.deny`)
  - or add it to `tools.sandbox.tools.allow` (or per-agent allow)

### “I thought this was main, why is it sandboxed?”

In `"non-main"` mode, group/channel keys are _not_ main. Use the main session key (shown by `sandbox explain`) or switch mode to `"off"`.
