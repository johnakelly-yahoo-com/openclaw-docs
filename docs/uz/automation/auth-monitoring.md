---
summary: "Model provayderlari uchun OAuth muddati tugashini kuzatish"
read_when:
  - Auth muddati tugashini kuzatishni yoki ogohlantirishlarni sozlash
  - Claude Code / Codex OAuth yangilanish tekshiruvlarini avtomatlashtirish
title: "Auth monitoringi"
---

# Auth monitoringi

OpenClaw OAuth muddati holatini `openclaw models status` orqali ochib beradi. Buni avtomatlashtirish va ogohlantirishlar uchun ishlating; telefon ish jarayonlari uchun skriptlar ixtiyoriy qo‘shimchalardir.

## Afzal: CLI tekshiruvi (portativ)

```bash
openclaw models status --check
```

Chiqish kodlari:

- `0`: OK
- `1`: muddati tugagan yoki yetishmayotgan hisob ma’lumotlari
- `2`: tez orada tugaydi (24 soat ichida)

1. Bu cron/systemd da ishlaydi va qo‘shimcha skriptlarni talab qilmaydi.

## Ixtiyoriy skriptlar (ops / telefon ish jarayonlari)

Bular `scripts/` ostida joylashgan va **ixtiyoriy**. Ular gateway xostiga SSH kirishini talab qiladi va systemd + Termux uchun moslangan.

- `scripts/claude-auth-status.sh` endi `openclaw models status --json` dan haqiqat manbai sifatida foydalanadi (CLI mavjud bo‘lmasa, to‘g‘ridan-to‘g‘ri fayl o‘qishga qaytadi), shuning uchun taymerlar uchun `openclaw`ni `PATH`da saqlang.
- `scripts/auth-monitor.sh`: cron/systemd taymeri nishoni; ogohlantirishlarni yuboradi (ntfy yoki telefon).
- `scripts/systemd/openclaw-auth-monitor.{service,timer}`: systemd foydalanuvchi taymeri.
- `scripts/claude-auth-status.sh`: Claude Code + OpenClaw auth tekshiruvchisi (to‘liq/json/oddiy).
- `scripts/mobile-reauth.sh`: SSH orqali yo‘naltirilgan qayta-auth oqimi.
- `scripts/termux-quick-auth.sh`: bir bosishda vidjet holati + auth URL’ni ochish.
- `scripts/termux-auth-widget.sh`: to‘liq yo‘naltirilgan vidjet oqimi.
- `scripts/termux-sync-widget.sh`: Claude Code hisob ma’lumotlarini → OpenClaw’ga sinxronlash.

Agar telefon avtomatlashtirish yoki systemd taymerlari kerak bo‘lmasa, bu skriptlarni o‘tkazib yuboring.
