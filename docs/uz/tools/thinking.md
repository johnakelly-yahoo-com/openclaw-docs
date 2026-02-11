---
summary: "Directive syntax for /think + /verbose and how they affect model reasoning"
read_when:
  - Adjusting thinking or verbose directive parsing or defaults
title: "Thinking Levels"
---

# Thinking Levels (/think directives)

## What it does

- Inline directive in any inbound body: `/t <level>`, `/think:<level>`, or `/thinking <level>`.
- Levels (aliases): `off | minimal | low | medium | high | xhigh` (GPT-5.2 + Codex models only)
  - minimal → “think”
  - low → “think hard”
  - medium → “think harder”
  - high → “ultrathink” (max budget)
  - xhigh → “ultrathink+” (GPT-5.2 + Codex models only)
  - `x-high`, `x_high`, `extra-high`, `extra high`, and `extra_high` map to `xhigh`.
  - `highest`, `max` map to `high`.
- Provider notes:
  - Z.AI (`zai/*`) only supports binary thinking (`on`/`off`). Any non-`off` level is treated as `on` (mapped to `low`).

## Resolution order

1. Inline directive on the message (applies only to that message).
2. Session override (set by sending a directive-only message).
3. Global default (`agents.defaults.thinkingDefault` in config).
4. Fallback: low for reasoning-capable models; off otherwise.

## Setting a session default

- Send a message that is **only** the directive (whitespace allowed), e.g. `/think:medium` or `/t high`.
- That sticks for the current session (per-sender by default); cleared by `/think:off` or session idle reset.
- Confirmation reply is sent (`Thinking level set to high.` / `Thinking disabled.`). If the level is invalid (e.g. `/thinking big`), the command is rejected with a hint and the session state is left unchanged.
- Send `/think` (or `/think:`) with no argument to see the current thinking level.

## Application by agent

- **Embedded Pi**: the resolved level is passed to the in-process Pi agent runtime.

## Verbose directives (/verbose or /v)

- Levels: `on` (minimal) | `full` | `off` (default).
- Directive-only message toggles session verbose and replies `Verbose logging enabled.` / `Verbose logging disabled.`; invalid levels return a hint without changing state.
- `/verbose off` stores an explicit session override; clear it via the Sessions UI by choosing `inherit`.
- Inline directive affects only that message; session/global defaults apply otherwise.
- Send `/verbose` (or `/verbose:`) with no argument to see the current verbose level.
- When verbose is on, agents that emit structured tool results (Pi, other JSON agents) send each tool call back as its own metadata-only message, prefixed with `<emoji> <tool-name>: <arg>` when available (path/command). These tool summaries are sent as soon as each tool starts (separate bubbles), not as streaming deltas.
- When verbose is `full`, tool outputs are also forwarded after completion (separate bubble, truncated to a safe length). If you toggle `/verbose on|full|off` while a run is in-flight, subsequent tool bubbles honor the new setting.

## Reasoning visibility (/reasoning)

- Levels: `on|off|stream`.
- Directive-only message toggles whether thinking blocks are shown in replies.
- When enabled, reasoning is sent as a **separate message** prefixed with `Reasoning:`.
- `stream` (Telegram only): streams reasoning into the Telegram draft bubble while the reply is generating, then sends the final answer without reasoning.
- Alias: `/reason`.
- Send `/reasoning` (or `/reasoning:`) with no argument to see the current reasoning level.

## Bogʻliq

- Yuqori rejim hujjatlari [Elevated mode](/tools/elevated) sahifasida joylashgan.

## Heartbeatlar

- Heartbeat probe tanasi sozlangan heartbeat promptidir (standart: `Read HEARTBEAT.md if it exists (workspace context). Bunga qatʼiy amal qiling. Oldingi chatlardan eski vazifalarni taxmin qilmang yoki takrorlamang. Agar eʼtibor talab qilinadigan narsa boʻlmasa, HEARTBEAT_OK.`) deb javob bering. Heartbeat xabaridagi inline direktivalar odatdagidek qoʻllaniladi (lekin heartbeatlar orqali sessiya standartlarini oʻzgartirishdan saqlaning).
- Heartbeat yetkazilishi standart holatda faqat yakuniy payload bilan cheklanadi. Alohida `Reasoning:` xabarini ham yuborish uchun (mavjud boʻlsa), `agents.defaults.heartbeat.includeReasoning: true` yoki har bir agent uchun `agents.list[].heartbeat.includeReasoning: true` ni sozlang.

## Veb chat UI

- Sahifa yuklanganda veb chatdagi thinking selector kiruvchi sessiya store/config dagi saqlangan darajani aks ettiradi.
- Boshqa darajani tanlash faqat keyingi xabarga qoʻllaniladi (`thinkingOnce`); yuborilgandan soʻng selector sessiyada saqlangan darajaga qaytadi.
- Sessiya standartini oʻzgartirish uchun `/think:<level>` direktivasini yuboring (avvalgidek); keyingi qayta yuklashdan soʻng selector buni aks ettiradi.
