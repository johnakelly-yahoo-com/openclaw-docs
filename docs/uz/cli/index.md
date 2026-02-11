---
summary: "8. `openclaw` buyruqlari, quyi buyruqlari va parametrlar uchun OpenClaw CLI ma’lumotnomasi"
read_when:
  - 9. CLI buyruqlari yoki parametrlarini qo‘shish yoki o‘zgartirish
  - 10. Yangi buyruq interfeyslarini hujjatlashtirish
title: "11. CLI ma’lumotnomasi"
---

# 12. CLI ma’lumotnomasi

13. Ushbu sahifa joriy CLI xatti-harakatini tavsiflaydi. 14. Agar buyruqlar o‘zgarsa, ushbu hujjatni yangilang.

## 15. Buyruq sahifalari

- 16. [`setup`](/cli/setup)
- 17. [`onboard`](/cli/onboard)
- 18. [`configure`](/cli/configure)
- 19. [`config`](/cli/config)
- 20. [`doctor`](/cli/doctor)
- 21. [`dashboard`](/cli/dashboard)
- 22. [`reset`](/cli/reset)
- 23. [`uninstall`](/cli/uninstall)
- 24. [`update`](/cli/update)
- 25. [`message`](/cli/message)
- 26. [`agent`](/cli/agent)
- 27. [`agents`](/cli/agents)
- 28. [`acp`](/cli/acp)
- 29. [`status`](/cli/status)
- 30. [`health`](/cli/health)
- 31. [`sessions`](/cli/sessions)
- 32. [`gateway`](/cli/gateway)
- 33. [`logs`](/cli/logs)
- 34. [`system`](/cli/system)
- 35. [`models`](/cli/models)
- 36. [`memory`](/cli/memory)
- 37. [`nodes`](/cli/nodes)
- 38. [`devices`](/cli/devices)
- 39. [`node`](/cli/node)
- 40. [`approvals`](/cli/approvals)
- 41. [`sandbox`](/cli/sandbox)
- [`tui`](/cli/tui)
- 43. [`browser`](/cli/browser)
- 44. [`cron`](/cli/cron)
- 45. [`dns`](/cli/dns)
- 46. [`docs`](/cli/docs)
- 47. [`hooks`](/cli/hooks)
- 48. [`webhooks`](/cli/webhooks)
- 49. [`pairing`](/cli/pairing)
- 50. [`plugins`](/cli/plugins) (plagin buyruqlari)
- [`channels`](/cli/channels)
- [`security`](/cli/security)
- [`skills`](/cli/skills)
- [`voicecall`](/cli/voicecall) (plugin; if installed)

## Global flags

- `--dev`: isolate state under `~/.openclaw-dev` and shift default ports.
- `--profile <name>`: isolate state under `~/.openclaw-<name>`.
- `--no-color`: disable ANSI colors.
- `--update`: shorthand for `openclaw update` (source installs only).
- `-V`, `--version`, `-v`: print version and exit.

## Output styling

- ANSI colors and progress indicators only render in TTY sessions.
- OSC-8 hyperlinks render as clickable links in supported terminals; otherwise we fall back to plain URLs.
- `--json` (and `--plain` where supported) disables styling for clean output.
- `--no-color` disables ANSI styling; `NO_COLOR=1` is also respected.
- Long-running commands show a progress indicator (OSC 9;4 when supported).

## Color palette

OpenClaw uses a lobster palette for CLI output.

- `accent` (#FF5A2D): headings, labels, primary highlights.
- `accentBright` (#FF7A3D): command names, emphasis.
- `accentDim` (#D14A22): secondary highlight text.
- `info` (#FF8A5B): informational values.
- `success` (#2FBF71): success states.
- `warn` (#FFB020): warnings, fallbacks, attention.
- `error` (#E23D2D): errors, failures.
- `muted` (#8B7F77): de-emphasis, metadata.

Palette source of truth: `src/terminal/palette.ts` (aka “lobster seam”).

## Command tree

```
openclaw [--dev] [--profile <name>] <command>
  setup
  onboard
  configure
  config
    get
    set
    unset
  doctor
  security
    audit
  reset
  uninstall
  update
  channels
    list
    status
    logs
    add
    remove
    login
    logout
  skills
    list
    info
    check
  plugins
    list
    info
    install
    enable
    disable
    doctor
  memory
    status
    index
    search
  message
  agent
  agents
    list
    add
    delete
  acp
  status
  health
  sessions
  gateway
    call
    health
    status
    probe
    discover
    install
    uninstall
    start
    stop
    restart
    run
  logs
  system
    event
    heartbeat last|enable|disable
    presence
  models
    list
    status
    set
    set-image
    aliases list|add|remove
    fallbacks list|add|remove|clear
    image-fallbacks list|add|remove|clear
    scan
    auth add|setup-token|paste-token
    auth order get|set|clear
  sandbox
    list
    recreate
    explain
  cron
    status
    list
    add
    edit
    rm
    enable
    disable
    runs
    run
  nodes
  devices
  node
    run
    status
    install
    uninstall
    start
    stop
    restart
  approvals
    get
    set
    allowlist add|remove
  browser
    status
    start
    stop
    reset-profile
    tabs
    open
    focus
    close
    profiles
    create-profile
    delete-profile
    screenshot
    snapshot
    navigate
    resize
    click
    type
    press
    hover
    drag
    select
    upload
    fill
    dialog
    wait
    evaluate
    console
    pdf
  hooks
    list
    info
    check
    enable
    disable
    install
    update
  webhooks
    gmail setup|run
  pairing
    list
    approve
  docs
  dns
    setup
  tui
```

Note: plugins can add additional top-level commands (for example `openclaw voicecall`).

## Security

- `openclaw security audit` — audit config + local state for common security foot-guns.
- `openclaw security audit --deep` — best-effort live Gateway probe.
- `openclaw security audit --fix` — tighten safe defaults and chmod state/config.

## Plugins

Manage extensions and their config:

- `openclaw plugins list` — discover plugins (use `--json` for machine output).
- `openclaw plugins info <id>` — show details for a plugin.
- `openclaw plugins install <path|.tgz|npm-spec>` — install a plugin (or add a plugin path to `plugins.load.paths`).
- `openclaw plugins enable <id>` / `disable <id>` — toggle `plugins.entries.<id>.enabled`.
- `openclaw plugins doctor` — report plugin load errors.

Most plugin changes require a gateway restart. See [/plugin](/tools/plugin).

## Memory

Vector search over `MEMORY.md` + `memory/*.md`:

- `openclaw memory status` — show index stats.
- `openclaw memory index` — reindex memory files.
- `openclaw memory search "<query>"` — semantic search over memory.

## Chat slash commands

Chat xabarlari `/...` buyruqlarini qo‘llab-quvvatlaydi (matn va mahalliy). Qarang: [/tools/slash-commands](/tools/slash-commands).

Highlights:

- `/status` tezkor diagnostika uchun.
- `/config` saqlanadigan konfiguratsiya o‘zgarishlari uchun.
- `/debug` for runtime-only config overrides (memory, not disk; requires `commands.debug: true`).

## Setup + onboarding

### `setup`

Konfiguratsiya va ish maydonini ishga tushirish.

Variantlar:

- `--workspace <dir>`: agent ish maydoni yo‘li (standart `~/.openclaw/workspace`).
- `--wizard`: onboarding ustasini ishga tushirish.
- `--non-interactive`: ustani so‘rovlarsiz ishga tushirish.
- `--mode <local|remote>`: usta rejimi.
- `--remote-url <url>`: masofaviy Gateway URL manzili.
- `--remote-token <token>`: masofaviy Gateway tokeni.

Wizard auto-runs when any wizard flags are present (`--non-interactive`, `--mode`, `--remote-url`, `--remote-token`).

### `onboard`

Gateway, ish maydoni va ko‘nikmalarni sozlash uchun interaktiv usta.

Variantlar:

- `--workspace <dir>`
- `--reset` (ustadan oldin konfiguratsiya + hisob ma’lumotlari + sessiyalar + ish maydonini tiklash)
- `--non-interactive`
- `--mode <local|remote>`
- `--flow <quickstart|advanced|manual>` (manual — advanced uchun alias)
- `--auth-choice <setup-token|token|chutes|openai-codex|openai-api-key|openrouter-api-key|ai-gateway-api-key|moonshot-api-key|moonshot-api-key-cn|kimi-code-api-key|synthetic-api-key|venice-api-key|gemini-api-key|zai-api-key|apiKey|minimax-api|minimax-api-lightning|opencode-zen|skip>`
- `--token-provider <id>` (interaktiv bo‘lmagan; `--auth-choice token` bilan ishlatiladi)
- `--token <token>` (interaktiv bo‘lmagan; `--auth-choice token` bilan ishlatiladi)
- `--token-profile-id <id>` (interaktiv bo‘lmagan; standart: `<provider>:manual`)
- `--token-expires-in <duration>` (interaktiv bo‘lmagan; masalan `365d`, `12h`)
- `--anthropic-api-key <key>`
- `--openai-api-key <key>`
- `--openrouter-api-key <key>`
- `--ai-gateway-api-key <key>`
- `--moonshot-api-key <key>`
- `--kimi-code-api-key <key>`
- `--gemini-api-key <key>`
- `--zai-api-key <key>`
- `--minimax-api-key <key>`
- `--opencode-zen-api-key <key>`
- `--gateway-port <port>`
- `--gateway-bind <loopback|lan|tailnet|auto|custom>`
- `--gateway-auth <token|password>`
- `--gateway-token <token>`
- `--gateway-password <password>`
- `--remote-url <url>`
- `--remote-token <token>`
- `--tailscale <off|serve|funnel>`
- `--tailscale-reset-on-exit`
- `--install-daemon`
- `--no-install-daemon` (alias: `--skip-daemon`)
- `--daemon-runtime <node|bun>`
- `--skip-channels`
- `--skip-skills`
- `--skip-health`
- `--skip-ui`
- `--node-manager <npm|pnpm|bun>` (pnpm tavsiya etiladi; Gateway runtime uchun bun tavsiya etilmaydi)
- `--json`

### `configure`

Interaktiv konfiguratsiya ustasi (modellar, kanallar, ko‘nikmalar, gateway).

### `config`

No-interaktiv konfiguratsiya yordamchilari (get/set/unset). Hech qanday quyi buyruqsiz `openclaw config` ishga tushirilsa, ustani ochadi.

Quyi buyruqlar:

- `config get <path>`: konfiguratsiya qiymatini chop etish (nuqta/qavs yo‘li).
- `config set <path> <value>`: qiymatni o‘rnatish (JSON5 yoki xom satr).
- `config unset <path>`: qiymatni olib tashlash.

### `doctor`

Sog‘liq tekshiruvlari + tezkor tuzatishlar (config + gateway + eski xizmatlar).

Variantlar:

- `--no-workspace-suggestions`: workspace xotira bo‘yicha maslahatlarni o‘chirish.
- `--yes`: so‘rovsiz sukut bo‘yicha qiymatlarni qabul qilish (headless).
- `--non-interactive`: so‘rovlarni o‘tkazib yuborish; faqat xavfsiz migratsiyalarni qo‘llash.
- `--deep`: tizim xizmatlarini qo‘shimcha gateway o‘rnatmalarini topish uchun skanerlash.

## Kanal yordamchilari

### `channels`

Chat kanallari hisoblarini boshqarish (WhatsApp/Telegram/Discord/Google Chat/Slack/Mattermost (plugin)/Signal/iMessage/MS Teams).

Quyi buyruqlar:

- `channels list`: sozlangan kanallar va autentifikatsiya profillarini ko‘rsatish.
- `channels status`: gatewayga ulanishni va kanal sog‘lig‘ini tekshirish (`--probe` qo‘shimcha tekshiruvlarni bajaradi; gateway sog‘ligi uchun `openclaw health` yoki `openclaw status --deep` dan foydalaning).
- Maslahat: `channels status` keng tarqalgan noto‘g‘ri sozlamalarni aniqlay olganda, tavsiya etilgan tuzatishlar bilan ogohlantirishlarni chiqaradi (so‘ng `openclaw doctor` ga yo‘naltiradi).
- `channels logs`: gateway log faylidan so‘nggi kanal loglarini ko‘rsatish.
- `channels add`: bayroqlar berilmasa, ustozona (wizard) uslubidagi sozlash; bayroqlar no-interaktiv rejimga o‘tkazadi.
- `channels remove`: sukut bo‘yicha o‘chiriladi; so‘rovlarsiz konfiguratsiya yozuvlarini olib tashlash uchun `--delete` ni bering.
- `channels login`: interaktiv kanalga kirish (faqat WhatsApp Web).
- `channels logout`: kanal sessiyasidan chiqish (qo‘llab-quvvatlansa).

Umumiy variantlar:

- `--channel <name>`: `whatsapp|telegram|discord|googlechat|slack|mattermost|signal|imessage|msteams`
- `--account <id>`: kanal hisob identifikatori (sukut bo‘yicha `default`)
- `--name <label>`: hisob uchun ko‘rinadigan nom

`channels login` variantlari:

- `--channel <channel>` (sukut bo‘yicha `whatsapp`; `whatsapp`/`web` qo‘llab-quvvatlanadi)
- `--account <id>`
- `--verbose`

`channels logout` variantlari:

- `--channel <channel>` (sukut bo‘yicha `whatsapp`)
- `--account <id>`

`channels list` variantlari:

- `--no-usage`: model provayderi foydalanishi/kvota suratlarini o‘tkazib yuborish (faqat OAuth/API asosidagi).
- `--json`: JSON chiqishi (`--no-usage` o‘rnatilmagan bo‘lsa, foydalanishni ham o‘z ichiga oladi).

`channels logs` variantlari:

- `--channel <name|all>` (standart `all`)
- `--lines <n>` (standart `200`)
- `--json`

Batafsil: [/concepts/oauth](/concepts/oauth)

Misollar:

```bash
openclaw channels add --channel telegram --account alerts --name "Alerts Bot" --token $TELEGRAM_BOT_TOKEN
openclaw channels add --channel discord --account work --name "Work Bot" --token $DISCORD_BOT_TOKEN
openclaw channels remove --channel discord --account work --delete
openclaw channels status --probe
openclaw status --deep
```

### `skills`

Mavjud skill’larni va ularning tayyorlik holatini ko‘rish va tekshirish.

Pastki buyruqlar:

- `skills list`: skill’lar ro‘yxati (pastki buyruq ko‘rsatilmasa, standart).
- `skills info <name>`: show details for one skill.
- `skills check`: tayyor va yetishmayotgan talablar bo‘yicha umumiy xulosa.

Variantlar:

- `--eligible`: faqat tayyor skill’larni ko‘rsatish.
- `--json`: JSON chiqishi (bezaksiz).
- `-v`, `--verbose`: yetishmayotgan talablar tafsilotlarini qo‘shish.

Maslahat: skill’larni qidirish, o‘rnatish va sinxronlash uchun `npx clawhub` dan foydalaning.

### `pairing`

Kanallar bo‘ylab DM pairing so‘rovlarini tasdiqlash.

Pastki buyruqlar:

- `pairing list <channel> [--json]`
- `pairing approve <channel> <code> [--notify]`

### `webhooks gmail`

Gmail Pub/Sub hook sozlamasi va runner. Qarang: [/automation/gmail-pubsub](/automation/gmail-pubsub).

Pastki buyruqlar:

- `webhooks gmail setup` (`--account <email>` talab qilinadi; `--project`, `--topic`, `--subscription`, `--label`, `--hook-url`, `--hook-token`, `--push-token`, `--bind`, `--port`, `--path`, `--include-body`, `--max-bytes`, `--renew-minutes`, `--tailscale`, `--tailscale-path`, `--tailscale-target`, `--push-endpoint`, `--json` ni qo‘llab-quvvatlaydi)
- `webhooks gmail run` (xuddi shu flag’lar uchun runtime override’lar)

### `dns setup`

Keng hududli kashfiyot uchun DNS yordamchisi (CoreDNS + Tailscale). Qarang: [/gateway/discovery](/gateway/discovery).

Variantlar:

- `--apply`: CoreDNS konfiguratsiyasini o‘rnatish/yangilash (sudo talab qilinadi; faqat macOS).

## Xabar almashish + agent

### `message`

Yagona chiqish xabarlari va kanal amallari.

Qarang: [/cli/message](/cli/message)

Pastki buyruqlar:

- `message send|poll|react|reactions|read|edit|delete|pin|unpin|pins|permissions|search|timeout|kick|ban`
- `message thread <create|list|reply>`
- `message emoji <list|upload>`
- `message sticker <send|upload>`
- `message role <info|add|remove>`
- `message channel <info|list>`
- `message member info`
- `message voice status`
- `message event <list|create>`

Misollar:

- `openclaw message send --target +15555550123 --message "Hi"`
- `openclaw message poll --channel discord --target channel:123 --poll-question "Snack?" --poll-option Pizza --poll-option Sushi`

### `agent`

Run one agent turn via the Gateway (or `--local` embedded).

Required:

- `--message <text>`

Options:

- `--to <dest>` (for session key and optional delivery)
- `--session-id <id>`
- `--thinking <off|minimal|low|medium|high|xhigh>` (GPT-5.2 + Codex models only)
- `--verbose <on|full|off>`
- `--channel <whatsapp|telegram|discord|slack|mattermost|signal|imessage|msteams>`
- `--local`
- `--deliver`
- `--json`
- `--timeout <seconds>`

### `agents`

Manage isolated agents (workspaces + auth + routing).

#### `agents list`

List configured agents.

Options:

- `--json`
- `--bindings`

#### `agents add [name]`

Add a new isolated agent. Runs the guided wizard unless flags (or `--non-interactive`) are passed; `--workspace` is required in non-interactive mode.

Options:

- `--workspace <dir>`
- `--model <id>`
- `--agent-dir <dir>`
- `--bind <channel[:accountId]>` (repeatable)
- `--non-interactive`
- `--json`

Binding specs use `channel[:accountId]`. When `accountId` is omitted for WhatsApp, the default account id is used.

#### `agents delete <id>`

Delete an agent and prune its workspace + state.

Options:

- `--force`
- `--json`

### `acp`

Run the ACP bridge that connects IDEs to the Gateway.

See [`acp`](/cli/acp) for full options and examples.

### `status`

Show linked session health and recent recipients.

Options:

- `--json`
- `--all` (full diagnosis; read-only, pasteable)
- `--deep` (probe channels)
- `--usage` (show model provider usage/quota)
- `--timeout <ms>`
- `--verbose`
- `--debug` (alias for `--verbose`)

Notes:

- Overview includes Gateway + node host service status when available.

### Usage tracking

OpenClaw can surface provider usage/quota when OAuth/API creds are available.

Surfaces:

- `/status` (adds a short provider usage line when available)
- `openclaw status --usage` (prints full provider breakdown)
- macOS menu bar (Usage section under Context)

Notes:

- Data comes directly from provider usage endpoints (no estimates).
- Providers: Anthropic, GitHub Copilot, OpenAI Codex OAuth, plus Gemini CLI/Antigravity when those provider plugins are enabled.
- If no matching credentials exist, usage is hidden.
- Details: see [Usage tracking](/concepts/usage-tracking).

### `health`

Fetch health from the running Gateway.

Options:

- `--json`
- `--timeout <ms>`
- `--verbose`

### `sessions`

List stored conversation sessions.

Options:

- `--json`
- `--verbose`
- `--store <path>`
- `--active <minutes>`

## Reset / Uninstall

### `reset`

Reset local config/state (keeps the CLI installed).

Options:

- `--scope <config|config+creds+sessions|full>`
- `--yes`
- `--non-interactive`
- `--dry-run`

Notes:

- `--non-interactive` requires `--scope` and `--yes`.

### `uninstall`

Uninstall the gateway service + local data (CLI remains).

Options:

- `--service`
- `--state`
- `--workspace`
- `--app`
- `--all`
- `--yes`
- `--non-interactive`
- `--dry-run`

Eslatmalar:

- `--non-interactive` `--yes` va aniq ko‘rsatilgan scope’larni (yoki `--all`) talab qiladi.

## Gateway

### `gateway`

WebSocket Gateway’ni ishga tushiring.

Parametrlar:

- `--port <port>`
- `--bind <loopback|tailnet|lan|auto|custom>`
- `--token <token>`
- `--auth <token|password>`
- `--password <password>`
- `--tailscale <off|serve|funnel>`
- `--tailscale-reset-on-exit`
- `--allow-unconfigured`
- `--dev`
- `--reset` (dev konfiguratsiyasi + hisob ma’lumotlari + sessiyalar + ish maydonini tiklash)
- `--force` (portdagi mavjud tinglovchini majburan o‘chirish)
- `--verbose`
- `--claude-cli-logs`
- `--ws-log <auto|full|compact>`
- `--compact` (`--ws-log compact` uchun alias)
- `--raw-stream`
- `--raw-stream-path <path>`

### gateway xizmati

Gateway xizmatini boshqarish (launchd/systemd/schtasks).

Pastki buyruqlar:

- `gateway status` (standart bo‘yicha Gateway RPC’ni tekshiradi)
- `gateway install` (xizmatni o‘rnatish)
- `gateway uninstall`
- `gateway start`
- `gateway stop`
- `gateway restart`

Eslatmalar:

- `gateway status` standart bo‘yicha xizmatning aniqlangan port/konfiguratsiyasidan foydalanib Gateway RPC’ni tekshiradi (`--url/--token/--password` bilan almashtirish mumkin).
- `gateway status` skriptlash uchun `--no-probe`, `--deep` va `--json` ni qo‘llab-quvvatlaydi.
- `gateway status` aniqlay olganda meros yoki qo‘shimcha gateway xizmatlarini ham ko‘rsatadi (`--deep` tizim darajasidagi skanerlashlarni qo‘shadi). Profil nomi bilan atalgan OpenClaw xizmatlari to‘liq huquqli deb qaraladi va "qo‘shimcha" sifatida belgilanmaydi.
- `gateway status` CLI qaysi konfiguratsiya yo‘lidan foydalanayotganini va xizmat qaysi konfiguratsiyadan foydalanayotgani ehtimolini (xizmat muhiti), shuningdek aniqlangan tekshiruv maqsadi URL’ini chiqaradi.
- `gateway install|uninstall|start|stop|restart` skriptlash uchun `--json` ni qo‘llab-quvvatlaydi (standart chiqish foydalanuvchi uchun qulay bo‘lib qoladi).
- `gateway install` standart bo‘yicha Node runtime’dan foydalanadi; bun **tavsiya etilmaydi** (WhatsApp/Telegram xatolari).
- `gateway install` parametrlari: `--port`, `--runtime`, `--token`, `--force`, `--json`.

### `logs`

RPC orqali Gateway fayl loglarini kuzatish.

Eslatmalar:

- TTY sessiyalar rangli, tuzilgan ko‘rinishni beradi; TTY bo‘lmaganda oddiy matnga o‘tiladi.
- `--json` qatorma-qator JSON chiqaradi (har bir log hodisasi — alohida qatorda).

Misollar:

```bash
openclaw logs --follow
openclaw logs --limit 200
openclaw logs --plain
openclaw logs --json
openclaw logs --no-color
```

### `gateway <subcommand>`

Gateway CLI yordamchilari (RPC pastki buyruqlari uchun `--url`, `--token`, `--password`, `--timeout`, `--expect-final` dan foydalaning).
When you pass `--url`, the CLI does not auto-apply config or environment credentials.
Include `--token` or `--password` explicitly. Missing explicit credentials is an error.

Subcommands:

- `gateway call <method> [--params <json>]`
- `gateway health`
- `gateway status`
- `gateway probe`
- `gateway discover`
- `gateway install|uninstall|start|stop|restart`
- `gateway run`

Common RPCs:

- `config.apply` (validate + write config + restart + wake)
- `config.patch` (merge a partial update + restart + wake)
- `update.run` (run update + restart + wake)

Tip: when calling `config.set`/`config.apply`/`config.patch` directly, pass `baseHash` from
`config.get` if a config already exists.

## Models

See [/concepts/models](/concepts/models) for fallback behavior and scanning strategy.

Preferred Anthropic auth (setup-token):

```bash
claude setup-token
openclaw models auth setup-token --provider anthropic
openclaw models status
```

### `models` (root)

`openclaw models` is an alias for `models status`.

Root options:

- `--status-json` (alias for `models status --json`)
- `--status-plain` (alias for `models status --plain`)

### `models list`

Options:

- `--all`
- `--local`
- `--provider <name>`
- `--json`
- `--plain`

### `models status`

Options:

- `--json`
- `--plain`
- `--check` (exit 1=expired/missing, 2=expiring)
- `--probe` (live probe of configured auth profiles)
- `--probe-provider <name>`
- `--probe-profile <id>` (repeat or comma-separated)
- `--probe-timeout <ms>`
- `--probe-concurrency <n>`
- `--probe-max-tokens <n>`

Always includes the auth overview and OAuth expiry status for profiles in the auth store.
`--probe` runs live requests (may consume tokens and trigger rate limits).

### `models set <model>`

Set `agents.defaults.model.primary`.

### `models set-image <model>`

Set `agents.defaults.imageModel.primary`.

### `models aliases list|add|remove`

Options:

- 2. `list`: `--json`, `--plain`
- 3. `add <alias> <model>`
- 4. `remove <alias>`

### 5. `models fallbacks list|add|remove|clear`

6. Variantlar:

- 7. `list`: `--json`, `--plain`
- 8. `add <model>`
- 9. `remove <model>`
- 10. `clear`

### 11. `models image-fallbacks list|add|remove|clear`

12. Variantlar:

- 13. `list`: `--json`, `--plain`
- 14. `add <model>`
- 15. `remove <model>`
- 16. `clear`

### 17. `models scan`

18. Variantlar:

- 19. `--min-params <b>`
- `--max-age-days <days>`
- 21. `--provider <name>`
- 22. `--max-candidates <n>`
- 23. `--timeout <ms>`
- 24. `--concurrency <n>`
- 25. `--no-probe`
- 26. `--yes`
- 27. `--no-input`
- 28. `--set-default`
- 29. `--set-image`
- 30. `--json`

### 31. `models auth add|setup-token|paste-token`

32. Variantlar:

- 33. `add`: interaktiv autentifikatsiya yordamchisi
- 34. `setup-token`: `--provider <name>` (standart `anthropic`), `--yes`
- 35. `paste-token`: `--provider <name>`, `--profile-id <id>`, `--expires-in <duration>`

### 36. `models auth order get|set|clear`

37. Variantlar:

- 38. `get`: `--provider <name>`, `--agent <id>`, `--json`
- 39. `set`: `--provider <name>`, `--agent <id>`, `<profileIds...>`
- 40. `clear`: `--provider <name>`, `--agent <id>`

## 41. Tizim

### 42. `system event`

43. Tizim hodisasini navbatga qo‘shadi va ixtiyoriy ravishda yurak urishini ishga tushiradi (Gateway RPC).

44. Majburiy:

- 45. `--text <text>`

46. Variantlar:

- 47. `--mode <now|next-heartbeat>`
- 48. `--json`
- 49. `--url`, `--token`, `--timeout`, `--expect-final`

### 50. `system heartbeat last|enable|disable`

Heartbeat controls (Gateway RPC).

Options:

- `--json`
- `--url`, `--token`, `--timeout`, `--expect-final`

### `system presence`

List system presence entries (Gateway RPC).

Options:

- `--json`
- `--url`, `--token`, `--timeout`, `--expect-final`

## Cron

Manage scheduled jobs (Gateway RPC). See [/automation/cron-jobs](/automation/cron-jobs).

Subcommands:

- `cron status [--json]`
- `cron list [--all] [--json]` (table output by default; use `--json` for raw)
- `cron add` (alias: `create`; requires `--name` and exactly one of `--at` | `--every` | `--cron`, and exactly one payload of `--system-event` | `--message`)
- `cron edit <id>` (patch fields)
- `cron rm <id>` (aliases: `remove`, `delete`)
- `cron enable <id>`
- `cron disable <id>`
- `cron runs --id <id> [--limit <n>]`
- `cron run <id> [--force]`

All `cron` commands accept `--url`, `--token`, `--timeout`, `--expect-final`.

## Node host

`node` runs a **headless node host** or manages it as a background service. See
[`openclaw node`](/cli/node).

Subcommands:

- `node run --host <gateway-host> --port 18789`
- `node status`
- `node install [--host <gateway-host>] [--port <port>] [--tls] [--tls-fingerprint <sha256>] [--node-id <id>] [--display-name <name>] [--runtime <node|bun>] [--force]`
- `node uninstall`
- `node stop`
- `node restart`

## Nodes

`nodes` talks to the Gateway and targets paired nodes. See [/nodes](/nodes).

Common options:

- `--url`, `--token`, `--timeout`, `--json`

Subcommands:

- `nodes status [--connected] [--last-connected <duration>]`
- `nodes describe --node <id|name|ip>`
- `nodes list [--connected] [--last-connected <duration>]`
- `nodes pending`
- `nodes approve <requestId>`
- `nodes reject <requestId>`
- `nodes rename --node <id|name|ip> --name <displayName>`
- `nodes invoke --node <id|name|ip> --command <command> [--params <json>] [--invoke-timeout <ms>] [--idempotency-key <key>]`
- `nodes run --node <id|name|ip> [--cwd <path>] [--env KEY=VAL] [--command-timeout <ms>] [--needs-screen-recording] [--invoke-timeout <ms>] <command...>` (mac node or headless node host)
- `nodes notify --node <id|name|ip> [--title <text>] [--body <text>] [--sound <name>] [--priority <passive|active|timeSensitive>] [--delivery <system|overlay|auto>] [--invoke-timeout <ms>]` (mac only)

Camera:

- `nodes camera list --node <id|name|ip>`
- `nodes camera snap --node <id|name|ip> [--facing front|back|both] [--device-id <id>] [--max-width <px>] [--quality <0-1>] [--delay-ms <ms>] [--invoke-timeout <ms>]`
- `nodes camera clip --node <id|name|ip> [--facing front|back] [--device-id <id>] [--duration <ms|10s|1m>] [--no-audio] [--invoke-timeout <ms>]`

Canvas + screen:

- `nodes canvas snapshot --node <id|name|ip> [--format png|jpg|jpeg] [--max-width <px>] [--quality <0-1>] [--invoke-timeout <ms>]`
- `nodes canvas present --node <id|name|ip> [--target <urlOrPath>] [--x <px>] [--y <px>] [--width <px>] [--height <px>] [--invoke-timeout <ms>]`
- `nodes canvas hide --node <id|name|ip> [--invoke-timeout <ms>]`
- `nodes canvas navigate <url> --node <id|name|ip> [--invoke-timeout <ms>]`
- `nodes canvas eval [<js>] --node <id|name|ip> [--js <code>] [--invoke-timeout <ms>]`
- `nodes canvas a2ui push --node <id|name|ip> (--jsonl <path> | --text <text>) [--invoke-timeout <ms>]`
- `nodes canvas a2ui reset --node <id|name|ip> [--invoke-timeout <ms>]`
- `nodes screen record --node <id|name|ip> [--screen <index>] [--duration <ms|10s>] [--fps <n>] [--no-audio] [--out <path>] [--invoke-timeout <ms>]`

Location:

- `nodes location get --node <id|name|ip> [--max-age <ms>] [--accuracy <coarse|balanced|precise>] [--location-timeout <ms>] [--invoke-timeout <ms>]`

## Browser

Browser control CLI (dedicated Chrome/Brave/Edge/Chromium). See [`openclaw browser`](/cli/browser) and the [Browser tool](/tools/browser).

Common options:

- `--url`, `--token`, `--timeout`, `--json`
- `--browser-profile <name>`

Manage:

- `browser status`
- `browser start`
- `browser stop`
- `browser reset-profile`
- `browser tabs`
- `browser open <url>`
- `browser focus <targetId>`
- `browser close [targetId]`
- `browser profiles`
- `browser create-profile --name <name> [--color <hex>] [--cdp-url <url>]`
- `browser delete-profile --name <name>`

Inspect:

- `browser screenshot [targetId] [--full-page] [--ref <ref>] [--element <selector>] [--type png|jpeg]`
- `browser snapshot [--format aria|ai] [--target-id <id>] [--limit <n>] [--interactive] [--compact] [--depth <n>] [--selector <sel>] [--out <path>]`

Actions:

- `browser navigate <url> [--target-id <id>]`
- `browser resize <width> <height> [--target-id <id>]`
- `browser click <ref> [--double] [--button <left|right|middle>] [--modifiers <csv>] [--target-id <id>]`
- `browser type <ref> <text> [--submit] [--slowly] [--target-id <id>]`
- `browser press <key> [--target-id <id>]`
- `browser hover <ref> [--target-id <id>]`
- `browser drag <startRef> <endRef> [--target-id <id>]`
- `browser select <ref> <values...> [--target-id <id>]`
- `browser upload <paths...> [--ref <ref>] [--input-ref <ref>] [--element <selector>] [--target-id <id>] [--timeout-ms <ms>]`
- `browser fill [--fields <json>] [--fields-file <path>] [--target-id <id>]`
- `browser dialog --accept|--dismiss [--prompt <text>] [--target-id <id>] [--timeout-ms <ms>]`
- `browser wait [--time <ms>] [--text <value>] [--text-gone <value>] [--target-id <id>]`
- `browser evaluate --fn <code> [--ref <ref>] [--target-id <id>]`
- `browser console [--level <error|warn|info>] [--target-id <id>]`
- `browser pdf [--target-id <id>]`

## Docs search

### `docs [query...]`

Search the live docs index.

## TUI

### `tui`

Open the terminal UI connected to the Gateway.

Options:

- `--url <url>`
- `--token <token>`
- `--password <password>`
- `--session <key>`
- `--deliver`
- `--thinking <level>`
- `--message <text>`
- `--timeout-ms <ms>` (defaults to `agents.defaults.timeoutSeconds`)
- `--history-limit <n>`
