---
summary: "Fast channel level troubleshooting with per channel failure signatures and fixes"
read_when:
  - Channel transport says connected but replies fail
  - You need channel specific checks before deep provider docs
title: "Channel Troubleshooting"
---

# Channel troubleshooting

Use this page when a channel connects but behavior is wrong.

## Command ladder

Run these in order first:

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Healthy baseline:

- `Runtime: running`
- `RPC probe: ok`
- Channel probe shows connected/ready

## WhatsApp

### WhatsApp failure signatures

| Symptom                         | Fastest check                                       | Fix                                                                                        |
| ------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Connected but no DM replies     | `openclaw pairing list whatsapp`                    | Approve sender or switch DM policy/allowlist.                              |
| Group messages ignored          | Check `requireMention` + mention patterns in config | Mention the bot or relax mention policy for that group.                    |
| Random disconnect/relogin loops | `openclaw channels status --probe` + loglar         | Qayta kirib chiqing va hisob maʼlumotlari katalogi soz ekanini tekshiring. |

Toʻliq nosozliklarni bartaraf etish: [/channels/whatsapp#troubleshooting-quick](/channels/whatsapp#troubleshooting-quick)

## Telegram

### Telegram nosozlik alomatlari

| Alomat                                                | Eng tezkor tekshiruv                                                                    | Yechim                                                                                           |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `/start`, ammo foydalanib bo‘ladigan javob oqimi yo‘q | `openclaw pairing list telegram`                                                        | Ulanishni tasdiqlang yoki DM siyosatini o‘zgartiring.                            |
| Bot onlayn, ammo guruh jim                            | Eslatib o‘tish (mention) talabi va bot maxfiylik rejimini tekshiring | Guruhda ko‘rinishi uchun maxfiylik rejimini o‘chiring yoki botni mention qiling. |
| Tarmoq xatolari bilan yuborish muvaffaqiyatsiz        | Telegram API chaqiruvlari xatolari uchun loglarni tekshiring                            | `api.telegram.org` ga DNS/IPv6/proksi marshrutlashini tuzating.                  |

Toʻliq nosozliklarni bartaraf etish: [/channels/telegram#troubleshooting](/channels/telegram#troubleshooting)

## Discord

### Discord nosozlik alomatlari

| Alomat                                   | Eng tezkor tekshiruv                                                   | Yechim                                                                                             |
| ---------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Bot onlayn, ammo guilddan javob yo‘q     | `openclaw channels status --probe`                                     | Guild/kanalga ruxsat bering va xabar mazmuni intentini tekshiring.                 |
| Guruh xabarlari e’tiborsiz qoldirilmoqda | Mention cheklovi sababli tashlab yuborishlar uchun loglarni tekshiring | Botni mention qiling yoki guild/kanal uchun `requireMention: false` qilib qo‘ying. |
| DM javoblari yo‘q                        | `openclaw pairing list discord`                                        | DM ulanishini tasdiqlang yoki DM siyosatini moslang.                               |

Toʻliq nosozliklarni bartaraf etish: [/channels/discord#troubleshooting](/channels/discord#troubleshooting)

## Slack

### Slack nosozlik alomatlari

| Alomat                                    | Eng tezkor tekshiruv                           | Yechim                                                                           |
| ----------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------- |
| Socket rejimi ulangan, ammo javoblar yo‘q | `openclaw channels status --probe`             | Ilova tokeni va bot tokenini hamda zarur scope’larni tekshiring. |
| DMlar bloklangan                          | `openclaw pairing list slack`                  | Ulanishni tasdiqlang yoki DM siyosatini yumshating.              |
| Kanal xabari e’tiborsiz qoldirildi        | `groupPolicy` va kanal allowlistini tekshiring | Kanalga ruxsat bering yoki siyosatni `open` ga o‘tkazing.        |

Toʻliq nosozliklarni bartaraf etish: [/channels/slack#troubleshooting](/channels/slack#troubleshooting)

## iMessage va BlueBubbles

### iMessage va BlueBubbles nosozlik alomatlari

| Belgi                                                                      | 2. Eng tezkor tekshiruv                                      | 3. Tuzatish                                                                                 |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 4. Kiruvchi hodisalar yo‘q                          | 5. Webhook/serverga ulanish va ilova ruxsatlarini tekshiring | 6. Webhook URL manzilini yoki BlueBubbles server holatini tuzating.         |
| 7. macOS’da yuborish mumkin, lekin qabul qilinmaydi | Messages avtomatlashtirish uchun macOS maxfiylik ruxsatlarini tekshiring            | 9. TCC ruxsatlarini qayta bering va kanal jarayonini qayta ishga tushiring. |
| 10. DM yuboruvchi bloklangan                        | `openclaw pairing list imessage` yoki `openclaw pairing list bluebubbles`           | Juftlashni tasdiqlang yoki ruxsatlar ro‘yxatini yangilang.                                         |

To‘liq nosozliklarni bartaraf etish:

- 14. [/channels/imessage#troubleshooting-macos-privacy-and-security-tcc](/channels/imessage#troubleshooting-macos-privacy-and-security-tcc)
- [/channels/bluebubbles#troubleshooting](/channels/bluebubbles#troubleshooting)

## 16. Signal

### Signal nosozligi imzolari

| 18. Alomat                          | 19. Eng tezkor tekshiruv                                 | 20. Tuzatish                                                                                         |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 21. Demon mavjud, lekin bot jim     | 22. `openclaw channels status --probe`                   | 23. `signal-cli` demon URL/manzilini, akkauntni va qabul qilish rejimini tekshiring. |
| 24. DM bloklangan                   | 25. `openclaw pairing list signal`                       | 26. Yuboruvchini tasdiqlang yoki DM siyosatini sozlang.                              |
| 27. Guruh javoblari ishga tushmaydi | 28. Guruh allowlistini va mention naqshlarini tekshiring | 29. Yuboruvchi/guruhni qo‘shing yoki cheklovlarni yumshating.                        |

30. To‘liq nosozliklarni bartaraf etish: [/channels/signal#troubleshooting](/channels/signal#troubleshooting)

## 31. Matrix

### 32. Matrix nosozlik belgilari

| 33. Alomat                                                        | 34. Eng tezkor tekshiruv                                  | 35. Tuzatish                                                                                             |
| ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 36. Tizimga kirilgan, lekin xona xabarlarini e’tiborsiz qoldiradi | 37. `openclaw channels status --probe`                    | 38. `groupPolicy` va xona allowlistini tekshiring.                                       |
| 39. DMlar qayta ishlanmaydi                                       | 40. `openclaw pairing list matrix`                        | 41. Yuboruvchini tasdiqlang yoki DM siyosatini sozlang.                                  |
| 42. Shifrlangan xonalar ishlamaydi                                | 43. Kripto modulini va shifrlash sozlamalarini tekshiring | 44. Shifrlash qo‘llab-quvvatlashini yoqing va xonaga qayta qo‘shiling/sinxronlashtiring. |

45. To‘liq nosozliklarni bartaraf etish: [/channels/matrix#troubleshooting](/channels/matrix#troubleshooting)
