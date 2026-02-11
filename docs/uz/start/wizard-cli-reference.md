---
summary: "CLI onboarding jarayoni, autentifikatsiya/model sozlamalari, chiqishlar va ichki mexanizmlar bo‘yicha to‘liq ma’lumotnoma"
read_when:
  - "`openclaw onboard` uchun batafsil xatti-harakatlar kerak"
  - Siz onboarding natijalarini debug qilyapsiz yoki onboarding klientlarini integratsiya qilyapsiz
title: "CLI Onboarding Reference"
sidebarTitle: "CLI ma’lumotnomasi"
---

# CLI Onboarding Reference

Ushbu sahifa `openclaw onboard` uchun to‘liq ma’lumotnomadir.
Qisqa qo‘llanma uchun [Onboarding Wizard (CLI)](/start/wizard) ga qarang.

## Wizard nima qiladi

Mahalliy rejim (standart) sizni quyidagilar bo‘yicha bosqichma-bosqich olib boradi:

- Model va autentifikatsiya sozlamalari (OpenAI Code obunasi OAuth, Anthropic API kaliti yoki sozlash tokeni, shuningdek MiniMax, GLM, Moonshot va AI Gateway variantlari)
- Ishchi makon joylashuvi va bootstrap fayllari
- Gateway settings (port, bind, auth, tailscale)
- Kanallar va provayderlar (Telegram, WhatsApp, Discord, Google Chat, Mattermost plagini, Signal)
- Daemon install (LaunchAgent or systemd user unit)
- Health check
- Skills setup

Remote mode configures this machine to connect to a gateway elsewhere.
It does not install or modify anything on the remote host.

## Mahalliy oqim tafsilotlari

<Steps>
  <Step title="Existing config detection">
    - Agar `~/.openclaw/openclaw.json` mavjud bo‘lsa, Keep, Modify yoki Reset’ni tanlang.
    - Re-running the wizard does not wipe anything unless you explicitly choose Reset (or pass `--reset`).
    - If config is invalid or contains legacy keys, the wizard stops and asks you to run `openclaw doctor` before continuing.
    - Reset `trash` dan foydalanadi va quyidagi doiralarni taklif qiladi:
      - Faqat konfiguratsiya
      - Konfiguratsiya + hisob ma’lumotlari + sessiyalar
      - To‘liq reset (ishchi makonni ham olib tashlaydi)  
</Step>
  <Step title="Model and auth">
    - Full option matrix is in [Auth and model options](#auth-and-model-options).
  </Step>
  <Step title="Workspace">
    - Sukut bo‘yicha `~/.openclaw/workspace` (sozlanishi mumkin).
    - Seeds workspace files needed for first-run bootstrap ritual.
    - Ishchi makon tuzilishi: [Agent workspace](/concepts/agent-workspace).
  </Step>
  <Step title="Gateway">
    - Prompts for port, bind, auth mode, and tailscale exposure.
    - Tavsiya etiladi: loopback uchun ham token autentifikatsiyasini yoqilgan holda saqlang, shunda mahalliy WS mijozlari autentifikatsiyadan o‘tishi shart bo‘ladi.
    - Disable auth only if you fully trust every local process.
    - Non-loopback binds still require auth.
  </Step>
  <Step title="Channels">
    - [WhatsApp](/channels/whatsapp): optional QR login
    - [Telegram](/channels/telegram): bot token
    - [Discord](/channels/discord): bot token
    - [Google Chat](/channels/googlechat): service account JSON + webhook audience
    - [Mattermost](/channels/mattermost) plugin: bot token + base URL
    - [Signal](/channels/signal): optional `signal-cli` install + account config
    - [BlueBubbles](/channels/bluebubbles): recommended for iMessage; server URL + password + webhook
    - [iMessage](/channels/imessage): legacy `imsg` CLI path + DB access
    - DM security: default is pairing. First DM sends a code; approve via
      `openclaw pairing approve <channel><code>` or use allowlists.
  </Step><code>` or use allowlists.
  </Step>
  <Step title="Daemon install">
    - macOS: LaunchAgent
      - Requires logged-in user session; for headless, use a custom LaunchDaemon (not shipped).
    - Linux and Windows via WSL2: systemd user unit
      - Wizard attempts `loginctl enable-linger <user>` so gateway stays up after logout.
      - May prompt for sudo (writes `/var/lib/systemd/linger`); it tries without sudo first.
    - Runtime selection: Node (recommended; required for WhatsApp and Telegram). Bun is not recommended.
  </Step>
  <Step title="Health check">
    - Starts gateway (if needed) and runs `openclaw health`.
    - `openclaw status --deep` adds gateway health probes to status output.
  </Step>
  <Step title="Skills">
    - Reads available skills and checks requirements.
    - Lets you choose node manager: npm or pnpm (bun not recommended).
    - Installs optional dependencies (some use Homebrew on macOS).
  </Step>
  <Step title="Finish">
    - Summary and next steps, including iOS, Android, and macOS app options.
  </Step>
</Steps>

<Note>
If no GUI is detected, the wizard prints SSH port-forward instructions for the Control UI instead of opening a browser.
If Control UI assets are missing, the wizard attempts to build them; fallback is `pnpm ui:build` (auto-installs UI deps).
</Note>

## Remote mode details

Remote mode configures this machine to connect to a gateway elsewhere.

<Info>
Remote mode does not install or modify anything on the remote host.
</Info>

What you set:

- Remote gateway URL (`ws://...`)
- Token if remote gateway auth is required (recommended)

<Note>
- If gateway is loopback-only, use SSH tunneling or a tailnet.
- Discovery hints:
  - macOS: Bonjour (`dns-sd`)
  - Linux: Avahi (`avahi-browse`)
</Note>

## Auth and model options

<AccordionGroup>
  <Accordion title="Anthropic API key (recommended)">
    Uses `ANTHROPIC_API_KEY` if present or prompts for a key, then saves it for daemon use.
  </Accordion>
  <Accordion title="Anthropic OAuth (Claude Code CLI)">
    - macOS: checks Keychain item "Claude Code-credentials"
    - Linux and Windows: reuses `~/.claude/.credentials.json` if present

    ```
    macOS’da "Always Allow" ni tanlang, shunda launchd ishga tushirishlari bloklanmaydi.
    ```

  </Accordion>
  <Accordion title="Anthropic token (setup-token paste)">
    `claude setup-token` buyrug‘ini istalgan mashinada ishga tushiring, so‘ng tokenni joylashtiring.
    Nom berishingiz mumkin; bo‘sh qoldirilsa, standart qiymat ishlatiladi.
  </Accordion>
  <Accordion title="OpenAI Code subscription (Codex CLI reuse)">
    Agar `~/.codex/auth.json` mavjud bo‘lsa, ustoz (wizard) undan qayta foydalanishi mumkin.
  </Accordion>
  <Accordion title="OpenAI Code subscription (OAuth)">
    Brauzer oqimi; `code#state` ni joylashtiring.

    ```
    Model o‘rnatilmagan yoki `openai/*` bo‘lsa, `agents.defaults.model` ni `openai-codex/gpt-5.3-codex` ga o‘rnatadi.
    ```

  </Accordion>
  <Accordion title="OpenAI API key">
    Agar mavjud bo‘lsa `OPENAI_API_KEY` dan foydalanadi yoki kalitni so‘raydi, so‘ng launchd o‘qishi uchun
    uni `~/.openclaw/.env` ga saqlaydi.

    ```
    Model o‘rnatilmagan, `openai/*` yoki `openai-codex/*` bo‘lsa, `agents.defaults.model` ni `openai/gpt-5.1-codex` ga o‘rnatadi.
    ```

  </Accordion>
  <Accordion title="xAI (Grok) API key">
    `XAI_API_KEY` ni so‘raydi va xAI ni model provayderi sifatida sozlaydi.
  </Accordion>
  <Accordion title="OpenCode Zen">
    `OPENCODE_API_KEY` (yoki `OPENCODE_ZEN_API_KEY`) ni so‘raydi.
    Sozlash URL’i: [opencode.ai/auth](https://opencode.ai/auth).
  </Accordion>
  <Accordion title="API key (generic)">
    Kalitni siz uchun saqlaydi.
  </Accordion>
  <Accordion title="Vercel AI Gateway">
    `AI_GATEWAY_API_KEY` ni so‘raydi.
    Batafsil: [Vercel AI Gateway](/providers/vercel-ai-gateway).
  </Accordion>
  <Accordion title="Cloudflare AI Gateway">
    Hisob ID’si, gateway ID’si va `CLOUDFLARE_AI_GATEWAY_API_KEY` ni so‘raydi.
    Batafsil: [Cloudflare AI Gateway](/providers/cloudflare-ai-gateway).
  </Accordion>
  <Accordion title="MiniMax M2.1">
    Konfiguratsiya avtomatik yoziladi.
    Batafsil: [MiniMax](/providers/minimax).
  </Accordion>
  <Accordion title="Synthetic (Anthropic-compatible)">
    `SYNTHETIC_API_KEY` ni so‘raydi.
    Batafsil: [Synthetic](/providers/synthetic).
  </Accordion>
  <Accordion title="Moonshot and Kimi Coding">
    Moonshot (Kimi K2) va Kimi Coding konfiguratsiyalari avtomatik yoziladi.
    Batafsil: [Moonshot AI (Kimi + Kimi Coding)](/providers/moonshot).
  </Accordion>
  <Accordion title="Skip">
    Autentifikatsiyani sozlanmagan holda qoldiradi.
  </Accordion>
</AccordionGroup>

Model xulqi:

- Aniqlangan variantlardan standart modelni tanlang yoki provayder va modelni qo‘lda kiriting.
- Ustoz model tekshiruvini o‘tkazadi va sozlangan model noma’lum bo‘lsa yoki autentifikatsiya yetishmasa, ogohlantiradi.

Kirish ma’lumotlari va profillar yo‘llari:

- OAuth kirish ma’lumotlari: `~/.openclaw/credentials/oauth.json`
- Auth profillari (API kalitlar + OAuth): `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`

<Note>
Brauzersiz va serverlar uchun maslahat: OAuth’ni brauzerli mashinada yakunlang, so‘ng
`~/.openclaw/credentials/oauth.json` (yoki `$OPENCLAW_STATE_DIR/credentials/oauth.json`)
ni gateway xostiga ko‘chiring.
</Note>

## Chiqishlar va ichki tuzilma

`~/.openclaw/openclaw.json` dagi odatiy maydonlar:

- `agents.defaults.workspace`
- `agents.defaults.model` / `models.providers` (agar Minimax tanlansa)
- `gateway.*` (rejim, bog‘lash, auth, tailscale)
- `channels.telegram.botToken`, `channels.discord.token`, `channels.signal.*`, `channels.imessage.*`
- So‘rovlar davomida rozilik bersangiz, kanal allowlistlari (Slack, Discord, Matrix, Microsoft Teams) (nomlar imkon bo‘lsa ID’larga moslashtiriladi)
- `skills.install.nodeManager`
- `wizard.lastRunAt`
- `wizard.lastRunVersion`
- `wizard.lastRunCommit`
- `wizard.lastRunCommand`
- `wizard.lastRunMode`

`openclaw agents add` `agents.list[]` va ixtiyoriy `bindings` ni yozadi.

WhatsApp kirish ma’lumotlari `~/.openclaw/credentials/whatsapp/<accountId>/` ostida saqlanadi.
Sessiyalar `~/.openclaw/agents/<agentId>/sessions/` ostida saqlanadi.

<Note>
Ba’zi kanallar plaginlar sifatida yetkazib beriladi. Onboarding jarayonida tanlanganda, ustoz (wizard) kanal konfiguratsiyasidan oldin plaginni (npm yoki lokal yo‘l) o‘rnatishni taklif qiladi.
</Note>

Gateway wizard RPC:

- `wizard.start`
- `wizard.next`
- `wizard.cancel`
- `wizard.status`

Mijozlar (macOS ilovasi va Control UI) onboarding mantiqini qayta amalga oshirmasdan qadamlarni ko‘rsatishi mumkin.

Signal sozlash xatti-harakati:

- Mos reliz assetini yuklab oladi
- `~/.openclaw/tools/signal-cli/<version>/` ostida saqlaydi
- Konfiguratsiyada `channels.signal.cliPath` ni yozadi
- JVM buildlar Java 21 ni talab qiladi
- Mavjud bo‘lganda native buildlar ishlatiladi
- Windows WSL2 dan foydalanadi va WSL ichida Linux signal-cli oqimiga amal qiladi

## Bog‘liq hujjatlar

- Onboarding hub: [Onboarding Wizard (CLI)](/start/wizard)
- Avtomatlashtirish va skriptlar: [CLI Automation](/start/wizard-cli-automation)
- Buyruqlar ma’lumotnomasi: [`openclaw onboard`](/cli/onboard)
