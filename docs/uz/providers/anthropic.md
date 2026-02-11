---
summary: "Anthropic Claude’dan API kalitlari yoki OpenClaw’dagi setup-token orqali foydalaning"
read_when:
  - Siz OpenClaw’da Anthropic modellaridan foydalanmoqchisiz
  - Siz API kalitlari o‘rniga setup-token’dan foydalanmoqchisiz
title: "Anthropic"
---

# Anthropic (Claude)

Anthropic **Claude** model oilasini yaratadi va API orqali ularga kirish imkonini beradi.
OpenClaw’da siz API kalit yoki **setup-token** yordamida autentifikatsiya qilishingiz mumkin.

## Variant A: Anthropic API kaliti

**Eng mos:** standart API kirishi va foydalanishga asoslangan billing uchun.
Anthropic Console’da API kalitingizni yarating.

### CLI sozlash

```bash
openclaw onboard
# tanlang: Anthropic API key

# yoki nointeraktiv
openclaw onboard --anthropic-api-key "$ANTHROPIC_API_KEY"
```

### Konfiguratsiya parchasi

```json5
{
  env: { ANTHROPIC_API_KEY: "sk-ant-..." },
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

## Prompt keshleme (Anthropic API)

OpenClaw Anthropic’ning prompt keshleme funksiyasini qo‘llab-quvvatlaydi. Bu **faqat API uchun**; obuna autentifikatsiyasi kesh sozlamalarini hisobga olmaydi.

### Konfiguratsiya

Model konfiguratsiyangizda `cacheRetention` parametridan foydalaning:

| Qiymat  | Kesh davomiyligi | Tavsif                                                           |
| ------- | ---------------- | ---------------------------------------------------------------- |
| `none`  | Keshleme yo‘q    | Prompt keshlemeni o‘chirish                                      |
| `short` | 5 daqiqa         | API kaliti autentifikatsiyasi uchun standart                     |
| `long`  | 1 soat           | Kengaytirilgan kesh (beta flag talab etiladi) |

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": {
          params: { cacheRetention: "long" },
        },
      },
    },
  },
}
```

### Standart sozlamalar

Anthropic API Key autentifikatsiyasidan foydalanganda, OpenClaw barcha Anthropic modellari uchun avtomatik ravishda `cacheRetention: "short"` (5 daqiqalik kesh) ni qo‘llaydi. Buni konfiguratsiyangizda `cacheRetention` ni aniq belgilash orqali o‘zgartirishingiz mumkin.

### Eski parametr

Avvalgi `cacheControlTtl` parametri orqaga moslik uchun hali ham qo‘llab-quvvatlanadi:

- `"5m"` → `short` ga mos keladi
- `"1h"` → `long` ga mos keladi

Yangi `cacheRetention` parametriga o‘tishni tavsiya qilamiz.

OpenClaw Anthropic API so‘rovlari uchun `extended-cache-ttl-2025-04-11` beta bayrog‘ini o‘z ichiga oladi; agar provayder sarlavhalarini o‘zgartirsangiz, uni saqlab qoling (qarang: [/gateway/configuration](/gateway/configuration)).

## Variant B: Claude setup-token

**Eng mos:** Claude obunangizdan foydalanish.

### Setup-token’ni qayerdan olish mumkin

Setup-tokenlar Anthropic Console emas, balki **Claude Code CLI** tomonidan yaratiladi. Buni **istalgan qurilmada** ishga tushirishingiz mumkin:

```bash
claude setup-token
```

Tokenni OpenClaw’ga joylashtiring (wizard: **Anthropic token (paste setup-token)**) yoki uni gateway host’da ishga tushiring:

```bash
openclaw models auth setup-token --provider anthropic
```

Agar tokenni boshqa qurilmada yaratgan bo‘lsangiz, uni joylashtiring:

```bash
openclaw models auth paste-token --provider anthropic
```

### CLI sozlash (setup-token)

```bash
# Paste a setup-token during onboarding
openclaw onboard --auth-choice setup-token
```

### Config parchasi (setup-token)

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

## Eslatmalar

- `claude setup-token` yordamida setup-token yarating va uni joylashtiring yoki gateway host’da `openclaw models auth setup-token` ni ishga tushiring.
- Agar Claude obunasida “OAuth token refresh failed …” xabarini ko‘rsangiz, setup-token bilan qayta autentifikatsiya qiling. Qarang: [/gateway/troubleshooting#oauth-token-refresh-failed-anthropic-claude-subscription](/gateway/troubleshooting#oauth-token-refresh-failed-anthropic-claude-subscription).
- Autentifikatsiya tafsilotlari va qayta foydalanish qoidalari [/concepts/oauth](/concepts/oauth) da keltirilgan.

## Nosozliklarni bartaraf etish

**401 xatolar / token kutilmaganda yaroqsiz**

- Claude obunasi autentifikatsiyasi muddati tugashi yoki bekor qilinishi mumkin. `claude setup-token` ni qayta ishga tushiring
  va uni **gateway host** ga joylashtiring.
- Agar Claude CLI login’i boshqa qurilmada bo‘lsa,
  `openclaw models auth paste-token --provider anthropic` ni gateway host’da ishlating.

**Provayder "anthropic" uchun API kalit topilmadi**

- Autentifikatsiya **har bir agent uchun alohida**. Yangi agentlar asosiy agentning kalitlarini meros qilib olmaydi.
- Ushbu agent uchun onboarding’ni qayta ishga tushiring yoki gateway host’da setup-token / API kalitni joylashtiring, so‘ng `openclaw models status` bilan tekshiring.

**`anthropic:default` profili uchun hisob ma’lumotlari topilmadi**

- Qaysi autentifikatsiya profili faol ekanini ko‘rish uchun `openclaw models status` ni ishga tushiring.
- Onboarding’ni qayta ishga tushiring yoki shu profil uchun setup-token / API kalitni joylashtiring.

**Mavjud autentifikatsiya profili yo‘q (barchasi cooldown/yaroqsiz)**

- `auth.unusableProfiles` ni tekshirish uchun `openclaw models status --json` ni ko‘ring.
- Yana bir Anthropic profilini qo‘shing yoki cooldown tugashini kuting.

Batafsil: [/gateway/troubleshooting](/gateway/troubleshooting) va [/help/faq](/help/faq).
