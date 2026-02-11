---
summary: "Envelope, prompt, tool va connectorlar bo‘ylab sana va vaqtni qayta ishlash"
read_when:
  - Siz model yoki foydalanuvchilarga ko‘rsatiladigan timestamp’lar qanday chiqishini o‘zgartiryapsiz
  - Xabarlar yoki system prompt chiqishidagi vaqt formatlashini tuzatyapsiz
title: "Sana va vaqt"
---

# Sana & vaqt

OpenClaw **transport timestamp’lari uchun host‑local vaqtni** va **faqat system prompt’da foydalanuvchi vaqt zonasini** standart sifatida ishlatadi.
Provayder timestamp’lari saqlanadi, shuning uchun tool’lar o‘zining tabiiy semantikasini saqlaydi (joriy vaqt `session_status` orqali mavjud).

## Xabar envelope’lari (standartda lokal)

Kirish xabarlari timestamp bilan o‘raladi (daqiqagacha aniqlikda):

```
[Provider ... 2026-01-05 16:26 PST] message text
```

Ushbu envelope timestamp’i provayder vaqt zonasidan qat’i nazar, **standartda host‑local** hisoblanadi.

Siz bu xatti-harakatni bekor qilishingiz mumkin:

```json5
{
  agents: {
    defaults: {
      envelopeTimezone: "local", // "utc" | "local" | "user" | IANA timezone
      envelopeTimestamp: "on", // "on" | "off"
      envelopeElapsed: "on", // "on" | "off"
    },
  },
}
```

- `envelopeTimezone: "utc"` UTC’dan foydalanadi.
- `envelopeTimezone: "local"` host vaqt zonasidan foydalanadi.
- `envelopeTimezone: "user"` `agents.defaults.userTimezone`’dan foydalanadi (host vaqt zonasiga qaytadi).
- Aniq IANA vaqt zonasini ishlating (masalan, `"America/Chicago"`) barqaror zona uchun.
- `envelopeTimestamp: "off"` envelope sarlavhalaridan mutlaq timestamp’larni olib tashlaydi.
- `envelopeElapsed: "off"` o‘tgan vaqt qo‘shimchalarini olib tashlaydi (`+2m` uslubi).

### Misollar

**Mahalliy (standart):**

```
[WhatsApp +1555 2026-01-18 00:19 PST] salom
```

**Foydalanuvchi vaqt zonasi:**

```
Swift generatori quyidagini hosil qiladi:
```

**O‘tgan vaqt yoqilgan:**

```
[WhatsApp +1555 +30s 2026-01-18T05:19Z] davomiy xabar
```

## [WhatsApp +1555 2026-01-18 00:19 CST] hello

Agar foydalanuvchi vaqt zonasi ma’lum bo‘lsa, tizim prompti keshni barqaror saqlash uchun **faqat vaqt zonasi** (soat/vaqt formatisiz) bilan alohida **Joriy sana va vaqt** bo‘limini o‘z ichiga oladi:

```
Vaqt zonasi: America/Chicago
```

Agentga joriy vaqt kerak bo‘lganda, `session_status` vositasidan foydalaning; status kartasida vaqt belgisi satri mavjud.

## Tizim hodisalari satrlari (standart bo‘yicha mahalliy)

Agent kontekstiga kiritilgan navbatdagi tizim hodisalari xabar konvertlari bilan bir xil vaqt zonasi tanlovidan foydalangan holda vaqt belgisi bilan prefiks qilinadi (standart: xost-mahalliy).

```
Tizim: [2026-01-12 12:19:17 PST] Model almashtirildi.
```

### Foydalanuvchi vaqt zonasi va formatini sozlash

```json5
{
  agents: {
    defaults: {
      userTimezone: "America/Chicago",
      timeFormat: "auto", // auto | 12 | 24
    },
  },
}
```

- `userTimezone` prompt konteksti uchun **foydalanuvchi-mahalliy vaqt zonasini** belgilaydi.
- `timeFormat` promptdagi **12/24 soatlik ko‘rinishni** boshqaradi. Tizim prompti: Joriy sana va vaqt

## Vaqt formatini aniqlash (auto)

`auto` OS sozlamalariga amal qiladi. Aniqlangan qiymat **har bir jarayon uchun keshda saqlanadi**, takroriy tizim chaqiruvlarini oldini olish uchun.

## Asbob payloadlari va konnektorlar (xom provayder vaqti + normallashtirilgan maydonlar)

Kanal asboblari **provayderga xos vaqt belgilarini** qaytaradi va izchillik uchun normallashtirilgan maydonlarni qo‘shadi:

- `timestampMs`: epoch millisekundlar (UTC)
- `timestampUtc`: ISO 8601 UTC qatori

Xom provayder maydonlari hech narsa yo‘qolmasligi uchun saqlanadi.

- Slack: API’dan epochga o‘xshash qatorlar
- Discord: UTC ISO vaqt belgilari
- Telegram/WhatsApp: provayderga xos raqamli/ISO vaqt belgilari

Agar sizga mahalliy vaqt kerak bo‘lsa, ma’lum vaqt zonasidan foydalanib, uni pastki qatlamda konvertatsiya qiling.

## Tegishli hujjatlar

- [System Prompt](/concepts/system-prompt)
- [Timezones](/concepts/timezone)
- [Messages](/concepts/messages)
