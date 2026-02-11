---
summary: "Nextcloud Talk qo‘llab-quvvatlash holati, imkoniyatlari va sozlamalari"
read_when:
  - Nextcloud Talk kanal funksiyalari ustida ishlash
title: "Nextcloud Talk"
---

# Nextcloud Talk (plagin)

Holat: plagin orqali qo‘llab-quvvatlanadi (webhook bot). To‘g‘ridan-to‘g‘ri xabarlar, xonalar, reaksiyalar va markdown xabarlar qo‘llab-quvvatlanadi.

## Plagin talab qilinadi

Nextcloud Talk ships as a plugin and is not bundled with the core install.

Install via CLI (npm registry):

```bash
openclaw plugins install @openclaw/nextcloud-talk
```

Mahalliy checkout (git repodan ishga tushirilganda):

```bash
openclaw plugins install ./extensions/nextcloud-talk
```

Agar sozlash/onboarding vaqtida Nextcloud Talk tanlansa va git checkout aniqlansa,
OpenClaw avtomatik ravishda mahalliy o‘rnatish yo‘lini taklif qiladi.

Tafsilotlar: [Plaginlar](/tools/plugin)

## Tezkor sozlash (boshlovchilar uchun)

1. Nextcloud Talk plaginini o‘rnating.

2. Nextcloud serveringizda bot yarating:

   ```bash
   ./occ talk:bot:install "OpenClaw" "<shared-secret>" "<webhook-url>" --feature reaction
   ```

3. Maqsadli xona sozlamalarida botni yoqing.

4. OpenClaw’ni sozlang:
   - Konfiguratsiya: `channels.nextcloud-talk.baseUrl` + `channels.nextcloud-talk.botSecret`
   - Yoki muhit o‘zgaruvchisi: `NEXTCLOUD_TALK_BOT_SECRET` (faqat standart akkaunt uchun)

5. Gateway’ni qayta ishga tushiring (yoki onboarding’ni yakunlang).

Minimal konfiguratsiya:

```json5
{
  channels: {
    "nextcloud-talk": {
      enabled: true,
      baseUrl: "https://cloud.example.com",
      botSecret: "shared-secret",
      dmPolicy: "pairing",
    },
  },
}
```

## Eslatmalar

- Botlar DMga tashabbus ko‘rsata olmaydi. Foydalanuvchi avval botga xabar yuborishi kerak.
- Webhook URL Gateway tomonidan yetib boriladigan bo‘lishi kerak; agar proksi ortida bo‘lsa, `webhookPublicUrl` ni sozlang.
- Media yuklash bot API tomonidan qo‘llab-quvvatlanmaydi; media URL sifatida yuboriladi.
- Webhook payload DM va xonalarni farqlamaydi; xona turini aniqlashni yoqish uchun `apiUser` + `apiPassword` ni sozlang (aks holda DMlar xonalar sifatida ko‘riladi).

## Kirish nazorati (DMlar)

- Standart: `channels.nextcloud-talk.dmPolicy = "pairing"`. Noma’lum yuboruvchilarga juftlash kodi beriladi.
- Approve via:
  - `openclaw pairing list nextcloud-talk`
  - `openclaw pairing approve nextcloud-talk <CODE>`
- Ochiq DMlar: `channels.nextcloud-talk.dmPolicy="open"` va `channels.nextcloud-talk.allowFrom=["*"]`.
- `allowFrom` faqat Nextcloud foydalanuvchi ID’lariga mos keladi; ko‘rinadigan nomlar e’tiborga olinmaydi.

## Xonalar (guruhlar)

- Standart: `channels.nextcloud-talk.groupPolicy = "allowlist"` (eslatma orqali cheklangan).
- `channels.nextcloud-talk.rooms` orqali ruxsat etilgan xonalar:

```json5
{
  channels: {
    "nextcloud-talk": {
      rooms: {
        "room-token": { requireMention: true },
      },
    },
  },
}
```

- Xonalarni umuman ruxsat etmaslik uchun allowlist’ni bo‘sh qoldiring yoki `channels.nextcloud-talk.groupPolicy="disabled"` qilib sozlang.

## Imkoniyatlar

| Xususiyat                   | Holat                  |
| --------------------------- | ---------------------- |
| To‘g‘ridan-to‘g‘ri xabarlar | Qo‘llab-quvvatlanadi   |
| Xonalar                     | Supported              |
| Mavzular                    | Qo‘llab-quvvatlanmaydi |
| Media                       | Faqat URL              |
| Reaksiyalar                 | Qo‘llab-quvvatlanadi   |
| Mahalliy buyruqlar          | Qo‘llab-quvvatlanmaydi |

## Konfiguratsiya ma’lumotnomasi (Nextcloud Talk)

To‘liq konfiguratsiya: [Configuration](/gateway/configuration)

Provayder parametrlari:

- `channels.nextcloud-talk.enabled`: kanalni ishga tushirishni yoqish/o‘chirish.
- `channels.nextcloud-talk.baseUrl`: Nextcloud instansiyasi URL manzili.
- `channels.nextcloud-talk.botSecret`: bot uchun umumiy maxfiy kalit.
- `channels.nextcloud-talk.botSecretFile`: maxfiy kalit fayli yo‘li.
- `channels.nextcloud-talk.apiUser`: xonalarni aniqlash uchun API foydalanuvchisi (DM aniqlash).
- `channels.nextcloud-talk.apiPassword`: API/app password for room lookups.
- `channels.nextcloud-talk.apiPasswordFile`: API password file path.
- `channels.nextcloud-talk.webhookPort`: webhook tinglovchi porti (standart: 8788).
- `channels.nextcloud-talk.webhookHost`: webhook xosti (standart: 0.0.0.0).
- `channels.nextcloud-talk.webhookPath`: webhook path (default: /nextcloud-talk-webhook).
- `channels.nextcloud-talk.webhookPublicUrl`: tashqi tomondan kirish mumkin bo‘lgan webhook URL.
- `channels.nextcloud-talk.dmPolicy`: `pairing | allowlist | open | disabled`.
- `channels.nextcloud-talk.allowFrom`: DM ruxsat etilgan ro‘yxati (foydalanuvchi IDlari). `open` uchun `"*"` talab qilinadi.
- `channels.nextcloud-talk.groupPolicy`: `allowlist | open | disabled`.
- `channels.nextcloud-talk.groupAllowFrom`: guruh ruxsat etilgan ro‘yxati (foydalanuvchi IDlari).
- `channels.nextcloud-talk.rooms`: har bir xona uchun sozlamalar va ruxsat etilgan ro‘yxat.
- `channels.nextcloud-talk.historyLimit`: guruh tarix chegarasi (0 o‘chiradi).
- `channels.nextcloud-talk.dmHistoryLimit`: DM tarix chegarasi (0 o‘chiradi).
- `channels.nextcloud-talk.dms`: har bir DM uchun alohida sozlamalar (historyLimit).
- `channels.nextcloud-talk.textChunkLimit`: chiqish matn bo‘lagi hajmi (belgilar).
- `channels.nextcloud-talk.chunkMode`: `length` (standart) yoki `newline` — uzunlik bo‘yicha bo‘lishdan oldin bo‘sh qatorlar (paragraf chegaralari) bo‘yicha ajratish.
- `channels.nextcloud-talk.blockStreaming`: ushbu kanal uchun blokli strimingni o‘chirish.
- `channels.nextcloud-talk.blockStreamingCoalesce`: blokli strimingni birlashtirishni sozlash.
- `channels.nextcloud-talk.mediaMaxMb`: kiruvchi media uchun maksimal hajm (MB).
