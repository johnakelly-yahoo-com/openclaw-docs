---
summary: "ClawHub qo‘llanmasi: ommaviy skilllar reyestri + CLI ish jarayonlari"
read_when:
  - ClawHub’ni yangi foydalanuvchilarga tanishtirish
  - 24. Ko‘nikmalarni o‘rnatish, qidirish yoki nashr qilish
  - ClawHub CLI flaglari va sinxronlash xatti-harakatlarini tushuntirish
title: "ClawHub"
---

# ClawHub

ClawHub — **OpenClaw uchun ommaviy skilllar reyestri**. Bu bepul xizmat: barcha skilllar ommaviy, ochiq va ulashish hamda qayta foydalanish uchun hammaga ko‘rinadi. Skill — bu shunchaki `SKILL.md` fayliga ega papka (va qo‘shimcha matn fayllari). Siz skilllarni veb-ilovada ko‘rib chiqishingiz yoki CLI orqali qidirish, o‘rnatish, yangilash va nashr qilishdan foydalanishingiz mumkin.

Sayt: [clawhub.ai](https://clawhub.ai)

## ClawHub nima

- OpenClaw skilllari uchun ommaviy reyestr.
- Skill to‘plamlari va metama’lumotlarning versiyalangan ombori.
- Qidiruv, teglar va foydalanish signallari uchun kashf etish maydoni.

## Qanday ishlaydi

1. Foydalanuvchi skill to‘plamini (fayllar + metama’lumotlar) nashr qiladi.
2. ClawHub to‘plamni saqlaydi, metama’lumotlarni tahlil qiladi va versiya belgilaydi.
3. Reyestr skillni qidiruv va kashf etish uchun indekslaydi.
4. Foydalanuvchilar OpenClaw’da skilllarni ko‘rib chiqadi, yuklab oladi va o‘rnatadi.

## Nimalar qilishingiz mumkin

- Yangi skilllar va mavjud skilllarning yangi versiyalarini nashr qilish.
- Skilllarni nomi, teglar yoki qidiruv orqali topish.
- Skill to‘plamlarini yuklab olish va ularning fayllarini ko‘zdan kechirish.
- Suiiste’mol qilingan yoki xavfli skilllar haqida xabar berish.
- Agar siz moderator bo‘lsangiz, yashirish, qayta ko‘rsatish, o‘chirish yoki taqiqlash.

## Kimlar uchun (boshlovchilar uchun qulay)

Agar OpenClaw agentingizga yangi imkoniyatlar qo‘shmoqchi bo‘lsangiz, ClawHub — skilllarni topish va o‘rnatishning eng oson yo‘li. Backend qanday ishlashini bilishingiz shart emas. Siz quyidagilarni qilishingiz mumkin:

- Skilllarni oddiy til orqali qidirish.
- Skillni ish muhitingizga o‘rnatish.
- Keyinroq skilllarni bitta buyruq bilan yangilash.
- O‘z skilllaringizni nashr qilib, zaxiralash.

## Tezkor boshlash (texnik bo‘lmagan)

1. CLI’ni o‘rnating (keyingi bo‘limga qarang).
2. Kerakli narsani qidiring:
   - `clawhub search "calendar"`
3. Skillni o‘rnating:
   - `clawhub install <skill-slug>`
4. Yangi skillni qabul qilishi uchun yangi OpenClaw sessiyasini boshlang.

## CLI’ni o‘rnatish

1. Bittasini tanlang:

```bash
2. npm i -g clawhub
```

```bash
3. pnpm add -g clawhub
```

## 4. OpenClaw ichida qanday moslashadi

5. Sukut bo‘yicha, CLI ko‘nikmalarni joriy ishchi katalogingiz ostidagi `./skills` ga o‘rnatadi. 6. Agar OpenClaw ish maydoni sozlangan bo‘lsa, `clawhub` `--workdir` (yoki `CLAWHUB_WORKDIR`) bilan bekor qilinmaguncha o‘sha ish maydoniga qaytadi. 7. OpenClaw ish maydoni ko‘nikmalarini `<workspace>/skills` dan yuklaydi va ularni **keyingi** sessiyada qabul qiladi. 8. Agar siz allaqachon `~/.openclaw/skills` yoki biriktirilgan ko‘nikmalardan foydalansangiz, ish maydoni ko‘nikmalari ustuvorlikka ega bo‘ladi.

9. Ko‘nikmalar qanday yuklanishi, ulashilishi va cheklanishi haqida batafsil ma’lumot uchun qarang
   [Skills](/tools/skills).

## 10. Ko‘nikmalar tizimi haqida umumiy ma’lumot

11. Ko‘nikma — bu OpenClaw’ga ma’lum bir vazifani qanday bajarishni o‘rgatadigan versiyalangan fayllar to‘plami. 12. Har bir nashr yangi versiyani yaratadi va reyestr foydalanuvchilar o‘zgarishlarni tekshirishi uchun versiyalar tarixini saqlab boradi.

13. Odatdagi ko‘nikma quyidagilarni o‘z ichiga oladi:

- 14. Asosiy tavsif va foydalanishni o‘z ichiga olgan `SKILL.md` fayli.
- 15. Ko‘nikma tomonidan ishlatiladigan ixtiyoriy sozlamalar, skriptlar yoki yordamchi fayllar.
- 16. Teglar, qisqacha mazmun va o‘rnatish talablari kabi metama’lumotlar.

17. ClawHub metama’lumotlardan ko‘nikmalarni kashf etishni kuchaytirish va imkoniyatlarini xavfsiz tarzda taqdim etish uchun foydalanadi.
18. Reyestr shuningdek reyting va ko‘rinuvchanlikni yaxshilash uchun foydalanish signallarini (masalan, yulduzlar va yuklab olishlar) kuzatadi.

## 19. Xizmat nimani taqdim etadi (xususiyatlar)

- 20. Ko‘nikmalar va ularning `SKILL.md` kontentini **ommaviy ko‘rish**.
- 21. Faqat kalit so‘zlargagina emas, balki embeddinglar (vektorli qidiruv) asosidagi **qidiruv**.
- 22. Semver, o‘zgarishlar jurnali va teglar (jumladan `latest`) bilan **versiyalash**.
- 23. Har bir versiya uchun zip ko‘rinishida **yuklab olishlar**.
- 24. Hamjamiyat fikri uchun **yulduzlar va izohlar**.
- 25. Tasdiqlash va auditlar uchun **moderatsiya** ilgaklari.
- 26. Avtomatlashtirish va skriptlash uchun **CLI-ga qulay API**.

## 27. Xavfsizlik va moderatsiya

28. ClawHub sukut bo‘yicha ochiq. 29. Har kim ko‘nikmalarni yuklashi mumkin, ammo nashr qilish uchun GitHub akkaunti kamida bir haftalik bo‘lishi kerak. 30. Bu qonuniy hissa qo‘shuvchilarni to‘smasdan, suiiste’molni sekinlashtirishga yordam beradi.

31. Hisobot berish va moderatsiya:

- 32. Tizimga kirgan har qanday foydalanuvchi ko‘nikma haqida shikoyat qilishi mumkin.
- 33. Shikoyat sabablari majburiy va qayd etiladi.
- 34. Har bir foydalanuvchi bir vaqtning o‘zida 20 tagacha faol shikoyatga ega bo‘lishi mumkin.
- 35. 3 tadan ortiq noyob shikoyatga ega ko‘nikmalar sukut bo‘yicha avtomatik yashiriladi.
- 36. Moderatorlar yashirilgan ko‘nikmalarni ko‘rishi, ularni qayta ko‘rsatishi, o‘chirishi yoki foydalanuvchilarni bloklashi mumkin.
- 37. Shikoyat funksiyasini suiiste’mol qilish akkauntni bloklashga olib kelishi mumkin.

38. Moderator bo‘lishga qiziqasizmi? 39. OpenClaw Discord’ida so‘rang va moderator yoki maintainer bilan bog‘laning.

## 40. CLI buyruqlari va parametrlari

41. Global opsiyalar (barcha buyruqlarga qo‘llaniladi):

- 42. `--workdir <dir>`: Ishchi katalog (sukut bo‘yicha: joriy katalog; OpenClaw ish maydoniga qaytadi).
- 43. `--dir <dir>`: Ishchi katalogga nisbatan ko‘nikmalar katalogi (sukut bo‘yicha: `skills`).
- 44. `--site <url>`: Saytning asosiy URL manzili (brauzer orqali kirish).
- 45. `--registry <url>`: Reyestr API asosiy URL manzili.
- 46. `--no-input`: So‘rovlarni o‘chirish (interaktiv emas).
- 47. `-V, --cli-version`: CLI versiyasini chiqarish.

48. Autentifikatsiya:

- 49. `clawhub login` (brauzer oqimi) yoki `clawhub login --token <token>`
- 50. `clawhub logout`
- 1. `clawhub whoami`

2. Variantlar:

- 3. `--token <token>`: API tokenini joylashtiring.
- 4. `--label <label>`: Brauzer orqali kirish tokenlari uchun saqlanadigan yorliq (standart: `CLI token`).
- 5. `--no-browser`: Brauzerni ochmang (`--token` talab qilinadi).

6. Qidiruv:

- 7. `clawhub search "query"`
- 8. `--limit <n>`: Maksimal natijalar soni.

9. O‘rnatish:

- 10. `clawhub install <slug>`
- 11. `--version <version>`: Muayyan versiyani o‘rnatish.
- 12. `--force`: Papka allaqachon mavjud bo‘lsa, ustiga yozish.

13. Yangilash:

- 14. `clawhub update <slug>`
- 15. `clawhub update --all`
- 16. `--version <version>`: Muayyan versiyaga yangilash (faqat bitta slug).
- 17. `--force`: Mahalliy fayllar chop etilgan hech bir versiyaga mos kelmasa, ustiga yozish.

18. Ro‘yxat:

- 19. `clawhub list` (`.clawhub/lock.json` ni o‘qiydi)

20. Chop etish:

- 21. `clawhub publish <path>`
- 22. `--slug <slug>`: Skill slug’i.
- 23. `--name <name>`: Ko‘rinadigan nom.
- 24. `--version <version>`: Semver versiyasi.
- 25. `--changelog <text>`: O‘zgarishlar jurnali matni (bo‘sh bo‘lishi mumkin).
- 26. `--tags <tags>`: Vergul bilan ajratilgan teglar (standart: `latest`).

27. O‘chirish/qayta tiklash (faqat egasi/admin):

- 28. `clawhub delete <slug> --yes`
- 29. `clawhub undelete <slug> --yes`

30. Sinxronlash (mahalliy skill’larni skanerlash + yangi/yangilanganlarini chop etish):

- 31. `clawhub sync`
- 32. `--root <dir...>`: Qo‘shimcha skanerlash ildizlari.
- 33. `--all`: So‘rovlarsiz hammasini yuklash.
- 34. `--dry-run`: Nimalar yuklanishini ko‘rsatish.
- 35. `--bump <type>`: Yangilanishlar uchun `patch|minor|major` (standart: `patch`).
- 36. `--changelog <text>`: Interaktiv bo‘lmagan yangilanishlar uchun o‘zgarishlar jurnali.
- 37. `--tags <tags>`: Vergul bilan ajratilgan teglar (standart: `latest`).
- 38. `--concurrency <n>`: Reestr tekshiruvlari (standart: 4).

## 39. Agentlar uchun umumiy ish jarayonlari

### 40. Skill’larni qidirish

```bash
41. clawhub search "postgres backups"
```

### 42. Yangi skill’larni yuklab olish

```bash
43. clawhub install my-skill-pack
```

### 44. O‘rnatilgan skill’larni yangilash

```bash
45. clawhub update --all
```

### 46. Skill’laringizni zaxiralash (chop etish yoki sinxronlash)

47. Bitta skill papkasi uchun:

```bash
48. clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0 --tags latest
```

49. Ko‘plab skill’larni bir vaqtda skanerlash va zaxiralash uchun:

```bash
50. clawhub sync --all
```

## Advanced details (technical)

### Versioning and tags

- Each publish creates a new **semver** `SkillVersion`.
- Tags (like `latest`) point to a version; moving tags lets you roll back.
- Changelogs are attached per version and can be empty when syncing or publishing updates.

### Local changes vs registry versions

Updates compare the local skill contents to registry versions using a content hash. If local files do not match any published version, the CLI asks before overwriting (or requires `--force` in non-interactive runs).

### Sync scanning and fallback roots

`clawhub sync` scans your current workdir first. If no skills are found, it falls back to known legacy locations (for example `~/openclaw/skills` and `~/.openclaw/skills`). This is designed to find older skill installs without extra flags.

### Storage and lockfile

- Installed skills are recorded in `.clawhub/lock.json` under your workdir.
- Auth tokens are stored in the ClawHub CLI config file (override via `CLAWHUB_CONFIG_PATH`).

### Telemetry (install counts)

When you run `clawhub sync` while logged in, the CLI sends a minimal snapshot to compute install counts. You can disable this entirely:

```bash
export CLAWHUB_DISABLE_TELEMETRY=1
```

## Environment variables

- `CLAWHUB_SITE`: Override the site URL.
- `CLAWHUB_REGISTRY`: Override the registry API URL.
- `CLAWHUB_CONFIG_PATH`: Override where the CLI stores the token/config.
- `CLAWHUB_WORKDIR`: Override the default workdir.
- `CLAWHUB_DISABLE_TELEMETRY=1`: Disable telemetry on `sync`.
