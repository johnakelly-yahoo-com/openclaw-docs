---
summary: "Advanced setup and development workflows for OpenClaw"
read_when:
  - Setting up a new machine
  - You want “latest + greatest” without breaking your personal setup
title: "Setup"
---

# Setup

<Note>
If you are setting up for the first time, start with [Getting Started](/start/getting-started).
For wizard details, see [Onboarding Wizard](/start/wizard).
</Note>

Last updated: 2026-01-01

## TL;DR

- **Tailoring lives outside the repo:** `~/.openclaw/workspace` (workspace) + `~/.openclaw/openclaw.json` (config).
- **Stable workflow:** install the macOS app; let it run the bundled Gateway.
- **Bleeding edge workflow:** run the Gateway yourself via `pnpm gateway:watch`, then let the macOS app attach in Local mode.

## Prereqs (from source)

- Node `>=22`
- `pnpm`
- Docker (optional; only for containerized setup/e2e — see [Docker](/install/docker))

## Tailoring strategy (so updates don’t hurt)

If you want “100% tailored to me” _and_ easy updates, keep your customization in:

- **Config:** `~/.openclaw/openclaw.json` (JSON/JSON5-ish)
- **Workspace:** `~/.openclaw/workspace` (skills, prompts, memories; make it a private git repo)

Bootstrap once:

```bash
openclaw setup
```

From inside this repo, use the local CLI entry:

```bash
openclaw setup
```

If you don’t have a global install yet, run it via `pnpm openclaw setup`.

## Run the Gateway from this repo

After `pnpm build`, you can run the packaged CLI directly:

```bash
node openclaw.mjs gateway --port 18789 --verbose
```

## Stable workflow (macOS app first)

1. Install + launch **OpenClaw.app** (menu bar).
2. Complete the onboarding/permissions checklist (TCC prompts).
3. Ensure Gateway is **Local** and running (the app manages it).
4. Link surfaces (example: WhatsApp):

```bash
openclaw channels login
```

5. Sanity check:

```bash
openclaw salomatligi
```

Agar onboarding sizning build’ingizda mavjud bo‘lmasa:

- `openclaw setup` ni ishga tushiring, so‘ng `openclaw channels login`, keyin Gateway’ni qo‘lda ishga tushiring (`openclaw gateway`).

## Bleeding edge ish jarayoni (Gateway terminalda)

Maqsad: TypeScript Gateway ustida ishlash, hot reload olish va macOS ilovasi UI’ni ulangan holda saqlash.

### 0. (Ixtiyoriy) macOS ilovasini ham manbadan ishga tushirish

Agar macOS ilovasini ham bleeding edge’da ishlatmoqchi bo‘lsangiz:

```bash
./scripts/restart-mac.sh
```

### 1. Dev Gateway’ni ishga tushirish

```bash
pnpm install
pnpm gateway:watch
```

`gateway:watch` Gateway’ni watch rejimida ishga tushiradi va TypeScript o‘zgarishlarida qayta yuklaydi.

### 2. macOS ilovasini ishlayotgan Gateway’ga yo‘naltirish

**OpenClaw.app** ichida:

- Ulanish rejimi: **Local**
  Ilova sozlangan portda ishlayotgan gateway’ga ulanadi.

### 3. Tekshirish

- Ilova ichidagi Gateway holati **“Using existing gateway …”** deb ko‘rsatishi kerak
- Yoki CLI orqali:

```bash
openclaw health
```

### Keng tarqalgan xatolar

- **Noto‘g‘ri port:** Gateway WS sukut bo‘yicha `ws://127.0.0.1:18789`; ilova va CLI bir xil portda bo‘lsin.
- **Holat qayerda saqlanadi:**
  - Credential’lar: `~/.openclaw/credentials/`
  - Sessiyalar: `~/.openclaw/agents/<agentId>/sessions/`
  - Loglar: `/tmp/openclaw/`

## Credential saqlash xaritasi

Buni auth’ni debugging qilishda yoki nimani zaxiralashni hal qilayotganda ishlating:

- **WhatsApp**: `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`
- **Telegram bot tokeni**: config/env yoki `channels.telegram.tokenFile`
- **Discord bot tokeni**: config/env (token fayli hali qo‘llab-quvvatlanmaydi)
- **Slack tokenlari**: config/env (`channels.slack.*`)
- **Pairing allowlist’lar**: `~/.openclaw/credentials/<channel>-allowFrom.json`
- **Model auth profillari**: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- **Legacy OAuth import**: `~/.openclaw/credentials/oauth.json`
  Batafsil: [Security](/gateway/security#credential-storage-map).

## Yangilash (sozlamangizni buzmasdan)

- `~/.openclaw/workspace` va `~/.openclaw/` ni “sizga tegishli” deb saqlang; shaxsiy prompt/config’larni `openclaw` repo’siga joylamang.
- Manbani yangilash: `git pull` + `pnpm install` (lockfile o‘zgarganda) + `pnpm gateway:watch` dan foydalanishda davom eting.

## Linux (systemd foydalanuvchi xizmati)

Linux o‘rnatmalari systemd **user** xizmatidan foydalanadi. Sukut bo‘yicha systemd foydalanuvchi xizmatlarini logout/idle’da to‘xtatadi, bu esa Gateway’ni o‘chiradi. Onboarding siz uchun lingering’ni yoqishga harakat qiladi (sudo so‘rashi mumkin). Agar hali ham o‘chiq bo‘lsa, ishga tushiring:

```bash
sudo loginctl enable-linger $USER
```

Doimiy ishlash yoki ko‘p foydalanuvchili serverlar uchun **system** xizmatini **user** xizmati o‘rniga ko‘rib chiqing (lingering kerak bo‘lmaydi). systemd bo‘yicha eslatmalar uchun [Gateway runbook](/gateway) ga qarang.

## Tegishli hujjatlar

- [Gateway runbook](/gateway) (flag’lar, supervision, portlar)
- [Gateway konfiguratsiyasi](/gateway/configuration) (config sxemasi + misollar)
- [Discord](/channels/discord) va [Telegram](/channels/telegram) (reply tag’lar + replyToMode sozlamalari)
- [OpenClaw assistant sozlamalari](/start/openclaw)
- [macOS ilovasi](/platforms/macos) (gateway lifecycle)
