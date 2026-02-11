---
summary: "`openclaw cron` uchun CLI ma’lumotnomasi (fon vazifalarini rejalashtirish va ishga tushirish)"
read_when:
  - Rejalashtirilgan vazifalar va uyg‘otishlar kerak
  - Cron bajarilishi va loglarini nosozlikdan o‘tkazyapsiz
title: "cron"
---

# `openclaw cron`

Gateway rejalashtirgichi uchun cron vazifalarini boshqarish.

Bog‘liq:

- Cron vazifalari: [Cron jobs](/automation/cron-jobs)

Maslahat: buyruqlar to‘liq to‘plamini ko‘rish uchun `openclaw cron --help` ni ishga tushiring.

Eslatma: ajratilgan `cron add` vazifalari sukut bo‘yicha `--announce` yetkazib berishdan foydalanadi. Natijani ichki holatda saqlash uchun `--no-deliver` dan foydalaning. `--deliver` endi eskirgan alias sifatida `--announce` ga mos keladi.

Eslatma: bir martalik (`--at`) vazifalar sukut bo‘yicha muvaffaqiyatdan so‘ng o‘chiriladi. Ularni saqlab qolish uchun `--keep-after-run` dan foydalaning.

Eslatma: takrorlanuvchi ishlar ketma-ket xatolardan so‘ng endi eksponensial qayta urinish oraliqlaridan foydalanadi (30s → 1m → 5m → 15m → 60m), keyingi muvaffaqiyatli bajarilishdan so‘ng esa odatdagi jadvalga qaytadi.

## Keng tarqalgan tahrirlar

Xabarni o‘zgartirmasdan yetkazib berish sozlamalarini yangilang:

```bash
openclaw cron edit <job-id> --announce --channel telegram --to "123456789"
```

Alohida ish uchun yetkazib berishni o‘chirish:

```bash
openclaw cron edit <job-id> --no-deliver
```

Muayyan kanalga e’lon qilish:

```bash
openclaw cron edit <job-id> --announce --channel slack --to "channel:C1234567890"
```
