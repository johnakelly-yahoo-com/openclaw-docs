---
summary: "5. `openclaw update` uchun CLI ma’lumotnomasi (xavfsizroq manba yangilash + gateway’ni avtomatik qayta ishga tushirish)"
read_when:
  - 6. Siz manba checkout’ini xavfsiz yangilamoqchisiz
  - 7. `--update` qisqartmasi qanday ishlashini tushunishingiz kerak
title: "`--no-restart`: muvaffaqiyatli yangilashdan so‘ng Gateway xizmatini qayta ishga tushirishni o‘tkazib yuboradi."
---

# 9. `openclaw update`

10. OpenClaw’ni xavfsiz yangilang va stable/beta/dev kanallari o‘rtasida almashing.

11. Agar **npm/pnpm** orqali o‘rnatgan bo‘lsangiz (global o‘rnatish, git metama’lumotlarisiz), yangilanishlar [Updating](/install/updating) bo‘limida ko‘rsatilgan paket menejeri jarayoni orqali amalga oshiriladi.

## 12. Foydalanish

```bash
13. openclaw update
openclaw update status
openclaw update wizard
openclaw update --channel beta
openclaw update --channel dev
openclaw update --tag beta
openclaw update --no-restart
openclaw update --json
openclaw --update
```

## 14. Parametrlar

- `--timeout <seconds>`: har bir bosqich uchun timeout (standart 1200s).
- 16. `--channel <stable|beta|dev>`: yangilanish kanalini o‘rnatadi (git + npm; konfiguratsiyada saqlanadi).
- 17. `--tag <dist-tag|version>`: faqat ushbu yangilanish uchun npm dist-tag yoki versiyani majburan belgilaydi.
- 18. `--json`: mashina o‘qiy oladigan `UpdateRunResult` JSON’ni chiqaradi.
- `update status`

20. Eslatma: pastga yangilash (downgrade) tasdiqni talab qiladi, chunki eski versiyalar konfiguratsiyani buzishi mumkin.

## Faol yangilash kanali + git teg/branch/SHA (manbadan yig‘ilganlar uchun) hamda yangilanish mavjudligini ko‘rsatadi.

`--json`: mashina o‘qiy oladigan status JSON ni chiqaradi.

```bash
23. openclaw update status
openclaw update status --json
openclaw update status --timeout 10
```

24. Parametrlar:

- [Development channels](/install/development-channels)
- 26. `--timeout <seconds>`: tekshiruvlar uchun vaqt cheklovi (standart: 3s).

## 27. `update wizard`

28. Yangilanish kanalini tanlash va yangilanishdan so‘ng Gateway’ni qayta ishga tushirish-yo‘qligini tasdiqlash uchun interaktiv jarayon (standart holat — qayta ishga tushirish). 29. Agar git checkout bo‘lmasdan `dev` ni tanlasangiz, uni yaratishni taklif qiladi.

## 30. Nima qiladi

31. Kanalni aniq almashtirganda (`--channel ...`), OpenClaw o‘rnatish usulini ham moslab boradi:

- 32. `dev` → git checkout’ni ta’minlaydi (standart: `~/openclaw`, `OPENCLAW_GIT_DIR` bilan o‘zgartirish mumkin), uni yangilaydi va global CLI’ni shu checkout’dan o‘rnatadi.
- 33. `stable`/`beta` → mos dist-tag’dan foydalanib npm orqali o‘rnatadi.

## 34. Git checkout jarayoni

35. Kanallar:

- 36. `stable`: eng so‘nggi beta bo‘lmagan tegni checkout qiladi, so‘ng build + doctor bajaradi.
- 37. `beta`: eng so‘nggi `-beta` tegini checkout qiladi, so‘ng build + doctor bajaradi.
- 38. `dev`: `main` ni checkout qiladi, so‘ng fetch + rebase qiladi.

39. Yuqori darajada:

1. 40. Toza worktree talab etiladi (commit qilinmagan o‘zgarishlarsiz).
2. 41. Tanlangan kanalga o‘tadi (teg yoki branch).
3. 42. Upstream’ni fetch qiladi (faqat dev).
4. 43. Faqat dev: vaqtinchalik worktree’da dastlabki lint va TypeScript build’ni bajaradi; agar eng so‘nggi commit muvaffaqiyatsiz bo‘lsa, eng yangi toza build’ni topish uchun 10 tagacha commit orqaga yuradi.
5. 44. Tanlangan commit ustiga rebase qiladi (faqat dev).
6. 45. Bog‘liqliklarni o‘rnatadi (pnpm afzal; npm zaxira variant).
7. 46. Build qiladi va Control UI’ni build qiladi.
8. 47. Yakuniy “xavfsiz yangilash” tekshiruvi sifatida `openclaw doctor` ni ishga tushiradi.
9. 48. Plaginlarni faol kanal bilan sinxronlaydi (dev — paketlangan kengaytmalar; stable/beta — npm) va npm orqali o‘rnatilgan plaginlarni yangilaydi.

## 49) `--update` qisqartmasi

50. `openclaw --update` `openclaw update` ga qayta yoziladi (shellar va launcher skriptlari uchun qulay).

## Shuningdek qarang

- `openclaw doctor` (git checkoutlarda avval yangilashni ishga tushirishni taklif qiladi)
- Siz voice-call plaginidan foydalanasiz va CLI kirish nuqtalarini xohlaysiz
- [Yangilash](/install/updating)
- [CLI ma’lumotnomasi](/cli)
