---
summary: "`openclaw configure` uchun CLI ma’lumotnomasi (interaktiv konfiguratsiya so‘rovlari)"
read_when:
  - Hisob ma’lumotlari, qurilmalar yoki agent standartlarini interaktiv tarzda sozlashni xohlaysiz
title: "configure"
---

# `openclaw configure`

Hisob ma’lumotlari, qurilmalar va agent standartlarini sozlash uchun interaktiv so‘rov.

Eslatma: **Model** bo‘limi endi
`agents.defaults.models` allowlist’i uchun ko‘p tanlovni o‘z ichiga oladi ( `/model` da va model tanlagichda ko‘rinadiganlar).

Maslahat: subbuyruqsiz `openclaw config` ishga tushirilsa, xuddi shu ustani ochadi. Interaktiv bo‘lmagan tahrirlar uchun `openclaw config get|set|unset` dan foydalaning.

Bog‘liq:

- Gateway konfiguratsiyasi ma’lumotnomasi: [Configuration](/gateway/configuration)
- Config CLI: [Config](/cli/config)

Eslatmalar:

- Gateway qayerda ishlashini tanlash har doim `gateway.mode` ni yangilaydi. Agar sizga faqat shu kerak bo‘lsa, boshqa bo‘limlarsiz "Continue" ni tanlashingiz mumkin.
- Kanalga yo‘naltirilgan xizmatlar (Slack/Discord/Matrix/Microsoft Teams) sozlash vaqtida kanal/xona allowlist’larini so‘raydi. Siz nomlar yoki ID’larni kiritishingiz mumkin; ustoz (wizard) imkon bo‘lsa nomlarni ID’larga moslaydi.

## Misollar

```bash
openclaw configure
openclaw configure --section models --section channels
```
