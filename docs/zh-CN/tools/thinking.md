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

## 相关

- 提升模式文档位于 [提升模式](/tools/elevated)。

## 心跳

- 心跳探测主体是配置的心跳提示（默认值：`Read HEARTBEAT.md if it exists (workspace context).`）。 请严格遵循。 不要从先前的聊天中推断或重复旧任务。 如果没有需要关注的事项，请回复 HEARTBEAT_OK.\`）。 心跳消息中的内联指令照常生效（但避免通过心跳更改会话默认设置）。
- 心跳交付默认仅包含最终负载。 如需同时发送单独的 `Reasoning:` 消息（如果可用），请设置 `agents.defaults.heartbeat.includeReasoning: true` 或按代理设置 `agents.list[].heartbeat.includeReasoning: true`。

## Web 聊天 UI

- Web 聊天的思考级别选择器在页面加载时会镜像入站会话存储/配置中保存的会话级别。
- 选择其他级别仅适用于下一条消息（`thinkingOnce`）；发送后，选择器会恢复到已保存的会话级别。
- 要更改会话默认值，请发送 `/think:<level>` 指令（与之前相同）；下次重新加载后选择器将反映该更改。
