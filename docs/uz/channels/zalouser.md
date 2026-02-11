---
summary: "zca-cli (QR orqali kirish), imkoniyatlar va konfiguratsiya orqali Zalo shaxsiy akkauntini qo‘llab-quvvatlash"
read_when:
  - OpenClaw uchun Zalo Personal’ni sozlash
  - Zalo Personal’ga kirish yoki xabar oqimini nosozliklarni aniqlash
title: "Zalo Personal"
---

# Zalo Personal (norasmiy)

Holat: eksperimental. Ushbu integratsiya `zca-cli` orqali **shaxsiy Zalo akkaunti**ni avtomatlashtiradi.

> **Ogohlantirish:** Bu norasmiy integratsiya bo‘lib, akkauntning to‘xtatilishi/bloklanishiga olib kelishi mumkin. O‘zingizning xavfingizga foydalaning.

## Plagin talab qilinadi

Zalo Personal plagin sifatida yetkaziladi va asosiy o‘rnatmaga kiritilmagan.

- CLI orqali o‘rnating: `openclaw plugins install @openclaw/zalouser`
- Yoki manba kodidan: `openclaw plugins install ./extensions/zalouser`
- Tafsilotlar: [Plugins](/tools/plugin)

## Talab: zca-cli

Gateway mashinasida `PATH` ichida `zca` binari mavjud bo‘lishi kerak.

- Tekshirish: `zca --version`
- Agar mavjud bo‘lmasa, zca-cli’ni o‘rnating (qarang `extensions/zalouser/README.md` yoki rasmiy zca-cli hujjatlari).

## Tezkor sozlash (boshlovchilar uchun)

1. Plaginni o‘rnating (yuqorida ko‘rsatilgan).
2. 1. Kirish (QR, Gateway mashinasida):
   - 2. `openclaw channels login --channel zalouser`
   - 3. Terminaldagi QR-kodni Zalo mobil ilovasi bilan skaner qiling.
3. 4. Kanalni yoqing:

```json5
5. {
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

4. 6. Gateway’ni qayta ishga tushiring (yoki onboarding’ni yakunlang).
5. 7. DM kirishi sukut bo‘yicha pairing; birinchi aloqada pairing kodini tasdiqlang.

## 8) Bu nima

- 9. Kiruvchi xabarlarni qabul qilish uchun `zca listen` dan foydalanadi.
- 10. Javoblarni (matn/media/havola) yuborish uchun `zca msg ...` dan foydalanadi.
- 11. Zalo Bot API mavjud bo‘lmagan “shaxsiy akkaunt” foydalanish holatlari uchun mo‘ljallangan.

## 12. Nomi

13. Kanal identifikatori `zalouser` — bu **shaxsiy Zalo foydalanuvchi akkaunti** (norasmiy) avtomatlashtirilishini aniq ko‘rsatish uchun. 14. `zalo` nomini kelajakda ehtimoliy rasmiy Zalo API integratsiyasi uchun zaxirada saqlaymiz.

## 15. ID’larni topish (katalog)

16. Peer/guruhlarni va ularning ID’larini aniqlash uchun katalog CLI’dan foydalaning:

```bash
17. openclaw directory self --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory groups list --channel zalouser --query "work"
```

## 18. Cheklovlar

- 19. Chiquvchi matn ~2000 belgiga bo‘linadi (Zalo mijoz cheklovlari).
- 20. Streaming sukut bo‘yicha bloklangan.

## 21. Kirishni boshqarish (DM’lar)

22. `channels.zalouser.dmPolicy` qo‘llab-quvvatlaydi: `pairing | allowlist | open | disabled` (sukut bo‘yicha: `pairing`).
23. `channels.zalouser.allowFrom` foydalanuvchi ID’lari yoki nomlarini qabul qiladi. 24. Mavjud bo‘lsa, ustoz (wizard) nomlarni `zca friend find` orqali ID’larga aniqlaydi.

25. Tasdiqlash:

- 26. `openclaw pairing list zalouser`
- 27. `openclaw pairing approve zalouser <code>`

## 28. Guruhga kirish (ixtiyoriy)

- 29. Sukut bo‘yicha: `channels.zalouser.groupPolicy = "open"` (guruhlar ruxsat etilgan). 30. Belgilanmagan bo‘lsa, sukutni bekor qilish uchun `channels.defaults.groupPolicy` dan foydalaning.
- 31. Allowlist bilan cheklash:
  - 32. `channels.zalouser.groupPolicy = "allowlist"`
  - 33. `channels.zalouser.groups` (kalitlar — guruh ID’lari yoki nomlari)
- 34. Barcha guruhlarni bloklash: `channels.zalouser.groupPolicy = "disabled"`.
- 35. Sozlash ustasi guruh allowlist’lari uchun so‘rov berishi mumkin.
- 36. Ishga tushishda OpenClaw allowlist’dagi guruh/foydalanuvchi nomlarini ID’larga aniqlaydi va moslikni log qiladi; aniqlanmagan yozuvlar kiritilgandek saqlanadi.

37. Misol:

```json5
38. {
  channels: {
    zalouser: {
      groupPolicy: "allowlist",
      groups: {
        "123456789": { allow: true },
        "Work Chat": { allow: true },
      },
    },
  },
}
```

## 39. Ko‘p akkauntli

40. Akkauntlar zca profillariga mos keladi. 41. Misol:

```json5
42. {
  channels: {
    zalouser: {
      enabled: true,
      defaultAccount: "default",
      accounts: {
        work: { enabled: true, profile: "work" },
      },
    },
  },
}
```

## 43. Nosozliklarni bartaraf etish

44. **`zca` topilmadi:**

- 45. zca-cli’ni o‘rnating va Gateway jarayoni uchun u `PATH`da ekanini ta’minlang.

46. **Kirish saqlanmayapti:**

- 47. `openclaw channels status --probe`
- 48. Qayta kirish: `openclaw channels logout --channel zalouser && openclaw channels login --channel zalouser`
