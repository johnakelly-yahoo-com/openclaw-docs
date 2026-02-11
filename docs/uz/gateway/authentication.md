---
summary: "Model autentifikatsiyasi: OAuth, API kalitlari va setup-token"
read_when:
  - Model autentifikatsiyasi yoki OAuth muddati tugashini debug qilish
  - Autentifikatsiya yoki credential saqlashni hujjatlashtirish
title: "Autentifikatsiya"
---

# Autentifikatsiya

OpenClaw model provayderlari uchun OAuth va API kalitlarini qo‘llab-quvvatlaydi. Anthropic hisoblari uchun **API kalit**dan foydalanishni tavsiya qilamiz. Claude obuna orqali kirish uchun, `claude setup-token` orqali yaratilgan uzoq muddatli token’dan foydalaning.

To‘liq OAuth oqimi va saqlash joylashuvi uchun [/concepts/oauth](/concepts/oauth) ga qarang.

## Tavsiya etilgan Anthropic sozlamasi (API kalit)

Agar Anthropic’dan to‘g‘ridan-to‘g‘ri foydalansangiz, API kalitdan foydalaning.

1. Anthropic Console’da API kalit yarating.
2. Uni **gateway host** ga joylashtiring ( `openclaw gateway` ishlayotgan mashina).

```bash
export ANTHROPIC_API_KEY="..."
openclaw models status
```

3. Agar Gateway systemd/launchd ostida ishlayotgan bo‘lsa, demon o‘qiy olishi uchun kalitni `~/.openclaw/.env` ga qo‘yish ma’qul:

```bash
cat >> ~/.openclaw/.env <<'EOF'
ANTHROPIC_API_KEY=...
EOF
```

So‘ng demonni (yoki Gateway jarayonini) qayta ishga tushiring va yana tekshiring:

```bash
openclaw models status
openclaw doctor
```

Agar env o‘zgaruvchilarni o‘zingiz boshqarishni istamasangiz, onboarding wizard demon foydalanishi uchun API kalitlarni saqlab qo‘yishi mumkin: `openclaw onboard`.

Env merosxo‘rligi (`env.shellEnv`, `~/.openclaw/.env`, systemd/launchd) tafsilotlari uchun [Help](/help) ga qarang.

## Anthropic: setup-token (obuna autentifikatsiyasi)

Anthropic uchun tavsiya etilgan yo‘l — **API kalit**. Agar Claude obunasidan foydalansangiz, setup-token oqimi ham qo‘llab-quvvatlanadi. Uni **gateway host** da ishga tushiring:

```bash
claude setup-token
```

So‘ng uni OpenClaw’ga joylashtiring:

```bash
openclaw models auth setup-token --provider anthropic
```

Agar token boshqa mashinada yaratilgan bo‘lsa, uni qo‘lda joylashtiring:

```bash
openclaw models auth paste-token --provider anthropic
```

Agar quyidagiga o‘xshash Anthropic xatosini ko‘rsangiz:

```
This credential is only authorized for use with Claude Code and cannot be used for other API requests.
```

…uning o‘rniga Anthropic API kalitidan foydalaning.

Tokenni qo‘lda kiritish (istalgan provayder; `auth-profiles.json` yoziladi + konfiguratsiya yangilanadi):

```bash
openclaw models auth paste-token --provider anthropic
openclaw models auth paste-token --provider openrouter
```

Avtomatlashtirishga qulay tekshiruv (muddati tugagan/yo‘q bo‘lsa `1`, tugash arafasida bo‘lsa `2` chiqadi):

```bash
openclaw models status --check
```

Ixtiyoriy ops skriptlari (systemd/Termux) bu yerda hujjatlashtirilgan:
[/automation/auth-monitoring](/automation/auth-monitoring)

> `claude setup-token` requires an interactive TTY.

## Checking model auth status

```bash
openclaw models status
openclaw doctor
```

## Controlling which credential is used

### Per-session (chat command)

Use `/model <alias-or-id>@<profileId>` to pin a specific provider credential for the current session (example profile ids: `anthropic:default`, `anthropic:work`).

Use `/model` (or `/model list`) for a compact picker; use `/model status` for the full view (candidates + next auth profile, plus provider endpoint details when configured).

### Per-agent (CLI override)

Set an explicit auth profile order override for an agent (stored in that agent’s `auth-profiles.json`):

```bash
openclaw models auth order get --provider anthropic
openclaw models auth order set --provider anthropic anthropic:default
openclaw models auth order clear --provider anthropic
```

Use `--agent <id>` to target a specific agent; omit it to use the configured default agent.

## Troubleshooting

### “No credentials found”

If the Anthropic token profile is missing, run `claude setup-token` on the
**gateway host**, then re-check:

```bash
openclaw models status
```

### Token expiring/expired

Run `openclaw models status` to confirm which profile is expiring. If the profile
is missing, rerun `claude setup-token` and paste the token again.

## Requirements

- Claude Max or Pro subscription (for `claude setup-token`)
- Claude Code CLI installed (`claude` command available)
