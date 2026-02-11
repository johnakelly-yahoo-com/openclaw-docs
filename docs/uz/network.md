---
summary: "Tarmoq xabi: gateway yuzalari, juftlash, kashfiyot va xavfsizlik"
read_when:
  - Sizga tarmoq arxitekturasi + xavfsizlik bo‘yicha umumiy ko‘rinish kerak
  - Siz lokal va tailnet kirishi yoki juftlashni sozlayapsiz
  - Siz tarmoq hujjatlarining kanonik ro‘yxatini xohlaysiz
title: "Tarmoq"
---

# Tarmoq xabi

Ushbu xab OpenClaw qanday qilib localhost, LAN va tailnet bo‘ylab qurilmalarni ulashi, juftlashi va himoyalashini tushuntiruvchi asosiy hujjatlarga havola qiladi.

## Asosiy model

- [Gateway arxitekturasi](/concepts/architecture)
- [Gateway protokoli](/gateway/protocol)
- [Gateway runbook](/gateway)
- [Veb yuzalar + bind rejimlari](/web)

## Juftlash + identifikatsiya

- [Juftlash bo‘yicha umumiy ko‘rinish (DM + tugunlar)](/channels/pairing)
- [Gateway egaligidagi tugunlarni juftlash](/gateway/pairing)
- [Qurilmalar CLI (juftlash + token aylantirish)](/cli/devices)
- [Juftlash CLI (DM tasdiqlari)](/cli/pairing)

Lokal ishonch:

- Lokal ulanishlar (loopback yoki gateway xostining o‘z tailnet manzili) bir xostdagi UX silliq bo‘lishi uchun juftlashda avtomatik tasdiqlanishi mumkin.
- Lokal bo‘lmagan tailnet/LAN mijozlari hali ham aniq juftlash tasdig‘ini talab qiladi.

## Kashfiyot + transportlar

- [Kashfiyot va transportlar](/gateway/discovery)
- [Bonjour / mDNS](/gateway/bonjour)
- [Masofaviy kirish (SSH)](/gateway/remote)
- [Tailscale](/gateway/tailscale)

## Tugunlar + transportlar

- [Tugunlar bo‘yicha umumiy ko‘rinish](/nodes)
- [Bridge protokoli (meros tugunlar)](/gateway/bridge-protocol)
- [Tugun runbook: iOS](/platforms/ios)
- [Node runbook: Android](/platforms/android)

## Xavfsizlik

- [Xavfsizlik sharhi](/gateway/security)
- [Gateway konfiguratsiyasi ma’lumotnomasi](/gateway/configuration)
- [Nosozliklarni bartaraf etish](/gateway/troubleshooting)
- [Doctor](/gateway/doctor)
