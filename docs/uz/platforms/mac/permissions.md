---
summary: "macOS ruxsatlarining saqlanib qolishi (TCC) va imzolash talablari"
read_when:
  - Yo‘qolgan yoki tiqilib qolgan macOS ruxsat so‘rovlarini sozlash
  - macOS ilovasini paketlash yoki imzolash
  - Bundle ID’larni yoki ilova o‘rnatish yo‘llarini o‘zgartirish
title: "macOS ruxsatlari"
---

# macOS ruxsatlari (TCC)

macOS ruxsat berish mexanizmi nozik hisoblanadi. TCC ruxsatni ilovaning kod imzosi, bundle identifikatori va diskdagi joylashuvi bilan bog‘laydi. Agar ularning birortasi o‘zgarsa, macOS ilovani yangi deb hisoblaydi va so‘rovlarni olib tashlashi yoki yashirishi mumkin.

## Barqaror ruxsatlar uchun talablar

- Bir xil yo‘l: ilovani doimiy joydan ishga tushiring (OpenClaw uchun `dist/OpenClaw.app`).
- Bir xil bundle identifikatori: bundle ID’ni o‘zgartirish yangi ruxsat identifikatorini yaratadi.
- Imzolangan ilova: imzolanmagan yoki ad-hoc imzolangan build’lar ruxsatlarni saqlab qolmaydi.
- Izchil imzo: haqiqiy Apple Development yoki Developer ID sertifikatidan foydalaning, shunda imzo qayta build’lar orasida barqaror bo‘ladi.

Ad-hoc signatures generate a new identity every build. macOS will forget previous
grants, and prompts can disappear entirely until the stale entries are cleared.

## So‘rovlar yo‘qolganda tiklash bo‘yicha tekshiruv ro‘yxati

1. Ilovani yoping.
2. System Settings -> Privacy & Security bo‘limida ilova yozuvini olib tashlang.
3. Ilovani o‘sha yo‘ldan qayta ishga tushiring va ruxsatlarni yana bering.
4. Agar so‘rov hanuz ko‘rinmasa, `tccutil` yordamida TCC yozuvlarini tiklab, yana urinib ko‘ring.
5. Ba’zi ruxsatlar faqat macOS’ni to‘liq qayta ishga tushirgandan so‘ng qayta paydo bo‘ladi.

Namunaviy reset buyruqlari (zaruratga ko‘ra bundle ID’ni almashtiring):

```bash
sudo tccutil reset Accessibility bot.molt.mac
sudo tccutil reset ScreenCapture bot.molt.mac
sudo tccutil reset AppleEvents
```

## Fayllar va papkalar ruxsatlari (Desktop/Documents/Downloads)

macOS shuningdek terminal yoki fon jarayonlari uchun Desktop, Documents va Downloads’ni cheklashi mumkin. Agar fayl o‘qish yoki katalog ro‘yxatlari osilib qolsa, fayl amallarini bajaradigan aynan o‘sha jarayon kontekstiga ruxsat bering (masalan Terminal/iTerm, LaunchAgent orqali ishga tushirilgan ilova yoki SSH jarayoni).

Aylanma yechim: agar alohida papka ruxsatlaridan qochmoqchi bo‘lsangiz, fayllarni OpenClaw ish maydoniga (`~/.openclaw/workspace`) ko‘chiring.

Agar ruxsatlarni sinovdan o‘tkazayotgan bo‘lsangiz, har doim haqiqiy sertifikat bilan imzolang. Ad-hoc build’lar faqat ruxsatlar muhim bo‘lmagan tezkor lokal ishga tushirishlar uchun maqbul.
