---
summary: "43. OpenClaw’da OAuth: token almashinuvi, saqlash va ko‘p-hisobli andozalar"
read_when:
  - 44. Siz OpenClaw OAuth’ni boshidan oxirigacha tushunmoqchisiz
  - 45. Siz token bekor qilinishi / logout muammolariga duch keldingiz
  - 46. Siz setup-token yoki OAuth autentifikatsiya oqimlarini xohlaysiz
  - 47. Sizga bir nechta hisoblar yoki profil marshrutlash kerak
title: "48. OAuth"
---

# 49. OAuth

50. OpenClaw OAuth orqali “subscription auth”ni qo‘llab-quvvatlaydi (ayniqsa **OpenAI Codex (ChatGPT OAuth)**). Anthropic obunalari uchun **setup-token** oqimidan foydalaning. Ushbu sahifa quyidagilarni tushuntiradi:

- OAuth **token exchange** qanday ishlashi (PKCE)
- tokenlar qayerda **saqlanishi** (va nega)
- **bir nechta akkauntlar** bilan qanday ishlash (profilar + sessiya bo‘yicha override’lar)

OpenClaw, shuningdek, o‘z OAuth yoki API‑kalit oqimiga ega bo‘lgan **provider pluginlari**ni ham qo‘llab-quvvatlaydi. Ularni quyidagicha ishga tushiring:

```bash
openclaw models auth login --provider <id>
```

## Token sink (nega u mavjud)

OAuth providerlari odatda login/refresh oqimlari vaqtida **yangi refresh token** yaratadi. Ba’zi providerlar (yoki OAuth klientlari) bir xil foydalanuvchi/app uchun yangi token berilganda eski refresh tokenlarni bekor qilishi mumkin.

Amaliy alomat:

- siz OpenClaw orqali _va_ Claude Code / Codex CLI orqali login qilasiz → ulardan biri keyinroq tasodifan “logout” bo‘lib qoladi

Buni kamaytirish uchun OpenClaw `auth-profiles.json` ni **token sink** sifatida ko‘radi:

- runtime credential’larni **bitta joydan** o‘qiydi
- biz bir nechta profilni saqlab, ularni deterministik tarzda yo‘naltira olamiz

## Saqlash (tokenlar qayerda yashaydi)

Sirlar **har bir agent** bo‘yicha saqlanadi:

- Auth profillari (OAuth + API kalitlar): `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- Runtime kesh (avtomatik boshqariladi; tahrirlamang): `~/.openclaw/agents/<agentId>/agent/auth.json`

Legacy faqat-import fayli (hali ham qo‘llab-quvvatlanadi, lekin asosiy ombor emas):

- `~/.openclaw/credentials/oauth.json` (birinchi foydalanishda `auth-profiles.json` ga import qilinadi)

Yuqoridagilarning barchasi `$OPENCLAW_STATE_DIR` ni ham hurmat qiladi (state dir override). To‘liq ma’lumotnoma: [/gateway/configuration](/gateway/configuration#auth-storage-oauth--api-keys)

## Anthropic setup-token (obuna autentifikatsiyasi)

Istalgan mashinada `claude setup-token` ni ishga tushiring, so‘ng uni OpenClaw’ga joylashtiring:

```bash
openclaw models auth setup-token --provider anthropic
```

Agar tokenni boshqa joyda yaratgan bo‘lsangiz, uni qo‘lda joylashtiring:

```bash
openclaw models auth paste-token --provider anthropic
```

Tekshirish:

```bash
openclaw models status
```

## OAuth exchange (login qanday ishlaydi)

OpenClaw’ning interaktiv login oqimlari `@mariozechner/pi-ai` da amalga oshirilgan va wizardlar/buyruqlarga ulangan.

### Anthropic (Claude Pro/Max) setup-token

Oqim shakli:

1. `claude setup-token` ni ishga tushiring
2. tokenni OpenClaw’ga joylashtiring
3. token auth profili sifatida saqlang (refresh yo‘q)

Wizard yo‘li: `openclaw onboard` → auth tanlovi `setup-token` (Anthropic).

### OpenAI Codex (ChatGPT OAuth)

Oqim shakli (PKCE):

1. PKCE verifier/challenge + tasodifiy `state` yarating
2. `https://auth.openai.com/oauth/authorize?...` ni oching
3. `http://127.0.0.1:1455/auth/callback` da callback’ni ushlashga harakat qiling
4. agar callback bog‘lana olmasa (yoki siz remote/headless bo‘lsangiz), redirect URL/kodni joylashtiring
5. `https://auth.openai.com/oauth/token` da exchange qiling
6. access token’dan `accountId` ni ajrating va `{ access, refresh, expires, accountId }` ni saqlang

Wizard yo‘li: `openclaw onboard` → auth tanlovi `openai-codex`.

## Refresh + muddati tugashi

Profillar `expires` vaqt tamg‘asini saqlaydi.

Ish vaqtida:

- `expires` kelajakda bo‘lsa → saqlangan access token’dan foydalaning
- agar muddati tugagan bo‘lsa → yangilang (fayl lock ostida) va saqlangan credential’larni ustiga yozing

Refresh jarayoni avtomatik; odatda tokenlarni qo‘lda boshqarishingiz shart emas.

## Bir nechta akkauntlar (profil) + marshrutlash

Ikki naqsh:

### 1. Afzal: alohida agentlar

Agar “personal” va “work” hech qachon o‘zaro aralashmasin desangiz, izolyatsiyalangan agentlardan foydalaning (alohida sessiyalar + credential’lar + workspace):

```bash
openclaw agents add work
openclaw agents add personal
```

So‘ng har bir agent uchun auth’ni sozlang (wizard orqali) va chatlarni mos agentga yo‘naltiring.

### 2. Kengaytirilgan: bitta agentda bir nechta profil

`auth-profiles.json` bir xil provider uchun bir nechta profile ID’larni qo‘llab-quvvatlaydi.

Qaysi profil ishlatilishini tanlang:

- global tarzda config tartibi orqali (`auth.order`)
- sessiya bo‘yicha `/model ...@<profileId>` orqali

Misol (sessiya override):

- `/model Opus@anthropic:work`

Qaysi profile ID’lar mavjudligini qanday ko‘rish mumkin:

- `openclaw channels list --json` (`auth[]` ni ko‘rsatadi)

Bog‘liq hujjatlar:

- [/concepts/model-failover](/concepts/model-failover) (rotatsiya + cooldown qoidalari)
- [/tools/slash-commands](/tools/slash-commands) (buyruqlar yuzasi)
