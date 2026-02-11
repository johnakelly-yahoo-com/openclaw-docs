---
summary: "OpenClaw muhit o‘zgaruvchilarini qayerdan yuklaydi va ustuvorlik tartibi"
read_when:
  - Qaysi env o‘zgaruvchilar yuklanishini va qaysi tartibda ekanini bilishingiz kerak
  - Gateway’da API kalitlari yetishmayotganini nosozlikdan o‘tkazyapsiz
  - Provayder autentifikatsiyasi yoki deployment muhitlarini hujjatlashtiryapsiz
title: "Environment Variables"
---

# Muhit o‘zgaruvchilari

OpenClaw muhit o‘zgaruvchilarini bir nechta manbalardan oladi. Qoidasi: **mavjud qiymatlarni hech qachon almashtirmaslik**.

## Ustuvorlik (eng yuqori → eng past)

1. **Jarayon muhiti** (Gateway jarayoni ota shell/daemon’dan allaqachon olganlari).
2. **Joriy ishchi katalogdagi `.env`** (dotenv standarti; ustiga yozmaydi).
3. **Global `.env`** `~/.openclaw/.env` da (ya’ni `$OPENCLAW_STATE_DIR/.env`; ustiga yozmaydi).
4. **Config `env` bloki** `~/.openclaw/openclaw.json` ichida (faqat yetishmasa qo‘llanadi).
5. **Ixtiyoriy login-shell importi** (`env.shellEnv.enabled` yoki `OPENCLAW_LOAD_SHELL_ENV=1`), faqat kutilgan kalitlar yetishmaganda qo‘llanadi.

Agar config fayli umuman mavjud bo‘lmasa, 4-qadam o‘tkazib yuboriladi; shell importi yoqilgan bo‘lsa baribir ishlaydi.

## Config `env` bloki

Inline env o‘zgaruvchilarni o‘rnatishning ikki ekvivalent usuli (ikkalasi ham ustiga yozmaydi):

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
  },
}
```

## Shell env importi

`env.shellEnv` login shell’ingizni ishga tushiradi va faqat **yetishmayotgan** kutilgan kalitlarni import qiladi:

```json5
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

Env var ekvivalentlari:

- `OPENCLAW_LOAD_SHELL_ENV=1`
- `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`

## Config ichida env varlarni almashtirish

Config string qiymatlarida env varlarni `${VAR_NAME}` sintaksisi orqali to‘g‘ridan-to‘g‘ri murojaat qilishingiz mumkin:

```json5
{
  models: {
    providers: {
      "vercel-gateway": {
        apiKey: "${VERCEL_GATEWAY_API_KEY}",
      },
    },
  },
}
```

Batafsil ma’lumotlar uchun [Configuration: Env var substitution](/gateway/configuration#env-var-substitution-in-config) ga qarang.

## Yo‘lga oid muhit o‘zgaruvchilari

| O‘zgaruvchi            | Maqsad                                                                                                                                                                                                                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `OPENCLAW_HOME`        | Barcha ichki yo‘l aniqlashlari uchun ishlatiladigan uy katalogini almashtiradi (`~/.openclaw/`, agent kataloglari, sessiyalar, hisob ma’lumotlari). OpenClaw’ni maxsus xizmat foydalanuvchisi sifatida ishga tushirganda foydali. |
| `OPENCLAW_STATE_DIR`   | Holat katalogini almashtiradi (standart `~/.openclaw`).                                                                                                                                                                                           |
| `OPENCLAW_CONFIG_PATH` | Konfiguratsiya fayli yo‘lini almashtiradi (standart `~/.openclaw/openclaw.json`).                                                                                                                                                                 |

### `OPENCLAW_HOME`

O‘rnatilganda, `OPENCLAW_HOME` barcha ichki yo‘l aniqlashlari uchun tizim uy katalogini (`$HOME` / `os.homedir()`) almashtiradi. Bu headless xizmat akkauntlari uchun to‘liq fayl tizimi izolyatsiyasini ta’minlaydi.

**Ustuvorlik:** `OPENCLAW_HOME` > `$HOME` > `USERPROFILE` > `os.homedir()`

**Misol** (macOS LaunchDaemon):

```xml
<key>EnvironmentVariables</key>
<dict>
  <key>OPENCLAW_HOME</key>
  <string>/Users/kira</string>
</dict>
```

`OPENCLAW_HOME` ni tilda yo‘li sifatida ham o‘rnatish mumkin (masalan `~/svc`), u ishlatishdan oldin `$HOME` yordamida kengaytiriladi.

## Bog‘liq

- [Gateway configuration](/gateway/configuration)
- [FAQ: env vars and .env loading](/help/faq#env-vars-and-env-loading)
- [Models overview](/concepts/models)
