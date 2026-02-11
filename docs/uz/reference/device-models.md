---
summary: "How OpenClaw vendors Apple device model identifiers for friendly names in the macOS app."
read_when:
  - Qurilma model identifikatori moslamalarini yoki NOTICE/litsenziya fayllarini yangilash
  - Instances UI qurilma nomlarini qanday ko‘rsatishini o‘zgartirish
title: "Qurilma modellari ma’lumotlar bazasi"
---

# Qurilma modellari ma’lumotlar bazasi (qulay nomlar)

macOS hamroh ilovasi Apple model identifikatorlarini (masalan, `iPad16,6`, `Mac16,6`) o‘qilishi oson nomlarga moslab, **Instances** UI’da ko‘rsatadi.

Moslash JSON ko‘rinishida quyida joylashgan:

- `apps/macos/Sources/OpenClaw/Resources/DeviceModels/`

## Ma’lumotlar manbai

Hozirda moslash MIT litsenziyali quyidagi repozitoriydan olinadi:

- kyle-seongwoo-jun/apple-device-identifiers

Buildlarni deterministik saqlash uchun JSON fayllar aniq upstream commitlarga bog‘langan (ular `apps/macos/Sources/OpenClaw/Resources/DeviceModels/NOTICE.md` da qayd etilgan).

## Ma’lumotlar bazasini yangilash

1. Bog‘lamoqchi bo‘lgan upstream commitlarni tanlang (bittasi iOS uchun, bittasi macOS uchun).
2. `apps/macos/Sources/OpenClaw/Resources/DeviceModels/NOTICE.md` dagi commit xeshlarini yangilang.
3. Tanlangan commitlarga bog‘langan JSON fayllarni qayta yuklab oling:

```bash
IOS_COMMIT="<commit sha for ios-device-identifiers.json>"
MAC_COMMIT="<commit sha for mac-device-identifiers.json>"

curl -fsSL "https://raw.githubusercontent.com/kyle-seongwoo-jun/apple-device-identifiers/${IOS_COMMIT}/ios-device-identifiers.json" \
  -o apps/macos/Sources/OpenClaw/Resources/DeviceModels/ios-device-identifiers.json

curl -fsSL "https://raw.githubusercontent.com/kyle-seongwoo-jun/apple-device-identifiers/${MAC_COMMIT}/mac-device-identifiers.json" \
  -o apps/macos/Sources/OpenClaw/Resources/DeviceModels/mac-device-identifiers.json
```

4. `apps/macos/Sources/OpenClaw/Resources/DeviceModels/LICENSE.apple-device-identifiers.txt` upstream bilan mos kelishini tekshiring (agar upstream litsenziyasi o‘zgargan bo‘lsa, almashtiring).
5. macOS ilovasi toza tarzda yig‘ilishini tekshiring (ogohlantirishlarsiz):

```bash
swift build --package-path apps/macos
```
