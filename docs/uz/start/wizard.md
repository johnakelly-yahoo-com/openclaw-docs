---
summary: "CLI onboarding wizard: gateway, workspace, kanallar va ko‘nikmalar uchun yo‘naltirilgan sozlash"
read_when:
  - Onboarding wizardni ishga tushirish yoki sozlash
  - Yangi mashinani sozlash
title: "Onboarding Wizard (CLI)"
sidebarTitle: "Onboarding: CLI"
---

# Onboarding Wizard (CLI)

Onboarding wizard — macOS, Linux yoki Windows (WSL2 orqali; qat’iy tavsiya etiladi) da OpenClaw’ni sozlashning **tavsiya etilgan** usuli.
U bitta yo‘naltirilgan oqimda lokal Gateway yoki masofaviy Gateway ulanishini, shuningdek kanallar, ko‘nikmalar va workspace standartlarini sozlaydi.

```bash
openclaw onboard
```

<Info>
Eng tezkor birinchi chat: Control UI ni oching (kanal sozlash shart emas). Ishga tushiring
`openclaw dashboard` va brauzerda chat qiling. Hujjatlar: [Dashboard](/web/dashboard).
</Info>

Keyinroq qayta sozlash uchun:

```bash
openclaw configure
openclaw agents add <name>
```

<Note>
`--json` interaktiv bo‘lmagan rejimni anglatmaydi. Skriptlar uchun `--non-interactive` dan foydalaning.
</Note>

<Tip>
Tavsiya etiladi: agent `web_search` dan foydalana olishi uchun Brave Search API kalitini sozlang (`web_fetch` kalitsiz ham ishlaydi). Eng oson yo‘l: `openclaw configure --section web`
`tools.web.search.apiKey` ni saqlaydi. Hujjatlar: [Web tools](/tools/web).
</Tip>

## QuickStart va Advanced

Wizard **QuickStart** (standartlar) yoki **Advanced** (to‘liq nazorat) bilan boshlanadi.

<Tabs>
  <Tab title="QuickStart (defaults)">
    - Lokal gateway (loopback)
    - Workspace standarti (yoki mavjud workspace)
    - Gateway porti **18789**
    - Gateway autentifikatsiyasi **Token** (loopback’da ham avtomatik yaratiladi)
    - Tailscale orqali ochish **O‘chiq**
    - Telegram + WhatsApp DM’lari **allowlist** ga standartlanadi (telefon raqamingiz so‘raladi)
  </Tab>
  <Tab title="Advanced (full control)">
    - Har bir qadamni ochib beradi (rejim, workspace, gateway, kanallar, daemon, ko‘nikmalar).
  </Tab>
</Tabs>

## Wizard nimani sozlaydi

**Lokal rejim (standart)** sizni quyidagi qadamlar orqali olib boradi:

1. **Model/Auth** — Anthropic API kaliti (tavsiya etiladi), OAuth, OpenAI yoki boshqa provayderlar. Standart modelni tanlang.
2. **Workspace** — agent fayllari uchun joy (standart `~/.openclaw/workspace`). Boshlang‘ich (bootstrap) fayllarni yaratadi.
3. **Gateway** — port, bog‘lanish manzili, autentifikatsiya rejimi, Tailscale orqali ochish.
4. **Kanallar** — WhatsApp, Telegram, Discord, Google Chat, Mattermost, Signal, BlueBubbles yoki iMessage.
5. **Daemon** — LaunchAgent (macOS) yoki systemd user unit (Linux/WSL2) ni o‘rnatadi.
6. **Health check** — Starts the Gateway and verifies it's running.
7. **Skills** — Installs recommended skills and optional dependencies.

<Note>
Re-running the wizard does **not** wipe anything unless you explicitly choose **Reset** (or pass `--reset`).
If the config is invalid or contains legacy keys, the wizard asks you to run `openclaw doctor` first.
</Note>

**Remote mode** only configures the local client to connect to a Gateway elsewhere.
It does **not** install or change anything on the remote host.

## Add another agent

Use `openclaw agents add <name>` to create a separate agent with its own workspace,
sessions, and auth profiles. Running without `--workspace` launches the wizard.

What it sets:

- `agents.list[].name`
- `agents.list[].workspace`
- `agents.list[].agentDir`

Notes:

- Default workspaces follow `~/.openclaw/workspace-<agentId>`.
- Add `bindings` to route inbound messages (the wizard can do this).
- Non-interactive flags: `--model`, `--agent-dir`, `--bind`, `--non-interactive`.

## Full reference

For detailed step-by-step breakdowns, non-interactive scripting, Signal setup,
RPC API, and a full list of config fields the wizard writes, see the
[Wizard Reference](/reference/wizard).

## Related docs

- CLI command reference: [`openclaw onboard`](/cli/onboard)
- macOS app onboarding: [Onboarding](/start/onboarding)
- Agent first-run ritual: [Agent Bootstrapping](/start/bootstrapping)
