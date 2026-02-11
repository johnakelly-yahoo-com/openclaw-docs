---
summary: "Kontekst oynasi + kompaksiyalash: OpenClaw sessiyalarni model limitlari ostida qanday saqlaydi"
read_when:
  - Siz avtomatik kompaksiyalash va /compact ni tushunmoqchisiz
  - Kontekst limitlariga urilib qolayotgan uzoq sessiyalarni nosozlikdan o‘tkazyapsiz
title: "Kompaksiyalash"
---

# Kontekst oynasi va kompaksiyalash

Har bir modelda **kontekst oynasi** (ko‘ra oladigan maksimal tokenlar soni) mavjud. Uzoq davom etuvchi chatlar xabarlar va asbob natijalarini to‘playdi; oyna torayganda, OpenClaw limitlar ichida qolish uchun eski tarixni **kompaktlaydi**.

## Kompaksiyalash nima

Kompaksiyalash **eski suhbatni qisqacha jamlaydi** va yaqindagi xabarlarni butunligicha qoldiradi. Xulosa sessiya tarixida saqlanadi, shuning uchun keyingi so‘rovlar quyidagilardan foydalanadi:

- Kompaksiyalash xulosasi
- Kompaksiyalash nuqtasidan keyingi so‘nggi xabarlar

Kompaksiyalash sessiyaning JSONL tarixida **saqlanib qoladi**.

## Konfiguratsiya

[Compaction config & modes](/concepts/compaction) sahifasini `agents.defaults.compaction` sozlamalari uchun ko‘ring.

## Avto-kompaktatsiya (standart yoqilgan)

Sessiya modelning kontekst oynasiga yaqinlashganda yoki undan oshib ketganda, OpenClaw avto-kompaktatsiyani ishga tushiradi va siqilgan kontekstdan foydalangan holda asl so‘rovni qayta urinib ko‘rishi mumkin.

Siz quyidagilarni ko‘rasiz:

- `🧹 Auto-compaction complete` — batafsil (verbose) rejimda
- `/status` da `🧹 Compactions: <count>` ko‘rsatiladi

Kompaktatsiyadan oldin, OpenClaw diskka saqlash uchun barqaror eslatmalarni yozib olish maqsadida **jim xotira tozalash** aylanishini bajarishi mumkin. Tafsilotlar va sozlamalar uchun [Memory](/concepts/memory) sahifasiga qarang.

## Qo‘lda kompaktatsiya

Kompaktatsiya bosqichini majburan ishga tushirish uchun `/compact` (ixtiyoriy ko‘rsatmalar bilan) dan foydalaning:

```
/compact Qarorlar va ochiq savollarga e’tibor qarating
```

## Kontekst oynasi manbai

Kontekst oynasi modelga xos. OpenClaw cheklovlarni aniqlash uchun sozlangan provayder katalogidagi model ta’rifidan foydalanadi.

## Kompaktatsiya va pruning taqqoslanishi

- **Kompaktatsiya**: umumlashtiradi va JSONL formatida **saqlab qoladi**.
- **Sessiyani pruning qilish**: faqat eski **asbob natijalari**ni qisqartiradi, **xotirada**, har bir so‘rov bo‘yicha.

Pruning tafsilotlari uchun [/concepts/session-pruning](/concepts/session-pruning) sahifasiga qarang.

## Maslahatlar

- Sessiyalar eskirib qolgan yoki kontekst shishib ketgandek tuyulganda `/compact` dan foydalaning.
- Katta asbob chiqishlari allaqachon qisqartiriladi; pruning asbob natijalari to‘planishini yanada kamaytirishi mumkin.
- Agar sizga butunlay yangi boshlash kerak bo‘lsa, `/new` yoki `/reset` yangi sessiya identifikatorini boshlaydi.
