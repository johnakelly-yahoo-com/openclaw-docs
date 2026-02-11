---
summary: "Telegram allowlist mustahkamlanishi: prefiks va bo‘shliqni normallashtirish"
read_when:
  - Tarixiy Telegram allowlist o‘zgarishlarini ko‘rib chiqish
title: "Telegram Allowlist mustahkamlanishi"
---

# Telegram Allowlist mustahkamlanishi

**Sana**: 2026-01-05  
**Holat**: Tugallangan  
**PR**: #216

## Xulosa

Telegram allowlistlari endi `telegram:` va `tg:` prefikslarini katta-kichik harfga sezgir bo‘lmagan holda qabul qiladi va tasodifiy bo‘shliqlarga chidamli. Bu kiruvchi allowlist tekshiruvlarini chiquvchi yuborish normallashtirilishi bilan moslashtiradi.

## Nimalar o‘zgardi

- `telegram:` va `tg:` prefikslari bir xil tarzda ko‘rib chiqiladi (katta-kichik harflarga sezgir emas).
- Allowlist yozuvlari qirqib tashlanadi; bo‘sh yozuvlar e’tiborsiz qoldiriladi.

## Misollar

Bir xil ID uchun bularning barchasi qabul qilinadi:

- `telegram:123456`
- `TG:123456`
- `tg:123456`

## Nima uchun bu muhim

Loglar yoki chat IDlardan nusxa ko‘chirish/qo‘yish ko‘pincha prefikslar va bo‘sh joylarni o‘z ichiga oladi. Normallashtirish DM yoki guruhlarda javob berish-bermaslikni aniqlashda
noto‘g‘ri manfiy holatlarning oldini oladi.

## Tegishli hujjatlar

- [Guruh chatlari](/channels/groups)
- [Telegram provayderi](/channels/telegram)
