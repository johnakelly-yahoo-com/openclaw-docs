---
summary: "Direct `openclaw agent` CLI runs (with optional delivery)"
read_when:
  - Adding or modifying the agent CLI entrypoint
title: "Agent Send"
---

# `openclaw agent` (to‘g‘ridan-to‘g‘ri agent ishga tushirishlari)

`openclaw agent` kiruvchi chat xabarisiz bitta agent navbatini ishga tushiradi.
By default it goes **through the Gateway**; add `--local` to force the embedded
runtime on the current machine.

## Behavior

- Required: `--message <text>`
- Session selection:
  - `--to <dest>` derives the session key (group/channel targets preserve isolation; direct chats collapse to `main`), **or**
  - `--session-id <id>` reuses an existing session by id, **or**
  - `--agent <id>` targets a configured agent directly (uses that agent's `main` session key)
- Runs the same embedded agent runtime as normal inbound replies.
- Thinking/verbose bayroqlari sessiya omborida saqlanib qoladi.
- Output:
  - default: prints reply text (plus `MEDIA:<url>` lines)
  - 1. `--json`: tuzilgan payload + metadata ni chiqaradi
- Optional delivery back to a channel with `--deliver` + `--channel` (target formats match `openclaw message --target`).
- Use `--reply-channel`/`--reply-to`/`--reply-account` to override delivery without changing the session.

If the Gateway is unreachable, the CLI **falls back** to the embedded local run.

## Examples

```bash
openclaw agent --to +15555550123 --message "status update"
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --to +15555550123 --message "Trace logs" --verbose on --json
openclaw agent --to +15555550123 --message "Summon reply" --deliver
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
```

## Flags

- `--local`: run locally (requires model provider API keys in your shell)
- `--deliver`: send the reply to the chosen channel
- `--channel`: delivery channel (`whatsapp|telegram|discord|googlechat|slack|signal|imessage`, default: `whatsapp`)
- `--reply-to`: delivery target override
- 2. `--reply-channel`: yetkazib berish kanalini almashtirish
- `--reply-account`: yetkazib berish akkaunti ID’si uchun override
- 3. `--thinking <off|minimal|low|medium|high|xhigh>`: fikrlash darajasini saqlab qolish (faqat GPT-5.2 + Codex modellari)
- `--verbose <on|full|off>`: batafsillik darajasini saqlash
- `--timeout <seconds>`: agent vaqt cheklovini override qilish
- `--json`: tuzilgan JSON chiqishi
