---
summary: "26. CLI backendlar: mahalliy AI CLI’lar orqali faqat matnli zaxira yo‘li"
read_when:
  - 27. API provayderlari ishdan chiqqanda ishonchli zaxira yo‘lini xohlaysiz
  - 28. Siz Claude Code CLI yoki boshqa mahalliy AI CLI’larni ishga tushiryapsiz va ularni qayta ishlatmoqchisiz
  - 29. Sessiyalar va rasmlarni qo‘llab-quvvatlaydigan, lekin faqat matnli, vositalarsiz yo‘l kerak
title: "30. CLI Backendlar"
---

# 31. CLI backendlar (zaxira ijro muhiti)

32. OpenClaw API provayderlari ishlamay qolganda, cheklanganda yoki vaqtincha nosoz bo‘lganda **mahalliy AI CLI**larni **faqat matnli zaxira** sifatida ishga tushirishi mumkin. 33. Bu ataylab konservativ:

- 34. **Vositalar o‘chirilgan** (tool chaqiriqlari yo‘q).
- 35. **Matn kiradi → matn chiqadi** (ishonchli).
- 36. **Sessiyalar qo‘llab-quvvatlanadi** (keyingi navbatlar izchil bo‘lib qoladi).
- 37. **Rasmlar uzatilishi mumkin**, agar CLI rasm yo‘llarini qabul qilsa.

38. Bu asosiy yo‘l emas, balki **xavfsizlik tarmog‘i** sifatida mo‘ljallangan. 39. Uni tashqi API’larga tayanmasdan “har doim ishlaydi” degan matnli javoblar xohlaganingizda ishlating.

## 40. Boshlovchilar uchun tezkor start

41. Siz Claude Code CLI’dan **hech qanday konfiguratsiyasiz** foydalanishingiz mumkin (OpenClaw ichki standart bilan keladi):

```bash
42. openclaw agent --message "hi" --model claude-cli/opus-4.6
```

43. Codex CLI ham qutidan chiqishi bilan ishlaydi:

```bash
44. openclaw agent --message "hi" --model codex-cli/gpt-5.3-codex
```

45. Agar shlyuzingiz launchd/systemd ostida ishlasa va PATH minimal bo‘lsa, faqat buyruq yo‘lini qo‘shing:

```json5
46. {
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
      },
    },
  },
}
```

47. Shuning o‘zi kifoya. 48. CLI’ning o‘zidan tashqari hech qanday kalitlar yoki qo‘shimcha autentifikatsiya sozlamalari kerak emas.

## 49. Uni zaxira sifatida ishlatish

50. Asosiy modellaringiz ishlamay qolgandagina ishga tushishi uchun zaxira ro‘yxatiga CLI backend qo‘shing:

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["claude-cli/opus-4.6", "claude-cli/opus-4.5"],
      },
      models: {
        "anthropic/claude-opus-4-6": { alias: "Opus" },
        "claude-cli/opus-4.6": {},
        "claude-cli/opus-4.5": {},
      },
    },
  },
}
```

Notes:

- If you use `agents.defaults.models` (allowlist), you must include `claude-cli/...`.
- If the primary provider fails (auth, rate limits, timeouts), OpenClaw will
  try the CLI backend next.

## Configuration overview

All CLI backends live under:

```
agents.defaults.cliBackends
```

Each entry is keyed by a **provider id** (e.g. `claude-cli`, `my-cli`).
The provider id becomes the left side of your model ref:

```
<provider>/<model>
```

### Example configuration

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
        "my-cli": {
          command: "my-cli",
          args: ["--json"],
          output: "json",
          input: "arg",
          modelArg: "--model",
          modelAliases: {
            "claude-opus-4-6": "opus",
            "claude-opus-4-5": "opus",
            "claude-sonnet-4-5": "sonnet",
          },
          sessionArg: "--session",
          sessionMode: "existing",
          sessionIdFields: ["session_id", "conversation_id"],
          systemPromptArg: "--system",
          systemPromptWhen: "first",
          imageArg: "--image",
          imageMode: "repeat",
          serialize: true,
        },
      },
    },
  },
}
```

## How it works

1. **Selects a backend** based on the provider prefix (`claude-cli/...`).
2. **Builds a system prompt** using the same OpenClaw prompt + workspace context.
3. **Executes the CLI** with a session id (if supported) so history stays consistent.
4. **Parses output** (JSON or plain text) and returns the final text.
5. **Persists session ids** per backend, so follow-ups reuse the same CLI session.

## Sessions

- If the CLI supports sessions, set `sessionArg` (e.g. `--session-id`) or
  `sessionArgs` (placeholder `{sessionId}`) when the ID needs to be inserted
  into multiple flags.
- If the CLI uses a **resume subcommand** with different flags, set
  `resumeArgs` (replaces `args` when resuming) and optionally `resumeOutput`
  (for non-JSON resumes).
- `sessionMode`:
  - `always`: always send a session id (new UUID if none stored).
  - `existing`: only send a session id if one was stored before.
  - `none`: never send a session id.

## Images (pass-through)

If your CLI accepts image paths, set `imageArg`:

```json5
imageArg: "--image",
imageMode: "repeat"
```

OpenClaw will write base64 images to temp files. If `imageArg` is set, those
paths are passed as CLI args. If `imageArg` is missing, OpenClaw appends the
file paths to the prompt (path injection), which is enough for CLIs that auto-
load local files from plain paths (Claude Code CLI behavior).

## Inputs / outputs

- `output: "json"` (default) tries to parse JSON and extract text + session id.
- `output: "jsonl"` parses JSONL streams (Codex CLI `--json`) and extracts the
  last agent message plus `thread_id` when present.
- `output: "text"` treats stdout as the final response.

Input modes:

- `input: "arg"` (default) passes the prompt as the last CLI arg.
- `input: "stdin"` sends the prompt via stdin.
- If the prompt is very long and `maxPromptArgChars` is set, stdin is used.

## Defaults (built-in)

OpenClaw ships a default for `claude-cli`:

- `command: "claude"`
- `args: ["-p", "--output-format", "json", "--dangerously-skip-permissions"]`
- `resumeArgs: ["-p", "--output-format", "json", "--dangerously-skip-permissions", "--resume", "{sessionId}"]`
- `modelArg: "--model"`
- `systemPromptArg: "--append-system-prompt"`
- `sessionArg: "--session-id"`
- `systemPromptWhen: "first"`
- `sessionMode: "always"`

OpenClaw also ships a default for `codex-cli`:

- `command: "codex"`
- `args: ["exec","--json","--color","never","--sandbox","read-only","--skip-git-repo-check"]`
- `resumeArgs: ["exec","resume","{sessionId}","--color","never","--sandbox","read-only","--skip-git-repo-check"]`
- `output: "jsonl"`
- `resumeOutput: "text"`
- `modelArg: "--model"`
- `imageArg: "--image"`
- `sessionMode: "existing"`

Override only if needed (common: absolute `command` path).

## Limitations

- **No OpenClaw tools** (the CLI backend never receives tool calls). Some CLIs
  may still run their own agent tooling.
- **No streaming** (CLI output is collected then returned).
- **Structured outputs** depend on the CLI’s JSON format.
- **Codex CLI sessions** resume via text output (no JSONL), which is less
  structured than the initial `--json` run. OpenClaw sessions still work
  normally.

## Troubleshooting

- **CLI not found**: set `command` to a full path.
- **Wrong model name**: use `modelAliases` to map `provider/model` → CLI model.
- **No session continuity**: ensure `sessionArg` is set and `sessionMode` is not
  `none` (Codex CLI currently cannot resume with JSON output).
- **Images ignored**: set `imageArg` (and verify CLI supports file paths).
