---
summary: "`openclaw config` uchun CLI ma’lumotnomasi (config qiymatlarini olish/o‘rnatish/o‘chirish)"
read_when:
  - Konfiguratsiyani interaktiv bo‘lmagan usulda o‘qish yoki tahrirlashni xohlaysiz
title: "config"
---

# `openclaw config`

Config yordamchilari: yo‘l bo‘yicha qiymatlarni get/set/unset qilish. Subbuyruqsiz ishga tushiring —
sozlash ustasini ochadi ( `openclaw configure` bilan bir xil).

## Misollar

```bash
openclaw config get browser.executablePath
openclaw config set browser.executablePath "/usr/bin/google-chrome"
openclaw config set agents.defaults.heartbeat.every "2h"
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"
openclaw config unset tools.web.search.apiKey
```

## Yo‘llar

Yo‘llar nuqta yoki qavsli yozuvdan foydalanadi:

```bash
openclaw config get agents.defaults.workspace
openclaw config get agents.list[0].id
```

Muayyan agentni nishonga olish uchun agentlar ro‘yxati indeksidan foydalaning:

```bash
openclaw config get agents.list
openclaw config set agents.list[1].tools.exec.node "node-id-or-name"
```

## Qiymatlar

Qiymatlar imkon bo‘lsa JSON5 sifatida tahlil qilinadi; aks holda ular satr sifatida qabul qilinadi.
JSON5 tahlilini majburiy qilish uchun `--json` dan foydalaning.

```bash
openclaw config set agents.defaults.heartbeat.every "0m"
openclaw config set gateway.port 19001 --json
openclaw config set channels.whatsapp.groups '["*"]' --json
```

Tahrirlardan so‘ng gateway’ni qayta ishga tushiring.
