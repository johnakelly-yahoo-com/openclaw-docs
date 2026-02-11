---
summary: "26. Zalo Personal plagini: QR orqali login + zca-cli orqali xabar almashish (plagin o‘rnatish + kanal sozlamasi + CLI + vosita)"
read_when:
  - 27. Siz OpenClaw’da Zalo Personal (rasmiy bo‘lmagan) qo‘llab-quvvatlashni xohlaysiz
  - Siz zalouser plaginini sozlayapsiz yoki ishlab chiqyapsiz
title: "29. Zalo Personal Plagini"
---

# 30. Zalo Personal (plagin)

31. `zca-cli` yordamida oddiy Zalo foydalanuvchi akkauntini avtomatlashtiruvchi, plagin orqali OpenClaw uchun Zalo Personal qo‘llab-quvvatlashi.

> 32. **Ogohlantirish:** Rasmiy bo‘lmagan avtomatlashtirish akkauntning to‘xtatilishi/bloklanishiga olib kelishi mumkin. 33. O‘z xavfingiz ostida foydalaning.

## 34. Nomlash

35. Kanal identifikatori `zalouser`, bu **shaxsiy Zalo foydalanuvchi akkaunti** (rasmiy bo‘lmagan) avtomatlashtirilishini aniq ko‘rsatish uchun. 36. `zalo` nomini kelajakda mumkin bo‘lgan rasmiy Zalo API integratsiyasi uchun saqlab qolamiz.

## 37. Qayerda ishlaydi

38. Ushbu plagin **Gateway jarayoni ichida** ishlaydi.

39. Agar siz masofaviy Gateway’dan foydalansangiz, uni **Gateway ishlayotgan mashinada** o‘rnating/sozlang, so‘ng Gateway’ni qayta ishga tushiring.

## 40. O‘rnatish

### 41. Variant A: npm’dan o‘rnatish

```bash
42. openclaw plugins install @openclaw/zalouser
```

43. Shundan so‘ng Gateway’ni qayta ishga tushiring.

### 44. Variant B: lokal papkadan o‘rnatish (dev)

```bash
45. openclaw plugins install ./extensions/zalouser
cd ./extensions/zalouser && pnpm install
```

46. Shundan so‘ng Gateway’ni qayta ishga tushiring.

## 47. Old shart: zca-cli

48. Gateway ishlayotgan mashinada `zca` `PATH` da bo‘lishi kerak:

```bash
49. zca --version
```

## 50. Sozlama

Channel config lives under `channels.zalouser` (not `plugins.entries.*`):

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

## CLI

```bash
openclaw channels login --channel zalouser
openclaw channels logout --channel zalouser
openclaw channels status --probe
openclaw message send --channel zalouser --target <threadId> --message "Hello from OpenClaw"
openclaw directory peers list --channel zalouser --query "name"
```

## Agent tool

Tool name: `zalouser`

Actions: `send`, `image`, `link`, `friends`, `groups`, `me`, `status`
