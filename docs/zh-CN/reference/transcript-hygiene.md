---
summary: "Reference: provider-specific transcript sanitization and repair rules"
read_when:
  - You are debugging provider request rejections tied to transcript shape
  - You are changing transcript sanitization or tool-call repair logic
  - You are investigating tool-call id mismatches across providers
title: "Transcript Hygiene"
---

# Transcript Hygiene (Provider Fixups)

This document describes **provider-specific fixes** applied to transcripts before a run
(building model context). These are **in-memory** adjustments used to satisfy strict
provider requirements. These hygiene steps do **not** rewrite the stored JSONL transcript
on disk; however, a separate session-file repair pass may rewrite malformed JSONL files
by dropping invalid lines before the session is loaded. When a repair occurs, the original
file is backed up alongside the session file.

Scope includes:

- Tool call id sanitization
- Tool call input validation
- Tool result pairing repair
- Turn validation / ordering
- Thought signature cleanup
- Image payload sanitization

If you need transcript storage details, see:

- [/reference/session-management-compaction](/reference/session-management-compaction)

---

## Where this runs

All transcript hygiene is centralized in the embedded runner:

- Policy selection: `src/agents/transcript-policy.ts`
- Sanitization/repair application: `sanitizeSessionHistory` in `src/agents/pi-embedded-runner/google.ts`

The policy uses `provider`, `modelApi`, and `modelId` to decide what to apply.

Separate from transcript hygiene, session files are repaired (if needed) before load:

- `repairSessionFileIfNeeded` in `src/agents/session-file-repair.ts`
- Called from `run/attempt.ts` and `compact.ts` (embedded runner)

---

## Global rule: image sanitization

Image payloads are always sanitized to prevent provider-side rejection due to size
limits (downscale/recompress oversized base64 images).

Implementation:

- `sanitizeSessionMessagesImages` in `src/agents/pi-embedded-helpers/images.ts`
- `sanitizeContentBlocksImages` in `src/agents/tool-images.ts`

---

## Global rule: malformed tool calls

Assistant tool-call blocks that are missing both `input` and `arguments` are dropped
before model context is built. This prevents provider rejections from partially
persisted tool calls (for example, after a rate limit failure).

Implementation:

- `sanitizeToolCallInputs` in `src/agents/session-transcript-repair.ts`
- Applied in `sanitizeSessionHistory` in `src/agents/pi-embedded-runner/google.ts`

---

## Provider matrix (current behavior)

**OpenAI / OpenAI Codex**

- Image sanitization only.
- On model switch into OpenAI Responses/Codex, drop orphaned reasoning signatures (standalone reasoning items without a following content block).
- No tool call id sanitization.
- No tool result pairing repair.
- No turn validation or reordering.
- No synthetic tool results.
- No thought signature stripping.

**Google (Generative AI / Gemini CLI / Antigravity)**

- Tool call id sanitization: strict alphanumeric.
- Tool result pairing repair and synthetic tool results.
- 1. 回合校验（Gemini 风格的回合交替）。
- 2. Google 回合顺序修复（如果历史以 assistant 开始，则在前面添加一个极小的 user 引导）。
- 3. 反重力 Claude：规范化思考签名；丢弃未签名的思考块。

4. **Anthropic / Minimax（Anthropic 兼容）**

- 5. 工具结果配对修复与合成工具结果。
- 6. 回合校验（合并连续的 user 回合以满足严格交替）。

7. **Mistral（包括基于 model-id 的检测）**

- 8. 工具调用 id 清理：strict9（字母数字，长度 9）。

9. **OpenRouter Gemini**

- 10. 思考签名清理：移除非 base64 的 `thought_signature` 值（保留 base64）。

11. **其他所有情况**

- 12. 仅进行图像清理。

---

## 13. 历史行为（2026.1.22 之前）

14. 在 2026.1.22 发布之前，OpenClaw 应用了多层对话记录清理：

- 15. **transcript-sanitize 扩展**在每次构建上下文时运行，并且可以：
  - 16. 修复工具使用/结果配对。
  - 17. 清理工具调用 id（包括保留 `_`/`-` 的非严格模式）。
- 18. 运行器还执行了特定于提供方的清理，从而产生了重复工作。
- 19. 还发生了提供方策略之外的额外变更，包括：
  - 20. 在持久化之前从 assistant 文本中移除 `<final>` 标签。
  - 21. 丢弃空的 assistant 错误回合。
  - 22. 在工具调用后裁剪 assistant 内容。

23. 这种复杂性导致了跨提供方的回归问题（尤其是 `openai-responses`
    `call_id|fc_id` 配对）。 24. 2026.1.22 的清理移除了该扩展，将逻辑集中到运行器中，并使 OpenAI 除了图像清理之外保持 **no-touch**。
