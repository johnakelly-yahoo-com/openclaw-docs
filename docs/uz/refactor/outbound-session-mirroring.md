---
title: 40. Chiqish sessiyasini ko‘zgulashni qayta tuzish (Issue #1520)
description: 41. Chiqish sessiyasini ko‘zgulashni qayta tuzish bo‘yicha qaydlar, qarorlar, testlar va ochiq masalalarni kuzatish.
---

# 42. Chiqish sessiyasini ko‘zgulashni qayta tuzish (Issue #1520)

## 43. Holat

- 44. Jarayonda.
- 45. Chiqish ko‘zgulash uchun Core + plagin kanal marshrutlash yangilandi.
- 46. Gateway yuborishi endi sessionKey ko‘rsatilmaganida maqsad sessiyani aniqlaydi.

## 47. Kontekst

48. Chiqish yuborishlari maqsad kanal sessiyasi o‘rniga _joriy_ agent sessiyasiga (asbob sessiya kaliti) ko‘zgulanardi. 49. Kirish marshrutlash kanal/peer sessiya kalitlaridan foydalanadi, shu sababli chiqish javoblari noto‘g‘ri sessiyaga tushar va birinchi aloqa maqsadlarida ko‘pincha sessiya yozuvlari bo‘lmasdi.

## 50. Maqsadlar

- Mirror outbound messages into the target channel session key.
- Create session entries on outbound when missing.
- Keep thread/topic scoping aligned with inbound session keys.
- Cover core channels plus bundled extensions.

## Implementation Summary

- New outbound session routing helper:
  - `src/infra/outbound/outbound-session.ts`
  - `resolveOutboundSessionRoute` builds target sessionKey using `buildAgentSessionKey` (dmScope + identityLinks).
  - `ensureOutboundSessionEntry` writes minimal `MsgContext` via `recordSessionMetaFromInbound`.
- `runMessageAction` (send) derives target sessionKey and passes it to `executeSendAction` for mirroring.
- `message-tool` no longer mirrors directly; it only resolves agentId from the current session key.
- Plugin send path mirrors via `appendAssistantMessageToSessionTranscript` using the derived sessionKey.
- Gateway send derives a target session key when none is provided (default agent), and ensures a session entry.

## Thread/Topic Handling

- Slack: replyTo/threadId -> `resolveThreadSessionKeys` (suffix).
- Discord: threadId/replyTo -> `resolveThreadSessionKeys` with `useSuffix=false` to match inbound (thread channel id already scopes session).
- Telegram: topic IDs map to `chatId:topic:<id>` via `buildTelegramGroupPeerId`.

## Extensions Covered

- Matrix, MS Teams, Mattermost, BlueBubbles, Nextcloud Talk, Zalo, Zalo Personal, Nostr, Tlon.
- Notes:
  - Mattermost targets now strip `@` for DM session key routing.
  - Zalo Personal uses DM peer kind for 1:1 targets (group only when `group:` is present).
  - BlueBubbles group targets strip `chat_*` prefixes to match inbound session keys.
  - Slack auto-thread mirroring matches channel ids case-insensitively.
  - Gateway send lowercases provided session keys before mirroring.

## Decisions

- **Gateway send session derivation**: if `sessionKey` is provided, use it. If omitted, derive a sessionKey from target + default agent and mirror there.
- **Session entry creation**: always use `recordSessionMetaFromInbound` with `Provider/From/To/ChatType/AccountId/Originating*` aligned to inbound formats.
- **Target normalization**: outbound routing uses resolved targets (post `resolveChannelTarget`) when available.
- **Session key casing**: canonicalize session keys to lowercase on write and during migrations.

## Tests Added/Updated

- `src/infra/outbound/outbound-session.test.ts`
  - Slack thread session key.
  - Telegram topic session key.
  - dmScope identityLinks with Discord.
- `src/agents/tools/message-tool.test.ts`
  - Derives agentId from session key (no sessionKey passed through).
- `src/gateway/server-methods/send.test.ts`
  - Derives session key when omitted and creates session entry.

## Open Items / Follow-ups

- Voice-call plugin uses custom `voice:<phone>` session keys. Outbound mapping is not standardized here; if message-tool should support voice-call sends, add explicit mapping.
- Confirm if any external plugin uses non-standard `From/To` formats beyond the bundled set.

## Files Touched

- `src/infra/outbound/outbound-session.ts`
- `src/infra/outbound/outbound-send-service.ts`
- `src/infra/outbound/message-action-runner.ts`
- `src/agents/tools/message-tool.ts`
- `src/gateway/server-methods/send.ts`
- Tests in:
  - `src/infra/outbound/outbound-session.test.ts`
  - `src/agents/tools/message-tool.test.ts`
  - `src/gateway/server-methods/send.test.ts`
