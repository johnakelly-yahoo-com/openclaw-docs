---
summary: "Slash commands: text vs native, config, and supported commands"
read_when:
  - Using or configuring chat commands
  - Debugging command routing or permissions
title: "Slash Commands"
---

# Slash commands

Commands are handled by the Gateway. Most commands must be sent as a **standalone** message that starts with `/`.
The host-only bash chat command uses `! <cmd>` (with `/bash <cmd>` as an alias).

There are two related systems:

- **Commands**: standalone `/...` messages.
- **Directives**: `/think`, `/verbose`, `/reasoning`, `/elevated`, `/exec`, `/model`, `/queue`.
  - Directives are stripped from the message before the model sees it.
  - In normal chat messages (not directive-only), they are treated as “inline hints” and do **not** persist session settings.
  - In directive-only messages (the message contains only directives), they persist to the session and reply with an acknowledgement.
  - Directives are only applied for **authorized senders** (channel allowlists/pairing plus `commands.useAccessGroups`).
    Unauthorized senders see directives treated as plain text.

There are also a few **inline shortcuts** (allowlisted/authorized senders only): `/help`, `/commands`, `/status`, `/whoami` (`/id`).
They run immediately, are stripped before the model sees the message, and the remaining text continues through the normal flow.

## Config

```json5
{
  commands: {
    native: "auto",
    nativeSkills: "auto",
    text: true,
    bash: false,
    bashForegroundMs: 2000,
    config: false,
    debug: false,
    restart: false,
    useAccessGroups: true,
  },
}
```

- `commands.text` (default `true`) enables parsing `/...` in chat messages.
  - On surfaces without native commands (WhatsApp/WebChat/Signal/iMessage/Google Chat/MS Teams), text commands still work even if you set this to `false`.
- `commands.native` (default `"auto"`) registers native commands.
  - Auto: on for Discord/Telegram; off for Slack (until you add slash commands); ignored for providers without native support.
  - Set `channels.discord.commands.native`, `channels.telegram.commands.native`, or `channels.slack.commands.native` to override per provider (bool or `"auto"`).
  - `false` clears previously registered commands on Discord/Telegram at startup. Slack commands are managed in the Slack app and are not removed automatically.
- `commands.nativeSkills` (default `"auto"`) registers **skill** commands natively when supported.
  - Auto: on for Discord/Telegram; off for Slack (Slack requires creating a slash command per skill).
  - Set `channels.discord.commands.nativeSkills`, `channels.telegram.commands.nativeSkills`, or `channels.slack.commands.nativeSkills` to override per provider (bool or `"auto"`).
- `commands.bash` (default `false`) enables `! <cmd>` to run host shell commands (`/bash <cmd>` is an alias; requires `tools.elevated` allowlists).
- `commands.bashForegroundMs` (default `2000`) controls how long bash waits before switching to background mode (`0` backgrounds immediately).
- `commands.config` (default `false`) enables `/config` (reads/writes `openclaw.json`).
- `commands.debug` (default `false`) enables `/debug` (runtime-only overrides).
- `commands.useAccessGroups` (default `true`) enforces allowlists/policies for commands.

## Command list

Text + native (when enabled):

- `/help`
- `/commands`
- `/skill <name> [input]` (run a skill by name)
- `/status` (show current status; includes provider usage/quota for the current model provider when available)
- `/allowlist` (list/add/remove allowlist entries)
- `/approve <id> allow-once|allow-always|deny` (resolve exec approval prompts)
- `/context [list|detail|json]` (explain “context”; `detail` shows per-file + per-tool + per-skill + system prompt size)
- `/whoami` (show your sender id; alias: `/id`)
- `/subagents list|stop|log|info|send` (inspect, stop, log, or message sub-agent runs for the current session)
- `/config show|get|set|unset` (konfiguratsiyani diskka saqlaydi, faqat egasi; `commands.config: true` talab qilinadi)
- `/debug show|set|unset|reset` (ish vaqtida ustuvor sozlamalar, faqat egasi; `commands.debug: true` talab qilinadi)
- `/usage off|tokens|full|cost` (har bir javob uchun foydalanish pastki qismi yoki mahalliy xarajatlar xulosasi)
- `/tts off|always|inbound|tagged|status|provider|limit|summary|audio` (TTS boshqaruvi; qarang [/tts](/tts))
  - Discord: mahalliy buyruq `/voice` (`/tts` Discord tomonidan band qilingan); matnli `/tts` hanuz ishlaydi.
- `/stop`
- `/restart`
- `/dock-telegram` (taxallus: `/dock_telegram`) (javoblarni Telegram’ga o‘tkazish)
- `/dock-discord` (taxallus: `/dock_discord`) (javoblarni Discord’ga o‘tkazish)
- `/dock-slack` (taxallus: `/dock_slack`) (javoblarni Slack’ga o‘tkazish)
- `/activation mention|always` (faqat guruhlar uchun)
- `/send on|off|inherit` (faqat egasi)
- `/reset` yoki `/new [model]` (ixtiyoriy model ishorasi; qolgan matn uzatiladi)
- `/think <off|minimal|low|medium|high|xhigh>` (model/provayderga qarab dinamik variantlar; taxalluslar: `/thinking`, `/t`)
- `/verbose on|full|off` (taxallus: `/v`)
- `/reasoning on|off|stream` (taxallus: `/reason`; yoqilganda, `Reasoning:` prefiksi bilan alohida xabar yuboradi; `stream` = faqat Telegram qoralamasi)
- `/elevated on|off|ask|full` (taxallus: `/elev`; `full` bajarish tasdiqlarini o‘tkazib yuboradi)
- `/exec host=<sandbox|gateway|node> security=<deny|allowlist|full> ask=<off|on-miss|always> node=<id>` (joriy holatni ko‘rish uchun `/exec` yuboring)
- `/model <name>` (taxallus: `/models`; yoki `/<alias>` `agents.defaults.models.*.alias` dan)
- `/queue <mode>` (qo‘shimcha variantlar bilan, masalan `debounce:2s cap:25 drop:summarize`; joriy sozlamalarni ko‘rish uchun `/queue` yuboring)
- `/bash <command>` (faqat xost; `! 22. <command>` uchun taxallus; `commands.bash: true` + `tools.elevated` ruxsat ro‘yxatlari talab qilinadi) Faqat matnli:

`/compact [instructions]` (qarang [/concepts/compaction](/concepts/compaction))

- `! 26. <command>` (faqat xost; bir vaqtning o‘zida bittadan; uzoq ishlar uchun `!poll` + `!stop` dan foydalaning)
- `!poll` (chiqish / holatni tekshirish; ixtiyoriy `sessionId` qabul qiladi; `/bash poll` ham ishlaydi) `!stop` (ishlayotgan bash vazifasini to‘xtatish; ixtiyoriy `sessionId` qabul qiladi; `/bash stop` ham ishlaydi)
- Eslatmalar:
- Buyruqlar buyruq va argumentlar orasida ixtiyoriy `:` qabul qiladi (masalan, `/think: high`, `/send: on`, `/help:`).

`/new <model>` model taxallusini, `provider/model` ni yoki provayder nomini (taxminiy moslik) qabul qiladi; moslik topilmasa, matn xabar tanasi sifatida ko‘riladi.

- Provayder bo‘yicha to‘liq foydalanish tafsilotlari uchun `openclaw status --usage` dan foydalaning.
- `/allowlist add|remove` `commands.config=true` ni talab qiladi va kanal `configWrites` ga rioya qiladi.
- `/usage` har bir javob uchun foydalanish pastki qismini boshqaradi; `/usage cost` OpenClaw sessiya jurnallaridan mahalliy xarajatlar xulosasini chiqaradi.
- `/restart` sukut bo‘yicha o‘chirilgan; yoqish uchun `commands.restart: true` ni o‘rnating.
- `/verbose` nosozliklarni aniqlash va qo‘shimcha ko‘rinuvchanlik uchun mo‘ljallangan; odatiy foydalanishda **o‘chiq** holda qoldiring.
- `/reasoning` (va `/verbose`) guruh sozlamalarida xavfli: ular siz oshkor etishni istamagan ichki mulohazalar yoki asbob chiqishlarini ochib yuborishi mumkin.
- Ayniqsa guruh chatlarida ularni o‘chiq holda qoldirishni afzal ko‘ring.
- **Tezkor yo‘l:** ruxsat ro‘yxatidagi jo‘natuvchilardan faqat buyruqdan iborat xabarlar darhol qayta ishlanadi (navbat + modelni chetlab o‘tadi). **Guruhda eslatma cheklovi:** ruxsat ro‘yxatidagi jo‘natuvchilardan faqat buyruqdan iborat xabarlar eslatma talablarini chetlab o‘tadi.
- **Ichki yorliqlar (faqat ruxsat ro‘yxatidagi jo‘natuvchilar):** ayrim buyruqlar oddiy xabar ichiga joylashtirilganda ham ishlaydi va model qolgan matnni ko‘rishidan oldin olib tashlanadi.
- Misol: `hey /status` holat javobini ishga tushiradi va qolgan matn odatiy oqim orqali davom etadi.
- Hozirda: `/help`, `/commands`, `/status`, `/whoami` (`/id`).
  - Ruxsatsiz faqat-buyruq xabarlari jimjitlik bilan e’tiborsiz qoldiriladi va ichki `/...` tokenlari oddiy matn sifatida ko‘riladi.
- **Ko‘nikma buyruqlari:** `user-invocable` ko‘nikmalar slash-buyruqlar sifatida taqdim etiladi.
- Nomlar `a-z0-9_` ga tozalanadi (maks. 32 belgi); to‘qnashuvlarda raqamli suffikslar qo‘shiladi (masalan, `_2`).
- `/skill <name> [input]` ko‘nikmani nomi bo‘yicha ishga tushiradi (mahalliy buyruq cheklovlari har bir ko‘nikma uchun buyruqlarga to‘sqinlik qilganda foydali). Sukut bo‘yicha, ko‘nikma buyruqlari modelga oddiy so‘rov sifatida uzatiladi.
  - Ko‘nikmalar ixtiyoriy ravishda `command-dispatch: tool` ni e’lon qilishi mumkin, bu buyruqni bevosita asbobga yo‘naltiradi (deterministik, model yo‘q).
  - Misol: `/prose` (OpenProse plagini) — qarang [OpenProse](/prose).
  - Skills may optionally declare `command-dispatch: tool` to route the command directly to a tool (deterministic, no model).
  - Example: `/prose` (OpenProse plugin) — see [OpenProse](/prose).
- **Native buyruq argumentlari:** Discord dinamik opsiyalar uchun avtomatik to‘ldirishdan foydalanadi (va majburiy argumentlar qoldirilganda tugma menyulari). Telegram va Slack buyruq tanlovlarni qo‘llab-quvvatlaganda va siz argumentni qoldirsangiz, tugma menyusini ko‘rsatadi.

## 3. Foydalanish yuzalari (qayerda nima ko‘rsatiladi)

- **Provayderdan foydalanish/kvota** (masalan: “Claude 80% qoldi”) foydalanishni kuzatish yoqilgan bo‘lsa, joriy model provayderi uchun `/status` da ko‘rinadi.
- **Har bir javob uchun tokenlar/narx** `/usage off|tokens|full` orqali boshqariladi (oddiy javoblarga qo‘shib yuboriladi).
- `/model status` foydalanish haqida emas, balki **modelllar/auth/endpoints** haqida.

## Model tanlash (`/model`)

`/model` direktiva sifatida amalga oshirilgan.

Misollar:

```
/model
/model list
/model 3
/model openai/gpt-5.2
/model opus@anthropic:default
/model status
```

Eslatmalar:

- `/model` va `/model list` ixcham, raqamlangan tanlovchini ko‘rsatadi (model oilasi + mavjud provayderlar).
- `/model <#>` shu tanlovchidan tanlaydi (va imkon bo‘lsa, joriy provayderni afzal ko‘radi).
- `/model status` batafsil ko‘rinishni ko‘rsatadi, jumladan sozlangan provayder endpointi (`baseUrl`) va API rejimi (`api`) mavjud bo‘lsa.

## Debug override’lar

`/debug` **faqat ish vaqtiga oid** konfiguratsiya override’larini o‘rnatishga imkon beradi (xotirada, diskda emas). Faqat egasi uchun. Standart holatda o‘chiq; `commands.debug: true` bilan yoqing.

Misollar:

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug set channels.whatsapp.allowFrom=["+1555","+4477"]
/debug unset messages.responsePrefix
/debug reset
```

Eslatmalar:

- Override’lar darhol yangi konfiguratsiya o‘qishlariga qo‘llanadi, ammo `openclaw.json` ga yozilmaydi.
- Barcha override’larni tozalash va diskdagi konfiguratsiyaga qaytish uchun `/debug reset` dan foydalaning.

## Konfiguratsiyani yangilash

`/config` diskdagi konfiguratsiyangizga (`openclaw.json`) yozadi. Faqat egasi uchun. Standart holatda o‘chiq; `commands.config: true` bilan yoqing.

Misollar:

```
/config show
/config show messages.responsePrefix
/config get messages.responsePrefix
/config set messages.responsePrefix="[openclaw]"
/config unset messages.responsePrefix
```

Eslatmalar:

- Yozishdan oldin konfiguratsiya tekshiriladi; yaroqsiz o‘zgarishlar rad etiladi.
- `/config` yangilanishlari qayta ishga tushirishlar orasida saqlanib qoladi.

## Surface bo‘yicha eslatmalar

- **Matn buyruqlari** odatiy chat sessiyasida ishlaydi (DMlar `main` ni bo‘lishadi, guruhlarning o‘z sessiyasi bor).
- **Native buyruqlar** izolyatsiyalangan sessiyalardan foydalanadi:
  - Discord: `agent:<agentId>:discord:slash:<userId>`
  - Slack: `agent:<agentId>:slack:slash:<userId>` (prefiks `channels.slack.slashCommand.sessionPrefix` orqali sozlanadi)
  - Telegram: `telegram:slash:<userId>` (chat sessiyasini `CommandTargetSessionKey` orqali nishonga oladi)
- **`/stop`** joriy ishni bekor qilish uchun faol chat sessiyasini nishonga oladi.
- **Slack:** `channels.slack.slashCommand` hali ham bitta `/openclaw`-uslubidagi buyruq uchun qo‘llab-quvvatlanadi. Agar `commands.native` ni yoqsangiz, har bir ichki buyruq uchun Slack’da bitta slash buyruq yaratishingiz kerak (nomlari `/help` dagi bilan bir xil). Slack uchun buyruq argument menyulari ephemeral Block Kit tugmalari sifatida yetkaziladi.
