---
summary: "CLI reference for `openclaw models` (status/list/set/scan, aliases, fallbacks, auth)"
read_when:
  - You want to change default models or view provider auth status
  - You want to scan available models/providers and debug auth profiles
title: "models"
---

# `openclaw models`

Modelni aniqlash, skanerlash va sozlash (standart model, zaxira variantlar, autentifikatsiya profillari).

Bog‘liq:

- Provayderlar + modellar: [Models](/providers/models)
- Provayder autentifikatsiyasini sozlash: [Getting started](/start/getting-started)

## Umumiy buyruqlar

```bash
openclaw models status
openclaw models list
openclaw models set <model-or-alias>
openclaw models scan
```

`openclaw models status` aniqlangan standart/zaxira modellarni hamda autentifikatsiya bo‘yicha umumiy ko‘rinishni ko‘rsatadi.
Provayderdan foydalanish bo‘yicha snapshotlar mavjud bo‘lsa, OAuth/token holati bo‘limida provayderdan foydalanish sarlavhalari ko‘rsatiladi.
Har bir sozlangan provayder profili uchun jonli autentifikatsiya tekshiruvlarini ishga tushirish uchun `--probe` qo‘shing.
Tekshiruvlar haqiqiy so‘rovlar bo‘lib, tokenlarni sarflashi va tezlik cheklovlarini ishga tushirishi mumkin.
Sozlangan agentning model/auth holatini ko‘rish uchun `--agent <id>` dan foydalaning. Agar ko‘rsatilmasa, buyruq `OPENCLAW_AGENT_DIR`/`PI_CODING_AGENT_DIR` (agar o‘rnatilgan bo‘lsa) dan foydalanadi, aks holda sozlangan standart agent qo‘llaniladi.

Eslatmalar:

- `models set <model-or-alias>` `provider/model` yoki aliasni qabul qiladi.
- Model havolalari **birinchi** `/` bo‘yicha ajratib tahlil qilinadi. Agar model ID tarkibida `/` bo‘lsa (OpenRouter uslubida), provayder prefiksini kiriting (masalan: `openrouter/moonshotai/kimi-k2`).
- Agar provayderni ko‘rsatmasangiz, OpenClaw kiritmani alias yoki **standart provayder** uchun model sifatida qabul qiladi (faqat model ID da `/` bo‘lmaganda ishlaydi).

### `models status`

Variantlar:

- `--json`
- `--plain`
- `--check` (chiqish kodi 1=eskirgan/yo‘q, 2=muddati yaqin)
- `--probe` (sozlangan autentifikatsiya profillarini jonli tekshirish)
- `--probe-provider <name>` (bitta provayderni tekshirish)
- `--probe-profile <id>` (takrorlash yoki vergul bilan ajratilgan profil IDlari)
- `--probe-timeout <ms>`
- `--probe-concurrency <n>`
- `--probe-max-tokens <n>`
- `--agent <id>` (sozlangan agent ID; `OPENCLAW_AGENT_DIR`/`PI_CODING_AGENT_DIR` ni bekor qiladi)

## Aliaslar + zaxira variantlar

```bash
openclaw models aliases list
openclaw models fallbacks list
```

## Autentifikatsiya profillari

```bash
openclaw models auth add
openclaw models auth login --provider <id>
openclaw models auth setup-token
openclaw models auth paste-token
```

`models auth login` provayder plaginining autentifikatsiya jarayonini (OAuth/API kaliti) ishga tushiradi. Qaysi provayderlar o‘rnatilganini ko‘rish uchun `openclaw plugins list` dan foydalaning.

Eslatmalar:

- `setup-token` setup-token qiymatini so‘raydi (uni istalgan mashinada `claude setup-token` bilan yarating).
- `paste-token` boshqa joyda yoki avtomatlashtirish orqali yaratilgan token satrini qabul qiladi.
