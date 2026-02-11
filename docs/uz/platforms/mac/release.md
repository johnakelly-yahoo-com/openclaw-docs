---
summary: "OpenClaw macOS relizi uchun tekshiruv ro‘yxati (Sparkle feed, paketlash, imzolash)"
read_when:
  - OpenClaw macOS relizini chiqarish yoki tekshirish
  - Sparkle appcast yoki feed aktivlarini yangilash
title: "macOS relizi"
---

# OpenClaw macOS relizi (Sparkle)

Ushbu ilova endi Sparkle avtomatik yangilanishlari bilan yetkaziladi. Reliz build’lari Developer ID bilan imzolangan, zip qilingan va imzolangan appcast yozuvi bilan nashr etilgan bo‘lishi kerak.

## Oldindan talablar

- Developer ID Application sertifikati o‘rnatilgan (masalan: `Developer ID Application: <Developer Name> (<TEAMID>)`).
- Sparkle maxfiy kaliti yo‘li muhitda `SPARKLE_PRIVATE_KEY_FILE` sifatida o‘rnatilgan (Sparkle ed25519 maxfiy kalitingiz yo‘li; ommaviy kalit Info.plist ichiga kiritilgan). Agar u mavjud bo‘lmasa, `~/.profile` faylini tekshiring.
- `xcrun notarytool` uchun Notary hisob ma’lumotlari (keychain profili yoki API kaliti), agar Gatekeeper’ga mos DMG/zip tarqatishni xohlasangiz.
  - Biz `openclaw-notary` nomli Keychain profilidan foydalanamiz, u shell profilingizdagi App Store Connect API kalit muhit o‘zgaruvchilaridan yaratilgan:
    - `APP_STORE_CONNECT_API_KEY_P8`, `APP_STORE_CONNECT_KEY_ID`, `APP_STORE_CONNECT_ISSUER_ID`
    - `echo "$APP_STORE_CONNECT_API_KEY_P8" | sed 's/\\n/\n/g' > /tmp/openclaw-notary.p8`
    - `xcrun notarytool store-credentials "openclaw-notary" --key /tmp/openclaw-notary.p8 --key-id "$APP_STORE_CONNECT_KEY_ID" --issuer "$APP_STORE_CONNECT_ISSUER_ID"`
- `pnpm` bog‘liqliklari o‘rnatilgan (`pnpm install --config.node-linker=hoisted`).
- Sparkle vositalari SwiftPM orqali avtomatik yuklab olinadi: `apps/macos/.build/artifacts/sparkle/Sparkle/bin/` (`sign_update`, `generate_appcast` va boshqalar).

## Build va paketlash

Eslatmalar:

- `APP_BUILD` `CFBundleVersion`/`sparkle:version` ga mos keladi; uni raqamli va monoton qilib saqlang (`-beta`siz), aks holda Sparkle uni teng deb solishtiradi.
- Standart holatda joriy arxitektura ishlatiladi (`$(uname -m)`). For release/universal builds, set `BUILD_ARCHS="arm64 x86_64"` (or `BUILD_ARCHS=all`).
- Reliz artefaktlari (zip + DMG + notarizatsiya) uchun `scripts/package-mac-dist.sh` dan foydalaning. Lokal/dev paketlash uchun `scripts/package-mac-app.sh` dan foydalaning.

```bash
# From repo root; set release IDs so Sparkle feed is enabled.
# APP_BUILD must be numeric + monotonic for Sparkle compare.
BUNDLE_ID=bot.molt.mac \
APP_VERSION=2026.2.9 \
APP_BUILD="$(git rev-list --count HEAD)" \
BUILD_CONFIG=release \
SIGN_IDENTITY="Developer ID Application: <Developer Name> (<TEAMID>)" \
scripts/package-mac-app.sh

# Zip for distribution (includes resource forks for Sparkle delta support)
ditto -c -k --sequesterRsrc --keepParent dist/OpenClaw.app dist/OpenClaw-2026.2.9.zip

# Optional: also build a styled DMG for humans (drag to /Applications)
scripts/create-dmg.sh dist/OpenClaw.app dist/OpenClaw-2026.2.9.dmg

# Recommended: build + notarize/staple zip + DMG
# First, create a keychain profile once:
#   xcrun notarytool store-credentials "openclaw-notary" \
#     --apple-id "<apple-id>" --team-id "<team-id>" --password "<app-specific-password>"
NOTARIZE=1 NOTARYTOOL_PROFILE=openclaw-notary \
BUNDLE_ID=bot.molt.mac \
APP_VERSION=2026.2.9 \
APP_BUILD="$(git rev-list --count HEAD)" \
BUILD_CONFIG=release \
SIGN_IDENTITY="Developer ID Application: <Developer Name> (<TEAMID>)" \
scripts/package-mac-dist.sh

# Optional: ship dSYM alongside the release
ditto -c -k --keepParent apps/macos/.build/release/OpenClaw.app.dSYM dist/OpenClaw-2026.2.9.dSYM.zip
```

## Appcast yozuvi

Sparkle formatlangan HTML qaydlarini ko‘rsatishi uchun reliz qaydlari generatoridan foydalaning:

```bash
SPARKLE_PRIVATE_KEY_FILE=/path/to/ed25519-private-key scripts/make_appcast.sh dist/OpenClaw-2026.2.9.zip https://raw.githubusercontent.com/openclaw/openclaw/main/appcast.xml
```

`CHANGELOG.md` dan HTML reliz qaydlarini yaratadi ([`scripts/changelog-to-html.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/changelog-to-html.sh) orqali) va ularni appcast yozuviga joylaydi.
Nashr etishda yangilangan `appcast.xml` ni reliz aktivlari (zip + dSYM) bilan birga commit qiling.

## Nashr qilish va tekshirish

- `OpenClaw-2026.2.9.zip` (va `OpenClaw-2026.2.9.dSYM.zip`) ni `v2026.2.9` tegi uchun GitHub reliziga yuklang.
- Xom appcast URL pishirilgan feed bilan mos kelishini tekshiring: `https://raw.githubusercontent.com/openclaw/openclaw/main/appcast.xml`.
- Tezkor tekshiruvlar:
  - `curl -I https://raw.githubusercontent.com/openclaw/openclaw/main/appcast.xml` 200 qaytaradi.
  - Aktivlar yuklangach, `curl -I <enclosure url>` 200 qaytaradi.
  - Oldingi ommaviy buildda, About bo‘limidan “Check for Updates…” ni ishga tushiring va Sparkle yangi buildni toza o‘rnatishini tekshiring.

Bajarilganlik ta’rifi: imzolangan ilova + appcast nashr etilgan, yangilanish oqimi eski o‘rnatilgan versiyadan ishlaydi va reliz aktivlari GitHub reliziga biriktirilgan.
