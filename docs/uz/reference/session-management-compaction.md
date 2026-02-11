---
summary: "Deep dive: session store + transcripts, lifecycle, and (auto)compaction internals"
read_when:
  - You need to debug session ids, transcript JSONL, or sessions.json fields
  - You are changing auto-compaction behavior or adding “pre-compaction” housekeeping
  - You want to implement memory flushes or silent system turns
title: "Session Management Deep Dive"
---

# Session Management & Compaction (Deep Dive)

This document explains how OpenClaw manages sessions end-to-end:

- **Session routing** (how inbound messages map to a `sessionKey`)
- **Session store** (`sessions.json`) and what it tracks
- **Transcript persistence** (`*.jsonl`) and its structure
- **Transcript hygiene** (provider-specific fixups before runs)
- **Context limits** (context window vs tracked tokens)
- **Compaction** (manual + auto-compaction) and where to hook pre-compaction work
- **Silent housekeeping** (e.g. memory writes that shouldn’t produce user-visible output)

If you want a higher-level overview first, start with:

- [/concepts/session](/concepts/session)
- [/concepts/compaction](/concepts/compaction)
- [/concepts/session-pruning](/concepts/session-pruning)
- [/reference/transcript-hygiene](/reference/transcript-hygiene)

---

## Source of truth: the Gateway

OpenClaw is designed around a single **Gateway process** that owns session state.

- UIs (macOS app, web Control UI, TUI) should query the Gateway for session lists and token counts.
- In remote mode, session files are on the remote host; “checking your local Mac files” won’t reflect what the Gateway is using.

---

## Two persistence layers

OpenClaw persists sessions in two layers:

1. **Session store (`sessions.json`)**
   - Key/value map: `sessionKey -> SessionEntry`
   - Small, mutable, safe to edit (or delete entries)
   - Tracks session metadata (current session id, last activity, toggles, token counters, etc.)

2. **Transcript (`<sessionId>.jsonl`)**
   - Append-only transcript with tree structure (entries have `id` + `parentId`)
   - Stores the actual conversation + tool calls + compaction summaries
   - Used to rebuild the model context for future turns

---

## On-disk locations

Per agent, on the Gateway host:

- Store: `~/.openclaw/agents/<agentId>/sessions/sessions.json`
- Transcripts: `~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl`
  - Telegram topic sessions: `.../<sessionId>-topic-<threadId>.jsonl`

OpenClaw resolves these via `src/config/sessions.ts`.

---

## Session keys (`sessionKey`)

A `sessionKey` identifies _which conversation bucket_ you’re in (routing + isolation).

Common patterns:

- Main/direct chat (per agent): `agent:<agentId>:<mainKey>` (default `main`)
- Group: `agent:<agentId>:<channel>:group:<id>`
- Room/channel (Discord/Slack): `agent:<agentId>:<channel>:channel:<id>` or `...:room:<id>`
- Cron: `cron:<job.id>`
- Webhook: `hook:<uuid>` (unless overridden)

The canonical rules are documented at [/concepts/session](/concepts/session).

---

## Session ids (`sessionId`)

Each `sessionKey` points at a current `sessionId` (the transcript file that continues the conversation).

Rules of thumb:

- **Reset** (`/new`, `/reset`) creates a new `sessionId` for that `sessionKey`.
- **Daily reset** (default 4:00 AM local time on the gateway host) creates a new `sessionId` on the next message after the reset boundary.
- **Idle expiry** (`session.reset.idleMinutes` or legacy `session.idleMinutes`) creates a new `sessionId` when a message arrives after the idle window. When daily + idle are both configured, whichever expires first wins.

Implementation detail: the decision happens in `initSessionState()` in `src/auto-reply/reply/session.ts`.

---

## Session store schema (`sessions.json`)

The store’s value type is `SessionEntry` in `src/config/sessions.ts`.

Key fields (not exhaustive):

- `sessionId`: current transcript id (filename is derived from this unless `sessionFile` is set)
- `updatedAt`: last activity timestamp
- `sessionFile`: optional explicit transcript path override
- `chatType`: `direct | group | room` (helps UIs and send policy)
- `provider`, `subject`, `room`, `space`, `displayName`: metadata for group/channel labeling
- Toggles:
  - `thinkingLevel`, `verboseLevel`, `reasoningLevel`, `elevatedLevel`
  - `sendPolicy` (per-session override)
- Model selection:
  - `providerOverride`, `modelOverride`, `authProfileOverride`
- Token counters (best-effort / provider-dependent):
  - `inputTokens`, `outputTokens`, `totalTokens`, `contextTokens`
- `compactionCount`: how often auto-compaction completed for this session key
- `memoryFlushAt`: timestamp for the last pre-compaction memory flush
- `memoryFlushCompactionCount`: compaction count when the last flush ran

The store is safe to edit, but the Gateway is the authority: it may rewrite or rehydrate entries as sessions run.

---

## Transcript structure (`*.jsonl`)

Transcripts are managed by `@mariozechner/pi-coding-agent`’s `SessionManager`.

The file is JSONL:

- First line: session header (`type: "session"`, includes `id`, `cwd`, `timestamp`, optional `parentSession`)
- Then: session entries with `id` + `parentId` (tree)

Notable entry types:

- `message`: user/assistant/toolResult messages
- `custom_message`: extension-injected messages that _do_ enter model context (can be hidden from UI)
- `custom`: extension state that does _not_ enter model context
- `compaction`: persisted compaction summary with `firstKeptEntryId` and `tokensBefore`
- `branch_summary`: persisted summary when navigating a tree branch

OpenClaw intentionally does **not** “fix up” transcripts; the Gateway uses `SessionManager` to read/write them.

---

## Context windows vs tracked tokens

Two different concepts matter:

1. **Model context window**: hard cap per model (tokens visible to the model)
2. **Session store counters**: rolling stats written into `sessions.json` (used for /status and dashboards)

Agar limitlarni sozlayotgan bo‘lsangiz:

- Kontekst oynasi model katalogidan olinadi (va konfiguratsiya orqali o‘zgartirilishi mumkin).
- Store’dagi `contextTokens` — bu ish vaqtidagi taxminiy/hisobot qiymati; uni qat’iy kafolat sifatida qabul qilmang.

Batafsil ma’lumot uchun qarang: [/token-use](/reference/token-use).

---

## Kompaktsiya: bu nima

Kompaktsiya eski suhbatni transkriptda saqlanadigan `compaction` yozuviga qisqartirib, so‘nggi xabarlarni butunlay saqlab qoladi.

Kompaktsiyadan so‘ng, keyingi navbatlar quyidagilarni ko‘radi:

- Kompaktsiya xulosasi
- `firstKeptEntryId` dan keyingi xabarlar

Kompaktsiya **doimiy** (sessiya pruningidan farqli o‘laroq). Qarang: [/concepts/session-pruning](/concepts/session-pruning).

---

## Avto-kompaktsiya qachon sodir bo‘ladi (Pi runtime)

O‘rnatilgan Pi agentida avto-kompaktsiya ikki holatda ishga tushadi:

1. **Overflow tiklash**: model kontekst to‘lib ketish xatosini qaytaradi → kompaktsiya → qayta urinish.
2. **Chegara saqlanishi**: muvaffaqiyatli navbatdan so‘ng, qachonki:

`contextTokens > contextWindow - reserveTokens`

Bu yerda:

- `contextWindow` — modelning kontekst oynasi
- `reserveTokens` — promptlar + keyingi model chiqishi uchun ajratilgan bo‘sh joy

Bular Pi runtime semantikasi (OpenClaw hodisalarni iste’mol qiladi, ammo qachon kompaktsiya qilishni Pi hal qiladi).

---

## Kompaktsiya sozlamalari (`reserveTokens`, `keepRecentTokens`)

Pi’ning kompaktsiya sozlamalari Pi sozlamalarida joylashgan:

```json5
{
  compaction: {
    enabled: true,
    reserveTokens: 16384,
    keepRecentTokens: 20000,
  },
}
```

OpenClaw o‘rnatilgan ishga tushirishlar uchun xavfsizlik minimumini ham majburan qo‘llaydi:

- Agar `compaction.reserveTokens < reserveTokensFloor` bo‘lsa, OpenClaw uni oshiradi.
- Standart minimum `20000` token.
- `agents.defaults.compaction.reserveTokensFloor: 0` qilib o‘rnatsangiz, minimum o‘chiriladi.
- Agar u allaqachon yuqori bo‘lsa, OpenClaw unga tegmaydi.

Sababi: kompaktsiya muqarrar bo‘lishidan oldin ko‘p navbatli “xo‘jalik ishlari” (masalan, xotira yozuvlari) uchun yetarli bo‘sh joy qoldirish.

Implementatsiya: `ensurePiCompactionReserveTokens()` `src/agents/pi-settings.ts` da
(`src/agents/pi-embedded-runner.ts` dan chaqiriladi).

---

## Foydalanuvchiga ko‘rinadigan yuzalar

Siz kompaktsiya va sessiya holatini quyidagilar orqali kuzatishingiz mumkin:

- `/status` (istalgan chat sessiyasida)
- `openclaw status` (CLI)
- `openclaw sessions` / `sessions --json`
- Batafsil rejim: `🧹 Auto-compaction complete` + kompaktsiya soni

---

## Jim xo‘jalik ishlari (`NO_REPLY`)

OpenClaw foydalanuvchi oraliq chiqishni ko‘rmasligi kerak bo‘lgan fon vazifalari uchun “jim” navbatlarni qo‘llab-quvvatlaydi.

Konvensiya:

- Assistent o‘z chiqishini `NO_REPLY` bilan boshlaydi — bu “foydalanuvchiga javob yetkazilmasin” deganini bildiradi.
- OpenClaw yetkazish qatlamida buni olib tashlaydi/bosadi.

`2026.1.10` holatiga ko‘ra, OpenClaw qisman bo‘lak `NO_REPLY` bilan boshlansa, **draft/typing streaming** ni ham bostiradi, shuning uchun jim operatsiyalar navbat o‘rtasida qisman chiqishni oshkor qilmaydi.

---

## Kompaktsiyadan oldingi “xotira flush” (amalga oshirilgan)

Maqsad: avto-kompaktsiya sodir bo‘lishidan oldin, barqaror holatni diskka yozadigan jim agentli navbatni ishga tushirish (masalan, agent ish maydonidagi `memory/YYYY-MM-DD.md`), shunda kompaktsiya muhim kontekstni o‘chirib yubora olmaydi.

OpenClaw **oldindan-chegara flush** yondashuvidan foydalanadi:

1. Sessiya kontekstidan foydalanishni kuzatish.
2. U “yumshoq chegara”dan (Pi’ning kompaktsiya chegarasidan past) oshganda, agentga jim “xotirani hozir yoz” direktivasini ishga tushirish.
3. Foydalanuvchi hech narsa ko‘rmasligi uchun `NO_REPLY` dan foydalanish.

Konfiguratsiya (`agents.defaults.compaction.memoryFlush`):

- `enabled` (standart: `true`)
- `softThresholdTokens` (standart: `4000`)
- `prompt` (flush navbati uchun foydalanuvchi xabari)
- `systemPrompt` (flush navbati uchun qo‘shimcha tizim prompti qo‘shiladi)

Eslatmalar:

- Standart prompt/tizim prompti yetkazib berishni bostirish uchun `NO_REPLY` ishorasini o‘z ichiga oladi.
- Flush har bir siqish (compaction) siklida bir marta ishga tushadi (`sessions.json` da kuzatiladi).
- Flush faqat ichki (embedded) Pi sessiyalari uchun ishlaydi (CLI backendlar uni o‘tkazib yuboradi).
- Sessiya ishchi muhiti faqat o‘qish uchun bo‘lsa (`workspaceAccess: "ro"` yoki `"none"`), flush o‘tkazib yuboriladi.
- Ishchi muhitdagi fayllar joylashuvi va yozish naqshlari uchun [Memory](/concepts/memory) ga qarang.

Pi kengaytma API’da `session_before_compact` xukini ham taqdim etadi, ammo OpenClaw’ning flush mantiqi hozircha Gateway tomonida joylashgan.

---

## Nosozliklarni bartaraf etish uchun tekshiruv ro‘yxati

- Sessiya kaliti noto‘g‘rimi? [/concepts/session](/concepts/session) dan boshlang va `/status` dagi `sessionKey` ni tasdiqlang.
- Saqlash (store) va transkript mos kelmayaptimi? `openclaw status` dan Gateway xosti va saqlash yo‘lini tasdiqlang.
- Siqish (compaction) haddan tashqari ko‘pmi? Tekshiring:
  - model kontekst oynasi (juda kichik)
  - siqish sozlamalari (`reserveTokens` model oynasi uchun juda yuqori bo‘lsa, erta siqishga olib kelishi mumkin)
  - vosita-natija shishishi: sessiyani qisqartirishni (pruning) yoqing/sozlang
- Jim navbatlar sizib chiqyaptimi? Javob `NO_REPLY` (aniq token) bilan boshlanishini va siz streaming bostirish tuzatishi kiritilgan buildda ekaningizni tasdiqlang.
