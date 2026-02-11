---
summary: "50. Chatlar uchun sessiyani boshqarish qoidalari, kalitlar va saqlanishi"
read_when:
  - Modifying session handling or storage
title: "Session Management"
---

# Session Management

OpenClaw treats **one direct-chat session per agent** as primary. Direct chats collapse to `agent:<agentId>:<mainKey>` (default `main`), while group/channel chats get their own keys. `activeMinutes?: number` — faqat N daqiqa ichida yangilangan sessiyalar

`session.mainKey` hisobga olinadi.

- `main` (default): all DMs share the main session for continuity.
- `per-peer`: isolate by sender id across channels.
- `per-channel-peer`: isolate by channel + sender (recommended for multi-user inboxes).
- `per-account-channel-peer`: isolate by account + channel + sender (recommended for multi-account inboxes).
  Use `session.identityLinks` to map provider-prefixed peer ids to a canonical identity so the same person shares a DM session across channels when using `per-peer`, `per-channel-peer`, or `per-account-channel-peer`.

## Secure DM mode (recommended for multi-user setups)

> **Security Warning:** If your agent can receive DMs from **multiple people**, you should strongly consider enabling secure DM mode. Without it, all users share the same conversation context, which can leak private information between users.

**Example of the problem with default settings:**

- Alice (`<SENDER_A>`) messages your agent about a private topic (for example, a medical appointment)
- Bob (`<SENDER_B>`) messages your agent asking "What were we talking about?"
- Because both DMs share the same session, the model may answer Bob using Alice's prior context.

**The fix:** Set `dmScope` to isolate sessions per user:

```json5
// ~/.openclaw/openclaw.json
{
  session: {
    // Secure DM mode: isolate DM context per channel + sender.
    dmScope: "per-channel-peer",
  },
}
```

**When to enable this:**

- You have pairing approvals for more than one sender
- You use a DM allowlist with multiple entries
- You set `dmPolicy: "open"`
- Multiple phone numbers or accounts can message your agent

Notes:

- Default is `dmScope: "main"` for continuity (all DMs share the main session). This is fine for single-user setups.
- For multi-account inboxes on the same channel, prefer `per-account-channel-peer`.
- If the same person contacts you on multiple channels, use `session.identityLinks` to collapse their DM sessions into one canonical identity.
- You can verify your DM settings with `openclaw security audit` (see [security](/cli/security)).

## Gateway is the source of truth

All session state is **owned by the gateway** (the “master” OpenClaw). UI clients (macOS app, WebChat, etc.) must query the gateway for session lists and token counts instead of reading local files.

- In **remote mode**, the session store you care about lives on the remote gateway host, not your Mac.
- Token counts shown in UIs come from the gateway’s store fields (`inputTokens`, `outputTokens`, `totalTokens`, `contextTokens`). Clients do not parse JSONL transcripts to “fix up” totals.

## Where state lives

- On the **gateway host**:
  - Store file: `~/.openclaw/agents/<agentId>/sessions/sessions.json` (per agent).
- Transcripts: `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl` (Telegram topic sessions use `.../<SessionId>-topic-<threadId>.jsonl`).
- The store is a map `sessionKey -> { sessionId, updatedAt, ... }`. Deleting entries is safe; they are recreated on demand.
- Group entries may include `displayName`, `channel`, `subject`, `room`, and `space` to label sessions in UIs.
- Session entries include `origin` metadata (label + routing hints) so UIs can explain where a session came from.
- OpenClaw does **not** read legacy Pi/Tau session folders.

## Session pruning

1. OpenClaw sukut bo‘yicha LLM chaqiruvlaridan oldin xotira kontekstidan **eski asbob natijalarini** qisqartiradi.
2. Bu **JSONL tarixini** qayta yozmaydi. 3. Qarang: [/concepts/session-pruning](/concepts/session-pruning).

## 4. Oldindan kompaktlash xotira tozalashi

5. Sessiya avtomatik kompaktlashga yaqinlashganda, OpenClaw **jim xotira tozalash** bosqichini ishga tushirishi mumkin,
   modelga barqaror eslatmalarni diskka yozishni eslatadi. 6. Bu faqat ish maydoni yozish uchun ruxsat etilganida ishlaydi. **To‘g‘ridan-to‘g‘ri xabarlar** qanday guruhlanishini boshqarish uchun `session.dmScope` dan foydalaning:

## 8. Transportlarni → sessiya kalitlariga moslash

- 9. To‘g‘ridan-to‘g‘ri chatlar `session.dmScope` ga amal qiladi (sukut bo‘yicha `main`).
  - 10. `main`: `agent:<agentId>:<mainKey>` (qurilmalar/kanallar bo‘ylab uzluksizlik).
    - 11. Bir nechta telefon raqamlari va kanallar bir xil agentning asosiy kalitiga mos kelishi mumkin; ular bitta suhbatga kirish transportlari sifatida ishlaydi.
  - 12. `per-peer`: `agent:<agentId>:dm:<peerId>`.
  - 13. `per-channel-peer`: `agent:<agentId>:<channel>:dm:<peerId>`.
  - 14. `per-account-channel-peer`: `agent:<agentId>:<channel>:<accountId>:dm:<peerId>` (`accountId` sukut bo‘yicha `default`).
  - 15. Agar `session.identityLinks` provayder prefiksi bilan berilgan peer id ga mos kelsa (masalan `telegram:123`), kanonik kalit `<peerId>` ni almashtiradi, shunda bir xil odam kanallar bo‘ylab bitta sessiyani ulashadi.
- 16. Guruh chatlari holatni izolyatsiya qiladi: `agent:<agentId>:<channel>:group:<id>` (xona/kanallar `agent:<agentId>:<channel>:channel:<id>` dan foydalanadi).
  - Qarang: [Memory](/concepts/memory) va
    [Compaction](/concepts/compaction).
  - 18. Meros `group:<id>` kalitlari migratsiya uchun hanuz tan olinadi.
- 19. Kiruvchi kontekstlar hanuz `group:<id>` dan foydalanishi mumkin; kanal `Provider` dan aniqlanadi va kanonik `agent:<agentId>:<channel>:group:<id>` shakliga normallashtiriladi.
- 20. Boshqa manbalar:
  - 21. Cron vazifalari: `cron:<job.id>`
  - 22. Webhooklar: `hook:<uuid>` (agar hook tomonidan aniq belgilab qo‘yilmagan bo‘lsa)
  - 23. Node ishga tushirishlari: `node-<nodeId>`

## 24. Hayotiy sikl

- 25. Qayta o‘rnatish siyosati: sessiyalar muddati tugaguncha qayta ishlatiladi va muddati keyingi kiruvchi xabarda baholanadi.
- 26. Kunlik qayta o‘rnatish: sukut bo‘yicha **gateway xostidagi mahalliy vaqt bilan 4:00 AM**. 27. Sessiya oxirgi yangilanishi eng so‘nggi kunlik qayta o‘rnatish vaqtidan oldin bo‘lsa, u eskirgan hisoblanadi.
- 28. Bo‘sh turish bo‘yicha qayta o‘rnatish (ixtiyoriy): `idleMinutes` sirpanma bo‘sh turish oynasini qo‘shadi. 29. Kunlik va bo‘sh turish bo‘yicha qayta o‘rnatishlar birgalikda sozlanganida, **qaysi biri avval tugasa**, yangi sessiyani majbur qiladi.
- 30. Meros faqat bo‘sh turish rejimi: agar `session.idleMinutes` ni hech qanday `session.reset`/`resetByType` konfiguratsiyasisiz o‘rnatsangiz, OpenClaw orqaga moslik uchun faqat bo‘sh turish rejimida qoladi.
- 47. // ~/.openclaw/openclaw.json
      {
      session: {
      scope: "per-sender", // guruh kalitlarini alohida saqlash
      dmScope: "main", // DM uzluksizligi (umumiy inboxlar uchun per-channel-peer/per-account-channel-peer qilib o‘rnating)
      identityLinks: {
      alice: ["telegram:123456789", "discord:987654321012345678"],
      },
      reset: {
      // Sukut bo‘yicha: mode=daily, atHour=4 (gateway xosti mahalliy vaqti).
      // Agar idleMinutes ham o‘rnatilsa, qaysi biri tezroq tugasa, o‘sha yutadi.
      mode: "daily",
      atHour: 4,
      idleMinutes: 120,
      },
      resetByType: {
      thread: { mode: "daily", atHour: 4 },
      direct: { mode: "idle", idleMinutes: 240 },
      group: { mode: "idle", idleMinutes: 120 },
      },
      resetByChannel: {
      discord: { mode: "idle", idleMinutes: 10080 },
      },
      resetTriggers: ["/new", "/reset"],
      store: "~/.openclaw/agents/{agentId}/sessions/sessions.json",
      mainKey: "main",
      },
      }
- 31. Kanal bo‘yicha istisnolar (ixtiyoriy): `resetByChannel` kanal uchun qayta o‘rnatish siyosatini bekor qiladi (shu kanal uchun barcha sessiya turlariga qo‘llanadi va `reset`/`resetByType` dan ustun turadi).
- 32. Qayta o‘rnatish triggerlari: aniq `/new` yoki `/reset` (va `resetTriggers` dagi qo‘shimchalar) yangi sessiya id ni boshlaydi va xabarning qolgan qismini o‘tkazadi. 33. `/new <model>` yangi sessiya modelini o‘rnatish uchun model aliasini, `provider/model` ni yoki provayder nomini (noaniq moslash) qabul qiladi. 34. Agar `/new` yoki `/reset` yolg‘iz yuborilsa, OpenClaw qayta o‘rnatishni tasdiqlash uchun qisqa “salom” tabrigini bajaradi.
- 35. Qo‘lda qayta o‘rnatish: do‘kondan aniq kalitlarni o‘chiring yoki JSONL transkriptini olib tashlang; keyingi xabar ularni qayta yaratadi.
- 36. Izolyatsiyalangan cron vazifalari har bir ishga tushishda doimo yangi `sessionId` yaratadi (bo‘sh turish bo‘yicha qayta foydalanish yo‘q).

## 37. Yuborish siyosati (ixtiyoriy)

38. Muayyan sessiya turlari uchun yetkazib berishni alohida id larni sanamasdan bloklash.

```json5
39. {
  session: {
    sendPolicy: {
      rules: [
        { action: "deny", match: { channel: "discord", chatType: "group" } },
        { action: "deny", match: { keyPrefix: "cron:" } },
      ],
      default: "allow",
    },
  },
}
```

40. Ish vaqtidagi bekor qilish (faqat egasi):

- 41. `/send on` → ushbu sessiya uchun ruxsat berish
- 42. `/send off` → ushbu sessiya uchun rad etish
- 43. `/send inherit` → bekor qilishni tozalash va konfiguratsiya qoidalaridan foydalanish
      Bular ro‘yxatdan o‘tishi uchun alohida xabarlar sifatida yuboring.

## 44. Konfiguratsiya (ixtiyoriy nomni o‘zgartirish misoli)

```json5
48. `match.peer` (ixtiyoriy; `{ kind: direct|group|channel, id }`)
```

## 45. Tekshirish

- 46. `openclaw status` — do‘kon yo‘lini va so‘nggi sessiyalarni ko‘rsatadi.
- 47. `openclaw sessions --json` — barcha yozuvlarni chiqaradi (`--active <minutes>` bilan filtrlash).
- 48. `openclaw gateway call sessions.list --params '{}'` — ishlayotgan gateway dan sessiyalarni oladi (masofaviy gateway ga kirish uchun `--url`/`--token` dan foydalaning).
- 49. Agentga ulanilgan-ulanmaganini, sessiya kontekstidan qanchasi ishlatilayotganini, joriy fikrlash/verbose sozlamalarini va WhatsApp web hisob ma’lumotlaringiz oxirgi marta qachon yangilangani (qayta ulash ehtiyojini aniqlashga yordam beradi) ko‘rish uchun chatda `/status` ni alohida xabar sifatida yuboring.
- 50. Tizim promptida va kiritilgan ish maydoni fayllarida nimalar borligini (va eng katta kontekst hissachilarini) ko‘rish uchun `/context list` yoki `/context detail` ni yuboring.
- 1. Joriy ishni bekor qilish, ushbu sessiya uchun navbatdagi kuzatuvlarni tozalash va undan ishga tushirilgan barcha sub-agent ishlarini to‘xtatish uchun `/stop` ni alohida xabar sifatida yuboring (javobda to‘xtatilganlar soni ko‘rsatiladi).
- 2. Eski kontekstni qisqartirib xulosa qilish va oynada joy bo‘shatish uchun `/compact` (ixtiyoriy ko‘rsatmalar bilan) ni alohida xabar sifatida yuboring. 3. [/concepts/compaction](/concepts/compaction) ni ko‘ring.
- 4. To‘liq navbatlarni ko‘rib chiqish uchun JSONL transkriptlarini bevosita ochish mumkin.

## 5. Maslahatlar

- 6. Asosiy kalitni 1:1 trafik uchun ajratib qo‘ying; guruhlar o‘z kalitlariga ega bo‘lsin.
- 7. Tozalashni avtomatlashtirganda, boshqa joylardagi kontekstni saqlab qolish uchun butun omborni emas, balki alohida kalitlarni o‘chiring.

## 8. Sessiya kelib chiqishi metama’lumotlari

9. Har bir sessiya yozuvi qayerdan kelganini (imkon qadar) `origin` da qayd etadi:

- 10. `label`: inson uchun tushunarli yorliq (suhbat yorlig‘i + guruh mavzusi/kanalidan aniqlanadi)
- 11. `provider`: normallashtirilgan kanal identifikatori (kengaytmalarni ham o‘z ichiga oladi)
- 12. `from`/`to`: kiruvchi konvertdagi xom marshrutlash identifikatorlari
- 13. `accountId`: provayder hisob identifikatori (ko‘p hisobli bo‘lsa)
- 14. `threadId`: kanal qo‘llab-quvvatlaganda mavzu/ip identifikatori
      Kelib chiqish maydonlari to‘g‘ridan-to‘g‘ri xabarlar, kanallar va guruhlar uchun to‘ldiriladi. 15. Agar ulagich faqat yetkazib berish marshrutlashini yangilasa (masalan, DM asosiy sessiyasini yangilab turish uchun), sessiya o‘zining tushuntiruvchi metama’lumotlarini saqlab qolishi uchun baribir kiruvchi kontekstni taqdim etishi kerak. 16. Kengaytmalar buni kiruvchi kontekstda `ConversationLabel`, `GroupSubject`, `GroupChannel`, `GroupSpace` va `SenderName` yuborish hamda `recordSessionMetaFromInbound` ni chaqirish (yoki xuddi shu kontekstni `updateLastRoute` ga uzatish) orqali bajarishi mumkin.
