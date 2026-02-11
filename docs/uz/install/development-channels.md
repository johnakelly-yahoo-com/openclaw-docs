---
summary: "Stable, beta, and dev channels: semantics, switching, and tagging"
read_when:
  - You want to switch between stable/beta/dev
  - You are tagging or publishing prereleases
title: "Development Channels"
---

# Development channels

Last updated: 2026-01-21

OpenClaw ships three update channels:

- **stable**: npm dist-tag `latest`.
- **beta**: npm dist-tag `beta` (builds under test).
- **dev**: `main` (git) tarmog‘ining harakatlanuvchi boshi. npm dist-tag: `dev` (nashr qilinganda).

Biz buildlarni **beta** ga jo‘natamiz, ularni sinovdan o‘tkazamiz, so‘ng **tekshirilgan buildni `latest` ga ko‘taramiz** — versiya raqamini o‘zgartirmasdan. npm o‘rnatishlari uchun haqiqat manbai dist-taglardir.

## Kanallarni almashtirish

Git checkout:

```bash
openclaw update --channel stable
openclaw update --channel beta
openclaw update --channel dev
```

- `stable`/`beta` mos keladigan eng so‘nggi tegni checkout qiladi (ko‘pincha bir xil teg).
- `dev` `main` ga o‘tadi va upstream bilan rebase qiladi.

npm/pnpm global o‘rnatish:

```bash
openclaw update --channel stable
openclaw update --channel beta
openclaw update --channel dev
```

Bu mos npm dist-tag (`latest`, `beta`, `dev`) orqali yangilanadi.

`--channel` bilan kanalni **aniq** almashtirganda, OpenClaw o‘rnatish usulini ham moslaydi:

- `dev` git checkoutni ta’minlaydi (standart `~/openclaw`, `OPENCLAW_GIT_DIR` bilan o‘zgartiriladi), uni yangilaydi va global CLI’ni shu checkoutdan o‘rnatadi.
- `stable`/`beta` mos dist-tag yordamida npm’dan o‘rnatadi.

Maslahat: agar stable + dev ni parallel ishlatmoqchi bo‘lsangiz, ikkita klonni saqlang va gateway’ni stable ga yo‘naltiring.

## Plaginlar va kanallar

`openclaw update` bilan kanalni almashtirganda, OpenClaw plagin manbalarini ham sinxronlaydi:

- `dev` git checkoutdan kelgan paketlangan plaginlarni afzal ko‘radi.
- `stable` va `beta` npm orqali o‘rnatilgan plagin paketlarini tiklaydi.

## Teglash bo‘yicha eng yaxshi amaliyotlar

- Git checkoutlar tushishini xohlagan relizlarni teg bilan belgilang (`vYYYY.M.D` yoki `vYYYY.M.D-<patch>`).
- Teglarni o‘zgarmas saqlang: hech qachon tegni ko‘chirmang yoki qayta ishlatmang.
- npm o‘rnatishlari uchun haqiqat manbai bo‘lib dist-taglar qoladi:
  - `latest` → stable
  - `beta` → nomzod build
  - `dev` → main snapshot (ixtiyoriy)

## macOS ilovasi mavjudligi

Beta va dev buildlarida macOS ilovasi relizi **bo‘lmasligi** mumkin. Bu muammo emas:

- Git tegi va npm dist-tagi baribir nashr qilinishi mumkin.
- Reliz eslatmalari yoki changelog’da “bu beta uchun macOS build yo‘q” deb ko‘rsating.
