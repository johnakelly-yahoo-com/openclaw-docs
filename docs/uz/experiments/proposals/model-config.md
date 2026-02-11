---
summary: "Tadqiqot: model konfiguratsiyasi, autentifikatsiya profillari va fallback xatti-harakati"
read_when:
  - Kelajakdagi model tanlash + autentifikatsiya profili g‘oyalarini o‘rganish
title: "Model konfiguratsiyasini o‘rganish"
---

# Model konfiguratsiyasi (Tadqiqot)

Ushbu hujjat kelajakdagi model konfiguratsiyasi uchun **g‘oyalar** ni jamlaydi. Bu
jo‘natiladigan spetsifikatsiya emas. Joriy xatti-harakatlar uchun qarang:

- [Modellar](/concepts/models)
- [Model failover](/concepts/model-failover)
- [OAuth + profillar](/concepts/oauth)

## Motivatsiya

Operatorlar xohlaydi:

- Har bir provayder uchun bir nechta autentifikatsiya profillari (shaxsiy va ish).
- Oddiy `/model` tanlash va oldindan aytiladigan fallbacklar.
- Matn modellari va tasvir imkoniyatiga ega modellarning aniq ajratilishi.

## Mumkin bo‘lgan yo‘nalish (yuqori darajada)

- Model tanlashni sodda saqlash: `provider/model` va ixtiyoriy aliaslar bilan.
- Provayderlarga bir nechta autentifikatsiya profillariga ega bo‘lishga ruxsat berish, aniq tartib bilan.
- Barcha sessiyalar izchil ravishda failover qilishi uchun global fallback ro‘yxatidan foydalanish.
- Tasvir marshrutlashini faqat aniq sozlanganda almashtirish.

## Ochiq savollar

- Profil rotatsiyasi provayder bo‘yichami yoki model bo‘yichami bo‘lishi kerak?
- UI sessiya uchun profil tanlashni qanday ko‘rsatishi kerak?
- Meros konfiguratsiya kalitlaridan eng xavfsiz migratsiya yo‘li qanday?
