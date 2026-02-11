---
summary: "system"
read_when:
  - Siz cron job yaratmasdan tizim hodisasini navbatga qo‘ymoqchisiz
  - Siz heartbeat’larni yoqish yoki o‘chirishni xohlaysiz
  - Siz tizim presence yozuvlarini ko‘zdan kechirmoqchisiz
title: "**main** sessiyada tizim hodisasini navbatga qo‘shish."
---

# `openclaw system`

Gateway uchun tizim darajasidagi yordamchilar: tizim hodisalarini navbatga qo‘yish, heartbeat’larni boshqarish,
va presence’ni ko‘rish.

## Keng tarqalgan buyruqlar

```bash
openclaw system event --text "Check for urgent follow-ups" --mode now
openclaw system heartbeat enable
openclaw system heartbeat last
openclaw system presence
```

## `system event`

`--text <text>`: talab qilinadigan tizim hodisasi matni. Keyingi heartbeat uni prompt ichiga `System:` qatori sifatida kiritadi. Heartbeat’ni darhol ishga tushirish uchun `--mode now` dan foydalaning; `next-heartbeat` esa keyingi rejalashtirilgan tikni kutadi.

Bayroqlar:

- Joriy konfiguratsiyangiz orqali (mahalliy yoki masofaviy) yetib boriladigan, ishlayotgan Gateway talab qilinadi.
- `--mode <mode>`: `now` yoki `next-heartbeat` (standart).
- `--json`: mashina-o‘qiydigan chiqish.

## `system heartbeat last|enable|disable`

Heartbeat boshqaruvlari:

- `last`: oxirgi heartbeat hodisasini ko‘rsatadi.
- `enable`: heartbeat’larni qayta yoqadi (agar ular o‘chirilgan bo‘lsa, shundan foydalaning).
- `disable`: heartbeat’larni pauzaga qo‘yadi.

Bayroqlar:

- `--json`: mashina-o‘qiydigan chiqish.

## `system presence`

Gateway biladigan joriy tizim presence yozuvlarini ro‘yxatlaydi (tugunlar,
instansiyalar va shunga o‘xshash holat qatorlari).

Bayroqlar:

- `--json`: mashina-o‘qiydigan chiqish.

## Eslatmalar

- Tizim hodisalari vaqtinchalik va qayta ishga tushirishlar orasida saqlanmaydi.
- update
