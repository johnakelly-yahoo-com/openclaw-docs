---
summary: "Telegram 允许列表加固：前缀 + 空白规范化"
read_when:
  - Reviewing historical Telegram allowlist changes
title: "Telegram 允许列表加固"
---

# Telegram 允许列表加固

**Date**: 2026-01-05  
**Status**: Complete  
**PR**: #216

## 摘要

Telegram allowlists now accept `telegram:` and `tg:` prefixes case-insensitively, and tolerate
accidental whitespace. 这使入站允许列表检查与出站发送规范化保持一致。

## What changed

- Prefixes `telegram:` and `tg:` are treated the same (case-insensitive).
- Allowlist entries are trimmed; empty entries are ignored.

## Examples

All of these are accepted for the same ID:

- `telegram:123456`
- `TG:123456`
- `tg:123456`

## Why it matters

Copy/paste from logs or chat IDs often includes prefixes and whitespace. Normalizing avoids
false negatives when deciding whether to respond in DMs or groups.

## Related docs

- [Group Chats](/channels/groups)
- [Telegram Provider](/channels/telegram)
