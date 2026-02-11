---
summary: "Agent tool surface for OpenClaw (browser, canvas, nodes, message, cron) replacing legacy `openclaw-*` skills"
read_when:
  - Adding or modifying agent tools
  - Retiring or changing `openclaw-*` skills
title: "Tools"
---

# Tools (OpenClaw)

25. OpenClaw brauzer, canvas, tugunlar va cron uchun **birinchi darajali agent vositalarini** taqdim etadi.
    These replace the old `openclaw-*` skills: the tools are typed, no shelling,
    and the agent should rely on them directly.

## Disabling tools

26. Siz `openclaw.json` dagi `tools.allow` / `tools.deny` orqali vositalarni global tarzda ruxsat berishingiz yoki taqiqlashingiz mumkin
    (taqiqlash ustun turadi). This prevents disallowed tools from being sent to model providers.

```json5
{
  tools: { deny: ["browser"] },
}
```

Notes:

- Matching is case-insensitive.
- `*` wildcards are supported (`"*"` means all tools).
- If `tools.allow` only references unknown or unloaded plugin tool names, OpenClaw logs a warning and ignores the allowlist so core tools stay available.

## Tool profiles (base allowlist)

`tools.profile` sets a **base tool allowlist** before `tools.allow`/`tools.deny`.
Per-agent override: `agents.list[].tools.profile`.

27. Profillar:

- `minimal`: `session_status` only
- `coding`: `group:fs`, `group:runtime`, `group:sessions`, `group:memory`, `image`
- `messaging`: `group:messaging`, `sessions_list`, `sessions_history`, `sessions_send`, `session_status`
- `full`: no restriction (same as unset)

Example (messaging-only by default, allow Slack + Discord tools too):

```json5
{
  tools: {
    profile: "messaging",
    allow: ["slack", "discord"],
  },
}
```

Example (coding profile, but deny exec/process everywhere):

```json5
{
  tools: {
    profile: "coding",
    deny: ["group:runtime"],
  },
}
```

Example (global coding profile, messaging-only support agent):

```json5
{
  tools: { profile: "coding" },
  agents: {
    list: [
      {
        id: "support",
        tools: { profile: "messaging", allow: ["slack"] },
      },
    ],
  },
}
```

## Provider-specific tool policy

Use `tools.byProvider` to **further restrict** tools for specific providers
(or a single `provider/model`) without changing your global defaults.
Per-agent override: `agents.list[].tools.byProvider`.

This is applied **after** the base tool profile and **before** allow/deny lists,
so it can only narrow the tool set.
Provider keys accept either `provider` (e.g. `google-antigravity`) or
`provider/model` (e.g. `openai/gpt-5.2`).

Example (keep global coding profile, but minimal tools for Google Antigravity):

```json5
{
  tools: {
    profile: "coding",
    byProvider: {
      "google-antigravity": { profile: "minimal" },
    },
  },
}
```

Example (provider/model-specific allowlist for a flaky endpoint):

```json5
{
  tools: {
    allow: ["group:fs", "group:runtime", "sessions_list"],
    byProvider: {
      "openai/gpt-5.2": { allow: ["group:fs", "sessions_list"] },
    },
  },
}
```

Example (agent-specific override for a single provider):

```json5
{
  agents: {
    list: [
      {
        id: "support",
        tools: {
          byProvider: {
            "google-antigravity": { allow: ["message", "sessions_list"] },
          },
        },
      },
    ],
  },
}
```

## Tool groups (shorthands)

Tool policies (global, agent, sandbox) support `group:*` entries that expand to multiple tools.
Use these in `tools.allow` / `tools.deny`.

Available groups:

- `group:runtime`: `exec`, `bash`, `process`
- `group:fs`: `read`, `write`, `edit`, `apply_patch`
- `group:sessions`: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
- `group:memory`: `memory_search`, `memory_get`
- `group:web`: `web_search`, `web_fetch`
- `group:ui`: `browser`, `canvas`
- `group:automation`: `cron`, `gateway`
- `group:messaging`: `message`
- `group:nodes`: `nodes`
- 28. `group:openclaw`: barcha o‘rnatilgan OpenClaw vositalari (provayder plaginlari bundan mustasno)

2. Misol (faqat fayl vositalari + brauzerga ruxsat berish):

```json5
3. {
  tools: {
    allow: ["group:fs", "browser"],
  },
}
```

## 29. Plaginlar + vositalar

5. Plaginlar asosiy to‘plamdan tashqari **qo‘shimcha vositalar** (va CLI buyruqlari)ni ro‘yxatdan o‘tkazishi mumkin.
6. O‘rnatish va sozlash uchun [Plugins](/tools/plugin), hamda vositalardan foydalanish bo‘yicha yo‘riqnomalar promptlarga qanday kiritilishini bilish uchun [Skills](/tools/skills) sahifalariga qarang. 7. Ayrim plaginlar vositalar bilan birga o‘zlarining skill’larini ham taqdim etadi (masalan, voice-call plagini).

30. Ixtiyoriy plagin vositalari:

- 31. [Lobster](/tools/lobster): qayta tiklanadigan tasdiqlar bilan tiplangan workflow runtime (gateway xostida Lobster CLI talab qilinadi).
- 10. [LLM Task](/tools/llm-task): strukturalangan workflow chiqishi uchun faqat JSON’li LLM bosqichi (ixtiyoriy sxema tekshiruvi).

## 11. Vositalar inventari

### 12. `apply_patch`

13. Bir yoki bir nechta fayllar bo‘ylab strukturalangan patch’larni qo‘llash. 32. Ko‘p-hunk tahrirlar uchun foydalaning.
14. Eksperimental: `tools.exec.applyPatch.enabled` orqali yoqing (faqat OpenAI modellari).

### 34. `exec`

17. Ish maydonida shell buyruqlarini ishga tushirish.

35. Asosiy parametrlar:

- 19. `command` (majburiy)
- 20. `yieldMs` (vaqt tugagach avtomatik fon rejimiga o‘tadi, standart 10000)
- 21. `background` (darhol fon rejimi)
- 22. `timeout` (soniyalar; oshib ketsa jarayon to‘xtatiladi, standart 1800)
- 23. `elevated` (bool; elevated rejimi yoqilgan/ruxsat etilgan bo‘lsa xostda ishga tushiradi; agent sandbox qilinganida xulq-atvorni o‘zgartiradi)
- 24. `host` (`sandbox | gateway | node`)
- 25. `security` (`deny | allowlist | full`)
- 26. `ask` (`off | on-miss | always`)
- 27. `node` (`host=node` uchun node id/nomi)
- 28. Haqiqiy TTY kerakmi? 29. `pty: true` qilib sozlang.

30. Eslatmalar:

- 31. Fon rejimida `status: "running"` va `sessionId` qaytariladi.
- 32. Fon sessiyalarini so‘rash/loglash/yozish/o‘chirish/tozalash uchun `process` dan foydalaning.
- 33. Agar `process` taqiqlangan bo‘lsa, `exec` sinxron ishlaydi va `yieldMs`/`background` ni e’tiborsiz qoldiradi.
- 34. `elevated` `tools.elevated` hamda `agents.list[].tools.elevated` override’i bilan cheklanadi (ikkalasi ham ruxsat berishi kerak) va `host=gateway` + `security=full` uchun alias hisoblanadi.
- 35. `elevated` faqat agent sandbox qilinganida xulq-atvorni o‘zgartiradi (aks holda ta’siri yo‘q).
- 36. `host=node` macOS companion ilovasini yoki headless node xostni nishonga olishi mumkin (`openclaw node run`).
- 37. gateway/node tasdiqlari va allowlist’lar: [Exec approvals](/tools/exec-approvals).

### 38. `process`

39. Fon rejimidagi exec sessiyalarini boshqarish.

40. Asosiy amallar:

- 41. `list`, `poll`, `log`, `write`, `kill`, `clear`, `remove`

42. Eslatmalar:

- 43. `poll` yakunlanganda yangi chiqishni va chiqish holatini qaytaradi.
- 44. `log` qatorma-qator `offset`/`limit` ni qo‘llab-quvvatlaydi (`offset`ni qoldirsangiz oxirgi N qator olinadi).
- 45. `process` har bir agent doirasida ishlaydi; boshqa agentlardagi sessiyalar ko‘rinmaydi.

### 46. `web_search`

47. Brave Search API orqali vebni qidirish.

48. Asosiy parametrlar:

- 49. `query` (majburiy)
- 50. `count` (1–10; standart qiymat `tools.web.search.maxResults` dan olinadi)

1. Eslatmalar:

- 2. Brave API kalitini talab qiladi (tavsiya etiladi: `openclaw configure --section web`, yoki `BRAVE_API_KEY` ni o‘rnating).
- 3. `tools.web.search.enabled` orqali yoqing.
- 4. Javoblar keshlanadi (standart 15 daqiqa).
- 5. Sozlash uchun [Web tools](/tools/web) ga qarang.

### 6. `web_fetch`

7. URL manzildan o‘qilishi mumkin bo‘lgan kontentni olish va ajratib chiqarish (HTML → markdown/text).

8. Asosiy parametrlar:

- 9. `url` (majburiy)
- 10. `extractMode` (`markdown` | `text`)
- 11. `maxChars` (uzun sahifalarni qisqartirish)

12. Eslatmalar:

- 13. `tools.web.fetch.enabled` orqali yoqing.
- 14. `maxChars` `tools.web.fetch.maxCharsCap` bilan cheklanadi (standart 50000).
- 15. Javoblar keshlanadi (standart 15 daqiqa).
- 16. JS-ga boy saytlar uchun brauzer vositasini afzal ko‘ring.
- 17. Sozlash uchun [Web tools](/tools/web) ga qarang.
- 18. Ixtiyoriy anti-bot zaxira varianti uchun [Firecrawl](/tools/firecrawl) ga qarang.

### 19. `browser`

20. OpenClaw tomonidan boshqariladigan maxsus brauzerni nazorat qilish.

21. Asosiy amallar:

- 22. `status`, `start`, `stop`, `tabs`, `open`, `focus`, `close`
- 23. `snapshot` (aria/ai)
- 24. `screenshot` (rasm bloki + `MEDIA:<path>` qaytaradi)
- 25. `act` (UI amallari: click/type/press/hover/drag/select/fill/resize/wait/evaluate)
- 26. `navigate`, `console`, `pdf`, `upload`, `dialog`

27. Profil boshqaruvi:

- 28. `profiles` — holati bilan barcha brauzer profillarini ro‘yxatlash
- 29. `create-profile` — avtomatik ajratilgan port bilan yangi profil yaratish (yoki `cdpUrl`)
- 30. `delete-profile` — brauzerni to‘xtatish, foydalanuvchi ma’lumotlarini o‘chirish, konfiguratsiyadan olib tashlash (faqat lokal)
- 31. `reset-profile` — profil portidagi yetim jarayonni to‘xtatish (faqat lokal)

32. Umumiy parametrlar:

- 33. `profile` (ixtiyoriy; sukut bo‘yicha `browser.defaultProfile`)
- 34. `target` (`sandbox` | `host` | `node`)
- 35. `node` (ixtiyoriy; aniq node id/nomini tanlaydi)
      Eslatmalar:
- 36. `browser.enabled=true` talab qilinadi (standart `true`; o‘chirish uchun `false` ga o‘rnating).
- 37. Barcha amallar ko‘p instansiya qo‘llab-quvvatlashi uchun ixtiyoriy `profile` parametrini qabul qiladi.
- 38. `profile` ko‘rsatilmasa, `browser.defaultProfile` ishlatiladi (standart "chrome").
- 39. Profil nomlari: faqat kichik harfli alfanumerik belgilar va defislar (maks. 64 belgi).
- 40. Port diapazoni: 18800–18899 (taxm. 100 ta profil maksimal).
- 41. Masofaviy profillar faqat ulanish uchun (start/stop/reset yo‘q).
- 42. Agar brauzerga qodir node ulangan bo‘lsa, vosita avtomatik ravishda unga yo‘naltirishi mumkin (agar `target` ni mahkamlab qo‘ymasangiz).
- 43. Playwright o‘rnatilganda `snapshot` sukut bo‘yicha `ai`; accessibility daraxti uchun `aria` dan foydalaning.
- 44. `snapshot` shuningdek role-snapshot variantlarini (`interactive`, `compact`, `depth`, `selector`) qo‘llab-quvvatlaydi, ular `e12` kabi havolalarni qaytaradi.
- 45. `act` `snapshot` dan `ref` ni talab qiladi (AI snapshotlaridan raqamli `12`, yoki role snapshotlardan `e12`); kamdan-kam CSS selektor ehtiyojlari uchun `evaluate` dan foydalaning.
- 46. Odatiy holatda `act` → `wait` dan qoching; uni faqat istisno holatlarda ishlating (kutiladigan ishonchli UI holati bo‘lmaganda).
- 36. `upload` qurollantirilgandan so‘ng avtomatik bosish uchun ixtiyoriy ravishda `ref` uzatishi mumkin.
- 48. `upload` shuningdek `<input type="file">` ni bevosita sozlash uchun `inputRef` (aria ref) yoki `element` (CSS selektor) ni qo‘llab-quvvatlaydi.

### 49. `canvas`

50. Node Canvas’ni boshqarish (present, eval, snapshot, A2UI).

37. Asosiy amallar:

- `present`, `hide`, `navigate`, `eval`
- `snapshot` (returns image block + `MEDIA:<path>`)
- `a2ui_push`, `a2ui_reset`

Notes:

- Uses gateway `node.invoke` under the hood.
- If no `node` is provided, the tool picks a default (single connected node or local mac node).
- A2UI is v0.8 only (no `createSurface`); the CLI rejects v0.9 JSONL with line errors.
- 38. Tezkor smoke-test: `openclaw nodes canvas a2ui push --node <id> --text "Hello from A2UI"`.

### `nodes`

39. Juftlangan tugunlarni aniqlash va nishonga olish; bildirishnomalar yuborish; kamera/ekranni yozib olish.

Core actions:

- 40. `status`, `describe`
- 41. `pending`, `approve`, `reject` (juftlash)
- `notify` (macOS `system.notify`)
- 42. `run` (macOS `system.run`)
- `camera_snap`, `camera_clip`, `screen_record`
- `location_get`

Notes:

- Camera/screen commands require the node app to be foregrounded.
- Images return image blocks + `MEDIA:<path>`.
- Videos return `FILE:<path>` (mp4).
- Location returns a JSON payload (lat/lon/accuracy/timestamp).
- `run` params: `command` argv array; optional `cwd`, `env` (`KEY=VAL`), `commandTimeoutMs`, `invokeTimeoutMs`, `needsScreenRecording`.

Example (`run`):

```json
{
  "action": "run",
  "node": "office-mac",
  "command": ["echo", "Hello"],
  "env": ["FOO=bar"],
  "commandTimeoutMs": 12000,
  "invokeTimeoutMs": 45000,
  "needsScreenRecording": false
}
```

### `image`

Analyze an image with the configured image model.

Core parameters:

- `image` (required path or URL)
- `prompt` (optional; defaults to "Describe the image.")
- `model` (optional override)
- `maxBytesMb` (optional size cap)

Notes:

- 43. Faqat `agents.defaults.imageModel` sozlanganida (asosiy yoki zaxira), yoki standart model + sozlangan autentifikatsiyadan yashirin tasvir modeli aniqlanishi mumkin bo‘lganda (eng yaxshi urinish bilan juftlash) mavjud.
- Uses the image model directly (independent of the main chat model).

### `message`

Send messages and channel actions across Discord/Google Chat/Slack/Telegram/WhatsApp/Signal/iMessage/MS Teams.

Core actions:

- `send` (text + optional media; MS Teams also supports `card` for Adaptive Cards)
- `poll` (WhatsApp/Discord/MS Teams polls)
- `react` / `reactions` / `read` / `edit` / `delete`
- `pin` / `unpin` / `list-pins`
- `permissions`
- `thread-create` / `thread-list` / `thread-reply`
- `search`
- `sticker`
- `member-info` / `role-info`
- `emoji-list` / `emoji-upload` / `sticker-upload`
- `role-add` / `role-remove`
- `channel-info` / `channel-list`
- `voice-status`
- `event-list` / `event-create`
- `timeout` / `kick` / `ban`

Eslatmalar:

- `send` WhatsApp’ni Gateway orqali yo‘naltiradi; boshqa kanallar to‘g‘ridan-to‘g‘ri boradi.
- `poll` WhatsApp va MS Teams uchun Gateway’dan foydalanadi; Discord so‘rovlari to‘g‘ridan-to‘g‘ri boradi.
- Xabar vositasi chaqiruvi faol chat sessiyasiga bog‘langanda, yuborishlar kontekstlararo sizib chiqishni oldini olish uchun o‘sha sessiyaning manziliga cheklanadi.

### `cron`

Gateway cron ishlarini va uyg‘otishlarni boshqaring.

Asosiy amallar:

- `status`, `list`
- `add`, `update`, `remove`, `run`, `runs`
- `wake` (tizim hodisasini navbatga qo‘shish + ixtiyoriy darhol yurak urishi)

Eslatmalar:

- `add` to‘liq cron ish obyektini kutadi (sxema `cron.add` RPC bilan bir xil).
- `update` `{ jobId, patch }` dan foydalanadi (`id` moslik uchun qabul qilinadi).

### `gateway`

Ishlayotgan Gateway jarayonini qayta ishga tushiring yoki yangilanishlarni qo‘llang (joyida).

Asosiy amallar:

- `restart` (avtorizatsiya qiladi + jarayon ichida qayta ishga tushirish uchun `SIGUSR1` yuboradi; `openclaw gateway` joyida qayta ishga tushiradi)
- `config.get` / `config.schema`
- `config.apply` (tekshirish + konfiguratsiyani yozish + qayta ishga tushirish + uyg‘otish)
- `config.patch` (qisman yangilanishni birlashtirish + qayta ishga tushirish + uyg‘otish)
- `update.run` (yangilanishni ishga tushirish + qayta ishga tushirish + uyg‘otish)

Eslatmalar:

- 44. Amaldagi javobni to‘xtatib qo‘ymaslik uchun `delayMs` (standart 2000) dan foydalaning.
- `restart` sukut bo‘yicha o‘chirilgan; `commands.restart: true` bilan yoqing.

### `sessions_list` / `sessions_history` / `sessions_send` / `sessions_spawn` / `session_status`

Sessiyalarni ro‘yxatlang, transkript tarixini ko‘ring yoki boshqa sessiyaga yuboring.

Asosiy parametrlar:

- `sessions_list`: `kinds?`, `limit?`, `activeMinutes?`, `messageLimit?` (0 = yo‘q)
- `sessions_history`: `sessionKey` (yoki `sessionId`), `limit?`, `includeTools?`
- `sessions_send`: `sessionKey` (yoki `sessionId`), `message`, `timeoutSeconds?` (0 = yuborib unutish)
- `sessions_spawn`: `task`, `label?`, `agentId?`, `model?`, `runTimeoutSeconds?`, `cleanup?`
- `session_status`: `sessionKey?` (sukut bo‘yicha joriy; `sessionId` qabul qilinadi), `model?` (`default` bekor qilishni tozalaydi)

Eslatmalar:

- `main` — to‘g‘ridan-to‘g‘ri chat uchun kanonik kalit; global/noma’lum yashirilgan.
- 45. `messageLimit > 0` har bir sessiya uchun oxirgi N ta xabarni oladi (vosita xabarlari filtrlanadi).
- `sessions_send` `timeoutSeconds > 0` bo‘lganda yakuniy tugashni kutadi.
- Yetkazish/e’lon qilish yakunlangandan keyin sodir bo‘ladi va eng yaxshi sa’y-harakat asosida bajariladi; `status: "ok"` agent yugurishi tugaganini tasdiqlaydi, e’lon yetkazilganini emas.
- `sessions_spawn` sub-agent yugurishini boshlaydi va so‘rovchi chatga e’lon javobini joylaydi.
- `sessions_spawn` bloklanmaydi va darhol `status: "accepted"` ni qaytaradi.
- `sessions_send` javob qaytarish ping‑pongini bajaradi (to‘xtatish uchun `REPLY_SKIP` bilan javob bering; maksimal aylanishlar `session.agentToAgent.maxPingPongTurns` orqali, 0–5).
- Ping‑pongdan so‘ng, nishon agent **e’lon bosqichi**ni bajaradi; e’lonni bostirish uchun `ANNOUNCE_SKIP` bilan javob bering.

### `agents_list`

Joriy sessiya `sessions_spawn` bilan nishonga olishi mumkin bo‘lgan agent identifikatorlarini ro‘yxatlang.

Eslatmalar:

- Natija har bir agent uchun ruxsat ro‘yxatlari bilan cheklanadi (`agents.list[].subagents.allowAgents`).
- `["*"]` sozlanganda, vosita barcha sozlangan agentlarni o‘z ichiga oladi va `allowAny: true` deb belgilaydi.

## Parametrlar (umumiy)

Gateway-ga tayangan vositalar (`canvas`, `nodes`, `cron`):

- `gatewayUrl` (standart `ws://127.0.0.1:18789`)
- `gatewayToken` (agar autentifikatsiya yoqilgan bo‘lsa)
- `timeoutMs`

Eslatma: `gatewayUrl` o‘rnatilganda, `gatewayToken`ni aniq ko‘rsatib kiriting. Vositalar sozlamalarni yoki muhit (environment) hisob ma’lumotlarini override uchun meros qilib olmaydi, va aniq ko‘rsatilmagan hisob ma’lumotlari xato hisoblanadi.

Brauzer vositasi:

- `profile` (ixtiyoriy; standart `browser.defaultProfile`)
- `target` (`sandbox` | `host` | `node`)
- `node` (ixtiyoriy; aniq node id/nomini biriktirish)

## Tavsiya etilgan agent oqimlari

Brauzer avtomatlashtirish:

1. `browser` → `status` / `start`
2. `snapshot` (ai yoki aria)
3. `act` (bosish/yozish/tugma bosish)
4. Agar vizual tasdiq kerak bo‘lsa `screenshot`

Canvas renderi:

1. `canvas` → `present`
2. `a2ui_push` (ixtiyoriy)
3. `snapshot`

Node nishonlash:

1. `nodes` → `status`
2. Tanlangan node’da `describe`
3. `notify` / `run` / `camera_snap` / `screen_record`

## Xavfsizlik

- To‘g‘ridan-to‘g‘ri `system.run`dan qoching; faqat aniq foydalanuvchi roziligi bilan `nodes` → `run`dan foydalaning.
- Kamera/ekran yozib olish uchun foydalanuvchi roziligini hurmat qiling.
- Media buyruqlarini chaqirishdan oldin ruxsatlarni tekshirish uchun `status/describe`dan foydalaning.

## Vositalar agentga qanday taqdim etiladi

Vositalar ikki parallel kanalda ochiladi:

1. **Tizim prompt matni**: odam o‘qiy oladigan ro‘yxat + yo‘riqnoma.
2. **Vosita sxemasi**: model API’ga yuboriladigan tuzilgan funksiya ta’riflari.

Bu shuni anglatadiki, agent ham “qaysi vositalar mavjud”ligini, ham “ularni qanday chaqirish”ni ko‘radi. Agar biror vosita
