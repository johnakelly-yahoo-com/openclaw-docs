---
summary: "Ko‘p-agentli marshrutlash: ajratilgan agentlar, kanal akkauntlari va bog‘lamalar"
title: Ko‘p-agentli marshrutlash
read_when: "Siz bitta gateway jarayonida bir nechta ajratilgan agentlarni (ish maydonlari + auth) xohlaysiz."
status: faol
---

# Ko‘p-agentli marshrutlash

Maqsad: bitta ishlayotgan Gateway’da bir nechta _ajratilgan_ agentlar (alohida ish maydoni + `agentDir` + sessiyalar), shuningdek bir nechta kanal akkauntlari (masalan, ikkita WhatsApp). Kirish oqimi bog‘lamalar orqali agentga yo‘naltiriladi.

## “Bitta agent” nima?

**Agent** — bu o‘ziga xos, to‘liq chegaralangan miya bo‘lib, quyidagilarga ega:

- **Ish maydoni** (fayllar, AGENTS.md/SOUL.md/USER.md, mahalliy qaydlar, persona qoidalari).
- **Holat katalogi** (`agentDir`) — auth profillari, model reyestri va har bir agent uchun sozlamalar.
- **Sessiyalar ombori** (chat tarixi + marshrutlash holati) `~/.openclaw/agents/<agentId>/sessions` ostida.

1. Auth profillari **har bir agent uchun alohida**. 2. Har bir agent o‘zining quyidagi manbasidan o‘qiydi:

```
3. ~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

4. Asosiy agent credentiallari avtomatik ravishda **ulashilmaydi**. 5. `agentDir` ni hech qachon qayta ishlatmang
   agentlar o‘rtasida (bu auth/session to‘qnashuvlariga olib keladi). 6. Agar credentiallarni ulashmoqchi bo‘lsangiz,
   `auth-profiles.json` faylini boshqa agentning `agentDir` ichiga nusxalang.

7. Skilllar har bir agent uchun alohida bo‘lib, har bir workspace’ning `skills/` papkasi orqali boshqariladi, umumiy skilllar esa
   `~/.openclaw/skills` dan mavjud. 8. Qarang: [Skills: per-agent vs shared](/tools/skills#per-agent-vs-shared-skills).

9. Gateway **bitta agent**ni (default) yoki **bir nechta agent**ni yonma-yon joylashtirib ishlata oladi.

10. **Workspace eslatmasi:** har bir agentning workspace’i **default cwd** hisoblanadi, qat’iy
    sandbox emas. 11. Nisbiy yo‘llar workspace ichida yechiladi, ammo absolut yo‘llar
    sandboxing yoqilmagan bo‘lsa, hostdagi boshqa joylarga yetib borishi mumkin. 12. Qarang
    [Sandboxing](/gateway/sandboxing).

## 13. Yo‘llar (tezkor xarita)

- 14. Config: `~/.openclaw/openclaw.json` (yoki `OPENCLAW_CONFIG_PATH`)
- 15. State dir: `~/.openclaw` (yoki `OPENCLAW_STATE_DIR`)
- 16. Workspace: `~/.openclaw/workspace` (yoki `~/.openclaw/workspace-<agentId>`)
- 17. Agent dir: `~/.openclaw/agents/<agentId>/agent` (yoki `agents.list[].agentDir`)
- 18. Sessions: `~/.openclaw/agents/<agentId>/sessions`

### 19. Yakka-agent rejimi (default)

20. Hech narsa qilmasangiz, OpenClaw bitta agentni ishga tushiradi:

- 21. `agentId` default bo‘yicha **`main`**.
- 22. Sessionlar `agent:main:<mainKey>` sifatida kalitlanadi.
- 23. Workspace default bo‘yicha `~/.openclaw/workspace` (yoki `OPENCLAW_PROFILE` o‘rnatilganda `~/.openclaw/workspace-<profile>`).
- 24. State default bo‘yicha `~/.openclaw/agents/main/agent`.

## 25. Agent yordamchisi

26. Yangi izolyatsiyalangan agent qo‘shish uchun agent wizard’dan foydalaning:

```bash
27. openclaw agents add work
```

28. So‘ngra kiruvchi xabarlarni yo‘naltirish uchun `bindings` qo‘shing (yoki wizard’ga buni avtomatik bajarishga ruxsat bering).

29. Tekshirish:

```bash
30. openclaw agents list --bindings
```

## 31. Bir nechta agent = bir nechta odam, bir nechta shaxsiyat

32. **Bir nechta agent** bilan, har bir `agentId` **to‘liq izolyatsiyalangan persona**ga aylanadi:

- 33. **Turli telefon raqamlari/akkauntlar** (har bir kanal uchun `accountId`).
- 34. **Turli shaxsiyatlar** (har bir agent workspace’iga xos `AGENTS.md` va `SOUL.md` kabi fayllar).
- 35. **Alohida auth + sessionlar** (aniq yoqilmaguncha o‘zaro aralashuv yo‘q).

36. Bu **bir nechta odam**ga bitta Gateway serverdan foydalanib, ularning AI “miyalari” va ma’lumotlarini izolyatsiya holatda saqlash imkonini beradi.

## 37. Bitta WhatsApp raqami, bir nechta odam (DM bo‘linishi)

38. **Turli WhatsApp DM**larni **bitta WhatsApp akkaunti**da qolgan holda turli agentlarga yo‘naltirishingiz mumkin. 44. {
    agents: {
    list: [
    { id: "alex", workspace: "~/.openclaw/workspace-alex" },
    { id: "mia", workspace: "~/.openclaw/workspace-mia" },
    ],
    },
    bindings: [
    {
    agentId: "alex",
    match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230001" } },
    },
    {
    agentId: "mia",
    match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230002" } },
    },
    ],
    channels: {
    whatsapp: {
    dmPolicy: "allowlist",
    allowFrom: ["+15551230001", "+15551230002"],
    },
    },
    } 39. Javoblar baribir bir xil WhatsApp raqamidan keladi (har bir agent uchun alohida yuboruvchi identifikatori yo‘q).

40. Muhim tafsilot: to‘g‘ridan-to‘g‘ri chatlar agentning **asosiy session kaliti**ga birlashadi, shuning uchun haqiqiy izolyatsiya **har bir odam uchun bitta agent**ni talab qiladi.

41. Misol:

```json5
45. {
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "opus",
        name: "Deep Work",
        workspace: "~/.openclaw/workspace-opus",
        model: "anthropic/claude-opus-4-6",
      },
    ],
  },
  bindings: [
    {
      agentId: "opus",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551234567" } },
    },
    { agentId: "chat", match: { channel: "whatsapp" } },
  ],
}
```

42. Eslatmalar:

- 43. DM kirish nazorati **har bir WhatsApp akkaunti uchun global** (pairing/allowlist), agent bo‘yicha emas.
- 44. Umumiy guruhlar uchun guruhni bitta agentga bog‘lang yoki [Broadcast groups](/channels/broadcast-groups) dan foydalaning.

## 45. Marshrutlash qoidalari (xabarlar agentni qanday tanlaydi)

46. Bindinglar **deterministik** va **eng aniq moslik yutadi**:

1. 47. `peer` mosligi (aniq DM/guruh/kanal id)
2. 48. `guildId` (Discord)
3. 49. `teamId` (Slack)
4. 50. Kanal uchun `accountId` mosligi
5. 1. kanal darajasidagi moslash (`accountId: "*"`)
6. 2. standart agentga qaytish (`agents.list[].default`, aks holda roʻyxatdagi birinchi element, standart: `main`)

## 3) Bir nechta hisoblar / telefon raqamlari

4. **Bir nechta hisoblarni** qoʻllab-quvvatlaydigan kanallar (masalan, WhatsApp) har bir loginni aniqlash uchun `accountId` dan foydalanadi. **Vektor o‘xshashligi** (semantik moslik, ifodalar farq qilishi mumkin)

## 6. Tushunchalar

- 7. `agentId`: bitta “miya” (ish maydoni, har-agent autentifikatsiyasi, har-agent seanslar ombori).
- 8. `accountId`: kanal hisobining bitta nusxasi (masalan, WhatsApp hisobi "personal" va "biz").
- 9. `binding`: kiruvchi xabarlarni `(channel, accountId, peer)` va ixtiyoriy ravishda guild/jamoa IDlari orqali `agentId` ga yoʻnaltiradi.
- 10. Toʻgʻridan-toʻgʻri chatlar `agent:<agentId>:<mainKey>` ga yigʻiladi (har-agent uchun “main”; `session.mainKey`).

## 11. Misol: ikkita WhatsApp → ikkita agent

Har bir `accountId` alohida agentga yo‘naltirilishi mumkin, shuning uchun bitta server sessiyalarni aralashtirmasdan bir nechta telefon raqamlarini joylashtira oladi.

```js
13. {
  agents: {
    list: [
      {
        id: "home",
        default: true,
        name: "Home",
        workspace: "~/.openclaw/workspace-home",
        agentDir: "~/.openclaw/agents/home/agent",
      },
      {
        id: "work",
        name: "Work",
        workspace: "~/.openclaw/workspace-work",
        agentDir: "~/.openclaw/agents/work/agent",
      },
    ],
  },

  // Deterministik marshrutlash: birinchi mos kelgani yutadi (eng aniqdan boshlab).
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },

    // Ixtiyoriy peer bo‘yicha override (misol: muayyan guruhni work agentga yuborish).
    {
      agentId: "work",
      match: {
        channel: "whatsapp",
        accountId: "personal",
        peer: { kind: "group", id: "1203630...@g.us" },
      },
    },
  ],

  // Sukut bo‘yicha o‘chiq: agentdan agentga xabar almashish aniq yoqilishi va allowlist qilinishi kerak.
  tools: {
    agentToAgent: {
      enabled: false,
      allow: ["home", "work"],
    },
  },

  channels: {
    whatsapp: {
      accounts: {
        personal: {
          // Ixtiyoriy override. Sukut bo‘yicha: ~/.openclaw/credentials/whatsapp/personal
          // authDir: "~/.openclaw/credentials/whatsapp/personal",
        },
        biz: {
          // Ixtiyoriy override. Sukut bo‘yicha: ~/.openclaw/credentials/whatsapp/biz
          // authDir: "~/.openclaw/credentials/whatsapp/biz",
        },
      },
    },
  },
}
```

## 14. Misol: WhatsApp kundalik chat + Telegram chuqur ish

`~/.openclaw/openclaw.json` (JSON5):

```json5
16. {
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "opus",
        name: "Deep Work",
        workspace: "~/.openclaw/workspace-opus",
        model: "anthropic/claude-opus-4-6",
      },
    ],
  },
  bindings: [
    { agentId: "chat", match: { channel: "whatsapp" } },
    { agentId: "opus", match: { channel: "telegram" } },
  ],
}
```

Kanal bo‘yicha ajrating: WhatsApp’ni tezkor kundalik agentga, Telegram’ni esa Opus agentiga yo‘naltiring.

- 18. Agar kanal uchun bir nechta hisobingiz bo‘lsa, binding’ga `accountId` qo‘shing (masalan, `{ channel: "whatsapp", accountId: "personal" }`).
- 19. Qolganlarini chatda qoldirib, bitta DM/guruhni Opus’ga yo‘naltirish uchun o‘sha peer uchun `match.peer` binding qo‘shing; peer mosliklari har doim kanal darajasidagi qoidalardan ustun keladi.

## 20. Misol: bir xil kanal, bitta peer Opus’ga

21. WhatsApp’ni tezkor agentda qoldiring, lekin bitta DM’ni Opus’ga yo‘naltiring:

```json5
46. Tur bo‘yicha alohida sozlamalar (ixtiyoriy): `resetByType` `direct`, `group` va `thread` sessiyalari uchun siyosatni almashtirish imkonini beradi (thread = Slack/Discord tarmoqlari, Telegram mavzulari, Matrix tarmoqlari — konnektor taqdim etsa).
```

Eslatmalar:

## 23. WhatsApp guruhiga bog‘langan oila agenti

24. Bitta WhatsApp guruhiga maxsus oila agentini bog‘lang, mention gating va yanada qat’iyroq tool siyosati bilan:

```json5
25. {
  agents: {
    list: [
      {
        id: "family",
        name: "Family",
        workspace: "~/.openclaw/workspace-family",
        identity: { name: "Family Bot" },
        groupChat: {
          mentionPatterns: ["@family", "@familybot", "@Family Bot"],
        },
        sandbox: {
          mode: "all",
          scope: "agent",
        },
        tools: {
          allow: [
            "exec",
            "read",
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
          ],
          deny: ["write", "edit", "apply_patch", "browser", "canvas", "nodes", "cron"],
        },
      },
    ],
  },
  bindings: [
    {
      agentId: "family",
      match: {
        channel: "whatsapp",
        peer: { kind: "group", id: "120363999999999999@g.us" },
      },
    },
  ],
}
```

26. Eslatmalar:

- Peer bog‘lanishlari har doim ustun turadi, shuning uchun ularni kanal bo‘yicha umumiy qoidadan yuqorida saqlang. 28. Agar skill binar faylni ishga tushirishi kerak bo‘lsa, `exec` ruxsat etilganligiga va binar sandbox’da mavjudligiga ishonch hosil qiling.
- 29. Yanada qat’iy gating uchun `agents.list[].groupChat.mentionPatterns` ni sozlang va kanal uchun guruh allowlist’larini yoqilgan holda saqlang.

## 30. Har-Agent Sandbox va Tool konfiguratsiyasi

31. v2026.1.6 dan boshlab, har bir agent o‘z sandbox’i va tool cheklovlariga ega bo‘lishi mumkin:

```js
32. {
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: {
          mode: "off",  // personal agent uchun sandbox yo‘q
        },
        // Tool cheklovlari yo‘q - barcha tool’lar mavjud
      },
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",     // Har doim sandbox’da
          scope: "agent",  // Har bir agent uchun alohida konteyner
          docker: {
            // Konteyner yaratilgandan keyin bir martalik ixtiyoriy sozlash
            setupCommand: "apt-get update && apt-get install -y git curl",
          },
        },
        tools: {
          allow: ["read"],                    // Faqat read tool
          deny: ["exec", "write", "edit", "apply_patch"],    // Qolganlarini taqiqlash
        },
      },
    ],
  },
}
```

33. Eslatma: `setupCommand` `sandbox.docker` ostida joylashadi va konteyner yaratilganda bir marta ishga tushadi.
34. Agar yakuniy scope `"shared"` bo‘lsa, har-agent `sandbox.docker.*` override’lari e’tiborga olinmaydi.

35. **Afzalliklar:**

- 36. **Xavfsizlik izolyatsiyasi**: ishonchsiz agentlar uchun tool’larni cheklash
- 37. **Resurslarni boshqarish**: ayrim agentlarni sandbox’da, boshqalarini esa host’da qoldirish
- 38. **Moslashuvchan siyosatlar**: har agent uchun turli ruxsatlar

39. Eslatma: `tools.elevated` **global** va yuboruvchi asosida ishlaydi; uni har agent uchun sozlab bo‘lmaydi.
40. Agar har-agent chegaralari kerak bo‘lsa, `agents.list[].tools` dan foydalanib `exec` ni taqiqlang.
41. Guruhni nishonga olish uchun `agents.list[].groupChat.mentionPatterns` dan foydalaning, shunda @mention’lar to‘g‘ri agentga aniq mos keladi.

42. Batafsil misollar uchun [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools) sahifasiga qarang.
