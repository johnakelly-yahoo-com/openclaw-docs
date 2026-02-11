---
summary: "39. OpenClaw’ni xavfsiz yangilash (global o‘rnatish yoki manbadan), shuningdek qaytish (rollback) strategiyasi"
read_when:
  - 40. OpenClaw’ni yangilash
  - 41. Yangilanishdan keyin nimadir buzildi
title: "42. Yangilash"
---

# 43. Yangilash

44. OpenClaw tez rivojlanmoqda (“1.0” dan oldin). 45. Yangilanishlarga infratuzilma jo‘natishdek yondashing: yangilash → tekshiruvlarni ishga tushirish → qayta ishga tushirish (yoki qayta ishga tushiradigan `openclaw update` dan foydalanish) → tekshirish.

## 46. Tavsiya etiladi: veb-sayt o‘rnatuvchisini qayta ishga tushirish (joyida yangilash)

47. **Afzal** yangilash yo‘li — veb-saytdagi o‘rnatuvchini qayta ishga tushirish. 48. U
    mavjud o‘rnatishlarni aniqlaydi, joyida yangilaydi va kerak bo‘lsa `openclaw doctor` ni ishga tushiradi.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

50. Eslatmalar:

- Add `--no-onboard` if you don’t want the onboarding wizard to run again.

- For **source installs**, use:

  ```bash
  curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git --no-onboard
  ```

  The installer will `git pull --rebase` **only** if the repo is clean.

- For **global installs**, the script uses `npm install -g openclaw@latest` under the hood.

- Legacy note: `clawdbot` remains available as a compatibility shim.

## Before you update

- Know how you installed: **global** (npm/pnpm) vs **from source** (git clone).
- Know how your Gateway is running: **foreground terminal** vs **supervised service** (launchd/systemd).
- Snapshot your tailoring:
  - Config: `~/.openclaw/openclaw.json`
  - Credentials: `~/.openclaw/credentials/`
  - Workspace: `~/.openclaw/workspace`

## Update (global install)

Global install (pick one):

```bash
npm i -g openclaw@latest
```

```bash
pnpm add -g openclaw@latest
```

We do **not** recommend Bun for the Gateway runtime (WhatsApp/Telegram bugs).

To switch update channels (git + npm installs):

```bash
openclaw update --channel beta
openclaw update --channel dev
openclaw update --channel stable
```

Use `--tag <dist-tag|version>` for a one-off install tag/version.

See [Development channels](/install/development-channels) for channel semantics and release notes.

Note: on npm installs, the gateway logs an update hint on startup (checks the current channel tag). Disable via `update.checkOnStart: false`.

Then:

```bash
openclaw doctor
openclaw gateway restart
openclaw health
```

Notes:

- If your Gateway runs as a service, `openclaw gateway restart` is preferred over killing PIDs.
- If you’re pinned to a specific version, see “Rollback / pinning” below.

## Update (`openclaw update`)

For **source installs** (git checkout), prefer:

```bash
openclaw update
```

It runs a safe-ish update flow:

- Requires a clean worktree.
- Switches to the selected channel (tag or branch).
- Fetches + rebases against the configured upstream (dev channel).
- Installs deps, builds, builds the Control UI, and runs `openclaw doctor`.
- Restarts the gateway by default (use `--no-restart` to skip).

If you installed via **npm/pnpm** (no git metadata), `openclaw update` will try to update via your package manager. If it can’t detect the install, use “Update (global install)” instead.

## Update (Control UI / RPC)

The Control UI has **Update & Restart** (RPC: `update.run`). It:

1. Runs the same source-update flow as `openclaw update` (git checkout only).
2. Writes a restart sentinel with a structured report (stdout/stderr tail).
3. Restarts the gateway and pings the last active session with the report.

If the rebase fails, the gateway aborts and restarts without applying the update.

## Update (from source)

From the repo checkout:

Preferred:

```bash
openclaw yangilanishi
```

Qo‘llanma (taxminan mos):

```bash
git pull
pnpm install
pnpm build
pnpm ui:build # birinchi ishga tushishda UI bog‘liqliklarini avtomatik o‘rnatadi
openclaw doctor
openclaw health
```

Eslatmalar:

- `pnpm build` qadoqlangan `openclaw` binarini ([`openclaw.mjs`](https://github.com/openclaw/openclaw/blob/main/openclaw.mjs)) ishga tushirganda yoki Node orqali `dist/` ni ishlatganda muhim.
- Agar global o‘rnatmasiz repo checkout’dan ishlayotgan bo‘lsangiz, CLI buyruqlari uchun `pnpm openclaw ...` dan foydalaning.
- Agar to‘g‘ridan-to‘g‘ri TypeScript’dan (`pnpm openclaw ...`) ishga tushirsangiz, odatda qayta build kerak emas, ammo **konfiguratsiya migratsiyalari baribir qo‘llanadi** → doctor’ni ishga tushiring.
- Global va git o‘rnatishlar o‘rtasida almashish oson: boshqa variantni o‘rnating, so‘ng gateway xizmati kirish nuqtasi joriy o‘rnatishga moslab qayta yozilishi uchun `openclaw doctor` buyrug‘ini ishga tushiring.

## Har doim ishga tushiring: `openclaw doctor`

Doctor — “xavfsiz yangilash” buyrug‘i. U ataylab zerikarli: ta’mirlash + migratsiya + ogohlantirish.

Eslatma: agar siz **manba o‘rnatma**da (git checkout) bo‘lsangiz, `openclaw doctor` avval `openclaw update` ni ishga tushirishni taklif qiladi.

Odatda bajaradigan ishlar:

- Eskirgan konfiguratsiya kalitlari / eski konfiguratsiya fayli joylashuvlarini migratsiya qiladi.
- DM siyosatlarini audit qiladi va xavfli “ochiq” sozlamalar bo‘yicha ogohlantiradi.
- Gateway holatini tekshiradi va qayta ishga tushirishni taklif qilishi mumkin.
- Eski gateway xizmatlarini (launchd/systemd; eski schtasks) joriy OpenClaw xizmatlariga aniqlaydi va migratsiya qiladi.
- Linux’da systemd user lingering’ni ta’minlaydi (Gateway logout’dan keyin ham ishlashi uchun).

Tafsilotlar: [Doctor](/gateway/doctor)

## Gateway’ni boshlash / to‘xtatish / qayta ishga tushirish

CLI (OS’dan qat’i nazar ishlaydi):

```bash
openclaw gateway status
openclaw gateway stop
openclaw gateway restart
openclaw gateway --port 18789
openclaw logs --follow
```

Agar siz nazorat ostida bo‘lsangiz:

- macOS launchd (ilova bilan birga keladigan LaunchAgent): `launchctl kickstart -k gui/$UID/bot.molt.gateway` ( `bot.molt.<profile>` dan foydalaning
  ; eski `com.openclaw.*` hamon ishlaydi)
- Linux systemd user xizmati: `systemctl --user restart openclaw-gateway[-<profile>].service`
- Windows (WSL2): `systemctl --user restart openclaw-gateway[-<profile>].service`
  - `launchctl`/`systemctl` faqat xizmat o‘rnatilgan bo‘lsa ishlaydi; aks holda `openclaw gateway install` ni ishga tushiring.

Runbook + aniq xizmat yorliqlari: [Gateway runbook](/gateway)

## Rollback / pinlash (nimadir buzilganda)

### Pinlash (global o‘rnatma)

Ishonchli versiyani o‘rnating (`<version>` ni oxirgi ishlagan versiya bilan almashtiring):

```bash
npm i -g openclaw@<version>
```

```bash
pnpm add -g openclaw@<version>
```

Maslahat: joriy e’lon qilingan versiyani ko‘rish uchun `npm view openclaw version` ni ishga tushiring.

So‘ng qayta ishga tushiring + doctor’ni yana ishga tushiring:

```bash
openclaw doctor
openclaw gateway restart
```

### Pinlash (manba) sana bo‘yicha

Ma’lum bir sanadan commit tanlang (misol: “2026-01-01 holatidagi main”):

```bash
git fetch origin
git checkout "$(git rev-list -n 1 --before=\"2026-01-01\" origin/main)"
```

So‘ng bog‘liqliklarni qayta o‘rnating + qayta ishga tushiring:

```bash
pnpm install
pnpm build
openclaw gateway restart
```

Agar keyinroq eng so‘nggiga qaytmoqchi bo‘lsangiz:

```bash
git checkout main
git pull
```

## Agar tiqilib qolsangiz

- `openclaw doctor` ni yana ishga tushiring va chiqishni diqqat bilan o‘qing (ko‘pincha yechimni aytadi).
- Tekshiring: [Troubleshooting](/gateway/troubleshooting)
- Discord’da so‘rang: [https://discord.gg/clawd](https://discord.gg/clawd)
