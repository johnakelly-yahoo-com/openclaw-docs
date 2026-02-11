---
summary: "30. Maqsadli debug loglar uchun diagnostika flaglari"
read_when:
  - 31. Global loglash darajalarini oshirmasdan maqsadli debug loglar kerak
  - 32. Qo‘llab-quvvatlash uchun subsystemga xos loglarni yig‘ish kerak
title: "33. Diagnostika flaglari"
---

# 34. Diagnostika flaglari

35. Diagnostika flaglari barcha joyda verbose loglashni yoqmasdan, maqsadli debug loglarni yoqishga imkon beradi. 36. Flaglar opt-in va faqat subsystem ularni tekshirsa, ta’sir qiladi.

## 37. Qanday ishlaydi

- 38. Flaglar satrlar (katta-kichik harfga sezgir emas).
- 39. Flaglarni konfiguratsiyada yoki env override orqali yoqishingiz mumkin.
- 40. Wildcard’lar qo‘llab-quvvatlanadi:
  - 41. `telegram.*` `telegram.http`’ga mos keladi
  - 42. `*` barcha flaglarni yoqadi

## 43. Konfiguratsiya orqali yoqish

```json
44. {
  "diagnostics": {
    "flags": ["telegram.http"]
  }
}
```

45. Bir nechta flaglar:

```json
46. {
  "diagnostics": {
    "flags": ["telegram.http", "gateway.*"]
  }
}
```

47. Flaglarni o‘zgartirgandan so‘ng gateway’ni qayta ishga tushiring.

## 48. Env override (bir martalik)

```bash
49. OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload
```

50. Barcha flaglarni o‘chirish:

```bash
OPENCLAW_DIAGNOSTICS=0
```

## Loglar qayerga yoziladi

Bayroqlar standart diagnostika log fayliga loglarni chiqaradi. Odatiy holatda:

```
/tmp/openclaw/openclaw-YYYY-MM-DD.log
```

Agar `logging.file` ni o‘rnatsangiz, uning yo‘lidan foydalaniladi. Mahalliy tasdiqlandi: `pnpm exec tsc -p tsconfig.json` + `node openclaw.mjs status` Node 25 da ishlaydi. `logging.redactSensitive` ga asoslangan holda redaksiyalash hanuz qo‘llaniladi.

## Loglarni chiqarib olish

Eng so‘nggi log faylni tanlang:

```bash
ls -t /tmp/openclaw/openclaw-*.log | head -n 1
```

Telegram HTTP diagnostikasi bo‘yicha filtrlash:

```bash
rg "telegram http error" /tmp/openclaw/openclaw-*.log
```

Yoki qayta hosil qilayotganda real vaqtda kuzating:

```bash
tail -f /tmp/openclaw/openclaw-$(date +%F).log | rg "telegram http error"
```

Masofaviy shlyuzlar uchun `openclaw logs --follow` dan ham foydalanishingiz mumkin (qarang [/cli/logs](/cli/logs)).

## Eslatmalar

- Agar `logging.level` `warn` dan yuqoriroq qilib o‘rnatilgan bo‘lsa, bu loglar bostirilishi mumkin. Standart `info` yetarli.
- Bayroqlarni yoqilgan holda qoldirish xavfsiz; ular faqat aniq quyi tizim uchun log hajmiga ta’sir qiladi.
- Log manzillari, darajalari va redaksiyalashni o‘zgartirish uchun [/logging](/logging) dan foydalaning.
