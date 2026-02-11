---
summary: Node + tsx "__name is not a function" nosozligi bo‘yicha eslatmalar va yechimlar
read_when:
  - Faqat Node’da ishlab chiqish skriptlari yoki kuzatuv (watch) rejimidagi nosozliklarni tuzatish
  - OpenClaw’da tsx/esbuild yuklagich nosozliklarini tekshirish
title: "Node + tsx nosozligi"
---

# Node + tsx "__name is not a function" nosozligi

## Xulosa

`tsx` bilan Node orqali OpenClaw’ni ishga tushirish boshlanishida quyidagi xato bilan muvaffaqiyatsiz tugaydi:

```
[openclaw] CLI’ni ishga tushirib bo‘lmadi: TypeError: __name is not a function
    at createSubsystemLogger (.../src/logging/subsystem.ts:203:25)
    at .../src/agents/auth-profiles/constants.ts:25:20
```

Bu holat ishlab chiqish skriptlarini Bun’dan `tsx` ga almashtirgandan so‘ng boshlandi (commit `2871657e`, 2026-01-06). Xuddi shu ish vaqti yo‘li Bun bilan ishlagan.

## Muhit

- Node: v25.x (v25.3.0 da kuzatilgan)
- tsx: 4.21.0
- OS: macOS (Node 25 ishlaydigan boshqa platformalarda ham qayta yuzaga kelishi ehtimol)

## Qayta ishlab chiqarish (faqat Node)

```bash
# in repo root
node --version
pnpm install
node --import tsx src/entry.ts status
```

## 1. Repozitoriyda minimal qayta ishlab chiqarish

```bash
2. node --import tsx scripts/repro/tsx-name-repro.ts
```

## 3. Node versiyasini tekshirish

- 4. Node 25.3.0: muvaffaqiyatsiz
- 5. Node 22.22.0 (Homebrew `node@22`): muvaffaqiyatsiz
- 6. Node 24: bu yerda hali o‘rnatilmagan; tekshiruv talab etiladi

## 7. Eslatmalar / gipoteza

- `timeFormat: "auto"` bo‘lganda, OpenClaw OS (macOS/Windows) afzalligini tekshiradi va zarurat bo‘lsa, mahalliy formatlashga qaytadi. 9. esbuild’ning `keepNames` opsiyasi `__name` helper’ini chiqaradi va funksiya ta’riflarini `__name(...)` bilan o‘rab qo‘yadi.
- 10. Xatolik shuni ko‘rsatadiki, `__name` mavjud, lekin runtime’da funksiya emas; bu esa Node 25 loader yo‘lida ushbu modul uchun helper yo‘qolgan yoki ustiga yozilganini anglatadi.
- 11. Shunga o‘xshash `__name` helper muammolari helper yo‘q yoki qayta yozilgan holatlarda boshqa esbuild iste’molchilarida ham xabar qilingan.

## 12. Regression tarixi

- 13. `2871657e` (2026-01-06): Bun’ni ixtiyoriy qilish uchun skriptlar Bun’dan tsx’ga o‘zgartirildi.
- 14. Undan oldin (Bun yo‘li), `openclaw status` va `gateway:watch` ishlagan.

## 15. Muqobil yechimlar

- 16. Dev skriptlar uchun Bun’dan foydalanish (joriy vaqtinchalik qaytish).

- 17. Node + tsc watch’dan foydalanib, so‘ng kompilyatsiya qilingan chiqishni ishga tushirish:

  ```bash
  `tsx` TS/ESM ni transformatsiya qilish uchun esbuild’dan foydalanadi.
  ```

- pnpm exec tsc --watch --preserveWatchOutput
  node --watch openclaw.mjs status

- 20. Agar imkon bo‘lsa, TS loader’da esbuild keepNames’ni o‘chirib qo‘yish (`__name` helper kiritilishini oldini oladi); tsx hozircha buni ochiq qilmaydi.

- 21. Muammo Node 25’ga xosligini aniqlash uchun `tsx` bilan Node LTS (22/24) ni sinab ko‘ring.

## 22. Manbalar

- 23. https://opennext.js.org/cloudflare/howtos/keep_names
- 24. https://esbuild.github.io/api/#keep-names
- 25. https://github.com/evanw/esbuild/issues/1031

## 26. Keyingi qadamlar

- 27. Node 25 regressiyasini tasdiqlash uchun Node 22/24’da qayta ishlab chiqarish.
- 28. Agar ma’lum regressiya mavjud bo‘lsa, `tsx` nightly’ni sinab ko‘ring yoki oldingi versiyaga pin qiling.
- 29. Agar Node LTS’da ham takrorlansa, `__name` stack trace bilan upstream’ga minimal repro yuboring.
