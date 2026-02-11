---
summary: "30. Pairing sharhi: kim sizga DM yubora olishini + qaysi tugunlar qo‘shila olishini tasdiqlash"
read_when:
  - 31. DM kirish nazoratini sozlash
  - 32. Yangi iOS/Android tugunini pairing qilish
  - 33. OpenClaw xavfsizlik holatini ko‘rib chiqish
title: "34. Pairing"
---

# 35. Pairing

36. “Pairing” — bu OpenClaw’ning aniq **egasi tasdig‘i** bosqichi.
37. U ikki joyda qo‘llaniladi:

1. 38. **DM pairing** (bot bilan kim gaplasha olishi)
2. 39. **Node pairing** (qaysi qurilmalar/tugunlar gateway tarmog‘iga qo‘shila olishi)

40) Xavfsizlik konteksti: [Security](/gateway/security)

## 41. 1. DM pairing (kiruvchi chatga kirish)

42. Kanal DM siyosati `pairing` ga sozlanganda, noma’lum yuboruvchilar qisqa kod oladi va siz tasdiqlamaguningizcha ularning xabari **qayta ishlanmaydi**.

43. Standart DM siyosatlari bu yerda hujjatlashtirilgan: [Security](/gateway/security)

44. Pairing kodlari:

- 45. 8 ta belgi, katta harflar, noaniq belgilar yo‘q (`0O1I`).
- 46. **1 soatdan keyin muddati tugaydi**. 47. Bot pairing xabarini faqat yangi so‘rov yaratilganda yuboradi (taxminan har bir yuboruvchi uchun soatiga bir marta).
- 48. Kutilayotgan DM pairing so‘rovlari sukut bo‘yicha **har bir kanal uchun 3 ta** bilan cheklanadi; bittasi muddati tugamaguncha yoki tasdiqlanmaguncha qo‘shimcha so‘rovlar e’tiborga olinmaydi.

### 49. Yuboruvchini tasdiqlash

```bash
50. openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

Supported channels: `telegram`, `whatsapp`, `signal`, `imessage`, `discord`, `slack`.

### Where the state lives

Stored under `~/.openclaw/credentials/`:

- Pending requests: `<channel>-pairing.json`
- Approved allowlist store: `<channel>-allowFrom.json`

Treat these as sensitive (they gate access to your assistant).

## 2. Node device pairing (iOS/Android/macOS/headless nodes)

Nodes connect to the Gateway as **devices** with `role: node`. The Gateway
creates a device pairing request that must be approved.

### 13. Agar `device-pair` plagini ishlatilsa, birinchi martalik qurilma juftlashni to‘liq Telegram orqali bajarish mumkin:

14. Telegram’da botingizga xabar yuboring: `/pair`

1. 15. Bot ikkita xabar bilan javob beradi: ko‘rsatma xabari va alohida **sozlash kodi** xabari (Telegram’da oson nusxalash/joylash uchun).
2. 16. Telefoningizda OpenClaw iOS ilovasini oching → Settings → Gateway.
3. 17. Sozlash kodini joylashtiring va ulang.
4. 18. Telegram’ga qayting: `/pair approve`
5. 19. Sozlash kodi base64 formatida kodlangan JSON yuklamasidir va u quyidagilarni o‘z ichiga oladi:

20) `url`: Gateway WebSocket URL manzili (`ws://...` yoki `wss://...`)

- 21. `token`: qisqa muddatli juftlash tokeni
- 22. Sozlash kodi amal qilayotgan paytda uni parol kabi saqlang.

23. Ba’zi buyruqlar Telegram’ning buyruqlar menyusida ro‘yxatdan o‘tmasdan plaginlar/ko‘nikmalar orqali qayta ishlanishi mumkin.

### Approve a node device

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
```

### Node pairing state storage

Stored under `~/.openclaw/devices/`:

- `pending.json` (short-lived; pending requests expire)
- `paired.json` (paired devices + tokens)

### Notes

- The legacy `node.pair.*` API (CLI: `openclaw nodes pending/approve`) is a
  separate gateway-owned pairing store. WS nodes still require device pairing.

## Related docs

- Security model + prompt injection: [Security](/gateway/security)
- Updating safely (run doctor): [Updating](/install/updating)
- Channel configs:
  - Telegram: [Telegram](/channels/telegram)
  - WhatsApp: [WhatsApp](/channels/whatsapp)
  - Signal: [Signal](/channels/signal)
  - BlueBubbles (iMessage): [BlueBubbles](/channels/bluebubbles)
  - iMessage (legacy): [iMessage](/channels/imessage)
  - Discord: [Discord](/channels/discord)
  - Slack: [Slack](/channels/slack)
