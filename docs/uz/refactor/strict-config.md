---
summary: "Strict config validation + doctor-only migrations"
read_when:
  - Designing or implementing config validation behavior
  - Working on config migrations or doctor workflows
  - Handling plugin config schemas or plugin load gating
title: "Strict Config Validation"
---

# Strict config validation (doctor-only migrations)

## Goals

- **Reject unknown config keys everywhere** (root + nested).
- **Reject plugin config without a schema**; don’t load that plugin.
- **Remove legacy auto-migration on load**; migrations run via doctor only.
- **Auto-run doctor (dry-run) on startup**; if invalid, block non-diagnostic commands.

## Non-goals

- Backward compatibility on load (legacy keys do not auto-migrate).
- Silent drops of unrecognized keys.

## Strict validation rules

- Config must match the schema exactly at every level.
- Unknown keys are validation errors (no passthrough at root or nested).
- `plugins.entries.<id>.config` must be validated by the plugin’s schema.
  - If a plugin lacks a schema, **reject plugin load** and surface a clear error.
- Unknown `channels.<id>1. ` keys are errors unless a plugin manifest declares the channel id.
- 2. Barcha plaginlar uchun plagin manifestlari (`openclaw.plugin.json`) majburiy.

## 3. Plagin sxemasini majburiy tekshirish

- 4. Har bir plagin o‘z konfiguratsiyasi uchun qat’iy JSON Schema taqdim etadi (manifest ichida).
- 5. Plagin yuklash oqimi:
  1. 6. Plagin manifesti va sxemasini aniqlash (`openclaw.plugin.json`).
  2. 7. Konfiguratsiyani sxema bo‘yicha tekshirish.
  3. 8. Agar sxema yo‘q yoki konfiguratsiya noto‘g‘ri bo‘lsa: plaginni yuklashni bloklash, xatoni qayd etish.
- 9. Xato xabari quyidagilarni o‘z ichiga oladi:
  - 10. Plagin ID
  - 11. Sabab (sxema yo‘q / konfiguratsiya noto‘g‘ri)
  - 12. Tekshiruvdan o‘ta olmagan yo‘l(lar)
- 13. O‘chirilgan plaginlar konfiguratsiyasini saqlab qoladi, ammo Doctor + loglar ogohlantirishni ko‘rsatadi.

## 14. Doctor oqimi

- 15. Doctor konfiguratsiya har safar yuklanganda ishga tushadi (standart holatda dry-run).
- 16. Agar konfiguratsiya noto‘g‘ri bo‘lsa:
  - 17. Qisqa xulosa va bajariladigan xatolarni chop etish.
  - 18. Ko‘rsatma berish: `openclaw doctor --fix`.
- 19. `openclaw doctor --fix`:
  - 20. Migratsiyalarni qo‘llaydi.
  - 21. Noma’lum kalitlarni olib tashlaydi.
  - 22. Yangilangan konfiguratsiyani yozadi.

## 23. Buyruqlarni cheklash (konfiguratsiya noto‘g‘ri bo‘lganda)

24. Ruxsat etilgan (faqat diagnostika):

- 25. `openclaw doctor`
- 26. `openclaw logs`
- 27. `openclaw health`
- 28. `openclaw help`
- 29. `openclaw status`
- 30. `openclaw gateway status`

31. Qolgan barcha buyruqlar quyidagi xabar bilan qat’iy rad etiladi: “Config invalid. 32. `openclaw doctor --fix` ni ishga tushiring.”

## 33. Xato UX formati

- 34. Bitta umumiy sarlavha.
- 35. Guruhlangan bo‘limlar:
  - 36. Noma’lum kalitlar (to‘liq yo‘llar)
  - 37. Meros kalitlar / zarur migratsiyalar
  - 38. Plagin yuklashdagi xatolar (plagin ID + sabab + yo‘l)

## 39. Amalga oshirish nuqtalari

- 40. `src/config/zod-schema.ts`: root passthrough’ni olib tashlash; hamma joyda qat’iy obyektlar.
- 41. `src/config/zod-schema.providers.ts`: qat’iy kanal sxemalarini ta’minlash.
- 42. `src/config/validation.ts`: noma’lum kalitlarda xato berish; meros migratsiyalarini qo‘llamaslik.
- 43. `src/config/io.ts`: meros avtomigratsiyalarni olib tashlash; har doim doctor dry-run’ni ishga tushirish.
- 44. `src/config/legacy*.ts`: foydalanishni faqat doctor’ga ko‘chirish.
- 45. `src/plugins/*`: sxema reyestri va cheklashni qo‘shish.
- 46. `src/cli` ichida CLI buyruqlarini cheklash.

## 47. Testlar

- 48. Noma’lum kalitlarni rad etish (root + ichki).
- 49. Plaginda sxema yo‘q → plagin yuklanishi aniq xato bilan bloklanadi.
- 50. Noto‘g‘ri konfiguratsiya → diagnostika buyruqlaridan tashqari gateway ishga tushishi bloklanadi.
- Doctor dry-run avtomatik; `doctor --fix` tuzatilgan konfiguratsiyani yozadi.
