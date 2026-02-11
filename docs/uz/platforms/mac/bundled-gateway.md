---
summary: "macOS’dagi Gateway ish vaqti (tashqi launchd xizmati)"
read_when:
  - OpenClaw.app’ni paketlash
  - macOS Gateway launchd xizmatini sozlash (debug)
  - macOS uchun Gateway CLI’ni o‘rnatish
title: "macOS’da Gateway"
---

# macOS’da Gateway (tashqi launchd)

OpenClaw.app endi Node/Bun yoki Gateway ish vaqtini o‘z ichiga olmaydi. macOS ilovasi **tashqi** `openclaw` CLI o‘rnatilishini talab qiladi, Gateway’ni bola jarayon sifatida ishga tushirmaydi va Gateway’ni doimiy ishlatib turish uchun foydalanuvchi darajasidagi launchd xizmatini boshqaradi (yoki agar allaqachon mahalliy Gateway ishlayotgan bo‘lsa, unga ulanadi).

## CLI’ni o‘rnating (mahalliy rejim uchun majburiy)

Mac’da Node 22+ kerak, so‘ng `openclaw`’ni global o‘rnating:

```bash
npm install -g openclaw@<version>
```

macOS ilovasidagi **Install CLI** tugmasi xuddi shu jarayonni npm/pnpm orqali bajaradi (Gateway ish vaqti uchun bun tavsiya etilmaydi).

## Launchd (Gateway LaunchAgent sifatida)

Yorliq:

- `bot.molt.gateway` (yoki `bot.molt.<profile>``; eski `com.openclaw.\*\` qolishi mumkin)

Plist joylashuvi (har bir foydalanuvchi uchun):

- `~/Library/LaunchAgents/bot.molt.gateway.plist`
  (yoki `~/Library/LaunchAgents/bot.molt.<profile>`.plist\`)

Boshqaruv:

- macOS ilovasi Mahalliy rejimda LaunchAgent’ni o‘rnatish/yangilashni boshqaradi.
- CLI ham o‘rnatishi mumkin: `openclaw gateway install`.

Xulq-atvor:

- “OpenClaw Active” LaunchAgent’ni yoqadi/o‘chiradi.
- Ilovadan chiqish Gateway’ni to‘xtatmaydi (launchd uni tirik saqlaydi).
- Agar sozlangan portda Gateway allaqachon ishlayotgan bo‘lsa, ilova yangisini boshlash o‘rniga unga ulanadi.

Jurnallar:

- launchd stdout/err: `/tmp/openclaw/openclaw-gateway.log`

## Versiyalar mosligi

macOS ilovasi Gateway versiyasini o‘z versiyasi bilan solishtiradi. Agar ular mos kelmasa, global CLI’ni ilova versiyasiga moslab yangilang.

## Tezkor tekshiruv

```bash
openclaw --version

OPENCLAW_SKIP_CHANNELS=1 \
OPENCLAW_SKIP_CANVAS_HOST=1 \
openclaw gateway --port 18999 --bind loopback
```

So‘ng:

```bash
openclaw gateway call health --url ws://127.0.0.1:18999 --timeout 3000
```
