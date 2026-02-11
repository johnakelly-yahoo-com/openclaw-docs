---
summary: "Sessionlarni ro‘yxatlash, tarixni olish va sessionlararo xabar yuborish uchun agent session tool’lari"
read_when:
  - Session tool’larini qo‘shish yoki o‘zgartirish
title: "Session Tool’lari"
---

# Session Tool’lari

Maqsad: agentlar sessionlarni ro‘yxatlay olishi, tarixni ola olishi va boshqa sessionga yubora olishi uchun kichik va suiiste’mol qilish qiyin bo‘lgan tool to‘plami.

## Tool nomlari

- `sessions_list`
- `sessions_history`
- `sessions_send`
- `sessions_spawn`

## Kalit modeli

- Asosiy to‘g‘ridan-to‘g‘ri chat bucket har doim literal kalit `"main"` bo‘ladi (joriy agentning asosiy kalitiga yechiladi).
- Guruh chatlari `agent:<agentId>:<channel>:group:<id>` yoki `agent:<agentId>:<channel>:channel:<id>` dan foydalanadi (to‘liq kalitni uzating).
- Cron job’lar `cron:<job.id>` dan foydalanadi.
- Hook’lar aniq belgilab qo‘yilmagan bo‘lsa `hook:<uuid>` dan foydalanadi.
- Node session’lari aniq belgilab qo‘yilmagan bo‘lsa `node-<nodeId>` dan foydalanadi.

`global` va `unknown` rezerv qilingan qiymatlar bo‘lib, hech qachon ro‘yxatlanmaydi. Agar `session.scope = "global"` bo‘lsa, biz uni barcha tool’lar uchun `main` ga alias qilamiz, shunda chaqiruvchilar hech qachon `global` ni ko‘rmaydi.

## sessions_list

List sessions as an array of rows.

Parameters:

- `kinds?: string[]` filter: any of `"main" | "group" | "cron" | "hook" | "node" | "other"`
- `limit?: number` max rows (default: server default, clamp e.g. 200)
- Qarang: [/concepts/compaction](/concepts/compaction).
- `messageLimit?: number` 0 = no messages (default 0); >0 = include last N messages

Behavior:

- `messageLimit > 0` fetches `chat.history` per session and includes the last N messages.
- Tool results are filtered out in list output; use `sessions_history` for tool messages.
- When running in a **sandboxed** agent session, session tools default to **spawned-only visibility** (see below).

Row shape (JSON):

- `key`: session key (string)
- `kind`: `main | group | cron | hook | node | other`
- `channel`: `whatsapp | telegram | discord | signal | imessage | webchat | internal | unknown`
- `displayName` (group display label if available)
- `updatedAt` (ms)
- `sessionId`
- `model`, `contextTokens`, `totalTokens`
- `thinkingLevel`, `verboseLevel`, `systemSent`, `abortedLastRun`
- `sendPolicy` (session override if set)
- `lastChannel`, `lastTo`
- `deliveryContext` (normalized `{ channel, to, accountId }` when available)
- `transcriptPath` (best-effort path derived from store dir + sessionId)
- `messages?` (only when `messageLimit > 0`)

## sessions_history

Fetch transcript for one session.

Parameters:

- `sessionKey` (required; accepts session key or `sessionId` from `sessions_list`)
- `limit?: number` max messages (server clamps)
- `includeTools?: boolean` (default false)

Behavior:

- `includeTools=false` filters `role: "toolResult"` messages.
- Returns messages array in the raw transcript format.
- When given a `sessionId`, OpenClaw resolves it to the corresponding session key (missing ids error).

## sessions_send

Send a message into another session.

Parameters:

- `sessionKey` (required; accepts session key or `sessionId` from `sessions_list`)
- `message` (required)
- `timeoutSeconds?: number` (default >0; 0 = fire-and-forget)

Behavior:

- `timeoutSeconds = 0`: enqueue and return `{ runId, status: "accepted" }`.
- `timeoutSeconds > 0`: wait up to N seconds for completion, then return `{ runId, status: "ok", reply }`.
- If wait times out: `{ runId, status: "timeout", error }`. Run continues; call `sessions_history` later.
- If the run fails: `{ runId, status: "error", error }`.
- Announce delivery runs after the primary run completes and is best-effort; `status: "ok"` does not guarantee the announce was delivered.
- Waits via gateway `agent.wait` (server-side) so reconnects don't drop the wait.
- Agent-to-agent message context is injected for the primary run.
- After the primary run completes, OpenClaw runs a **reply-back loop**:
  - 1. 2+ raund so‘rovchi va nishon agentlar o‘rtasida navbatma‑navbat almashadi.
  - 2. Ping‑pongni to‘xtatish uchun aniq `REPLY_SKIP` deb javob bering.
  - 3. Maksimal burilishlar soni `session.agentToAgent.maxPingPongTurns` (0–5, standart 5).
- 4. Tsikl tugagach, OpenClaw **agentdan‑agentga e’lon qilish bosqichi**ni ishga tushiradi (faqat nishon agent):
  - 5. Jim qolish uchun aniq `ANNOUNCE_SKIP` deb javob bering.
  - 6. Boshqa har qanday javob nishon kanaliga yuboriladi.
  - 7. E’lon bosqichi asl so‘rov + 1‑rau ndagi javob + so‘nggi ping‑pong javobini o‘z ichiga oladi.

## 8. Kanal maydoni

- 9. Guruhlar uchun `channel` sessiya yozuvida qayd etilgan kanal bo‘ladi.
- 10. To‘g‘ridan‑to‘g‘ri chatlar uchun `channel` `lastChannel`dan moslanadi.
- 11. Cron/hook/node uchun `channel` — `internal`.
- 12. Agar mavjud bo‘lmasa, `channel` — `unknown`.

## 13. Xavfsizlik / Yuborish siyosati

14. Kanal/chat turi bo‘yicha siyosatga asoslangan bloklash (sessiya identifikatori bo‘yicha emas).

```json
15. {
  "session": {
    "sendPolicy": {
      "rules": [
        {
          "match": { "channel": "discord", "chatType": "group" },
          "action": "deny"
        }
      ],
      "default": "allow"
    }
  }
}
```

16. Ish vaqtida bekor qilish (har bir sessiya yozuvi uchun):

- 17. `sendPolicy: "allow" | "deny"` (o‘rnatilmasa = konfiguratsiyani meros qilib oladi)
- 18. `sessions.patch` orqali yoki faqat egaga ruxsat etilgan `/send on|off|inherit` (alohida xabar) orqali o‘rnatiladi.

19. Majburiy ijro nuqtalari:

- 20. `chat.send` / `agent` (shlyuz)
- 21. avtomatik javob yetkazib berish mantiqi

## 22. sessions_spawn

23. Izolyatsiyalangan sessiyada quyi‑agent ishini ishga tushiring va natijani so‘rovchi chat kanaliga e’lon qiling.

24. Parametrlar:

- 25. `task` (majburiy)
- 26. `label?` (ixtiyoriy; loglar/UI uchun ishlatiladi)
- 27. `agentId?` (ixtiyoriy; ruxsat etilsa, boshqa agent identifikatori ostida ishga tushiradi)
- 28. `model?` (ixtiyoriy; quyi‑agent modelini almashtiradi; noto‘g‘ri qiymatlar xato beradi)
- 29. `runTimeoutSeconds?` (standart 0; o‘rnatilganda, N soniyadan so‘ng quyi‑agent ishini to‘xtatadi)
- 30. `cleanup?` (`delete|keep`, standart `keep`)

31. Ruxsat etilganlar ro‘yxati:

- 32. `agents.list[].subagents.allowAgents`: `agentId` orqali ruxsat etilgan agent identifikatorlari ro‘yxati (`["*"]` — har qandayiga ruxsat). 33. Standart: faqat so‘rovchi agent.

34. Aniqlash:

- 35. `sessions_spawn` uchun qaysi agent identifikatorlariga ruxsat berilganini aniqlashda `agents_list`dan foydalaning.

36. Xatti‑harakat:

- 37. `deliver: false` bilan yangi `agent:<agentId>:subagent:<uuid>` sessiyasini boshlaydi.
- 38. Quyi‑agentlar sukut bo‘yicha to‘liq vositalar to‘plamiga ega bo‘ladi **sessiya vositalarisiz** ( `tools.subagents.tools` orqali sozlanadi ).
- 39. Quyi‑agentlarga `sessions_spawn`ni chaqirishga ruxsat berilmaydi (quyi‑agent → quyi‑agent ishga tushirish yo‘q).
- 40. Har doim bloklanmaydi: darhol `{ status: "accepted", runId, childSessionKey }`ni qaytaradi.
- 41. Yakunlangach, OpenClaw quyi‑agent **e’lon qilish bosqichi**ni ishga tushiradi va natijani so‘rovchi chat kanaliga joylaydi.
- 42. E’lon bosqichida jim qolish uchun aniq `ANNOUNCE_SKIP` deb javob bering.
- 43. E’lon javoblari `Status`/`Result`/`Notes` ga normallashtiriladi; `Status` ish vaqti natijasidan olinadi (model matnidan emas).
- 44. Quyi‑agent sessiyalari `agents.defaults.subagents.archiveAfterMinutes` dan so‘ng avtomatik arxivlanadi (standart: 60).
- 45. E’lon javoblari statistika qatorini o‘z ichiga oladi (ish vaqti, tokenlar, sessionKey/sessionId, transkript yo‘li va ixtiyoriy xarajat).

## 46. Sandbox sessiya ko‘rinuvchanligi

47. Sandboxlangan sessiyalar sessiya vositalaridan foydalanishi mumkin, ammo sukut bo‘yicha ular faqat `sessions_spawn` orqali o‘zlari ishga tushirgan sessiyalarni ko‘ra oladi.

48. Konfiguratsiya:

```json5
49. {
  agents: {
    defaults: {
      sandbox: {
        // default: "spawned"
        sessionToolsVisibility: "spawned", // yoki "all"
      },
    },
  },
}
```
