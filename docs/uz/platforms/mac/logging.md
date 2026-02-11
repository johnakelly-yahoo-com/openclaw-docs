---
summary: "33. OpenClaw loglash: aylanuvchi diagnostika fayl logi + unified log maxfiylik bayroqlari"
read_when:
  - 34. macOS loglarini yozib olish yoki maxfiy ma’lumot loglanishini tekshirish
  - 35. Ovoz uyg‘otish/session hayotiy sikli muammolarini debug qilish
title: "36. macOS Logging"
---

# 37. Logging (macOS)

## 38. Aylanuvchi diagnostika fayl logi (Debug panel)

39. OpenClaw macOS ilova loglarini swift-log orqali yo‘naltiradi (sukut bo‘yicha unified logging) va zarur bo‘lganda diskka lokal, aylanuvchi fayl logini yozishi mumkin.

- 40. Batafsillik: **Debug panel → Logs → App logging → Verbosity**
- 41. Yoqish: **Debug panel → Logs → App logging → “Write rolling diagnostics log (JSONL)”**
- 42. Joylashuv: `~/Library/Logs/OpenClaw/diagnostics.jsonl` (avtomatik aylantiriladi; eski fayllar `.1`, `.2`, … bilan qo‘shimchalanadi)
- 43. Tozalash: **Debug panel → Logs → App logging → “Clear”**

44. Eslatmalar:

- 45. Bu **sukut bo‘yicha o‘chiq**. 46. Faqat faol debug qilayotganda yoqing.
- 47. Faylni maxfiy deb hisoblang; ko‘rib chiqmasdan ulashmang.

## 48. macOS’da unified logging maxfiy ma’lumotlari

49. Unified logging ko‘p payloadlarni redakt qiladi, agar subsystem `privacy -off` ga opt-in qilmagan bo‘lsa. 50. Peter’ning macOS’dagi [logging privacy shenanigans](https://steipete.me/posts/2025/logging-privacy-shenanigans) (2025) haqidagi yozuviga ko‘ra, bu subsystem nomi bilan kalitlangan `/Library/Preferences/Logging/Subsystems/` dagi plist orqali boshqariladi. Faqat yangi log yozuvlari flagni oladi, shuning uchun muammoni qayta yuzaga keltirishdan oldin uni yoqing.

## OpenClaw (`bot.molt`) uchun yoqing

- Avval plistni vaqtinchalik faylga yozing, so‘ng uni root sifatida atomik tarzda o‘rnating:

```bash
cat <<'EOF' >/tmp/bot.molt.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>DEFAULT-OPTIONS</key>
    <dict>
        <key>Enable-Private-Data</key>
        <true/>
    </dict>
</dict>
</plist>
EOF
sudo install -m 644 -o root -g wheel /tmp/bot.molt.plist /Library/Preferences/Logging/Subsystems/bot.molt.plist
```

- Qayta yuklash talab qilinmaydi; logd faylni tezda payqaydi, ammo faqat yangi log satrlari shaxsiy payloadlarni o‘z ichiga oladi.
- Mavjud yordamchi bilan boyroq chiqishni ko‘ring, masalan `./scripts/clawlog.sh --category WebChat --last 5m`.

## Nosozlikni tuzatgandan so‘ng o‘chiring

- Override-ni olib tashlang: `sudo rm /Library/Preferences/Logging/Subsystems/bot.molt.plist`.
- Ixtiyoriy ravishda `sudo log config --reload` ni ishga tushirib, logd override-ni darhol bekor qilishga majburlashingiz mumkin.
- Yodda tuting, bu sirt telefon raqamlari va xabar matnlarini o‘z ichiga olishi mumkin; plistni faqat qo‘shimcha tafsilotlar faol kerak bo‘lgan paytda qoldiring.
