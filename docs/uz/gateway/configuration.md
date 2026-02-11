---
summary: "`~/.openclaw/openclaw.json` uchun barcha konfiguratsiya opsiyalari misollar bilan"
read_when:
  - Konfiguratsiya maydonlarini qo‘shish yoki o‘zgartirish
title: "Konfiguratsiya"
---

# Konfiguratsiya 🔧

OpenClaw `~/.openclaw/openclaw.json` faylidan ixtiyoriy **JSON5** konfiguratsiyani o‘qiydi (izohlar va oxirgi vergullar ruxsat etiladi).

Agar fayl mavjud bo‘lmasa, OpenClaw nisbatan xavfsiz standart sozlamalardan foydalanadi (o‘rnatilgan Pi agenti + yuboruvchi bo‘yicha sessiyalar + `~/.openclaw/workspace` ish maydoni). Odatda konfiguratsiya faqat quyidagilar uchun kerak bo‘ladi:

- botni kim ishga tushira olishini cheklash (`channels.whatsapp.allowFrom`, `channels.telegram.allowFrom`, va hokazo)
- guruhlar uchun ruxsat ro‘yxatlari va eslatish xatti-harakatini boshqarish (`channels.whatsapp.groups`, `channels.telegram.groups`, `channels.discord.guilds`, `agents.list[].groupChat`)
- xabar prefikslarini moslashtirish (`messages`)
- agentning ish maydonini belgilash (`agents.defaults.workspace` yoki `agents.list[].workspace`)
- o‘rnatilgan agentning standart sozlamalarini (`agents.defaults`) va sessiya xatti-harakatini (`session`) sozlash
- Mijoz `hello` ni tugun metama’lumotlari + token bilan yuboradi (agar allaqachon juftlangan bo‘lsa).

> **Konfiguratsiyaga yangimisiz?** Batafsil tushuntirishlar bilan to‘liq misollar uchun [Configuration Examples](/gateway/configuration-examples) qo‘llanmasini ko‘ring!

## Qat’iy konfiguratsiya tekshiruvi

Har bir agent uchun identifikatsiyani o‘rnating (`agents.list[].identity`).
Unknown keys, malformed types, or invalid values cause the Gateway to **refuse to start** for safety.

Tekshiruv muvaffaqiyatsiz bo‘lsa:

- The Gateway does not boot.
- Only diagnostic commands are allowed (for example: `openclaw doctor`, `openclaw logs`, `openclaw health`, `openclaw status`, `openclaw service`, `openclaw help`).
- Aniq muammolarni ko‘rish uchun `openclaw doctor` ni ishga tushiring.
- Migratsiya/tuzatishlarni qo‘llash uchun `openclaw doctor --fix` (yoki `--yes`) ni ishga tushiring.

Doctor siz aniq `--fix`/`--yes` ni tanlamaguningizcha hech qanday o‘zgarish yozmaydi.

## Sxema + UI ko‘rsatmalari

Gateway UI muharrirlari uchun konfiguratsiyaning JSON Schema ko‘rinishini `config.schema` orqali taqdim etadi.
Control UI ushbu sxema asosida forma chizadi va chiqish yo‘li sifatida **Raw JSON** muharririni ham taqdim etadi.

Kanal plaginlari va kengaytmalari o‘z konfiguratsiyasi uchun sxema va UI ko‘rsatmalarini ro‘yxatdan o‘tkazishi mumkin, shunda kanal sozlamalari ilovalar bo‘ylab qattiq kodlangan formalarsiz sxema asosida qoladi.

Ko‘rsatmalar (yorliqlar, guruhlash, maxfiy maydonlar) sxema bilan birga yetkaziladi, shuning uchun mijozlar konfiguratsiya bilimlarini qattiq kodlamasdan yaxshiroq formalar chiza oladi.

## Qo‘llash + qayta ishga tushirish (RPC)

`config.apply` dan foydalanib, butun konfiguratsiyani bir qadamda tekshiring + yozing va Gateway’ni qayta ishga tushiring.
Gateway qayta ishga tushgach, u restart belgisi yozadi va oxirgi faol sessiyani ping qiladi.

Ogohlantirish: `config.apply` **butun konfiguratsiyani** almashtiradi. Agar faqat bir nechta kalitlarni o‘zgartirmoqchi bo‘lsangiz, `config.patch` yoki `openclaw config set` dan foydalaning.

`~/.openclaw/openclaw.json` faylining zaxira nusxasini saqlang.

- Parametrlar:
- `baseHash` (optional) — config hash from `config.get` (required when a config already exists)
- `baseHash` (ixtiyoriy) — `config.get` dan olingan konfiguratsiya xeshi (konfiguratsiya allaqachon mavjud bo‘lsa, talab qilinadi)
- `note` (optional) — note to include in the restart sentinel
- `note` (ixtiyoriy) — qayta ishga tushirish belgisiga qo‘shiladigan eslatma

`restartDelayMs` (ixtiyoriy) — qayta ishga tushirishdan oldingi kechikish (standart 2000)

```bash
openclaw gateway call config.get --params '{}' # capture payload.hash
openclaw gateway call config.apply --params '{
  "raw": "{\\n  agents: { defaults: { workspace: \\"~/.openclaw/workspace\\" } }\\n}\\n",
  "baseHash": "<hash-from-config.get>",
  "sessionKey": "agent:main:whatsapp:dm:+15555550123",
  "restartDelayMs": 1000
}'
```

## Partial updates (RPC)

Use `config.patch` to merge a partial update into the existing config without clobbering
unrelated keys. It applies JSON merge patch semantics:

- objects merge recursively
- `null` deletes a key
- arrays replace
  Like `config.apply`, it validates, writes the config, stores a restart sentinel, and schedules
  the Gateway restart (with an optional wake when `sessionKey` is provided).

Params:

- `raw` (string) — JSON5 payload containing just the keys to change
- `baseHash` (required) — config hash from `config.get`
- `sessionKey` (optional) — last active session key for the wake-up ping
- `note` (optional) — note to include in the restart sentinel
- `restartDelayMs` (optional) — delay before restart (default 2000)

Example:

```bash
openclaw gateway call config.get --params '{}' # capture payload.hash
openclaw gateway call config.patch --params '{
  "raw": "{\\n  channels: { telegram: { groups: { \\"*\\": { requireMention: false } } } }\\n}\\n",
  "baseHash": "<hash-from-config.get>",
  "sessionKey": "agent:main:whatsapp:dm:+15555550123",
  "restartDelayMs": 1000
}'
```

## Minimal config (recommended starting point)

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

Build the default image once with:

```bash
scripts/sandbox-setup.sh
```

## Self-chat mode (recommended for group control)

To prevent the bot from responding to WhatsApp @-mentions in groups (only respond to specific text triggers):

```json5
{
  agents: {
    defaults: { workspace: "~/.openclaw/workspace" },
    list: [
      {
        id: "main",
        groupChat: { mentionPatterns: ["@openclaw", "reisponde"] },
      },
    ],
  },
  channels: {
    whatsapp: {
      // Allowlist is DMs only; including your own number enables self-chat mode.
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
}
```

## Config Includes (`$include`)

Split your config into multiple files using the `$include` directive. This is useful for:

- Organizing large configs (e.g., per-client agent definitions)
- Sharing common settings across environments
- Keeping sensitive configs separate

### Basic usage

```json5
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789 },

  // Include a single file (replaces the key's value)
  agents: { $include: "./agents.json5" },

  // Include multiple files (deep-merged in order)
  broadcast: {
    $include: ["./clients/mueller.json5", "./clients/schmidt.json5"],
  },
}
```

```json5
// ~/.openclaw/agents.json5
{
  defaults: { sandbox: { mode: "all", scope: "session" } },
  list: [{ id: "main", workspace: "~/.openclaw/workspace" }],
}
```

### Merge behavior

- **Single file**: Replaces the object containing `$include`
- **Array of files**: Deep-merges files in order (later files override earlier ones)
- **With sibling keys**: Sibling keys are merged after includes (override included values)
- **Sibling keys + arrays/primitives**: Not supported (included content must be an object)

```json5
// Sibling keys override included values
{
  $include: "./base.json5", // { a: 1, b: 2 }
  b: 99, // Result: { a: 1, b: 99 }
}
```

### Nested includes

Included files can themselves contain `$include` directives (up to 10 levels deep):

```json5
// clients/mueller.json5
{
  agents: { $include: "./mueller/agents.json5" },
  broadcast: { $include: "./mueller/broadcast.json5" },
}
```

### Path resolution

- **Relative paths**: Resolved relative to the including file
- **Absolute paths**: Used as-is
- **Parent directories**: `../` references work as expected

```json5
{ "$include": "./sub/config.json5" }      // relative
{ "$include": "/etc/openclaw/base.json5" } // absolute
{ "$include": "../shared/common.json5" }   // parent dir
```

### Error handling

- **Missing file**: Clear error with resolved path
- **Parse error**: Shows which included file failed
- **Circular includes**: Detected and reported with include chain

### Example: Multi-client legal setup

```json5
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789, auth: { token: "secret" } },

  // Common agent defaults
  agents: {
    defaults: {
      sandbox: { mode: "all", scope: "session" },
    },
    // Merge agent lists from all clients
    list: { $include: ["./clients/mueller/agents.json5", "./clients/schmidt/agents.json5"] },
  },

  // Merge broadcast configs
  broadcast: {
    $include: ["./clients/mueller/broadcast.json5", "./clients/schmidt/broadcast.json5"],
  },

  channels: { whatsapp: { groupPolicy: "allowlist" } },
}
```

```json5
// ~/.openclaw/clients/mueller/agents.json5
[
  { id: "mueller-transcribe", workspace: "~/clients/mueller/transcribe" },
  { id: "mueller-docs", workspace: "~/clients/mueller/docs" },
]
```

```json5
// ~/.openclaw/clients/mueller/broadcast.json5
{
  "120363403215116621@g.us": ["mueller-transcribe", "mueller-docs"],
}
```

## Common options

### Env vars + `.env`

OpenClaw reads env vars from the parent process (shell, launchd/systemd, CI, etc.).

Additionally, it loads:

- `.env` from the current working directory (if present)
- a global fallback `.env` from `~/.openclaw/.env` (aka `$OPENCLAW_STATE_DIR/.env`)

Neither `.env` file overrides existing env vars.

You can also provide inline env vars in config. These are only applied if the
process env is missing the key (same non-overriding rule):

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
  },
}
```

See [/environment](/help/environment) for full precedence and sources.

### `env.shellEnv` (optional)

Opt-in convenience: if enabled and none of the expected keys are set yet, OpenClaw runs your login shell and imports only the missing expected keys (never overrides).
This effectively sources your shell profile.

```json5
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

Env var equivalent:

- `OPENCLAW_LOAD_SHELL_ENV=1`
- `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`

### Env var substitution in config

You can reference environment variables directly in any config string value using
`${VAR_NAME}` syntax. Variables are substituted at config load time, before validation.

```json5
{
  models: {
    providers: {
      "vercel-gateway": {
        apiKey: "${VERCEL_GATEWAY_API_KEY}",
      },
    },
  },
  gateway: {
    auth: {
      token: "${OPENCLAW_GATEWAY_TOKEN}",
    },
  },
}
```

**Rules:**

- Only uppercase env var names are matched: `[A-Z_][A-Z0-9_]*`
- Missing or empty env vars throw an error at config load
- Escape with `$${VAR}` to output a literal `${VAR}`
- Works with `$include` (included files also get substitution)

**Inline substitution:**

```json5
{
  models: {
    providers: {
      custom: {
        baseUrl: "${CUSTOM_API_BASE}/v1", // → "https://api.example.com/v1"
      },
    },
  },
}
```

### Auth storage (OAuth + API keys)

OpenClaw stores **per-agent** auth profiles (OAuth + API keys) in:

- `<agentDir>/auth-profiles.json` (default: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`)

See also: [/concepts/oauth](/concepts/oauth)

Legacy OAuth imports:

- `~/.openclaw/credentials/oauth.json` (or `$OPENCLAW_STATE_DIR/credentials/oauth.json`)

The embedded Pi agent maintains a runtime cache at:

- `<agentDir>/auth.json` (managed automatically; don’t edit manually)

Legacy agent dir (pre multi-agent):

- `~/.openclaw/agent/*` (migrated by `openclaw doctor` into `~/.openclaw/agents/<defaultAgentId>/agent/*`)

Overrides:

- OAuth dir (legacy import only): `OPENCLAW_OAUTH_DIR`
- Agent dir (default agent root override): `OPENCLAW_AGENT_DIR` (preferred), `PI_CODING_AGENT_DIR` (legacy)

On first use, OpenClaw imports `oauth.json` entries into `auth-profiles.json`.

### `auth`

Optional metadata for auth profiles. This does **not** store secrets; it maps
profile IDs to a provider + mode (and optional email) and defines the provider
rotation order used for failover.

```json5
{
  auth: {
    profiles: {
      "anthropic:me@example.com": { provider: "anthropic", mode: "oauth", email: "me@example.com" },
      "anthropic:work": { provider: "anthropic", mode: "api_key" },
    },
    order: {
      anthropic: ["anthropic:me@example.com", "anthropic:work"],
    },
  },
}
```

### `agents.list[].identity`

Optional per-agent identity used for defaults and UX. This is written by the macOS onboarding assistant.

If set, OpenClaw derives defaults (only when you haven’t set them explicitly):

- `messages.ackReaction` from the **active agent**’s `identity.emoji` (falls back to 👀)
- `agents.list[].groupChat.mentionPatterns` from the agent’s `identity.name`/`identity.emoji` (so “@Samantha” works in groups across Telegram/Slack/Discord/Google Chat/iMessage/WhatsApp)
- `identity.avatar` accepts a workspace-relative image path or a remote URL/data URL. Local files must live inside the agent workspace.

`identity.avatar` accepts:

- Workspace-relative path (must stay within the agent workspace)
- `http(s)` URL
- `data:` URI

```json5
{
  agents: {
    list: [
      {
        id: "main",
        identity: {
          name: "Samantha",
          theme: "helpful sloth",
          emoji: "🦥",
          avatar: "avatars/samantha.png",
        },
      },
    ],
  },
}
```

### `wizard`

Metadata written by CLI wizards (`onboard`, `configure`, `doctor`).

```json5
{
  wizard: {
    lastRunAt: "2026-01-01T00:00:00.000Z",
    lastRunVersion: "2026.1.4",
    lastRunCommit: "abc1234",
    lastRunCommand: "configure",
    lastRunMode: "local",
  },
}
```

### `logging`

- Default log file: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- If you want a stable path, set `logging.file` to `/tmp/openclaw/openclaw.log`.
- Console output can be tuned separately via:
  - `logging.consoleLevel` (defaults to `info`, bumps to `debug` when `--verbose`)
  - `logging.consoleStyle` (`pretty` | `compact` | `json`)
- Tool summaries can be redacted to avoid leaking secrets:
  - `logging.redactSensitive` (`off` | `tools`, default: `tools`)
  - `logging.redactPatterns` (array of regex strings; overrides defaults)

```json5
{
  logging: {
    level: "info",
    file: "/tmp/openclaw/openclaw.log",
    consoleLevel: "info",
    consoleStyle: "pretty",
    redactSensitive: "tools",
    redactPatterns: [
      // Example: override defaults with your own rules.
      "\\bTOKEN\\b\\s*[=:]\\s*([\"']?)([^\\s\"']+)\\1",
      "/\\bsk-[A-Za-z0-9_-]{8,}\\b/gi",
    ],
  },
}
```

### `channels.whatsapp.dmPolicy`

Controls how WhatsApp direct chats (DMs) are handled:

- `"pairing"` (default): unknown senders get a pairing code; owner must approve
- `"allowlist"`: only allow senders in `channels.whatsapp.allowFrom` (or paired allow store)
- `"open"`: allow all inbound DMs (**requires** `channels.whatsapp.allowFrom` to include `"*"`)
- `"disabled"`: ignore all inbound DMs

Pairing codes expire after 1 hour; the bot only sends a pairing code when a new request is created. Pending DM pairing requests are capped at **3 per channel** by default.

Pairing approvals:

- `openclaw pairing list whatsapp`
- `openclaw pairing approve whatsapp <code>`

### `channels.whatsapp.allowFrom`

Allowlist of E.164 phone numbers that may trigger WhatsApp auto-replies (**DMs only**).
If empty and `channels.whatsapp.dmPolicy="pairing"`, unknown senders will receive a pairing code.
For groups, use `channels.whatsapp.groupPolicy` + `channels.whatsapp.groupAllowFrom`.

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing", // pairing | allowlist | open | disabled
      allowFrom: ["+15555550123", "+447700900123"],
      textChunkLimit: 4000, // optional outbound chunk size (chars)
      chunkMode: "length", // optional chunking mode (length | newline)
      mediaMaxMb: 50, // optional inbound media cap (MB)
    },
  },
}
```

### `channels.whatsapp.sendReadReceipts`

Controls whether inbound WhatsApp messages are marked as read (blue ticks). Default: `true`.

Self-chat mode always skips read receipts, even when enabled.

Per-account override: `channels.whatsapp.accounts.<id>.sendReadReceipts`.

```json5
{
  channels: {
    whatsapp: { sendReadReceipts: false },
  },
}
```

### `channels.whatsapp.accounts` (multi-account)

1. Bitta shlyuzda bir nechta WhatsApp akkauntlarini ishga tushiring:

```json5
2. {
  channels: {
    whatsapp: {
      accounts: {
        default: {}, // ixtiyoriy; default id ni barqaror saqlaydi
        personal: {},
        biz: {
          // Ixtiyoriy override. Default: ~/.openclaw/credentials/whatsapp/biz
          // authDir: "~/.openclaw/credentials/whatsapp/biz",
        },
      },
    },
  },
}
```

3. Eslatmalar:

- 4. Chiqish buyruqlari `default` akkaunt mavjud bo‘lsa, unga yo‘naltiriladi; aks holda, sozlangan akkaunt id larining birinchisi (tartiblangan holda) ishlatiladi.
- 5. Eski bitta-akkauntli Baileys auth katalogi `openclaw doctor` tomonidan `whatsapp/default` ga ko‘chiriladi.

### 6. `channels.telegram.accounts` / `channels.discord.accounts` / `channels.googlechat.accounts` / `channels.slack.accounts` / `channels.mattermost.accounts` / `channels.signal.accounts` / `channels.imessage.accounts`

7. Har bir kanal uchun bir nechta akkauntni ishga tushiring (har bir akkauntning o‘z `accountId` si va ixtiyoriy `name` i bor):

```json5
8. {
  channels: {
    telegram: {
      accounts: {
        default: {
          name: "Primary bot",
          botToken: "123456:ABC...",
        },
        alerts: {
          name: "Alerts bot",
          botToken: "987654:XYZ...",
        },
      },
    },
  },
}
```

9. Eslatmalar:

- 10. `accountId` ko‘rsatilmaganida `default` ishlatiladi (CLI + marshrutlash).
- 11. Muhit (Env) tokenlari faqat **default** akkauntga tatbiq etiladi.
- 12. Asosiy kanal sozlamalari (guruh siyosati, mention gating va h.k.) 13. har bir akkaunt uchun alohida override qilinmasa, barcha akkauntlarga qo‘llanadi.
- 14. Har bir akkauntni turli `agents.defaults` ga yo‘naltirish uchun `bindings[].match.accountId` dan foydalaning.

### 15. Guruh chatlarida mention gating (`agents.list[].groupChat` + `messages.groupChat`)

16. Guruh xabarlari uchun standart holat — **mention talab qilinadi** (metadata mention yoki regex andozalari orqali). 17. WhatsApp, Telegram, Discord, Google Chat va iMessage guruh chatlariga qo‘llanadi.

18. **Mention turlari:**

- 19. **Metadata mentionlar**: Platformaga xos @-mentionlar (masalan, WhatsApp’da bosib-mention qilish). 20. WhatsApp self-chat rejimida e’tiborga olinmaydi (qarang: `channels.whatsapp.allowFrom`).
- 21. **Matn andozalari**: `agents.list[].groupChat.mentionPatterns` da aniqlangan regex andozalar. Always checked regardless of self-chat mode.
- 23. Mention gating faqat mentionni aniqlash mumkin bo‘lganda qo‘llanadi (native mentionlar yoki kamida bitta `mentionPattern` mavjud bo‘lsa).

```json5
24. {
  messages: {
    groupChat: { historyLimit: 50 },
  },
  agents: {
    list: [{ id: "main", groupChat: { mentionPatterns: ["@openclaw", "openclaw"] } }],
  },
}
```

25. `messages.groupChat.historyLimit` guruhlar uchun tarix kontekstining global standartini belgilaydi. 26. Kanallar `channels.<channel>` orqali override qilishi mumkin27. `.historyLimit` (yoki ko‘p akkauntli holatda `channels.<channel>`28. `.accounts.*.historyLimit`). 29. Tarixni o‘rashni o‘chirish uchun `0` ga sozlang.

#### 30. DM tarix limitlari

31. DM suhbatlari agent tomonidan boshqariladigan sessiyaga asoslangan tarixdan foydalanadi. 32. Har bir DM sessiyasida saqlanadigan foydalanuvchi navbatlari sonini cheklashingiz mumkin:

```json5
33. {
  channels: {
    telegram: {
      dmHistoryLimit: 30, // DM sessiyalarini 30 ta foydalanuvchi navbatigacha cheklash
      dms: {
        "123456789": { historyLimit: 50 }, // foydalanuvchi bo‘yicha override (user ID)
      },
    },
  },
}
```

34. Hal qilish tartibi:

1. 35. Har bir DM bo‘yicha override: `channels.<provider>`36. `.dms[userId].historyLimit`
2. 37. Provider standarti: `channels.<provider>`38. `.dmHistoryLimit`
3. 39. Cheklov yo‘q (butun tarix saqlanadi)

40) Qo‘llab-quvvatlanadigan providerlar: `telegram`, `whatsapp`, `discord`, `slack`, `signal`, `imessage`, `msteams`.

41. Agent bo‘yicha override (belgilansa, hatto `[]` bo‘lsa ham, ustunlikka ega):

```json5
42. {
  agents: {
    list: [
      { id: "work", groupChat: { mentionPatterns: ["@workbot", "\\+15555550123"] } },
      { id: "personal", groupChat: { mentionPatterns: ["@homebot", "\\+15555550999"] } },
    ],
  },
}
```

43. Mention gating uchun standart sozlamalar kanal darajasida joylashgan (`channels.whatsapp.groups`, `channels.telegram.groups`, `channels.imessage.groups`, `channels.discord.guilds`). 44. `*.groups` sozlanganda, u guruhlar uchun allowlist sifatida ham ishlaydi; barcha guruhlarni ruxsat berish uchun `"*"` ni kiriting.

45. Faqat **ma’lum matn triggerlari** ga javob berish uchun (native @-mentionlarni e’tiborsiz qoldirib):

```json5
46. {
  channels: {
    whatsapp: {
      // O‘zingizning raqamingizni qo‘shib, self-chat rejimini yoqing (native @-mentionlarni e’tiborsiz qoldiradi).
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          // Faqat ushbu matn andozalari javobni ishga tushiradi
          mentionPatterns: ["reisponde", "@openclaw"],
        },
      },
    ],
  },
}
```

### 47. Guruh siyosati (kanal bo‘yicha)

48. Guruh/xona xabarlari umuman qabul qilinishini boshqarish uchun `channels.*.groupPolicy` dan foydalaning:

```json5
49. {
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
    telegram: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["tg:123456789", "@alice"],
    },
    signal: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
    imessage: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["chat_id:123"],
    },
    msteams: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["user@org.com"],
    },
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        GUILD_ID: {
          channels: { help: { allow: true } },
        },
      },
    },
    slack: {
      groupPolicy: "allowlist",
      channels: { "#general": { allow: true } },
    },
  },
}
```

50. Eslatmalar:

- "open": guruhlar allowlist’larni chetlab o‘tadi; mention-gating baribir qo‘llaniladi.
- "disabled": barcha guruh/xona xabarlarini bloklash.
- "allowlist": faqat sozlangan allowlist’ga mos keladigan guruh/xonalarga ruxsat berish.
- `channels.defaults.groupPolicy` provayderning `groupPolicy` qiymati sozlanmagan bo‘lsa, standartni belgilaydi.
- WhatsApp/Telegram/Signal/iMessage/Microsoft Teams `groupAllowFrom` dan foydalanadi (zaxira: aniq `allowFrom`).
- Discord/Slack kanal allowlist’laridan foydalanadi (`channels.discord.guilds.*.channels`, `channels.slack.channels`).
- Guruh DM’lari (Discord/Slack) hanuz `dm.groupEnabled` + `dm.groupChannels` orqali boshqariladi.
- Standart qiymat `groupPolicy: "allowlist"` (agar `channels.defaults.groupPolicy` bilan bekor qilinmasa); agar allowlist sozlanmagan bo‘lsa, guruh xabarlari bloklanadi.

### Ko‘p-agentli marshrutlash (`agents.list` + `bindings`).

Bitta Gateway ichida bir nechta izolyatsiyalangan agentlarni ishga tushirish (alohida workspace, `agentDir`, sessiyalar).
Kiruvchi xabarlar binding’lar orqali agentga yo‘naltiriladi.

- `agents.list[]`: har bir agent uchun override’lar.
  - `id`: barqaror agent ID (majburiy).
  - `default`: ixtiyoriy; bir nechta belgilansa, birinchisi ustun bo‘ladi va ogohlantirish yoziladi.
    Agar hech biri belgilanmasa, ro‘yxatdagi **birinchi yozuv** standart agent bo‘ladi.
  - `name`: agent uchun ko‘rinadigan nom.
  - `workspace`: standart `~/.openclaw/workspace-<agentId>` (`main` uchun `agents.defaults.workspace` ga qaytadi).
  - `agentDir`: standart `~/.openclaw/agents/<agentId>/agent`.
  - `model`: agentga xos standart model; shu agent uchun `agents.defaults.model` ni bekor qiladi.
    - string ko‘rinishi: `"provider/model"`, faqat `agents.defaults.model.primary` ni bekor qiladi.
    - obyekt ko‘rinishi: `{ primary, fallbacks }` (fallback’lar `agents.defaults.model.fallbacks` ni bekor qiladi; `[]` — shu agent uchun global fallback’larni o‘chiradi).
  - `identity`: agentga xos nom/mavzu/emoji (mention pattern’lari + ack reaksiyalarida ishlatiladi).
  - `groupChat`: agentga xos mention-gating (`mentionPatterns`).
  - `sandbox`: agentga xos sandbox sozlamalari (`agents.defaults.sandbox` ni bekor qiladi).
    - `mode`: `"off"` | `"non-main"` | `"all"`.
    - `workspaceAccess`: `"none"` | `"ro"` | `"rw"`.
    - `scope`: `"session"` | `"agent"` | `"shared"`.
    - `workspaceRoot`: sandbox uchun maxsus workspace ildizi.
    - `docker`: agentga xos docker override’lari (masalan, `image`, `network`, `env`, `setupCommand`, limitlar; `scope: "shared"` bo‘lsa e’tiborga olinmaydi).
    - `browser`: agentga xos sandboxlangan brauzer override’lari (`scope: "shared"` bo‘lsa e’tiborga olinmaydi).
    - `prune`: agentga xos sandbox tozalash override’lari (`scope: "shared"` bo‘lsa e’tiborga olinmaydi).
  - `subagents`: agentga xos sub-agent standartlari.
    - `allowAgents`: shu agentdan `sessions_spawn` uchun ruxsat etilgan agent ID’lari allowlist’i (`["*"]` = hammasiga ruxsat; standart: faqat o‘sha agent).
  - `tools`: agentga xos asbob cheklovlari (sandbox asbob siyosatidan oldin qo‘llaniladi).
    - `profile`: asosiy asbob profili (allow/deny’dan oldin qo‘llaniladi).
    - `allow`: ruxsat etilgan asbob nomlari massivi.
    - `deny`: taqiqlangan asbob nomlari massivi (deny ustun).
- `agents.defaults`: umumiy agent standartlari (model, workspace, sandbox va h.k.).
- `bindings[]`: kiruvchi xabarlarni `agentId` ga yo‘naltiradi.
  - `match.channel` (majburiy).
  - `match.accountId` (ixtiyoriy; `*` = istalgan akkaunt; ko‘rsatilmasa = standart akkaunt).
  - 49. {
        session: {
        scope: "per-sender",
        dmScope: "main",
        identityLinks: {
        alice: ["telegram:123456789", "discord:987654321012345678"],
        },
        reset: {
        mode: "daily",
        atHour: 4,
        idleMinutes: 60,
        },
        resetByType: {
        thread: { mode: "daily", atHour: 4 },
        direct: { mode: "idle", idleMinutes: 240 },
        group: { mode: "idle", idleMinutes: 120 },
        },
        resetTriggers: ["/new", "/reset"],
        // Sukut bo‘yicha allaqachon ~/.openclaw/agents/<agentId>/sessions/sessions.json ostida per-agent
        // {agentId} shablonlash bilan almashtirishingiz mumkin:
        store: "~/.openclaw/agents/{agentId}/sessions/sessions.json",
        // To‘g‘ridan-to‘g‘ri chatlar agent:<agentId>:<mainKey> ga birlashadi (sukut bo‘yicha: "main").
        mainKey: "main",
        agentToAgent: {
        // So‘rovchi/maqsad o‘rtasidagi ping-pong javob aylanishlarining maksimal soni (0–5).
        maxPingPongTurns: 5,
        },
        sendPolicy: {
        rules: [{ action: "deny", match: { channel: "discord", chatType: "group" } }],
        default: "allow",
        },
        },
        }
  - `match.guildId` / `match.teamId` (ixtiyoriy; kanalga xos).

Deterministik moslik tartibi:

1. `match.peer`.
2. `match.guildId`.
3. `match.teamId`.
4. `match.accountId` (aniq moslik, peer/guild/team yo‘q).
5. `match.accountId: "*"` (kanal bo‘yicha, peer/guild/team yo‘q).
6. standart agent (`agents.list[].default`, aks holda ro‘yxatdagi birinchi yozuv, aks holda `"main"`).

Har bir moslik darajasida `bindings` dagi birinchi mos kelgan yozuv ustun bo‘ladi.

#### Har bir agent uchun kirish profillari (ko‘p agentli)

Har bir agent o‘zining sandboxi va vositalar siyosatiga ega bo‘lishi mumkin. Bundan bitta gateway ichida
kirish darajalarini aralashtirish uchun foydalaning:

- **To‘liq kirish** (shaxsiy agent)
- **Faqat o‘qish** vositalari + ish muhiti
- **Fayl tizimiga kirish yo‘q** (faqat xabarlar/seans vositalari)

Ustuvorlik va qo‘shimcha misollar uchun [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools) sahifasiga qarang.

Full access (no sandbox):

```json5
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: { mode: "off" },
      },
    ],
  },
}
```

Faqat o‘qish vositalari + faqat o‘qish ish muhiti:

```json5
{
  agents: {
    list: [
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "ro",
        },
        tools: {
          allow: [
            "read",
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
          ],
          deny: ["write", "edit", "apply_patch", "exec", "process", "browser"],
        },
      },
    ],
  },
}
```

Fayl tizimiga kirish yo‘q (xabarlar/seans vositalari yoqilgan):

```json5
{
  agents: {
    list: [
      {
        id: "public",
        workspace: "~/.openclaw/workspace-public",
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "none",
        },
        tools: {
          allow: [
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
            "whatsapp",
            "telegram",
            "slack",
            "discord",
            "gateway",
          ],
          deny: [
            "read",
            "write",
            "edit",
            "apply_patch",
            "exec",
            "process",
            "browser",
            "canvas",
            "nodes",
            "cron",
            "gateway",
            "image",
          ],
        },
      },
    ],
  },
}
```

Example: two WhatsApp accounts → two agents:

```json5
{
  agents: {
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
  channels: {
    whatsapp: {
      accounts: {
        personal: {},
        biz: {},
      },
    },
  },
}
```

### `tools.agentToAgent` (ixtiyoriy)

Agentdan agentga xabar almashish ixtiyoriy ravishda yoqiladi:

```json5
{
  tools: {
    agentToAgent: {
      enabled: false,
      allow: ["home", "work"],
    },
  },
}
```

### `messages.queue`

Agent ishga tushirilgan paytda kiruvchi xabarlar qanday tutishini boshqaradi.

```json5
{
  messages: {
    queue: {
      mode: "collect", // steer | followup | collect | steer-backlog (steer+backlog ok) | interrupt (queue=steer legacy)
      debounceMs: 1000,
      cap: 20,
      drop: "summarize", // old | new | summarize
      byChannel: {
        whatsapp: "collect",
        telegram: "collect",
        discord: "collect",
        imessage: "collect",
        webchat: "collect",
      },
    },
  },
}
```

### `messages.inbound`

**Bir xil jo‘natuvchidan** tez-tez keladigan kiruvchi xabarlarni debounce qiling, shunda ketma-ket bir nechta xabarlar bitta agent navbatiga birlashtiriladi. Debounce kanal + suhbat bo‘yicha chegaralanadi
va javobni bog‘lash/IDlar uchun eng so‘nggi xabardan foydalanadi.

```json5
{
  messages: {
    inbound: {
      debounceMs: 2000, // 0 disables
      byChannel: {
        whatsapp: 5000,
        slack: 1500,
        discord: 1500,
      },
    },
  },
}
```

Eslatmalar:

- Debounce **faqat matnli** xabarlarni guruhlaydi; media/ilovalar darhol uzatiladi.
- Boshqaruv buyruqlari (masalan, `/queue`, `/new`) debounce’dan chetlab o‘tadi, shuning uchun ular alohida qoladi.

### `commands` (chat buyruqlarini boshqarish)

Chat buyruqlari turli konnektorlar bo‘ylab qanday yoqilishini boshqaradi.

```json5
{
  commands: {
    native: "auto", // register native commands when supported (auto)
    text: true, // parse slash commands in chat messages
    bash: false, // allow ! (alias: /bash) (host-only; requires tools.elevated allowlists)
    bashForegroundMs: 2000, // bash foreground window (0 backgrounds immediately)
    config: false, // allow /config (writes to disk)
    debug: false, // allow /debug (runtime-only overrides)
    restart: false, // allow /restart + gateway restart tool
    useAccessGroups: true, // enforce access-group allowlists/policies for commands
  },
}
```

Eslatmalar:

- Matn buyruqlari **alohida** xabar sifatida yuborilishi va boshida `/` bo‘lishi kerak (oddiy matn aliaslari yo‘q).
- `commands.text: false` chat xabarlarida buyruqlarni tahlil qilishni o‘chiradi.
- `commands.native: "auto"` (standart) Discord/Telegram uchun native buyruqlarni yoqadi va Slack’ni o‘chiq qoldiradi; qo‘llab-quvvatlanmagan kanallar faqat matnli bo‘lib qoladi.
- `commands.native: true|false` ni o‘rnating — barchasini majburlash uchun, yoki kanal bo‘yicha `channels.discord.commands.native`, `channels.telegram.commands.native`, `channels.slack.commands.native` (bool yoki `"auto"`) orqali bekor qiling. `false` Discord/Telegram’da avval ro‘yxatdan o‘tgan buyruqlarni ishga tushirish paytida o‘chiradi; Slack buyruqlari Slack ilovasida boshqariladi.
- `channels.telegram.customCommands` Telegram bot menyusiga qo‘shimcha yozuvlar qo‘shadi. Nomlar normallashtiriladi; native buyruqlar bilan to‘qnashuvlar e’tiborga olinmaydi.
- `commands.bash: true` `! <cmd>` orqali host shell buyruqlarini ishga tushirishni yoqadi (`/bash <cmd>` ham alias sifatida ishlaydi). `tools.elevated.enabled` ni va jo‘natuvchini `tools.elevated.allowFrom.<channel>` da ruxsat etishni talab qiladi .`commands.bashForegroundMs` bash fon rejimiga o‘tishdan oldin qancha kutishini boshqaradi.
- Bash vazifasi ishlayotgan paytda, yangi `! <cmd>` so‘rovlari rad etiladi (bir vaqtning o‘zida bittadan). `commands.config: true` `/config` ni yoqadi (`openclaw.json` ni o‘qiydi/yozadi). `channels.<provider>
  .configWrites` shu kanal tomonidan boshlangan konfiguratsiya o‘zgarishlarini cheklaydi (standart: true).
- Bu `/config set|unset` hamda provayderga xos avtomatik migratsiyalarga (Telegram superguruh ID o‘zgarishlari, Slack kanal ID o‘zgarishlari) taalluqlidir.
- `channels.<provider>.configWrites` gates config mutations initiated by that channel (default: true). This applies to `/config set|unset` plus provider-specific auto-migrations (Telegram supergroup ID changes, Slack channel ID changes).
- `commands.debug: true` enables `/debug` (runtime-only overrides).
- `commands.restart: true` enables `/restart` and the gateway tool restart action.
- `commands.useAccessGroups: false` allows commands to bypass access-group allowlists/policies.
- Slash commands and directives are only honored for **authorized senders**. Authorization is derived from
  channel allowlists/pairing plus `commands.useAccessGroups`.

### `web` (WhatsApp web channel runtime)

WhatsApp runs through the gateway’s web channel (Baileys Web). It starts automatically when a linked session exists.
Set `web.enabled: false` to keep it off by default.

```json5
{
  web: {
    enabled: true,
    heartbeatSeconds: 60,
    reconnect: {
      initialMs: 2000,
      maxMs: 120000,
      factor: 1.4,
      jitter: 0.2,
      maxAttempts: 0,
    },
  },
}
```

### `channels.telegram` (bot transport)

OpenClaw starts Telegram only when a `channels.telegram` config section exists. The bot token is resolved from `channels.telegram.botToken` (or `channels.telegram.tokenFile`), with `TELEGRAM_BOT_TOKEN` as a fallback for the default account.
Set `channels.telegram.enabled: false` to disable automatic startup.
Multi-account support lives under `channels.telegram.accounts` (see the multi-account section above). Env tokens only apply to the default account.
Set `channels.telegram.configWrites: false` to block Telegram-initiated config writes (including supergroup ID migrations and `/config set|unset`).

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "your-bot-token",
      dmPolicy: "pairing", // pairing | allowlist | open | disabled
      allowFrom: ["tg:123456789"], // optional; "open" requires ["*"]
      groups: {
        "*": { requireMention: true },
        "-1001234567890": {
          allowFrom: ["@admin"],
          systemPrompt: "Keep answers brief.",
          topics: {
            "99": {
              requireMention: false,
              skills: ["search"],
              systemPrompt: "Stay on topic.",
            },
          },
        },
      },
      customCommands: [
        { command: "backup", description: "Git backup" },
        { command: "generate", description: "Create an image" },
      ],
      historyLimit: 50, // include last N group messages as context (0 disables)
      replyToMode: "first", // off | first | all
      linkPreview: true, // toggle outbound link previews
      streamMode: "partial", // off | partial | block (draft streaming; separate from block streaming)
      draftChunk: {
        // optional; only for streamMode=block
        minChars: 200,
        maxChars: 800,
        breakPreference: "paragraph", // paragraph | newline | sentence
      },
      actions: { reactions: true, sendMessage: true }, // tool action gates (false disables)
      reactionNotifications: "own", // off | own | all
      mediaMaxMb: 5,
      retry: {
        // outbound retry policy
        attempts: 3,
        minDelayMs: 400,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
      network: {
        // transport overrides
        autoSelectFamily: false,
      },
      proxy: "socks5://localhost:9050",
      webhookUrl: "https://example.com/telegram-webhook", // requires webhookSecret
      webhookSecret: "secret",
      webhookPath: "/telegram-webhook",
    },
  },
}
```

Draft streaming notes:

- Uses Telegram `sendMessageDraft` (draft bubble, not a real message).
- Requires **private chat topics** (message_thread_id in DMs; bot has topics enabled).
- `/reasoning stream` streams reasoning into the draft, then sends the final answer.
  Retry policy defaults and behavior are documented in [Retry policy](/concepts/retry).

### `channels.discord` (bot transport)

Configure the Discord bot by setting the bot token and optional gating:
Multi-account support lives under `channels.discord.accounts` (see the multi-account section above). Env tokens only apply to the default account.

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "your-bot-token",
      mediaMaxMb: 8, // clamp inbound media size
      allowBots: false, // allow bot-authored messages
      actions: {
        // tool action gates (false disables)
        reactions: true,
        stickers: true,
        polls: true,
        permissions: true,
        messages: true,
        threads: true,
        pins: true,
        search: true,
        memberInfo: true,
        roleInfo: true,
        roles: false,
        channelInfo: true,
        voiceStatus: true,
        events: true,
        moderation: false,
      },
      replyToMode: "off", // off | first | all
      dm: {
        enabled: true, // disable all DMs when false
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["1234567890", "steipete"], // optional DM allowlist ("open" requires ["*"])
        groupEnabled: false, // enable group DMs
        groupChannels: ["openclaw-dm"], // optional group DM allowlist
      },
      guilds: {
        "123456789012345678": {
          // guild id (preferred) or slug
          slug: "friends-of-openclaw",
          requireMention: false, // per-guild default
          reactionNotifications: "own", // off | own | all | allowlist
          users: ["987654321098765432"], // optional per-guild user allowlist
          channels: {
            general: { allow: true },
            help: {
              allow: true,
              requireMention: true,
              users: ["987654321098765432"],
              skills: ["docs"],
              systemPrompt: "Short answers only.",
            },
          },
        },
      },
      historyLimit: 20, // include last N guild messages as context
      textChunkLimit: 2000, // optional outbound text chunk size (chars)
      chunkMode: "length", // optional chunking mode (length | newline)
      maxLinesPerMessage: 17, // soft max lines per message (Discord UI clipping)
      retry: {
        // outbound retry policy
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}
```

OpenClaw starts Discord only when a `channels.discord` config section exists. The token is resolved from `channels.discord.token`, with `DISCORD_BOT_TOKEN` as a fallback for the default account (unless `channels.discord.enabled` is `false`). Use `user:<id>` (DM) or `channel:<id>` (guild channel) when specifying delivery targets for cron/CLI commands; bare numeric IDs are ambiguous and rejected.
Guild slugs are lowercase with spaces replaced by `-`; channel keys use the slugged channel name (no leading `#`). Prefer guild ids as keys to avoid rename ambiguity.
Bot-authored messages are ignored by default. Enable with `channels.discord.allowBots` (own messages are still filtered to prevent self-reply loops).
Reaction notification modes:

- `off`: no reaction events.
- `own`: reactions on the bot's own messages (default).
- `all`: all reactions on all messages.
- `allowlist`: reactions from `guilds.<id>.users` on all messages (empty list disables).
  Outbound text is chunked by `channels.discord.textChunkLimit` (default 2000). Set `channels.discord.chunkMode="newline"` to split on blank lines (paragraph boundaries) before length chunking. Discord clients can clip very tall messages, so `channels.discord.maxLinesPerMessage` (default 17) splits long multi-line replies even when under 2000 chars.
  Retry policy defaults and behavior are documented in [Retry policy](/concepts/retry).

### `channels.googlechat` (Chat API webhook)

Google Chat runs over HTTP webhooks with app-level auth (service account).
Multi-account support lives under `channels.googlechat.accounts` (see the multi-account section above). Env vars only apply to the default account.

```json5
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountFile: "/path/to/service-account.json",
      audienceType: "app-url", // app-url | project-number
      audience: "https://gateway.example.com/googlechat",
      webhookPath: "/googlechat",
      botUser: "users/1234567890", // optional; improves mention detection
      dm: {
        enabled: true,
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["users/1234567890"], // optional; "open" requires ["*"]
      },
      groupPolicy: "allowlist",
      groups: {
        "spaces/AAAA": { allow: true, requireMention: true },
      },
      actions: { reactions: true },
      typingIndicator: "message",
      mediaMaxMb: 20,
    },
  },
}
```

Notes:

- Service account JSON can be inline (`serviceAccount`) or file-based (`serviceAccountFile`).
- Env fallbacks for the default account: `GOOGLE_CHAT_SERVICE_ACCOUNT` or `GOOGLE_CHAT_SERVICE_ACCOUNT_FILE`.
- `audienceType` + `audience` must match the Chat app’s webhook auth config.
- Use `spaces/<spaceId>` or `users/<userId|email>` when setting delivery targets.

### `channels.slack` (socket mode)

Slack runs in Socket Mode and requires both a bot token and app token:

```json5
{
  channels: {
    slack: {
      enabled: true,
      botToken: "xoxb-...",
      appToken: "xapp-...",
      dm: {
        enabled: true,
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["U123", "U456", "*"], // optional; "open" requires ["*"]
        groupEnabled: false,
        groupChannels: ["G123"],
      },
      channels: {
        C123: { allow: true, requireMention: true, allowBots: false },
        "#general": {
          allow: true,
          requireMention: true,
          allowBots: false,
          users: ["U123"],
          skills: ["docs"],
          systemPrompt: "Short answers only.",
        },
      },
      historyLimit: 50, // include last N channel/group messages as context (0 disables)
      allowBots: false,
      reactionNotifications: "own", // off | own | all | allowlist
      reactionAllowlist: ["U123"],
      replyToMode: "off", // off | first | all
      thread: {
        historyScope: "thread", // thread | channel
        inheritParent: false,
      },
      actions: {
        reactions: true,
        messages: true,
        pins: true,
        memberInfo: true,
        emojiList: true,
      },
      slashCommand: {
        enabled: true,
        name: "openclaw",
        sessionPrefix: "slack:slash",
        ephemeral: true,
      },
      textChunkLimit: 4000,
      chunkMode: "length",
      mediaMaxMb: 20,
    },
  },
}
```

Multi-account support lives under `channels.slack.accounts` (see the multi-account section above). Env tokens only apply to the default account.

OpenClaw starts Slack when the provider is enabled and both tokens are set (via config or `SLACK_BOT_TOKEN` + `SLACK_APP_TOKEN`). Use `user:<id>` (DM) or `channel:<id>` when specifying delivery targets for cron/CLI commands.
Set `channels.slack.configWrites: false` to block Slack-initiated config writes (including channel ID migrations and `/config set|unset`).

Bot-authored messages are ignored by default. Enable with `channels.slack.allowBots` or `channels.slack.channels.<id>.allowBots`.

Reaction notification modes:

- `off`: no reaction events.
- `own`: reactions on the bot's own messages (default).
- `all`: all reactions on all messages.
- `allowlist`: reactions from `channels.slack.reactionAllowlist` on all messages (empty list disables).

Thread session isolation:

- `channels.slack.thread.historyScope` controls whether thread history is per-thread (`thread`, default) or shared across the channel (`channel`).
- `channels.slack.thread.inheritParent` controls whether new thread sessions inherit the parent channel transcript (default: false).

Slack action groups (gate `slack` tool actions):

| Action group | Default | Notes                  |
| ------------ | ------- | ---------------------- |
| reactions    | enabled | React + list reactions |
| messages     | enabled | Read/send/edit/delete  |
| pins         | enabled | Pin/unpin/list         |
| memberInfo   | enabled | Member info            |
| emojiList    | enabled | Custom emoji list      |

### `channels.mattermost` (bot token)

Mattermost ships as a plugin and is not bundled with the core install.
Install it first: `openclaw plugins install @openclaw/mattermost` (or `./extensions/mattermost` from a git checkout).

Mattermost requires a bot token plus the base URL for your server:

```json5
{
  channels: {
    mattermost: {
      enabled: true,
      botToken: "mm-token",
      baseUrl: "https://chat.example.com",
      dmPolicy: "pairing",
      chatmode: "oncall", // oncall | onmessage | onchar
      oncharPrefixes: [">", "!"],
      textChunkLimit: 4000,
      chunkMode: "length",
    },
  },
}
```

OpenClaw starts Mattermost when the account is configured (bot token + base URL) and enabled. The token + base URL are resolved from `channels.mattermost.botToken` + `channels.mattermost.baseUrl` or `MATTERMOST_BOT_TOKEN` + `MATTERMOST_URL` for the default account (unless `channels.mattermost.enabled` is `false`).

Chat modes:

- `oncall` (default): respond to channel messages only when @mentioned.
- `onmessage`: respond to every channel message.
- `onchar`: xabar trigger prefiksi (`channels.mattermost.oncharPrefixes`, standart `[">", "!"]`) bilan boshlanganda javob beradi.

Kirishni boshqarish:

- Standart DMlar: `channels.mattermost.dmPolicy="pairing"` (noma’lum yuboruvchilar juftlash kodi oladi).
- Public DMs: `channels.mattermost.dmPolicy="open"` plus `channels.mattermost.allowFrom=["*"]`.
- Groups: `channels.mattermost.groupPolicy="allowlist"` by default (mention-gated). Use `channels.mattermost.groupAllowFrom` to restrict senders.

Ko‘p hisobni qo‘llab-quvvatlash `channels.mattermost.accounts` ostida joylashgan (yuqoridagi ko‘p hisob bo‘limiga qarang). Muhit o‘zgaruvchilari faqat standart hisobga qo‘llaniladi.
Use `channel:<id>` or `user:<id>` (or `@username`) when specifying delivery targets; bare ids are treated as channel ids.

### `channels.signal` (signal-cli)

Signal reaksiyalari tizim hodisalarini chiqarishi mumkin (umumiy reaksiya vositalari):

```json5
{
  channels: {
    signal: {
      reactionNotifications: "own", // off | own | all | allowlist
      reactionAllowlist: ["+15551234567", "uuid:123e4567-e89b-12d3-a456-426614174000"],
      historyLimit: 50, // include last N group messages as context (0 disables)
    },
  },
}
```

Reaction notification modes:

- `off`: reaksiya hodisalari yo‘q.
- `own`: botning o‘z xabarlaridagi reaksiyalar (standart).
- `all`: all reactions on all messages.
- `allowlist`: reactions from `channels.signal.reactionAllowlist` on all messages (empty list disables).

### `channels.imessage` (imsg CLI)

OpenClaw `imsg rpc` ni ishga tushiradi (stdio orqali JSON-RPC). Daemon yoki port talab qilinmaydi.

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "imsg",
      dbPath: "~/Library/Messages/chat.db",
      remoteHost: "user@gateway-host", // SSH o‘ramidan foydalanganda masofaviy biriktirmalar uchun SCP
      dmPolicy: "pairing", // pairing | allowlist | open | disabled
      allowFrom: ["+15555550123", "user@example.com", "chat_id:123"],
      historyLimit: 50, // kontekst sifatida oxirgi N guruh xabarlarini qo‘shadi (0 o‘chiradi)
      includeAttachments: false,
      mediaMaxMb: 16,
      service: "auto",
      region: "US",
    },
  },
}
```

Ko‘p hisobni qo‘llab-quvvatlash `channels.imessage.accounts` ostida joylashgan (yuqoridagi ko‘p hisob bo‘limiga qarang).

Eslatmalar:

- Messages ma’lumotlar bazasiga To‘liq Diskga Kirish talab qilinadi.
- Birinchi yuborish Messages avtomatlashtirish ruxsatini so‘raydi.
- `chat_id:<id>` nishonlarini afzal ko‘ring. Suhbatlarni ko‘rish uchun `imsg chats --limit 20` dan foydalaning.
- `channels.imessage.cliPath` o‘ram skriptiga ishora qilishi mumkin (masalan, `imsg rpc` ni ishga tushiradigan boshqa Mac’ga `ssh`); parol so‘rovlarini oldini olish uchun SSH kalitlaridan foydalaning.
- For remote SSH wrappers, set `channels.imessage.remoteHost` to fetch attachments via SCP when `includeAttachments` is enabled.

Namunaviy o‘ram:

```bash
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"
```

### `agents.defaults.workspace`

Agent tomonidan fayl amallari uchun ishlatiladigan **yagona global ishchi katalog**ni o‘rnatadi.

Standart: `~/.openclaw/workspace`.

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

Agar `agents.defaults.sandbox` yoqilgan bo‘lsa, asosiy bo‘lmagan sessiyalar buni `agents.defaults.sandbox.workspaceRoot` ostidagi o‘z ko‘lamiga xos ishchi kataloglari bilan almashtirishi mumkin.

### `agents.defaults.repoRoot`

Tizim promptining Runtime satrida ko‘rsatish uchun ixtiyoriy repozitoriya ildizi. Agar o‘rnatilmagan bo‘lsa, OpenClaw ishchi katalogdan (va joriy ishchi katalogdan) yuqoriga qarab `.git` katalogini aniqlashga harakat qiladi. Foydalanish uchun yo‘l mavjud bo‘lishi kerak.

```json5
{
  agents: { defaults: { repoRoot: "~/Projects/openclaw" } },
}
```

### `agents.defaults.skipBootstrap`

Ishchi katalog bootstrap fayllarini (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md` va `BOOTSTRAP.md`) avtomatik yaratishni o‘chiradi.

Buni ishchi katalog fayllari repozitoriyadan keladigan oldindan tayyorlangan joylashtirishlar uchun ishlating.

```json5
{
  agents: { defaults: { skipBootstrap: true } },
}
```

### `agents.defaults.bootstrapMaxChars`

Qirqishdan oldin tizim promptiga kiritiladigan har bir ishchi katalog bootstrap faylining maksimal belgilar soni. Standart: `20000`.

Fayl ushbu chegaradan oshsa, OpenClaw ogohlantirishni logga yozadi va belgi bilan qisqartirilgan head/tail kiritadi.

```json5
{
  agents: { defaults: { bootstrapMaxChars: 20000 } },
}
```

### `agents.defaults.userTimezone`

Foydalanuvchining vaqt mintaqasini **tizim prompti konteksti** uchun o‘rnatadi (xabar konvertlaridagi vaqt belgilari uchun emas). Agar o‘rnatilmasa, OpenClaw ishga tushish vaqtida xostning vaqt mintaqasidan foydalanadi.

```json5
{
  agents: { defaults: { userTimezone: "America/Chicago" } },
}
```

### `agents.defaults.timeFormat`

Tizim promptidagi Current Date & Time bo‘limida ko‘rsatiladigan **vaqt formatini** boshqaradi.
Standart: `auto` (OS afzalligi).

```json5
{
  agents: { defaults: { timeFormat: "auto" } }, // auto | 12 | 24
}
```

### `messages`

Kirish/chiqish prefikslari va ixtiyoriy tasdiqlash reaksiyalarini boshqaradi.
Navbatlash, sessiyalar va oqimli kontekst haqida [Messages](/concepts/messages) sahifasiga qarang.

```json5
{
  messages: {
    responsePrefix: "🦞", // or "auto"
    ackReaction: "👀",
    ackReactionScope: "group-mentions",
    removeAckAfterReply: false,
  },
}
```

`responsePrefix` **barcha chiqish javoblariga** (asbob xulosalari, blok oqimi, yakuniy javoblar) kanallar bo‘ylab, agar allaqachon mavjud bo‘lmasa, qo‘llanadi.

Overrides can be configured per channel and per account:

- `channels.<channel>`.responsePrefix
- `channels.<channel>`.accounts.<id>.responsePrefix

Aniqlash tartibi (eng aniq ustun):

1. `channels.<channel>`.accounts.<id>.responsePrefix
2. `channels.<channel>`.responsePrefix\`
3. `messages.responsePrefix`

Semantika:

- `undefined` keyingi darajaga o‘tadi.
- `""` prefiksni aniq o‘chiradi va kaskadni to‘xtatadi.
- `"auto"` marshrutlangan agent uchun `[{identity.name}]` ni hosil qiladi.

Override’lar barcha kanallarga, jumladan kengaytmalarga ham, va har bir chiqish javobi turiga qo‘llanadi.

Agar `messages.responsePrefix` o‘rnatilmagan bo‘lsa, sukut bo‘yicha prefiks qo‘llanmaydi. WhatsApp self-chat
javoblari istisno hisoblanadi: ular o‘rnatilganda `[{identity.name}]` ga, aks holda `[openclaw]` ga sukut qiladi, shuning uchun bir telefon ichidagi suhbatlar o‘qilishi oson bo‘lib qoladi.
Marshrutlangan agent uchun `[{identity.name}]` ni hosil qilish uchun uni `"auto"` ga o‘rnating (o‘rnatilganda).

#### Shablon o‘zgaruvchilari

`responsePrefix` satri dinamik ravishda yechiladigan shablon o‘zgaruvchilarini o‘z ichiga olishi mumkin:

| O‘zgaruvchi       | Tavsif                      | Misol                                      |
| ----------------- | --------------------------- | ------------------------------------------ |
| `{model}`         | Qisqa model nomi            | `claude-opus-4-6`, `gpt-4o`                |
| `{modelFull}`     | To‘liq model identifikatori | `anthropic/claude-opus-4-6`                |
| `{provider}`      | Provayder nomi              | `anthropic`, `openai`                      |
| `{thinkingLevel}` | Current thinking level      | `high`, `low`, `off`                       |
| `{identity.name}` | Agent identity name         | (same as `"auto"` mode) |

Variables are case-insensitive (`{MODEL}` = `{model}`). `{think}` is an alias for `{thinkingLevel}`.
Unresolved variables remain as literal text.

```json5
{
  messages: {
    responsePrefix: "[{model} | think:{thinkingLevel}]",
  },
}
```

Example output: `[claude-opus-4-6 | think:high] Here's my response...`

WhatsApp inbound prefix is configured via `channels.whatsapp.messagePrefix` (deprecated:
`messages.messagePrefix`). Default stays **unchanged**: `"[openclaw]"` when
`channels.whatsapp.allowFrom` is empty, otherwise `""` (no prefix). When using
`"[openclaw]"`, OpenClaw will instead use `[{identity.name}]` when the routed
agent has `identity.name` set.

`ackReaction` sends a best-effort emoji reaction to acknowledge inbound messages
on channels that support reactions (Slack/Discord/Telegram/Google Chat). Defaults to the
active agent’s `identity.emoji` when set, otherwise `"👀"`. Set it to `""` to disable.

`ackReactionScope` controls when reactions fire:

- `group-mentions` (default): only when a group/room requires mentions **and** the bot was mentioned
- `group-all`: all group/room messages
- `direct`: direct messages only
- `all`: all messages

`removeAckAfterReply` removes the bot’s ack reaction after a reply is sent
(Slack/Discord/Telegram/Google Chat only). Default: `false`.

#### `messages.tts`

Enable text-to-speech for outbound replies. When on, OpenClaw generates audio
using ElevenLabs or OpenAI and attaches it to responses. Telegram uses Opus
voice notes; other channels send MP3 audio.

```json5
{
  messages: {
    tts: {
      auto: "always", // off | always | inbound | tagged
      mode: "final", // final | all (include tool/block replies)
      provider: "elevenlabs",
      summaryModel: "openai/gpt-4.1-mini",
      modelOverrides: {
        enabled: true,
      },
      maxTextLength: 4000,
      timeoutMs: 30000,
      prefsPath: "~/.openclaw/settings/tts.json",
      elevenlabs: {
        apiKey: "elevenlabs_api_key",
        baseUrl: "https://api.elevenlabs.io",
        voiceId: "voice_id",
        modelId: "eleven_multilingual_v2",
        seed: 42,
        applyTextNormalization: "auto",
        languageCode: "en",
        voiceSettings: {
          stability: 0.5,
          similarityBoost: 0.75,
          style: 0.0,
          useSpeakerBoost: true,
          speed: 1.0,
        },
      },
      openai: {
        apiKey: "openai_api_key",
        model: "gpt-4o-mini-tts",
        voice: "alloy",
      },
    },
  },
}
```

Notes:

- `messages.tts.auto` controls auto‑TTS (`off`, `always`, `inbound`, `tagged`).
- `/tts off|always|inbound|tagged` sets the per‑session auto mode (overrides config).
- `messages.tts.enabled` is legacy; doctor migrates it to `messages.tts.auto`.
- `prefsPath` stores local overrides (provider/limit/summarize).
- `maxTextLength` is a hard cap for TTS input; summaries are truncated to fit.
- `summaryModel` overrides `agents.defaults.model.primary` for auto-summary.
  - Accepts `provider/model` or an alias from `agents.defaults.models`.
- `modelOverrides` enables model-driven overrides like `[[tts:...]]` tags (on by default).
- `/tts limit` and `/tts summary` control per-user summarization settings.
- `apiKey` values fall back to `ELEVENLABS_API_KEY`/`XI_API_KEY` and `OPENAI_API_KEY`.
- `elevenlabs.baseUrl` overrides the ElevenLabs API base URL.
- `elevenlabs.voiceSettings` supports `stability`/`similarityBoost`/`style` (0..1),
  `useSpeakerBoost`, and `speed` (0.5..2.0).

### `talk`

Defaults for Talk mode (macOS/iOS/Android). Voice IDs fall back to `ELEVENLABS_VOICE_ID` or `SAG_VOICE_ID` when unset.
`apiKey` falls back to `ELEVENLABS_API_KEY` (or the gateway’s shell profile) when unset.
`voiceAliases` lets Talk directives use friendly names (e.g. `"voice":"Clawd"`).

```json5
{
  talk: {
    voiceId: "elevenlabs_voice_id",
    voiceAliases: {
      Clawd: "EXAVITQu4vr4xnSDxMaL",
      Roger: "CwhRBWXzGAHq8TQ4Fs17",
    },
    modelId: "eleven_v3",
    outputFormat: "mp3_44100_128",
    apiKey: "elevenlabs_api_key",
    interruptOnSpeech: true,
  },
}
```

### `agents.defaults`

Controls the embedded agent runtime (model/thinking/verbose/timeouts).
`agents.defaults.models` sozlangan model katalogini belgilaydi (va `/model` uchun ruxsat etilganlar roʻyxati sifatida ishlaydi).
`agents.defaults.model.primary` standart modelni belgilaydi; `agents.defaults.model.fallbacks` esa global zaxira variantlardir.
`agents.defaults.imageModel` ixtiyoriy va **faqat asosiy model rasm kiritishni qoʻllab-quvvatlamaganda ishlatiladi**.
Each `agents.defaults.models` entry can include:

- `alias` (ixtiyoriy model qisqartmasi, masalan `/opus`).
- `params` (ixtiyoriy provayderga xos API parametrlari, model soʻroviga uzatiladi).

`params` oqim (streaming) ishga tushirishlarda ham qoʻllanadi (ichki agent + kompaksiyalash). Hozirda qoʻllab-quvvatlanadigan kalitlar: `temperature`, `maxTokens`. Bular chaqirish vaqtidagi opsiyalar bilan birlashtiriladi; chaqiruvchi tomonidan berilgan qiymatlar ustun keladi. `temperature` — ilgʻor sozlama; modelning standartlarini bilmasangiz va oʻzgartirish zarur boʻlmasa, bo‘sh qoldiring.

Misol:

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-sonnet-4-5-20250929": {
          params: { temperature: 0.6 },
        },
        "openai/gpt-5.2": {
          params: { maxTokens: 8192 },
        },
      },
    },
  },
}
```

Z.AI GLM-4.x modellari quyidagilar qilinmaguncha avtomatik ravishda thinking rejimini yoqadi:

- `--thinking off` ni sozlang, yoki
- define `agents.defaults.models["zai/<model>"].params.thinking` yourself.

OpenClaw shuningdek bir nechta ichki alias qisqartmalarni ham taqdim etadi. Defaults only apply when the model
is already present in `agents.defaults.models`:

- `opus` -> `anthropic/claude-opus-4-6`
- `sonnet` -> `anthropic/claude-sonnet-4-5`
- `gpt` -> `openai/gpt-5.2`
- `gpt-mini` -> `openai/gpt-5-mini`
- `gemini` -> `google/gemini-3-pro-preview`
- `gemini-flash` -> `google/gemini-3-flash-preview`

Agar siz bir xil alias nomini (katta-kichik harfga sezgir emas) oʻzingiz sozlasangiz, sizning qiymatingiz ustun keladi (standartlar hech qachon ustidan yozmaydi).

Misol: Opus 4.6 asosiy, MiniMax M2.1 zaxira (host qilingan MiniMax):

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "opus" },
        "minimax/MiniMax-M2.1": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["minimax/MiniMax-M2.1"],
      },
    },
  },
}
```

MiniMax autentifikatsiyasi: `MINIMAX_API_KEY` ni (env) sozlang yoki `models.providers.minimax` ni konfiguratsiya qiling.

#### `agents.defaults.cliBackends` (CLI zaxirasi)

Matnli zaxira ishga tushirishlar uchun ixtiyoriy CLI backendlar (asbob chaqiruvlarisiz). Bular API provayderlari ishlamay qolganda
zaxira yoʻli sifatida foydalidir. Fayl yoʻllarini qabul qiladigan `imageArg` ni sozlaganingizda rasmni uzatish qoʻllab-quvvatlanadi.

Eslatmalar:

- CLI backendlar **matn-markazli**; asboblar har doim o‘chirilgan.
- `sessionArg` sozlanganda sessiyalar qoʻllab-quvvatlanadi; sessiya IDlari har bir backend boʻyicha saqlanadi.
- `claude-cli` uchun standartlar oldindan bogʻlangan. Agar PATH minimal boʻlsa buyruq yoʻlini almashtiring
  (launchd/systemd).

Misol:

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
          modelArg: "--model",
          sessionArg: "--session",
          sessionMode: "existing",
          systemPromptArg: "--system",
          systemPromptWhen: "first",
          imageArg: "--image",
          imageMode: "repeat",
        },
      },
    },
  },
}
```

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "Opus" },
        "anthropic/claude-sonnet-4-1": { alias: "Sonnet" },
        "openrouter/deepseek/deepseek-r1:free": {},
        "zai/glm-4.7": {
          alias: "GLM",
          params: {
            thinking: {
              type: "enabled",
              clear_thinking: false,
            },
          },
        },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: [
          "openrouter/deepseek/deepseek-r1:free",
          "openrouter/meta-llama/llama-3.3-70b-instruct:free",
        ],
      },
      imageModel: {
        primary: "openrouter/qwen/qwen-2.5-vl-72b-instruct:free",
        fallbacks: ["openrouter/google/gemini-2.0-flash-vision:free"],
      },
      thinkingDefault: "low",
      verboseDefault: "off",
      elevatedDefault: "on",
      timeoutSeconds: 600,
      mediaMaxMb: 5,
      heartbeat: {
        every: "30m",
        target: "last",
      },
      maxConcurrent: 3,
      subagents: {
        model: "minimax/MiniMax-M2.1",
        maxConcurrent: 1,
        archiveAfterMinutes: 60,
      },
      exec: {
        backgroundMs: 10000,
        timeoutSec: 1800,
        cleanupMs: 1800000,
      },
      contextTokens: 200000,
    },
  },
}
```

#### `agents.defaults.contextPruning` (asbob natijalarini qisqartirish)

`agents.defaults.contextPruning` soʻrov LLM ga yuborilishidan oldin xotiradagi kontekstdan **eski asbob natijalarini** qisqartiradi.
U diskdagi sessiya tarixini o‘zgartirmaydi (`*.jsonl` to‘liq saqlanadi).

Bu vaqt o‘tishi bilan katta asbob chiqishlarini to‘playdigan sergap agentlar uchun token sarfini kamaytirishga mo‘ljallangan.

Yuqori daraja:

- Hech qachon foydalanuvchi/assistant xabarlariga tegmaydi.
- Oxirgi `keepLastAssistants` ta assistant xabarlarini himoya qiladi (shu nuqtadan keyin hech qanday asbob natijalari qisqartirilmaydi).
- Boshlang‘ich prefiksni himoya qiladi (birinchi foydalanuvchi xabaridan oldin hech narsa qisqartirilmaydi).
- Rejimlar:
  - `adaptive`: taxminiy kontekst nisbati `softTrimRatio` dan oshganda haddan tashqari katta asbob natijalarini yumshoq qisqartiradi (boshi/oxirini qoldiradi).
    So‘ng, taxminiy kontekst nisbati `hardClearRatio` dan oshganda **va** qisqartiriladigan asbob-natija hajmi yetarli bo‘lsa (`minPrunableToolChars`), eng eski mos asbob natijalarini qat’iy tozalaydi.
  - `aggressive`: always replaces eligible tool results before the cutoff with the `hardClear.placeholder` (no ratio checks).

Soft vs hard pruning (what changes in the context sent to the LLM):

- **Soft-trim**: only for _oversized_ tool results. Keeps the beginning + end and inserts `...` in the middle.
  - Before: `toolResult("…very long output…")`
  - After: `toolResult("HEAD…\n...\n…TAIL\n\n[Tool result trimmed: …]")`
- **Hard-clear**: replaces the entire tool result with the placeholder.
  - Before: `toolResult("…very long output…")`
  - After: `toolResult("[Old tool result content cleared]")`

Notes / current limitations:

- Tool results containing **image blocks are skipped** (never trimmed/cleared) right now.
- The estimated “context ratio” is based on **characters** (approximate), not exact tokens.
- If the session doesn’t contain at least `keepLastAssistants` assistant messages yet, pruning is skipped.
- In `aggressive` mode, `hardClear.enabled` is ignored (eligible tool results are always replaced with `hardClear.placeholder`).

Default (adaptive):

```json5
{
  agents: { defaults: { contextPruning: { mode: "adaptive" } } },
}
```

To disable:

```json5
{
  agents: { defaults: { contextPruning: { mode: "off" } } },
}
```

Defaults (when `mode` is `"adaptive"` or `"aggressive"`):

- `keepLastAssistants`: `3`
- `softTrimRatio`: `0.3` (adaptive only)
- `hardClearRatio`: `0.5` (adaptive only)
- `minPrunableToolChars`: `50000` (adaptive only)
- `softTrim`: `{ maxChars: 4000, headChars: 1500, tailChars: 1500 }` (adaptive only)
- `hardClear`: `{ enabled: true, placeholder: "[Old tool result content cleared]" }`

Example (aggressive, minimal):

```json5
{
  agents: { defaults: { contextPruning: { mode: "aggressive" } } },
}
```

Example (adaptive tuned):

```json5
{
  agents: {
    defaults: {
      contextPruning: {
        mode: "adaptive",
        keepLastAssistants: 3,
        softTrimRatio: 0.3,
        hardClearRatio: 0.5,
        minPrunableToolChars: 50000,
        softTrim: { maxChars: 4000, headChars: 1500, tailChars: 1500 },
        hardClear: { enabled: true, placeholder: "[Old tool result content cleared]" },
        // Optional: restrict pruning to specific tools (deny wins; supports "*" wildcards)
        tools: { deny: ["browser", "canvas"] },
      },
    },
  },
}
```

See [/concepts/session-pruning](/concepts/session-pruning) for behavior details.

#### `agents.defaults.compaction` (reserve headroom + memory flush)

`agents.defaults.compaction.mode` selects the compaction summarization strategy. Defaults to `default`; set `safeguard` to enable chunked summarization for very long histories. See [/concepts/compaction](/concepts/compaction).

`agents.defaults.compaction.reserveTokensFloor` enforces a minimum `reserveTokens`
value for Pi compaction (default: `20000`). Set it to `0` to disable the floor.

`agents.defaults.compaction.memoryFlush` runs a **silent** agentic turn before
auto-compaction, instructing the model to store durable memories on disk (e.g.
`memory/YYYY-MM-DD.md`). It triggers when the session token estimate crosses a
soft threshold below the compaction limit.

Legacy defaults:

- `memoryFlush.enabled`: `true`
- `memoryFlush.softThresholdTokens`: `4000`
- `memoryFlush.prompt` / `memoryFlush.systemPrompt`: built-in defaults with `NO_REPLY`
- Note: memory flush is skipped when the session workspace is read-only
  (`agents.defaults.sandbox.workspaceAccess: "ro"` or `"none"`).

Example (tuned):

```json5
{
  agents: {
    defaults: {
      compaction: {
        mode: "safeguard",
        reserveTokensFloor: 24000,
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 6000,
          systemPrompt: "Session nearing compaction. Store durable memories now.",
          prompt: "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store.",
        },
      },
    },
  },
}
```

Block streaming:

- `agents.defaults.blockStreamingDefault`: `"on"`/`"off"` (default off).

- Channel overrides: `*.blockStreaming` (and per-account variants) to force block streaming on/off.
  Non-Telegram channels require an explicit `*.blockStreaming: true` to enable block replies.

- `agents.defaults.blockStreamingBreak`: `"text_end"` or `"message_end"` (default: text_end).

- `agents.defaults.blockStreamingChunk`: soft chunking for streamed blocks. Defaults to
  800–1200 chars, prefers paragraph breaks (`\n\n`), then newlines, then sentences.
  Example:

  ```json5
  {
    agents: { defaults: { blockStreamingChunk: { minChars: 800, maxChars: 1200 } } },
  }
  ```

- `agents.defaults.blockStreamingCoalesce`: merge streamed blocks before sending.
  Defaults to `{ idleMs: 1000 }` and inherits `minChars` from `blockStreamingChunk`
  with `maxChars` capped to the channel text limit. Signal/Slack/Discord/Google Chat default
  to `minChars: 1500` unless overridden.
  Channel overrides: `channels.whatsapp.blockStreamingCoalesce`, `channels.telegram.blockStreamingCoalesce`,
  `channels.discord.blockStreamingCoalesce`, `channels.slack.blockStreamingCoalesce`, `channels.mattermost.blockStreamingCoalesce`,
  `channels.signal.blockStreamingCoalesce`, `channels.imessage.blockStreamingCoalesce`, `channels.msteams.blockStreamingCoalesce`,
  `channels.googlechat.blockStreamingCoalesce`
  (and per-account variants).

- `agents.defaults.humanDelay`: randomized pause between **block replies** after the first.
  Modes: `off` (default), `natural` (800–2500ms), `custom` (use `minMs`/`maxMs`).
  Per-agent override: `agents.list[].humanDelay`.
  Example:

  ```json5
  {
    agents: { defaults: { humanDelay: { mode: "natural" } } },
  }
  ```

  See [/concepts/streaming](/concepts/streaming) for behavior + chunking details.

Typing indicators:

- `agents.defaults.typingMode`: `"never" | "instant" | "thinking" | "message"`. Defaults to
  `instant` for direct chats / mentions and `message` for unmentioned group chats.
- `session.typingMode`: per-session override for the mode.
- `agents.defaults.typingIntervalSeconds`: how often the typing signal is refreshed (default: 6s).
- `session.typingIntervalSeconds`: per-session override for the refresh interval.
  See [/concepts/typing-indicators](/concepts/typing-indicators) for behavior details.

`agents.defaults.model.primary` should be set as `provider/model` (e.g. `anthropic/claude-opus-4-6`).
Aliases come from `agents.defaults.models.*.alias` (e.g. `Opus`).
If you omit the provider, OpenClaw currently assumes `anthropic` as a temporary
deprecation fallback.
Z.AI models are available as `zai/<model>` (e.g. `zai/glm-4.7`) and require
`ZAI_API_KEY` (or legacy `Z_AI_API_KEY`) in the environment.

`agents.defaults.heartbeat` configures periodic heartbeat runs:

- `every`: duration string (`ms`, `s`, `m`, `h`); default unit minutes. Default:
  `30m`. Set `0m` to disable.
- `model`: optional override model for heartbeat runs (`provider/model`).
- `includeReasoning`: when `true`, heartbeats will also deliver the separate `Reasoning:` message when available (same shape as `/reasoning on`). Default: `false`.
- `session`: optional session key to control which session the heartbeat runs in. Default: `main`.
- `to`: optional recipient override (channel-specific id, e.g. E.164 for WhatsApp, chat id for Telegram).
- `target`: optional delivery channel (`last`, `whatsapp`, `telegram`, `discord`, `slack`, `msteams`, `signal`, `imessage`, `none`). Default: `last`.
- `prompt`: optional override for the heartbeat body (default: `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`). Overrides are sent verbatim; include a `Read HEARTBEAT.md` line if you still want the file read.
- `ackMaxChars`: max chars allowed after `HEARTBEAT_OK` before delivery (default: 300).

Per-agent heartbeats:

- Set `agents.list[].heartbeat` to enable or override heartbeat settings for a specific agent.
- If any agent entry defines `heartbeat`, **only those agents** run heartbeats; defaults
  become the shared baseline for those agents.

Heartbeats run full agent turns. Shorter intervals burn more tokens; be mindful
of `every`, keep `HEARTBEAT.md` tiny, and/or choose a cheaper `model`.

`tools.exec` configures background exec defaults:

- `backgroundMs`: time before auto-background (ms, default 10000)
- `timeoutSec`: auto-kill after this runtime (seconds, default 1800)
- `cleanupMs`: how long to keep finished sessions in memory (ms, default 1800000)
- `notifyOnExit`: enqueue a system event + request heartbeat when backgrounded exec exits (default true)
- `applyPatch.enabled`: enable experimental `apply_patch` (OpenAI/OpenAI Codex only; default false)
- `applyPatch.allowModels`: optional allowlist of model ids (e.g. `gpt-5.2` or `openai/gpt-5.2`)
  Note: `applyPatch` is only under `tools.exec`.

`tools.web` configures web search + fetch tools:

- `tools.web.search.enabled` (default: true when key is present)
- `tools.web.search.apiKey` (recommended: set via `openclaw configure --section web`, or use `BRAVE_API_KEY` env var)
- `tools.web.search.maxResults` (1–10, default 5)
- `tools.web.search.timeoutSeconds` (default 30)
- `tools.web.search.cacheTtlMinutes` (default 15)
- `tools.web.fetch.enabled` (default true)
- `tools.web.fetch.maxChars` (standart 50000)
- `tools.web.fetch.maxCharsCap` (default 50000; clamps maxChars from config/tool calls)
- `tools.web.fetch.timeoutSeconds` (default 30)
- `tools.web.fetch.cacheTtlMinutes` (default 15)
- `tools.web.fetch.userAgent` (ixtiyoriy almashtirish)
- `tools.web.fetch.readability` (default true; disable to use basic HTML cleanup only)
- `tools.web.fetch.firecrawl.enabled` (default true when an API key is set)
- `tools.web.fetch.firecrawl.apiKey` (optional; defaults to `FIRECRAWL_API_KEY`)
- `tools.web.fetch.firecrawl.baseUrl` (default [https://api.firecrawl.dev](https://api.firecrawl.dev))
- `tools.web.fetch.firecrawl.onlyMainContent` (default true)
- `tools.web.fetch.firecrawl.maxAgeMs` (optional)
- `tools.web.fetch.firecrawl.timeoutSeconds` (optional)

`tools.media` configures inbound media understanding (image/audio/video):

- `tools.media.models`: shared model list (capability-tagged; used after per-cap lists).
- `tools.media.concurrency`: max concurrent capability runs (default 2).
- `tools.media.image` / `tools.media.audio` / `tools.media.video`:
  - `enabled`: opt-out switch (default true when models are configured).
  - `prompt`: optional prompt override (image/video append a `maxChars` hint automatically).
  - `maxChars`: max output characters (default 500 for image/video; unset for audio).
  - `maxBytes`: max media size to send (defaults: image 10MB, audio 20MB, video 50MB).
  - `timeoutSeconds`: request timeout (defaults: image 60s, audio 60s, video 120s).
  - `language`: optional audio hint.
  - `attachments`: attachment policy (`mode`, `maxAttachments`, `prefer`).
  - `scope`: optional gating (first match wins) with `match.channel`, `match.chatType`, or `match.keyPrefix`.
  - `models`: ordered list of model entries; failures or oversize media fall back to the next entry.
- Each `models[]` entry:
  - Provider entry (`type: "provider"` or omitted):
    - `provider`: API provider id (`openai`, `anthropic`, `google`/`gemini`, `groq`, etc).
    - `model`: model id override (required for image; defaults to `gpt-4o-mini-transcribe`/`whisper-large-v3-turbo` for audio providers, and `gemini-3-flash-preview` for video).
    - `profile` / `preferredProfile`: auth profile selection.
  - CLI entry (`type: "cli"`):
    - `command`: executable to run.
    - `args`: templated args (supports `{{MediaPath}}`, `{{Prompt}}`, `{{MaxChars}}`, etc).
  - `capabilities`: optional list (`image`, `audio`, `video`) to gate a shared entry. Defaults when omitted: `openai`/`anthropic`/`minimax` → image, `google` → image+audio+video, `groq` → audio.
  - `prompt`, `maxChars`, `maxBytes`, `timeoutSeconds`, `language` can be overridden per entry.

If no models are configured (or `enabled: false`), understanding is skipped; the model still receives the original attachments.

Provider auth follows the standard model auth order (auth profiles, env vars like `OPENAI_API_KEY`/`GROQ_API_KEY`/`GEMINI_API_KEY`, or `models.providers.*.apiKey`).

Example:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        maxBytes: 20971520,
        scope: {
          default: "deny",
          rules: [{ action: "allow", match: { chatType: "direct" } }],
        },
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          { type: "cli", command: "whisper", args: ["--model", "base", "{{MediaPath}}"] },
        ],
      },
      video: {
        enabled: true,
        maxBytes: 52428800,
        models: [{ provider: "google", model: "gemini-3-flash-preview" }],
      },
    },
  },
}
```

`agents.defaults.subagents` sub-agent standartlarini sozlaydi:

- `model`: default model for spawned sub-agents (string or `{ primary, fallbacks }`). If omitted, sub-agents inherit the caller’s model unless overridden per agent or per call.
- `maxConcurrent`: max concurrent sub-agent runs (default 1)
- `archiveAfterMinutes`: N daqiqadan so‘ng sub-agent sessiyalarini avtomatik arxivlash (standart 60; o‘chirish uchun `0` qo‘ying)
- Har bir sub-agent uchun asbob siyosati: `tools.subagents.tools.allow` / `tools.subagents.tools.deny` (deny ustun)

`tools.profile` `tools.allow`/`tools.deny` dan oldin **asosiy ruxsat etilgan asboblar ro‘yxatini** belgilaydi:

- `minimal`: faqat `session_status`
- `coding`: `group:fs`, `group:runtime`, `group:sessions`, `group:memory`, `image`
- `messaging`: `group:messaging`, `sessions_list`, `sessions_history`, `sessions_send`, `session_status`
- `full`: cheklov yo‘q (o‘rnatilmagan bilan bir xil)

Per-agent override: `agents.list[].tools.profile`.

Misol (standart bo‘yicha faqat xabar almashish, Slack + Discord asboblariga ham ruxsat beriladi):

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

`tools.byProvider` lets you **further restrict** tools for specific providers (or a single `provider/model`).
Per-agent override: `agents.list[].tools.byProvider`.

Order: base profile → provider profile → allow/deny policies.
Provider keys accept either `provider` (e.g. `google-antigravity`) or `provider/model`
(e.g. `openai/gpt-5.2`).

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

Example (provider/model-specific allowlist):

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

`tools.allow` / `tools.deny` configure a global tool allow/deny policy (deny wins).
Matching is case-insensitive and supports `*` wildcards (`"*"` means all tools).
This is applied even when the Docker sandbox is **off**.

Example (disable browser/canvas everywhere):

```json5
{
  tools: { deny: ["browser", "canvas"] },
}
```

Tool groups (shorthands) work in **global** and **per-agent** tool policies:

- `group:runtime`: `exec`, `bash`, `process`
- `group:fs`: `read`, `write`, `edit`, `apply_patch`
- `group:sessions`: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
- `group:memory`: `memory_search`, `memory_get`
- `group:web`: `web_search`, `web_fetch`
- `group:ui`: `browser`, `canvas`
- `group:automation`: `cron`, `gateway`
- `group:messaging`: `message`
- `group:nodes`: `nodes`
- `group:openclaw`: all built-in OpenClaw tools (excludes provider plugins)

`tools.elevated` controls elevated (host) exec access:

- `enabled`: allow elevated mode (default true)
- `allowFrom`: per-channel allowlists (empty = disabled)
  - `whatsapp`: E.164 numbers
  - `telegram`: chat ids or usernames
  - `discord`: user ids or usernames (falls back to `channels.discord.dm.allowFrom` if omitted)
  - `signal`: E.164 numbers
  - `imessage`: handles/chat ids
  - `webchat`: session ids or usernames

Example:

```json5
{
  tools: {
    elevated: {
      enabled: true,
      allowFrom: {
        whatsapp: ["+15555550123"],
        discord: ["steipete", "1234567890123"],
      },
    },
  },
}
```

Per-agent override (further restrict):

```json5
{
  agents: {
    list: [
      {
        id: "family",
        tools: {
          elevated: { enabled: false },
        },
      },
    ],
  },
}
```

Notes:

- `tools.elevated` is the global baseline. `agents.list[].tools.elevated` can only further restrict (both must allow).
- `/elevated on|off|ask|full` stores state per session key; inline directives apply to a single message.
- Elevated `exec` runs on the host and bypasses sandboxing.
- Tool policy still applies; if `exec` is denied, elevated cannot be used.

`agents.defaults.maxConcurrent` sets the maximum number of embedded agent runs that can
execute in parallel across sessions. Each session is still serialized (one run
per session key at a time). Default: 1.

### `agents.defaults.sandbox`

Optional **Docker sandboxing** for the embedded agent. Intended for non-main
sessions so they cannot access your host system.

Details: [Sandboxing](/gateway/sandboxing)

Defaults (if enabled):

- scope: `"agent"` (one container + workspace per agent)
- Debian bookworm-slim based image
- agent workspace access: `workspaceAccess: "none"` (default)
  - `"none"`: use a per-scope sandbox workspace under `~/.openclaw/sandboxes`
- `"ro"`: keep the sandbox workspace at `/workspace`, and mount the agent workspace read-only at `/agent` (disables `write`/`edit`/`apply_patch`)
  - `"rw"`: mount the agent workspace read/write at `/workspace`
- auto-prune: idle > 24h OR age > 7d
- tool policy: allow only `exec`, `process`, `read`, `write`, `edit`, `apply_patch`, `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status` (deny wins)
  - configure via `tools.sandbox.tools`, override per-agent via `agents.list[].tools.sandbox.tools`
  - tool group shorthands supported in sandbox policy: `group:runtime`, `group:fs`, `group:sessions`, `group:memory` (see [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated#tool-groups-shorthands))
- optional sandboxed browser (Chromium + CDP, noVNC observer)
- hardening knobs: `network`, `user`, `pidsLimit`, `memory`, `cpus`, `ulimits`, `seccompProfile`, `apparmorProfile`

Warning: `scope: "shared"` means a shared container and shared workspace. No
cross-session isolation. Use `scope: "session"` for per-session isolation.

Legacy: `perSession` is still supported (`true` → `scope: "session"`,
`false` → `scope: "shared"`).

`setupCommand` runs **once** after the container is created (inside the container via `sh -lc`).
For package installs, ensure network egress, a writable root FS, and a root user.

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // off | non-main | all
        scope: "agent", // session | agent | shared (agent is default)
        workspaceAccess: "none", // none | ro | rw
        workspaceRoot: "~/.openclaw/sandboxes",
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          containerPrefix: "openclaw-sbx-",
          workdir: "/workspace",
          readOnlyRoot: true,
          tmpfs: ["/tmp", "/var/tmp", "/run"],
          network: "none",
          user: "1000:1000",
          capDrop: ["ALL"],
          env: { LANG: "C.UTF-8" },
          setupCommand: "apt-get update && apt-get install -y git curl jq",
          // Per-agent override (multi-agent): agents.list[].sandbox.docker.*
          pidsLimit: 256,
          memory: "1g",
          memorySwap: "2g",
          cpus: 1,
          ulimits: {
            nofile: { soft: 1024, hard: 2048 },
            nproc: 256,
          },
          seccompProfile: "/path/to/seccomp.json",
          apparmorProfile: "openclaw-sandbox",
          dns: ["1.1.1.1", "8.8.8.8"],
          extraHosts: ["internal.service:10.0.0.5"],
          binds: ["/var/run/docker.sock:/var/run/docker.sock", "/home/user/source:/source:rw"],
        },
        browser: {
          enabled: false,
          image: "openclaw-sandbox-browser:bookworm-slim",
          containerPrefix: "openclaw-sbx-browser-",
          cdpPort: 9222,
          vncPort: 5900,
          noVncPort: 6080,
          headless: false,
          enableNoVnc: true,
          allowHostControl: false,
          allowedControlUrls: ["http://10.0.0.42:18791"],
          allowedControlHosts: ["browser.lab.local", "10.0.0.42"],
          allowedControlPorts: [18791],
          autoStart: true,
          autoStartTimeoutMs: 12000,
        },
        prune: {
          idleHours: 24, // 0 disables idle pruning
          maxAgeDays: 7, // 0 disables max-age pruning
        },
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        allow: [
          "exec",
          "process",
          "read",
          "write",
          "edit",
          "apply_patch",
          "sessions_list",
          "sessions_history",
          "sessions_send",
          "sessions_spawn",
          "session_status",
        ],
        deny: ["browser", "canvas", "nodes", "cron", "discord", "gateway"],
      },
    },
  },
}
```

Build the default sandbox image once with:

```bash
scripts/sandbox-setup.sh
```

Note: sandbox containers default to `network: "none"`; set `agents.defaults.sandbox.docker.network`
to `"bridge"` (or your custom network) if the agent needs outbound access.

Note: inbound attachments are staged into the active workspace at `media/inbound/*`. With `workspaceAccess: "rw"`, that means files are written into the agent workspace.

Note: `docker.binds` mounts additional host directories; global and per-agent binds are merged.

Build the optional browser image with:

```bash
scripts/sandbox-browser-setup.sh
```

When `agents.defaults.sandbox.browser.enabled=true`, the browser tool uses a sandboxed
Chromium instance (CDP). If noVNC is enabled (default when headless=false),
the noVNC URL is injected into the system prompt so the agent can reference it.
This does not require `browser.enabled` in the main config; the sandbox control
URL is injected per session.

`agents.defaults.sandbox.browser.allowHostControl` (default: false) allows
sandboxed sessions to explicitly target the **host** browser control server
via the browser tool (`target: "host"`). Agar qat’iy sandbox izolyatsiyasini xohlasangiz, buni o‘chiring.

Allowlists for remote control:

- `allowedControlUrls`: `target: "custom"` uchun ruxsat etilgan aniq boshqaruv URL’lari.
- `allowedControlHosts`: ruxsat etilgan xost nomlari (faqat hostname, port yo‘q).
- `allowedControlPorts`: ports permitted (defaults: http=80, https=443).
  Defaults: all allowlists are unset (no restriction). `allowHostControl` defaults to false.

### `models` (maxsus provayderlar + asosiy URL’lar)

OpenClaw uses the **pi-coding-agent** model catalog. Siz maxsus provayderlarni qo‘shishingiz mumkin
(LiteLLM, lokal OpenAI-mos serverlar, Anthropic proksilari va h.k.) by writing
`~/.openclaw/agents/<agentId>/agent/models.json` or by defining the same schema inside your
OpenClaw config under `models.providers`.
Har bir provayder bo‘yicha sharh + misollar: [/concepts/model-providers](/concepts/model-providers).

When `models.providers` is present, OpenClaw writes/merges a `models.json` into
`~/.openclaw/agents/<agentId>/agent/` on startup:

- default behavior: **merge** (keeps existing providers, overrides on name)
- set `models.mode: "replace"` to overwrite the file contents

Select the model via `agents.defaults.model.primary` (provider/model).

```json5
{
  agents: {
    defaults: {
      model: { primary: "custom-proxy/llama-3.1-8b" },
      models: {
        "custom-proxy/llama-3.1-8b": {},
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      "custom-proxy": {
        baseUrl: "http://localhost:4000/v1",
        apiKey: "LITELLM_KEY",
        api: "openai-completions",
        models: [
          {
            id: "llama-3.1-8b",
            name: "Llama 3.1 8B",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            maxTokens: 32000,
          },
        ],
      },
    },
  },
}
```

### OpenCode Zen (multi-model proxy)

OpenCode Zen — har bir model uchun alohida endpointlarga ega ko‘p-modelli shlyuz. OpenClaw uses
the built-in `opencode` provider from pi-ai; set `OPENCODE_API_KEY` (or
`OPENCODE_ZEN_API_KEY`) from [https://opencode.ai/auth](https://opencode.ai/auth).

Notes:

- Model refs use `opencode/<modelId>` (example: `opencode/claude-opus-4-6`).
- If you enable an allowlist via `agents.defaults.models`, add each model you plan to use.
- Qisqa yo‘l: `openclaw onboard --auth-choice opencode-zen`.

```json5
{
  agents: {
    defaults: {
      model: { primary: "opencode/claude-opus-4-6" },
      models: { "opencode/claude-opus-4-6": { alias: "Opus" } },
    },
  },
}
```

### Z.AI (GLM-4.7) — provider alias support

Z.AI modellari o‘rnatilgan `zai` provayderi orqali mavjud. Set `ZAI_API_KEY`
in your environment and reference the model by provider/model.

Shortcut: `openclaw onboard --auth-choice zai-api-key`.

```json5
{
  agents: {
    defaults: {
      model: { primary: "zai/glm-4.7" },
      models: { "zai/glm-4.7": {} },
    },
  },
}
```

Notes:

- `z.ai/*` and `z-ai/*` are accepted aliases and normalize to `zai/*`.
- If `ZAI_API_KEY` is missing, requests to `zai/*` will fail with an auth error at runtime.
- Example error: `No API key found for provider "zai".`
- Z.AI’s general API endpoint is `https://api.z.ai/api/paas/v4`. GLM coding
  requests use the dedicated Coding endpoint `https://api.z.ai/api/coding/paas/v4`.
  The built-in `zai` provider uses the Coding endpoint. If you need the general
  endpoint, define a custom provider in `models.providers` with the base URL
  override (see the custom providers section above).
- Use a fake placeholder in docs/configs; never commit real API keys.

### Moonshot AI (Kimi)

Use Moonshot's OpenAI-compatible endpoint:

```json5
{
  env: { MOONSHOT_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "moonshot/kimi-k2.5" },
      models: { "moonshot/kimi-k2.5": { alias: "Kimi K2.5" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "kimi-k2.5",
            name: "Kimi K2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Notes:

- Set `MOONSHOT_API_KEY` in the environment or use `openclaw onboard --auth-choice moonshot-api-key`.
- Model ref: `moonshot/kimi-k2.5`.
- For the China endpoint, either:
  - Run `openclaw onboard --auth-choice moonshot-api-key-cn` (wizard will set `https://api.moonshot.cn/v1`), or
  - Manually set `baseUrl: "https://api.moonshot.cn/v1"` in `models.providers.moonshot`.

### Kimi Coding

Use Moonshot AI's Kimi Coding endpoint (Anthropic-compatible, built-in provider):

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "kimi-coding/k2p5" },
      models: { "kimi-coding/k2p5": { alias: "Kimi K2.5" } },
    },
  },
}
```

Eslatmalar:

- `KIMI_API_KEY` ni muhitda o‘rnating yoki `openclaw onboard --auth-choice kimi-code-api-key` dan foydalaning.
- Model havolasi: `kimi-coding/k2p5`.

### Synthetic (Anthropic bilan mos)

Synthetic’ning Anthropic bilan mos endpointidan foydalaning:

```json5
{
  env: { SYNTHETIC_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.1" },
      models: { "synthetic/hf:MiniMaxAI/MiniMax-M2.1": { alias: "MiniMax M2.1" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "hf:MiniMaxAI/MiniMax-M2.1",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 192000,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

Eslatmalar:

- `SYNTHETIC_API_KEY` ni o‘rnating yoki `openclaw onboard --auth-choice synthetic-api-key` dan foydalaning.
- Model havolasi: `synthetic/hf:MiniMaxAI/MiniMax-M2.1`.
- Anthropic klienti `/v1` ni avtomatik qo‘shgani uchun Base URL da `/v1` bo‘lmasligi kerak.

### Mahalliy modellar (LM Studio) — tavsiya etilgan sozlama

Joriy mahalliy ko‘rsatmalar uchun [/gateway/local-models](/gateway/local-models) ga qarang. Qisqacha: jiddiy apparatda MiniMax M2.1 ni LM Studio Responses API orqali ishga tushiring; zaxira uchun hosted modellarni birlashtirilgan holda qoldiring.

### MiniMax M2.1

MiniMax M2.1 dan LM Studio siz to‘g‘ridan-to‘g‘ri foydalaning:

```json5
{
  agent: {
    model: { primary: "minimax/MiniMax-M2.1" },
    models: {
      "anthropic/claude-opus-4-6": { alias: "Opus" },
      "minimax/MiniMax-M2.1": { alias: "Minimax" },
    },
  },
  models: {
    mode: "merge",
    providers: {
      minimax: {
        baseUrl: "https://api.minimax.io/anthropic",
        apiKey: "${MINIMAX_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "MiniMax-M2.1",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            // Narxlash: aniq xarajat kuzatuvi kerak bo‘lsa, models.json da yangilang.
            cost: { input: 15, output: 60, cacheRead: 2, cacheWrite: 10 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Eslatmalar:

- `MINIMAX_API_KEY` muhit o‘zgaruvchisini o‘rnating yoki `openclaw onboard --auth-choice minimax-api` dan foydalaning.
- Mavjud model: `MiniMax-M2.1` (standart).
- Aniq xarajat kuzatuvi kerak bo‘lsa, `models.json` dagi narxlarni yangilang.

### Cerebras (GLM 4.6 / 4.7)

Cerebras’dan ularning OpenAI bilan mos endpointi orqali foydalaning:

```json5
{
  env: { CEREBRAS_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: {
        primary: "cerebras/zai-glm-4.7",
        fallbacks: ["cerebras/zai-glm-4.6"],
      },
      models: {
        "cerebras/zai-glm-4.7": { alias: "GLM 4.7 (Cerebras)" },
        "cerebras/zai-glm-4.6": { alias: "GLM 4.6 (Cerebras)" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      cerebras: {
        baseUrl: "https://api.cerebras.ai/v1",
        apiKey: "${CEREBRAS_API_KEY}",
        api: "openai-completions",
        models: [
          { id: "zai-glm-4.7", name: "GLM 4.7 (Cerebras)" },
          { id: "zai-glm-4.6", name: "GLM 4.6 (Cerebras)" },
        ],
      },
    },
  },
}
```

Eslatmalar:

- Cerebras uchun `cerebras/zai-glm-4.7` dan foydalaning; Z.AI to‘g‘ridan-to‘g‘ri uchun `zai/glm-4.7` dan foydalaning.
- `CEREBRAS_API_KEY` ni muhitda yoki konfiguratsiyada o‘rnating.

Eslatmalar:

- Qo‘llab-quvvatlanadigan APIlar: `openai-completions`, `openai-responses`, `anthropic-messages`,
  `google-generative-ai`
- Maxsus autentifikatsiya ehtiyojlari uchun `authHeader: true` + `headers` dan foydalaning.
- `models.json` ni boshqa joyda saqlamoqchi bo‘lsangiz, agent konfiguratsiyasi ildizini `OPENCLAW_AGENT_DIR` (yoki `PI_CODING_AGENT_DIR`) bilan almashtiring (standart: `~/.openclaw/agents/main/agent`).

### `session`

Sessiya doirasini, qayta tiklash siyosatini, qayta tiklash triggerlarini va sessiya saqlanadigan joyni boshqaradi.

```json5
50. `resetByType`: `direct`, `group` va `thread` uchun sessiya bo‘yicha alohida sozlamalar.
```

Maydonlar:

- `mainKey`: to‘g‘ridan-to‘g‘ri chat uchun bucket kaliti (standart: `"main"`). `agentId` ni o‘zgartirmasdan asosiy DM oqimini “qayta nomlash”ni xohlaganingizda foydali.
  - Sandbox eslatmasi: `agents.defaults.sandbox.mode: "non-main"` asosiy sessiyani aniqlash uchun ushbu kalitdan foydalanadi. `mainKey` ga mos kelmaydigan har qanday sessiya kaliti (guruhlar/kanallar) sandbox qilinadi.
- `dmScope`: DM sessiyalari qanday guruhlanishi (standart: `"main"`).
  - `main`: uzluksizlik uchun barcha DMlar asosiy sessiyani ulashadi.
  - `per-peer`: kanallar bo‘ylab jo‘natuvchi ID bo‘yicha DMlarni ajratadi.
  - `per-channel-peer`: kanal + jo‘natuvchi bo‘yicha DMlarni ajratadi (ko‘p foydalanuvchili inboxlar uchun tavsiya etiladi).
  - `per-account-channel-peer`: akkaunt + kanal + jo‘natuvchi bo‘yicha DMlarni ajratadi (ko‘p akkauntli inboxlar uchun tavsiya etiladi).
  - Xavfsiz DM rejimi (tavsiya etiladi): bir nechta odam botga DM yubora olganda (`session.dmScope: "per-channel-peer"`) ni o‘rnating (umumiy inboxlar, ko‘p kishilik allowlistlar yoki `dmPolicy: "open"`).
- `identityLinks`: `per-peer`, `per-channel-peer` yoki `per-account-channel-peer` ishlatilganda bir xil shaxs kanallar bo‘ylab bitta DM sessiyasini ulashishi uchun kanonik IDlarni provayder prefiksli peerlar bilan moslaydi.
  - Misol: `alice: ["telegram:123456789", "discord:987654321012345678"]`.
- `reset`: asosiy qayta tiklash siyosati. Standart bo‘yicha gateway xostidagi mahalliy vaqt bilan har kuni soat 4:00 da qayta tiklanadi.
  - `mode`: `daily` yoki `idle` (standart: `reset` mavjud bo‘lsa `daily`).
  - `atHour`: kunlik qayta tiklash chegarasi uchun mahalliy soat (0–23).
  - `idleMinutes`: daqiqalarda sirpanma bo‘sh (idle) oynasi. Agar daily + idle ikkalasi ham sozlangan bo‘lsa, qaysi biri birinchi tugasa, o‘sha g‘olib bo‘ladi.
- `resetByType`: per-session overrides for `direct`, `group`, and `thread`. Eski `dm` kaliti `direct` uchun alias sifatida qabul qilinadi.
  - Agar siz faqat eski `session.idleMinutes` ni hech qanday `reset`/`resetByType` siz sozlasangiz, OpenClaw orqaga moslik uchun faqat idle rejimida qoladi.
- `heartbeatIdleMinutes`: heartbeat tekshiruvlari uchun ixtiyoriy idle override (yoqilgan bo‘lsa, daily reset baribir qo‘llanadi).
- `agentToAgent.maxPingPongTurns`: so‘rovchi/maqsad o‘rtasidagi maksimal javob-ortga aylanishlari (0–5, standart 5).
- `sendPolicy.default`: hech bir qoida mos kelmaganda `allow` yoki `deny` zaxira xatti-harakati.
- `sendPolicy.rules[]`: `channel`, `chatType` (`direct|group|room`) yoki `keyPrefix` (masalan, `cron:`) bo‘yicha moslashtirish. Avval deny ustun; aks holda allow.

### `skills` (skills konfiguratsiyasi)

Bundled allowlist, o‘rnatish afzalliklari, qo‘shimcha skill papkalari va har bir skill uchun override’larni boshqaradi. **Bundled** skill’lar va `~/.openclaw/skills` ga qo‘llanadi (nom to‘qnashuvida workspace skill’lar ustun).

Maydonlar:

- `allowBundled`: faqat **bundled** skill’lar uchun ixtiyoriy allowlist. Agar sozlansa, faqat o‘sha bundled skill’largina yaroqli bo‘ladi (managed/workspace skill’lar ta’sirlanmaydi).
- `load.extraDirs`: skanerlash uchun qo‘shimcha skill kataloglari (eng past ustuvorlik).
- `install.preferBrew`: mavjud bo‘lsa brew o‘rnatuvchilarini afzal ko‘rish (standart: true).
- `install.nodeManager`: node o‘rnatuvchi afzalligi (`npm` | `pnpm` | `yarn`, standart: npm).
- \`entries.<skillKey>: har bir skill uchun konfiguratsiya override’lari.

Har bir skill maydonlari:

- `enabled`: hatto bundled/o‘rnatilgan bo‘lsa ham skill’ni o‘chirish uchun `false` ga qo‘ying.
- `env`: agent ishga tushirilishi uchun kiritiladigan muhit o‘zgaruvchilari (faqat allaqachon o‘rnatilmagan bo‘lsa).
- `apiKey`: asosiy env o‘zgaruvchini e’lon qiladigan skill’lar uchun ixtiyoriy qulaylik (masalan, `nano-banana-pro` → `GEMINI_API_KEY`).

Misol:

```json5
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills", "~/Projects/oss/some-skill-pack/skills"],
    },
    install: {
      preferBrew: true,
      nodeManager: "npm",
    },
    entries: {
      "nano-banana-pro": {
        apiKey: "GEMINI_KEY_HERE",
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

### `plugins` (kengaytmalar)

Plaginlarni aniqlash, allow/deny va har bir plagin uchun konfiguratsiyani boshqaradi. Plaginlar `~/.openclaw/extensions`, `<workspace>/.openclaw/extensions`, hamda `plugins.load.paths` dagi yozuvlardan yuklanadi. **Konfiguratsiya o‘zgarishlari gateway’ni qayta ishga tushirishni talab qiladi.**
To‘liq foydalanish uchun [/plugin](/tools/plugin) ga qarang.

Maydonlar:

- `enabled`: plaginlarni yuklash uchun bosh kalit (standart: true).
- `allow`: ixtiyoriy plagin id’lari allowlist’i; sozlansa, faqat ro‘yxatdagilar yuklanadi.
- `deny`: ixtiyoriy plagin id’lari denylist’i (deny ustun).
- `load.paths`: yuklash uchun qo‘shimcha plagin fayllari yoki kataloglari (mutlaq yoki `~`).
- \`entries.<pluginId>: har bir plagin uchun override’lar.
  - `enabled`: o‘chirish uchun `false` ga qo‘ying.
  - `config`: plaginga xos konfiguratsiya obyekti (agar berilgan bo‘lsa, plagin tomonidan tekshiriladi).

Misol:

```json5
{
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    load: {
      paths: ["~/Projects/oss/voice-call-extension"],
    },
    entries: {
      "voice-call": {
        enabled: true,
        config: {
          provider: "twilio",
        },
      },
    },
  },
}
```

### `browser` (openclaw tomonidan boshqariladigan brauzer)

OpenClaw openclaw uchun **maxsus, izolyatsiyalangan** Chrome/Brave/Edge/Chromium instansiyasini ishga tushirishi va kichik loopback boshqaruv xizmatini taqdim etishi mumkin.
Profillar `profiles.<name>
.cdpUrl` orqali **masofaviy** Chromium-asosli brauzerga ishora qilishi mumkin.Masofaviy profillar faqat ulanish (attach-only) rejimida (start/stop/reset o‘chirilgan). `browser.cdpUrl` eski yagona-profil konfiguratsiyalari uchun va faqat `cdpPort` ni sozlaydigan profillar uchun asosiy sxema/xost sifatida qoladi.

Standartlar:

enabled: `true`

- evaluateEnabled: `true` (`act:evaluate` va `wait --fn` ni o‘chirish uchun `false` ga qo‘ying)
- control service: faqat loopback (port `gateway.port` dan olinadi, standart `18791`)
- control service: loopback only (port derived from `gateway.port`, default `18791`)
- 1. CDP URL: `http://127.0.0.1:18792` (boshqaruv xizmati + 1 ta, eski yagona profil)
- 2. profil rangi: `#FF4500` (lobster-orange)
- 3. Eslatma: boshqaruv serveri ishlayotgan gateway tomonidan ishga tushiriladi (OpenClaw.app menyu paneli yoki `openclaw gateway`).
- 4. Avtomatik aniqlash tartibi: agar Chromium-ga asoslangan bo‘lsa — standart brauzer; aks holda Chrome → Brave → Edge → Chromium → Chrome Canary.

```json5
5. {
  browser: {
    enabled: true,
    evaluateEnabled: true,
    // cdpUrl: "http://127.0.0.1:18792", // eski yagona profil uchun override
    defaultProfile: "chrome",
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC" },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
    },
    color: "#FF4500",
    // Advanced:
    // headless: false,
    // noSandbox: false,
    // executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    // attachOnly: false, // masofaviy CDP ni localhost ga tunnellashda true qilib qo‘ying
  },
}
```

### 6. `ui` (Tashqi ko‘rinish)

7. Native ilovalar tomonidan UI chrome uchun ishlatiladigan ixtiyoriy aksent rangi (masalan, Talk Mode pufakchasi ranglanishi).

8. Agar o‘rnatilmagan bo‘lsa, mijozlar xira och-ko‘k rangga qaytadi.

```json5
9. {
  ui: {
    seamColor: "#FF4500", // hex (RRGGBB yoki #RRGGBB)
    // Ixtiyoriy: Control UI yordamchisi identifikatorini override qilish.
    // Agar o‘rnatilmagan bo‘lsa, Control UI faol agent identifikatoridan foydalanadi (config yoki IDENTITY.md).
    assistant: {
      name: "OpenClaw",
      avatar: "CB", // emoji, qisqa matn yoki rasm URL/data URI
    },
  },
}
```

### 10. `gateway` (Gateway server rejimi + bog‘lash)

11. Ushbu mashina Gateway’ni ishga tushirishi kerakmi yoki yo‘qligini aniq belgilash uchun `gateway.mode` dan foydalaning.

12. Standart qiymatlar:

- 13. mode: **o‘rnatilmagan** ("avtomatik ishga tushirmaslik" sifatida qabul qilinadi)
- 14. bind: `loopback`
- 15. port: `18789` (WS + HTTP uchun yagona port)

```json5
16. {
  gateway: {
    mode: "local", // yoki "remote"
    port: 18789, // WS + HTTP multipleks
    bind: "loopback",
    // controlUi: { enabled: true, basePath: "/openclaw" }
    // auth: { mode: "token", token: "your-token" } // token WS + Control UI kirishini cheklaydi
    // tailscale: { mode: "off" | "serve" | "funnel" }
  },
}
```

17. Control UI bazaviy yo‘li:

- 18. `gateway.controlUi.basePath` Control UI xizmat ko‘rsatiladigan URL prefiksini belgilaydi.
- 19. Misollar: `"/ui"`, `"/openclaw"`, `"/apps/openclaw"`.
- 20. Standart: ildiz (`/`) (o‘zgarmagan).
- 21. `gateway.controlUi.root` Control UI assetlari uchun fayl tizimi ildizini belgilaydi (standart: `dist/control-ui`).
- 22. `gateway.controlUi.allowInsecureAuth` qurilma identifikatori ko‘rsatilmaganida (odatda HTTP orqali) Control UI uchun faqat tokenli autentifikatsiyaga ruxsat beradi. 23. Standart: `false`. 24. HTTPS’ni afzal ko‘ring
      (Tailscale Serve) yoki `127.0.0.1`.
- 25. `gateway.controlUi.dangerouslyDisableDeviceAuth` Control UI uchun qurilma identifikatori tekshiruvlarini o‘chiradi (faqat token/parol). 26. Standart: `false`. 27. Faqat favqulodda holatlar uchun.

28. Tegishli hujjatlar:

- 29. [Control UI](/web/control-ui)
- 30. [Web overview](/web)
- 31. [Tailscale](/gateway/tailscale)
- 32. [Remote access](/gateway/remote)

33. Ishonchli proksilar:

- 34. `gateway.trustedProxies`: Gateway oldida TLS ni yakunlaydigan reverse proksi IP’lari ro‘yxati.
- 35. Ulanish ushbu IP’lardan biridan kelganda, OpenClaw mahalliy juftlash tekshiruvlari va HTTP autentifikatsiyasi/mahalliy tekshiruvlar uchun mijoz IP’sini aniqlashda `x-forwarded-for` (yoki `x-real-ip`) dan foydalanadi.
- 36. Faqat to‘liq nazoratingizdagi proksilarni kiriting va ular kiruvchi `x-forwarded-for` ni **ustiga yozishini** ta’minlang.

37. Eslatmalar:

- 38. `openclaw gateway` `gateway.mode` `local` ga o‘rnatilmagan bo‘lsa (yoki override flag bermasangiz) ishga tushishni rad etadi.
- 39. `gateway.port` WebSocket + HTTP (control UI, hooks, A2UI) uchun ishlatiladigan yagona multiplekslangan portni boshqaradi.
- 40. OpenAI Chat Completions endpointi: **standart holatda o‘chirilgan**; `gateway.http.endpoints.chatCompletions.enabled: true` bilan yoqing.
- 41. Ustuvorlik: `--port` > `OPENCLAW_GATEWAY_PORT` > `gateway.port` > standart `18789`.
- 42. Gateway autentifikatsiyasi standart holatda talab qilinadi (token/parol yoki Tailscale Serve identifikatori). 43. Loopback bo‘lmagan bind’lar umumiy token/parolni talab qiladi.
- 44. Onboarding ustasi standart holatda gateway tokenini yaratadi (hatto loopback’da ham).
- 45. `gateway.remote.token` **faqat** masofaviy CLI chaqiruvlari uchun; u mahalliy gateway autentifikatsiyasini yoqmaydi. 46. `gateway.token` e’tiborga olinmaydi.

47. Autentifikatsiya va Tailscale:

- 48. `gateway.auth.mode` handshake talablarini belgilaydi (`token` yoki `password`). 49. Agar o‘rnatilmagan bo‘lsa, token autentifikatsiyasi qabul qilinadi.
- 50. `gateway.auth.token` token autentifikatsiyasi uchun umumiy tokenni saqlaydi (bir xil mashinadagi CLI tomonidan ishlatiladi).
- When `gateway.auth.mode` is set, only that method is accepted (plus optional Tailscale headers).
- `gateway.auth.password` can be set here, or via `OPENCLAW_GATEWAY_PASSWORD` (recommended).
- `gateway.auth.allowTailscale` allows Tailscale Serve identity headers
  (`tailscale-user-login`) to satisfy auth when the request arrives on loopback
  with `x-forwarded-for`, `x-forwarded-proto`, and `x-forwarded-host`. OpenClaw
  verifies the identity by resolving the `x-forwarded-for` address via
  `tailscale whois` before accepting it. When `true`, Serve requests do not need
  a token/password; set `false` to require explicit credentials. Defaults to
  `true` when `tailscale.mode = "serve"` and auth mode is not `password`.
- `gateway.tailscale.mode: "serve"` uses Tailscale Serve (tailnet only, loopback bind).
- `gateway.tailscale.mode: "funnel"` exposes the dashboard publicly; requires auth.
- `gateway.tailscale.resetOnExit` resets Serve/Funnel config on shutdown.

Remote client defaults (CLI):

- `gateway.remote.url` sets the default Gateway WebSocket URL for CLI calls when `gateway.mode = "remote"`.
- `gateway.remote.transport` selects the macOS remote transport (`ssh` default, `direct` for ws/wss). When `direct`, `gateway.remote.url` must be `ws://` or `wss://`. `ws://host` defaults to port `18789`.
- `gateway.remote.token` supplies the token for remote calls (leave unset for no auth).
- `gateway.remote.password` supplies the password for remote calls (leave unset for no auth).

macOS app behavior:

- OpenClaw.app watches `~/.openclaw/openclaw.json` and switches modes live when `gateway.mode` or `gateway.remote.url` changes.
- If `gateway.mode` is unset but `gateway.remote.url` is set, the macOS app treats it as remote mode.
- When you change connection mode in the macOS app, it writes `gateway.mode` (and `gateway.remote.url` + `gateway.remote.transport` in remote mode) back to the config file.

```json5
{
  gateway: {
    mode: "remote",
    remote: {
      url: "ws://gateway.tailnet:18789",
      token: "your-token",
      password: "your-password",
    },
  },
}
```

Direct transport example (macOS app):

```json5
{
  gateway: {
    mode: "remote",
    remote: {
      transport: "direct",
      url: "wss://gateway.example.ts.net",
      token: "your-token",
    },
  },
}
```

### `gateway.reload` (Config hot reload)

The Gateway watches `~/.openclaw/openclaw.json` (or `OPENCLAW_CONFIG_PATH`) and applies changes automatically.

Modes:

- `hybrid` (default): hot-apply safe changes; restart the Gateway for critical changes.
- `hot`: only apply hot-safe changes; log when a restart is required.
- `restart`: restart the Gateway on any config change.
- `off`: disable hot reload.

```json5
{
  gateway: {
    reload: {
      mode: "hybrid",
      debounceMs: 300,
    },
  },
}
```

#### Hot reload matrix (files + impact)

Files watched:

- `~/.openclaw/openclaw.json` (or `OPENCLAW_CONFIG_PATH`)

Hot-applied (no full gateway restart):

- `hooks` (webhook auth/path/mappings) + `hooks.gmail` (Gmail watcher restarted)
- `browser` (browser control server restart)
- `cron` (cron service restart + concurrency update)
- `agents.defaults.heartbeat` (heartbeat runner restart)
- `web` (WhatsApp web channel restart)
- `telegram`, `discord`, `signal`, `imessage` (channel restarts)
- `agent`, `models`, `routing`, `messages`, `session`, `whatsapp`, `logging`, `skills`, `ui`, `talk`, `identity`, `wizard` (dynamic reads)

Requires full Gateway restart:

- `gateway` (port/bind/auth/control UI/tailscale)
- `bridge` (legacy)
- `discovery`
- `canvasHost`
- `plugins`
- Any unknown/unsupported config path (defaults to restart for safety)

### Multi-instance isolation

Bir xostda bir nechta shlyuzlarni ishga tushirish uchun (zaxira yoki qutqaruv boti uchun), har bir instansiya holati + konfiguratsiyasini ajrating va noyob portlardan foydalaning:

- `OPENCLAW_CONFIG_PATH` (har bir instansiya uchun konfiguratsiya)
- `OPENCLAW_STATE_DIR` (sessions/creds)
- `agents.defaults.workspace` (memories)
- `gateway.port` (unique per instance)

Convenience flags (CLI):

- `openclaw --dev …` → `~/.openclaw-dev` dan foydalanadi + asosiy `19001` portidan siljitadi
- `openclaw --profile <name> …` → uses `~/.openclaw-<name>` (port via config/env/flags)

See [Gateway runbook](/gateway) for the derived port mapping (gateway/browser/canvas).
See [Multiple gateways](/gateway/multiple-gateways) for browser/CDP port isolation details.

Example:

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json \
OPENCLAW_STATE_DIR=~/.openclaw-a \
openclaw gateway --port 19001
```

### `hooks` (Gateway webhooks)

Enable a simple HTTP webhook endpoint on the Gateway HTTP server.

Defaults:

- enabled: `false`
- yo‘l: `/hooks`
- maxBodyBytes: `262144` (256 KB)

```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
    presets: ["gmail"],
    transformsDir: "~/.openclaw/hooks",
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        wakeMode: "now",
        name: "Gmail",
        sessionKey: "hook:gmail:{{messages[0].id}}",
        messageTemplate: "From: {{messages[0].from}}\nSubject: {{messages[0].subject}}\n{{messages[0].snippet}}",
        deliver: true,
        channel: "last",
        model: "openai/gpt-5.2-mini",
      },
    ],
  },
}
```

Requests must include the hook token:

- `Authorization: Bearer <token>` **or**
- `x-openclaw-token: <token>`

Endpoints:

- `POST /hooks/wake` → `{ text, mode?: "now"|"next-heartbeat" }`
- `POST /hooks/agent` → `{ message, name?, sessionKey?, wakeMode?, deliver?, channel?, to?, model?, thinking?, timeoutSeconds? }`
- `POST /hooks/<name>` → resolved via `hooks.mappings`

`/hooks/agent` always posts a summary into the main session (and can optionally trigger an immediate heartbeat via `wakeMode: "now"`).

Mapping notes:

- `match.path` matches the sub-path after `/hooks` (e.g. `/hooks/gmail` → `gmail`).
- `match.source` matches a payload field (e.g. `{ source: "gmail" }`) so you can use a generic `/hooks/ingest` path.
- Templates like `{{messages[0].subject}}` read from the payload.
- `transform` can point to a JS/TS module that returns a hook action.
- `deliver: true` sends the final reply to a channel; `channel` defaults to `last` (falls back to WhatsApp).
- If there is no prior delivery route, set `channel` + `to` explicitly (required for Telegram/Discord/Google Chat/Slack/Signal/iMessage/MS Teams).
- `model` overrides the LLM for this hook run (`provider/model` or alias; must be allowed if `agents.defaults.models` is set).

Gmail helper config (used by `openclaw webhooks gmail setup` / `run`):

```json5
{
  hooks: {
    gmail: {
      account: "openclaw@gmail.com",
      topic: "projects/<project-id>/topics/gog-gmail-watch",
      subscription: "gog-gmail-watch-push",
      pushToken: "shared-push-token",
      hookUrl: "http://127.0.0.1:18789/hooks/gmail",
      includeBody: true,
      maxBytes: 20000,
      renewEveryMinutes: 720,
      serve: { bind: "127.0.0.1", port: 8788, path: "/" },
      tailscale: { mode: "funnel", path: "/gmail-pubsub" },

      // Optional: use a cheaper model for Gmail hook processing
      // Falls back to agents.defaults.model.fallbacks, then primary, on auth/rate-limit/timeout
      model: "openrouter/meta-llama/llama-3.3-70b-instruct:free",
      // Optional: default thinking level for Gmail hooks
      thinking: "off",
    },
  },
}
```

Model override for Gmail hooks:

- `hooks.gmail.model` specifies a model to use for Gmail hook processing (defaults to session primary).
- Accepts `provider/model` refs or aliases from `agents.defaults.models`.
- Falls back to `agents.defaults.model.fallbacks`, then `agents.defaults.model.primary`, on auth/rate-limit/timeouts.
- If `agents.defaults.models` is set, include the hooks model in the allowlist.
- At startup, warns if the configured model is not in the model catalog or allowlist.
- `hooks.gmail.thinking` sets the default thinking level for Gmail hooks and is overridden by per-hook `thinking`.

Gateway auto-start:

- If `hooks.enabled=true` and `hooks.gmail.account` is set, the Gateway starts
  `gog gmail watch serve` on boot and auto-renews the watch.
- Set `OPENCLAW_SKIP_GMAIL_WATCHER=1` to disable the auto-start (for manual runs).
- Avoid running a separate `gog gmail watch serve` alongside the Gateway; it will
  fail with `listen tcp 127.0.0.1:8788: bind: address already in use`.

Note: when `tailscale.mode` is on, OpenClaw defaults `serve.path` to `/` so
Tailscale can proxy `/gmail-pubsub` correctly (it strips the set-path prefix).1) Agar backend prefiksli yo‘lni qabul qilishi kerak bo‘lsa, `hooks.gmail.tailscale.target` ni to‘liq URL ga sozlang (va `serve.path` ni moslang).

### 2. `canvasHost` (LAN/tailnet Canvas fayl serveri + jonli qayta yuklash)

3. Gateway HTML/CSS/JS katalogini HTTP orqali xizmat qiladi, shuning uchun iOS/Android tugunlari unga shunchaki `canvas.navigate` orqali o‘ta oladi.

4. Standart ildiz: `~/.openclaw/workspace/canvas`  
   Standart port: `18793` (openclaw brauzer CDP porti `18792` bilan to‘qnashmaslik uchun tanlangan)  
   Server **gateway bind host** (LAN yoki Tailnet) da tinglaydi, shunda tugunlar unga ulana oladi.

5. Server:

- 6. `canvasHost.root` ostidagi fayllarni xizmat qiladi
- 7. xizmat qilinayotgan HTML ichiga juda kichik jonli qayta yuklash klientini joylaydi
- 8. katalogni kuzatadi va `/__openclaw__/ws` dagi WebSocket endpoint orqali qayta yuklashlarni tarqatadi
- 9. katalog bo‘sh bo‘lsa, boshlang‘ich `index.html` ni avtomatik yaratadi (darhol nimanidir ko‘rishingiz uchun)
- 10. shuningdek `/__openclaw__/a2ui/` da A2UI ni xizmat qiladi va tugunlarga `canvasHostUrl` sifatida e’lon qilinadi
      (Canvas/A2UI uchun tugunlar doimo shundan foydalanadi)

11. Agar katalog katta bo‘lsa yoki `EMFILE` ga duch kelsangiz, jonli qayta yuklashni (va fayl kuzatuvini) o‘chiring:

- 12. config: `canvasHost: { liveReload: false }`

```json5
13. {
  canvasHost: {
    root: "~/.openclaw/workspace/canvas",
    port: 18793,
    liveReload: true,
  },
}
```

14. `canvasHost.*` dagi o‘zgarishlar gateway’ni qayta ishga tushirishni talab qiladi (config reload qayta ishga tushiradi).

15. O‘chirish:

- 16. config: `canvasHost: { enabled: false }`
- 17. env: `OPENCLAW_SKIP_CANVAS_HOST=1`

### 18. `bridge` (meros TCP bridge, olib tashlangan)

19. Joriy build’lar endi TCP bridge listener’ni o‘z ichiga olmaydi; `bridge.*` konfiguratsiya kalitlari e’tiborsiz qoldiriladi.
20. Tugunlar Gateway WebSocket orqali ulanadi. 21. Bu bo‘lim tarixiy ma’lumot uchun saqlangan.

22. Meros xatti-harakat:

- 23. Gateway tugunlar (iOS/Android) uchun oddiy TCP bridge’ni ochishi mumkin edi, odatda `18790` portida.

24. Standartlar:

- 25. enabled: `true`
- 26. port: `18790`
- 27. bind: `lan` (`0.0.0.0` ga bog‘lanadi)

28. Bind rejimlari:

- 29. `lan`: `0.0.0.0` (har qanday interfeysda, jumladan LAN/Wi‑Fi va Tailscale’da yetib boriladi)
- 30. `tailnet`: faqat mashinaning Tailscale IP manziliga bog‘lanadi (Vienna ⇄ London uchun tavsiya etiladi)
- 31. `loopback`: `127.0.0.1` (faqat lokal)
- 32. `auto`: agar mavjud bo‘lsa tailnet IP’ni afzal ko‘radi, aks holda `lan`

33. TLS:

- 34. `bridge.tls.enabled`: bridge ulanishlari uchun TLS’ni yoqadi (yoqilganda faqat TLS).
- 35. `bridge.tls.autoGenerate`: sert/kalit mavjud bo‘lmaganda o‘z-o‘zidan imzolangan sertifikat yaratadi (standart: true).
- 36. `bridge.tls.certPath` / `bridge.tls.keyPath`: bridge sertifikati va maxfiy kaliti uchun PEM yo‘llari.
- 37. `bridge.tls.caPath`: ixtiyoriy PEM CA to‘plami (maxsus root’lar yoki kelajakdagi mTLS).

38. TLS yoqilganda, Gateway aniqlash TXT yozuvlarida `bridgeTls=1` va `bridgeTlsSha256` ni e’lon qiladi, shunda tugunlar sertifikatni pin qilishi mumkin. 39. Qo‘lda ulanishlar, agar hali fingerprint saqlanmagan bo‘lsa, trust-on-first-use’dan foydalanadi.
39. Avtomatik yaratilgan sertifikatlar PATH’da `openssl` ni talab qiladi; agar yaratish muvaffaqiyatsiz bo‘lsa, bridge ishga tushmaydi.

```json5
41. {
  bridge: {
    enabled: true,
    port: 18790,
    bind: "tailnet",
    tls: {
      enabled: true,
      // Uses ~/.openclaw/bridge/tls/bridge-{cert,key}.pem when omitted.
      // certPath: "~/.openclaw/bridge/tls/bridge-cert.pem",
      // keyPath: "~/.openclaw/bridge/tls/bridge-key.pem"
    },
  },
}
```

### 42. `discovery.mdns` (Bonjour / mDNS broadcast rejimi)

43. LAN mDNS aniqlash broadcast’larini (`_openclaw-gw._tcp`) boshqaradi.

- 44. `minimal` (standart): TXT yozuvlaridan `cliPath` + `sshPort` ni chiqarib tashlaydi
- 45. `full`: TXT yozuvlariga `cliPath` + `sshPort` ni qo‘shadi
- 46. `off`: mDNS broadcast’larini butunlay o‘chiradi
- 47. Hostname: standart bo‘yicha `openclaw` (`openclaw.local` ni e’lon qiladi). 48. `OPENCLAW_MDNS_HOSTNAME` bilan almashtiring.

```json5
49. {
  discovery: { mdns: { mode: "minimal" } },
}
```

### 50. `discovery.wideArea` (Keng hududli Bonjour / unicast DNS‑SD)

When enabled, the Gateway writes a unicast DNS-SD zone for `_openclaw-gw._tcp` under `~/.openclaw/dns/` using the configured discovery domain (example: `openclaw.internal.`).

To make iOS/Android discover across networks (Vienna ⇄ London), pair this with:

- a DNS server on the gateway host serving your chosen domain (CoreDNS is recommended)
- Tailscale **split DNS** so clients resolve that domain via the gateway DNS server

One-time setup helper (gateway host):

```bash
openclaw dns setup --apply
```

```json5
{
  discovery: { wideArea: { enabled: true } },
}
```

## Media model template variables

Template placeholders are expanded in `tools.media.*.models[].args` and `tools.media.models[].args` (and any future templated argument fields).

\| Variable           | Description                                                                     |
\| ------------------ | ------------------------------------------------------------------------------- | -------- | ------- | ---------- | ----- | ------ | -------- | ------- | ------- | --- |
\| `{{Body}}`         | Full inbound message body                                                       |
\| `{{RawBody}}`      | Raw inbound message body (no history/sender wrappers; best for command parsing) |
\| `{{BodyStripped}}` | Body with group mentions stripped (best default for agents)                     |
\| `{{From}}`         | Sender identifier (E.164 for WhatsApp; may differ per channel)                  |
\| `{{To}}`           | Destination identifier                                                          |
\| `{{MessageSid}}`   | Channel message id (when available)                                             |
\| `{{SessionId}}`    | Current session UUID                                                            |
\| `{{IsNewSession}}` | `"true"` when a new session was created                                         |
\| `{{MediaUrl}}`     | Inbound media pseudo-URL (if present)                                           |
\| `{{MediaPath}}`    | Local media path (if downloaded)                                                |
\| `{{MediaType}}`    | Media type (image/audio/document/…)                                             |
\| `{{Transcript}}`   | Audio transcript (when enabled)                                                 |
\| `{{Prompt}}`       | Resolved media prompt for CLI entries                                           |
\| `{{MaxChars}}`     | Resolved max output chars for CLI entries                                       |
\| `{{ChatType}}`     | `"direct"` or `"group"`                                                         |
\| `{{GroupSubject}}` | Group subject (best effort)                                                     |
\| `{{GroupMembers}}` | Group members preview (best effort)                                             |
\| `{{SenderName}}`   | Sender display name (best effort)                                               |
\| `{{SenderE164}}`   | Sender phone number (best effort)                                               |
\| `{{Provider}}`     | Provider hint (whatsapp                                                         | telegram | discord | googlechat | slack | signal | imessage | msteams | webchat | …)  |

## Cron (Gateway scheduler)

Cron is a Gateway-owned scheduler for wakeups and scheduled jobs. See [Cron jobs](/automation/cron-jobs) for the feature overview and CLI examples.

```json5
{
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
  },
}
```

---

_Next: [Agent Runtime](/concepts/agent)_ 🦞
