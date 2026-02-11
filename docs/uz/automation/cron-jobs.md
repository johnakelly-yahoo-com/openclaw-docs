---
summary: "Gateway rejalashtirgichi uchun cron vazifalari + uyg‘otishlar"
read_when:
  - Fon vazifalari yoki uyg‘otishlarni rejalashtirish
  - Yurak urishlari bilan birga yoki yonma-yon ishlashi kerak bo‘lgan avtomatlashtirishni ulash
  - Rejalashtirilgan vazifalar uchun heartbeat va cron o‘rtasida tanlash
title: "Cron vazifalari"
---

# Cron vazifalari (Gateway rejalashtirgichi)

> **Cron vs Heartbeat?** Qaysi birini qachon ishlatish bo‘yicha ko‘rsatmalar uchun [Cron vs Heartbeat](/automation/cron-vs-heartbeat) ga qarang.

Cron — Gateway’ning ichki rejalashtirgichi. U vazifalarni saqlab qoladi, agentni kerakli vaqtda uyg‘otadi va ixtiyoriy ravishda natijani chatga yetkazishi mumkin.

Agar _“buni har tongda ishga tushir”_ yoki _“20 daqiqadan keyin agentni turt”_ desangiz, mexanizm — cron.

Nosozliklarni bartaraf etish: [/automation/troubleshooting](/automation/troubleshooting)

## Qisqacha

- Cron **Gateway ichida** ishlaydi (model ichida emas).
- Vazifalar `~/.openclaw/cron/` ostida saqlanadi, shuning uchun qayta ishga tushirishlar jadvalni yo‘qotmaydi.
- Ikki ijro uslubi:
  - **Asosiy sessiya**: tizim hodisasini navbatga qo‘ying, so‘ng keyingi heartbeat’da ishga tushiring.
  - **Izolyatsiyalangan**: `cron:<jobId>` da alohida agent aylanishini ishga tushiring, yetkazib berish bilan (standart bo‘yicha e’lon qilinadi yoki yo‘q).
- Uyg‘otishlar birinchi darajali: vazifa “hozir uyg‘ot” yoki “keyingi heartbeat”ni so‘rashi mumkin.

## Tezkor boshlash (amaliy)

Bir martalik eslatma yarating, mavjudligini tekshiring va darhol ishga tushiring:

```bash
openclaw cron add \
  --name "Reminder" \
  --at "2026-02-01T16:00:00Z" \
  --session main \
  --system-event "Reminder: check the cron docs draft" \
  --wake now \
  --delete-after-run

openclaw cron list
openclaw cron run <job-id>
openclaw cron runs --id <job-id>
```

Yetkazib berish bilan takrorlanuvchi izolyatsiyalangan vazifani rejalashtiring:

```bash
openclaw cron add \
  --name "Morning brief" \
  --cron "0 7 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize overnight updates." \
  --announce \
  --channel slack \
  --to "channel:C1234567890"
```

## Tool-chaqiruv muqobillari (Gateway cron tool)

For the canonical JSON shapes and examples, see [JSON schema for tool calls](/automation/cron-jobs#json-schema-for-tool-calls).

## Where cron jobs are stored

Cron jobs are persisted on the Gateway host at `~/.openclaw/cron/jobs.json` by default.
The Gateway loads the file into memory and writes it back on changes, so manual edits
are only safe when the Gateway is stopped. Prefer `openclaw cron add/edit` or the cron
tool call API for changes.

## Beginner-friendly overview

Think of a cron job as: **when** to run + **what** to do.

1. **Choose a schedule**
   - One-shot reminder → `schedule.kind = "at"` (CLI: `--at`)
   - Repeating job → `schedule.kind = "every"` or `schedule.kind = "cron"`
   - If your ISO timestamp omits a timezone, it is treated as **UTC**.

2. **Choose where it runs**
   - `sessionTarget: "main"` → run during the next heartbeat with main context.
   - `sessionTarget: "isolated"` → run a dedicated agent turn in `cron:<jobId>`.

3. **Choose the payload**
   - Main session → `payload.kind = "systemEvent"`
   - Isolated session → `payload.kind = "agentTurn"`

Optional: one-shot jobs (`schedule.kind = "at"`) delete after success by default. Set
`deleteAfterRun: false` to keep them (they will disable after success).

## Concepts

### Jobs

A cron job is a stored record with:

- a **schedule** (when it should run),
- a **payload** (what it should do),
- optional **delivery mode** (announce or none).
- optional **agent binding** (`agentId`): run the job under a specific agent; if
  missing or unknown, the gateway falls back to the default agent.

Jobs are identified by a stable `jobId` (used by CLI/Gateway APIs).
In agent tool calls, `jobId` is canonical; legacy `id` is accepted for compatibility.
One-shot jobs auto-delete after success by default; set `deleteAfterRun: false` to keep them.

### Schedules

Cron supports three schedule kinds:

- `at`: one-shot timestamp via `schedule.at` (ISO 8601).
- `every`: fixed interval (ms).
- `cron`: 5-field cron expression with optional IANA timezone.

Cron expressions use `croner`. If a timezone is omitted, the Gateway host’s
local timezone is used.

### Main vs isolated execution

#### Main session jobs (system events)

Main jobs enqueue a system event and optionally wake the heartbeat runner.
They must use `payload.kind = "systemEvent"`.

- `wakeMode: "now"` (default): event triggers an immediate heartbeat run.
- `wakeMode: "next-heartbeat"`: event waits for the next scheduled heartbeat.

This is the best fit when you want the normal heartbeat prompt + main-session context.
See [Heartbeat](/gateway/heartbeat).

#### Isolated jobs (dedicated cron sessions)

Isolated jobs run a dedicated agent turn in session `cron:<jobId>`.

Key behaviors:

- Prompt is prefixed with `[cron:<jobId> <job name>]` for traceability.
- Each run starts a **fresh session id** (no prior conversation carry-over).
- Default behavior: if `delivery` is omitted, isolated jobs announce a summary (`delivery.mode = "announce"`).
- `delivery.mode` (isolated-only) chooses what happens:
  - `announce`: deliver a summary to the target channel and post a brief summary to the main session.
  - 2. `none`: faqat ichki (yetkazib berish yo‘q, asosiy sessiya xulosasi yo‘q).
- `wakeMode` controls when the main-session summary posts:
  - 3. `now`: darhol heartbeat.
  - `next-heartbeat`: waits for the next scheduled heartbeat.

Use isolated jobs for noisy, frequent, or "background chores" that shouldn't spam
your main chat history.

### 4. Yuklama shakllari (nima ishga tushadi)

Two payload kinds are supported:

- `systemEvent`: main-session only, routed through the heartbeat prompt.
- `agentTurn`: isolated-session only, runs a dedicated agent turn.

Common `agentTurn` fields:

- `message`: required text prompt.
- `model` / `thinking`: optional overrides (see below).
- `timeoutSeconds`: optional timeout override.

Delivery config (isolated jobs only):

- `delivery.mode`: `none` | `announce`.
- `delivery.channel`: `last` or a specific channel.
- `delivery.to`: channel-specific target (phone/chat/channel id).
- 5. `delivery.bestEffort`: e’lonni yetkazish muvaffaqiyatsiz bo‘lsa, vazifani muvaffaqiyatsiz deb belgilamaslik.

Announce delivery suppresses messaging tool sends for the run; use `delivery.channel`/`delivery.to`
to target the chat instead. When `delivery.mode = "none"`, no summary is posted to the main session.

If `delivery` is omitted for isolated jobs, OpenClaw defaults to `announce`.

#### Announce delivery flow

When `delivery.mode = "announce"`, cron delivers directly via the outbound channel adapters.
The main agent is not spun up to craft or forward the message.

Behavior details:

- Content: delivery uses the isolated run's outbound payloads (text/media) with normal chunking and
  channel formatting.
- Heartbeat-only responses (`HEARTBEAT_OK` with no real content) are not delivered.
- If the isolated run already sent a message to the same target via the message tool, delivery is
  skipped to avoid duplicates.
- Missing or invalid delivery targets fail the job unless `delivery.bestEffort = true`.
- A short summary is posted to the main session only when `delivery.mode = "announce"`.
- The main-session summary respects `wakeMode`: `now` triggers an immediate heartbeat and
  `next-heartbeat` waits for the next scheduled heartbeat.

### Model and thinking overrides

Isolated jobs (`agentTurn`) can override the model and thinking level:

- `model`: Provider/model string (e.g., `anthropic/claude-sonnet-4-20250514`) or alias (e.g., `opus`)
- `thinking`: Thinking level (`off`, `minimal`, `low`, `medium`, `high`, `xhigh`; GPT-5.2 + Codex models only)

Note: You can set `model` on main-session jobs too, but it changes the shared main
session model. We recommend model overrides only for isolated jobs to avoid
unexpected context shifts.

Resolution priority:

1. Job payload override (highest)
2. Hook-specific defaults (e.g., `hooks.gmail.model`)
3. Agent config default

### Delivery (channel + target)

Isolated jobs can deliver output to a channel via the top-level `delivery` config:

- `delivery.mode`: `announce` (deliver a summary) or `none`.
- `delivery.channel`: `whatsapp` / `telegram` / `discord` / `slack` / `mattermost` (plugin) / `signal` / `imessage` / `last`.
- `delivery.to`: channel-specific recipient target.

Delivery config is only valid for isolated jobs (`sessionTarget: "isolated"`).

If `delivery.channel` or `delivery.to` is omitted, cron can fall back to the main session’s
“last route” (the last place the agent replied).

Maqsad formatiga oid eslatmalar:

- Slack/Discord/Mattermost (plagin) maqsadlari noaniqlikni oldini olish uchun aniq prefikslardan foydalanishi kerak (masalan, `channel:<id>`, `user:<id>`).
- Telegram mavzulari `:topic:` shaklidan foydalanishi kerak (quyida qarang).

#### Telegram yetkazib berish maqsadlari (mavzular / forum tarmoqlari)

Telegram `message_thread_id` orqali forum mavzularini qo‘llab-quvvatlaydi. Cron orqali yetkazib berish uchun siz mavzu/tarmoqni `to` maydoniga kodlashingiz mumkin:

- `-1001234567890` (faqat chat identifikatori)
- `-1001234567890:topic:123` (afzal: aniq mavzu belgisi)
- `-1001234567890:123` (qisqa shakl: raqamli suffiks)

`telegram:...` / `telegram:group:...` kabi prefiksli maqsadlar ham qabul qilinadi:

- `telegram:group:-1001234567890:topic:123`

## 6. Asbob chaqiruvlari uchun JSON sxemasi

Gateway `cron.*` asboblarini bevosita chaqirishda (agent asbob chaqiruvlari yoki RPC) ushbu shakllardan foydalaning.
CLI flaglari `20m` kabi insoniy davomiyliklarni qabul qiladi, ammo asbob chaqiruvlari `schedule.at` uchun ISO 8601 satrini va `schedule.everyMs` uchun millisekundlarni ishlatishi kerak.

### cron.add parametrlari

7. Bir martalik, asosiy sessiya vazifasi (tizim hodisasi):

```json
{
  "name": "Reminder",
  "schedule": { "kind": "at", "at": "2026-02-01T16:00:00Z" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": { "kind": "systemEvent", "text": "Reminder text" },
  "deleteAfterRun": true
}
```

Takrorlanuvchi, izolyatsiyalangan va yetkazib berishli vazifa:

```json
{
  "name": "Morning brief",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "America/Los_Angeles" },
  "sessionTarget": "isolated",
  "wakeMode": "next-heartbeat",
  "payload": {
    "kind": "agentTurn",
    "message": "Summarize overnight updates."
  },
  "delivery": {
    "mode": "announce",
    "channel": "slack",
    "to": "channel:C1234567890",
    "bestEffort": true
  }
}
```

Eslatmalar:

- `schedule.kind`: `at` (`at`), `every` (`everyMs`) yoki `cron` (`expr`, ixtiyoriy `tz`).
- `schedule.at` ISO 8601 ni qabul qiladi (vaqt mintaqasi ixtiyoriy; ko‘rsatilmasa UTC sifatida qabul qilinadi).
- `everyMs` — millisekundlarda.
- `sessionTarget` `"main"` yoki `"isolated"` bo‘lishi va `payload.kind` bilan mos kelishi kerak.
- Ixtiyoriy maydonlar: `agentId`, `description`, `enabled`, `deleteAfterRun` (`at` uchun sukut bo‘yicha true), `delivery`.
- `wakeMode` ko‘rsatilmasa, sukut bo‘yicha `"now"` bo‘ladi.

### cron.update parametrlari

```json
{
  "jobId": "job-123",
  "patch": {
    "enabled": false,
    "schedule": { "kind": "every", "everyMs": 3600000 }
  }
}
```

Eslatmalar:

- `jobId` kanonik; moslik uchun `id` ham qabul qilinadi.
- Agent bog‘lanishini tozalash uchun patch’da `agentId: null` dan foydalaning.

### cron.run va cron.remove parametrlari

```json
{ "jobId": "job-123", "mode": "force" }
```

```json
{ "jobId": "job-123" }
```

## Saqlash va tarix

- Vazifalar ombori: `~/.openclaw/cron/jobs.json` (Gateway tomonidan boshqariladigan JSON).
- Ishga tushirish tarixi: `~/.openclaw/cron/runs/<jobId>.jsonl` (JSONL, avtomatik tozalanadi).
- Ombor yo‘lini almashtirish: konfiguratsiyada `cron.store`.

## Konfiguratsiya

```json5
{
  cron: {
    enabled: true, // default true
    store: "~/.openclaw/cron/jobs.json",
    maxConcurrentRuns: 1, // default 1
  },
}
```

Cron’ni butunlay o‘chirish:

- `cron.enabled: false` (konfiguratsiya)
- `OPENCLAW_SKIP_CRON=1` (muhit)

## CLI tezkor boshlash

Bir martalik eslatma (UTC ISO, muvaffaqiyatdan so‘ng avtomatik o‘chiriladi):

```bash
openclaw cron add \
  --name "Send reminder" \
  --at "2026-01-12T18:00:00Z" \
  --session main \
  --system-event "Reminder: submit expense report." \
  --wake now \
  --delete-after-run
```

Bir martalik eslatma (asosiy sessiya, darhol uyg‘otish):

```bash
openclaw cron add \
  --name "Calendar check" \
  --at "20m" \
  --session main \
  --system-event "Next heartbeat: check calendar." \
  --wake now
```

Takrorlanuvchi izolyatsiyalangan vazifa (WhatsApp’ga e’lon qilish):

```bash
openclaw cron add \
  --name "Morning status" \
  --cron "0 7 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize inbox + calendar for today." \
  --announce \
  --channel whatsapp \
  --to "+15551234567"
```

Recurring isolated job (deliver to a Telegram topic):

```bash
openclaw cron add \
  --name "Nightly summary (topic)" \
  --cron "0 22 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize today; send to the nightly topic." \
  --announce \
  --channel telegram \
  --to "-1001234567890:topic:123"
```

Isolated job with model and thinking override:

```bash
openclaw cron add \
  --name "Deep analysis" \
  --cron "0 6 * * 1" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Weekly deep analysis of project progress." \
  --model "opus" \
  --thinking high \
  --announce \
  --channel whatsapp \
  --to "+15551234567"
```

Agent selection (multi-agent setups):

```bash
# Pin a job to agent "ops" (falls back to default if that agent is missing)
openclaw cron add --name "Ops sweep" --cron "0 6 * * *" --session isolated --message "Check ops queue" --agent ops

# Switch or clear the agent on an existing job
openclaw cron edit <jobId> --agent ops
openclaw cron edit <jobId> --clear-agent
```

Manual run (force is the default, use `--due` to only run when due):

```bash
openclaw cron run <jobId>
openclaw cron run <jobId> --due
```

Edit an existing job (patch fields):

```bash
openclaw cron edit <jobId> \
  --message "Updated prompt" \
  --model "opus" \
  --thinking low
```

Run history:

```bash
openclaw cron runs --id <jobId> --limit 50
```

Immediate system event without creating a job:

```bash
openclaw system event --mode now --text "Next heartbeat: check battery."
```

## Gateway API surface

- `cron.list`, `cron.status`, `cron.add`, `cron.update`, `cron.remove`
- `cron.run` (force or due), `cron.runs`
  For immediate system events without a job, use [`openclaw system event`](/cli/system).

## Troubleshooting

### “Nothing runs”

- 8. Cron yoqilganini tekshiring: `cron.enabled` va `OPENCLAW_SKIP_CRON`.
- Check the Gateway is running continuously (cron runs inside the Gateway process).
- For `cron` schedules: confirm timezone (`--tz`) vs the host timezone.

### A recurring job keeps delaying after failures

- OpenClaw applies exponential retry backoff for recurring jobs after consecutive errors:
  30s, 1m, 5m, 15m, then 60m between retries.
- Backoff resets automatically after the next successful run.
- One-shot (`at`) jobs disable after a terminal run (`ok`, `error`, or `skipped`) and do not retry.

### Telegram delivers to the wrong place

- For forum topics, use `-100…:topic:<id>` so it’s explicit and unambiguous.
- If you see `telegram:...` prefixes in logs or stored “last route” targets, that’s normal;
  cron delivery accepts them and still parses topic IDs correctly.
