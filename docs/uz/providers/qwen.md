---
summary: "OpenClaw’da Qwen OAuth (bepul daraja) dan foydalaning"
read_when:
  - Siz OpenClaw bilan Qwen’dan foydalanmoqchisiz
  - Siz Qwen Coder uchun bepul darajadagi OAuth kirishini xohlaysiz
title: "Qwen"
---

# Qwen

Qwen Qwen Coder va Qwen Vision modellari uchun bepul darajadagi OAuth oqimini taqdim etadi
(kuniga 2 000 so‘rov, Qwen tezlik cheklovlariga bo‘ysunadi).

## Plaginni yoqing

```bash
openclaw plugins enable qwen-portal-auth
```

Yoqilgandan so‘ng Gateway’ni qayta ishga tushiring.

## Autentifikatsiya qiling

```bash
openclaw models auth login --provider qwen-portal --set-default
```

Bu Qwen qurilma-kodi OAuth oqimini ishga tushiradi va provayder yozuvini
`models.json` fayliga yozadi (tez almashtirish uchun `qwen` aliasi bilan).

## Model ID’lari

- `qwen-portal/coder-model`
- `qwen-portal/vision-model`

Modellarni almashtirish:

```bash
openclaw models set qwen-portal/coder-model
```

## Qwen Code CLI kirishini qayta ishlatish

Agar siz allaqachon Qwen Code CLI orqali tizimga kirgan bo‘lsangiz, OpenClaw autentifikatsiya do‘konini yuklaganda
`~/.qwen/oauth_creds.json` faylidan hisob ma’lumotlarini sinxronlaydi. Sizga baribir
`models.providers.qwen-portal` yozuvi kerak (uni yaratish uchun yuqoridagi login buyrug‘idan foydalaning).

## Eslatmalar

- Tokenlar avtomatik yangilanadi; agar yangilash muvaffaqiyatsiz bo‘lsa yoki kirish bekor qilinsa, login buyrug‘ini qayta ishga tushiring.
- Standart bazaviy URL: `https://portal.qwen.ai/v1` (agar Qwen boshqa endpoint taqdim etsa,
  `models.providers.qwen-portal.baseUrl` orqali o‘zgartiring).
- Provayder darajasidagi qoidalar uchun [Model provayderlari](/concepts/model-providers) sahifasiga qarang.
