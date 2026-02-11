---
summary: "Nosozliklarni aniqlash vositalari: kuzatish rejimi, xom model oqimlari va reasoning sizib chiqishini kuzatish"
read_when:
  - Reasoning sizib chiqishini aniqlash uchun xom model chiqishini tekshirishingiz kerak
  - Iteratsiya paytida Gateway’ni watch rejimida ishga tushirmoqchisiz
  - Takrorlanadigan nosozliklarni aniqlash ish jarayoniga muhtoj siz
title: "Nosozliklarni aniqlash"
---

# Nosozliklarni aniqlash

Bu sahifa oqimli chiqishlar uchun nosozliklarni aniqlash yordamchilarini qamrab oladi, ayniqsa provayder reasoning’ni oddiy matn bilan aralashtirganda.

## Runtime uchun debug override’lar

Chatda **faqat runtime uchun** (xotirada, diskda emas) konfiguratsiya override’larini o‘rnatish uchun `/debug`dan foydalaning.
`/debug` sukut bo‘yicha o‘chirilgan; `commands.debug: true` bilan yoqing.
Bu `openclaw.json` faylini tahrirlashsiz, kamdan‑kam ishlatiladigan sozlamalarni yoqib‑o‘chirish kerak bo‘lganda qulay.

Misollar:

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug unset messages.responsePrefix
/debug reset
```

`/debug reset` barcha override’larni tozalaydi va diskdagi konfiguratsiyaga qaytaradi.

## Gateway kuzatuv (watch) rejimi

Tezkor iteratsiya uchun gateway’ni fayl kuzatuvchi ostida ishga tushiring:

```bash
pnpm gateway:watch --force
```

Bu quyidagiga mos keladi:

```bash
tsx watch src/entry.ts gateway --force
```

`gateway:watch` dan keyin istalgan gateway CLI flag’larini qo‘shing — ular har bir qayta ishga tushishda uzatiladi.

## Dev profili + dev gateway (--dev)

Holatni izolyatsiya qilish va xatolarni tuzatish uchun xavfsiz, vaqtinchalik muhit yaratish maqsadida dev profilidan foydalaning. **Ikki** ta `--dev` flag mavjud:

- **Global `--dev` (profil):** holatni `~/.openclaw-dev` ostida izolyatsiya qiladi va gateway portini sukut bo‘yicha `19001` ga o‘rnatadi (undan kelib chiqqan portlar ham mos ravishda siljiydi).
- **`gateway --dev`: Gateway’ga konfiguratsiya + workspace yo‘q bo‘lsa avtomatik yaratishni aytadi** (va BOOTSTRAP.md’ni o‘tkazib yuboradi).

Tavsiya etilgan oqim (dev profil + dev bootstrap):

```bash
pnpm gateway:dev
OPENCLAW_PROFILE=dev openclaw tui
```

Agar hali global o‘rnatma bo‘lmasa, CLI’ni `pnpm openclaw ...` orqali ishga tushiring.

Bu nima qiladi:

1. **Profil izolyatsiyasi** (global `--dev`)
   - `OPENCLAW_PROFILE=dev`
   - `OPENCLAW_STATE_DIR=~/.openclaw-dev`
   - `OPENCLAW_CONFIG_PATH=~/.openclaw-dev/openclaw.json`
   - `OPENCLAW_GATEWAY_PORT=19001` (brauzer/canvas ham mos ravishda siljiydi)

2. **Dev bootstrap** (`gateway --dev`)
   - Agar yo‘q bo‘lsa minimal konfiguratsiyani yozadi (`gateway.mode=local`, loopback’ga bind).
   - `agent.workspace` ni dev workspace’ga o‘rnatadi.
   - `agent.skipBootstrap=true` qilib belgilaydi (BOOTSTRAP.md yo‘q).
   - Agar yo‘q bo‘lsa workspace fayllarini yaratadi:
     `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`.
   - Sukut bo‘yicha identifikatsiya: **C3‑PO** (protokol droidi).
   - Dev rejimida kanal provayderlarini o‘tkazib yuboradi (`OPENCLAW_SKIP_CHANNELS=1`).

Qayta boshlash oqimi (toza start):

```bash
pnpm gateway:dev:reset
```

Eslatma: `--dev` **global** profil flag’i bo‘lib, ayrim runner’lar uni yutib yuboradi.
Agar aniq ko‘rsatish kerak bo‘lsa, muhit o‘zgaruvchisi shaklidan foydalaning:

```bash
OPENCLAW_PROFILE=dev openclaw gateway --dev --reset
```

`--reset` konfiguratsiya, credential’lar, sessiyalar va dev workspace’ni ( `rm` emas, `trash` orqali) tozalaydi, so‘ng sukutdagi dev sozlamasini qayta yaratadi.

Maslahat: agar dev bo‘lmagan gateway allaqachon ishlayotgan bo‘lsa (launchd/systemd), avval uni to‘xtating:

```bash
openclaw gateway stop
```

## Xom oqim (raw stream) loglash (OpenClaw)

OpenClaw har qanday filtrlash/formatlashdan oldin **assistant’ning xom oqimini** loglashi mumkin.
Bu reasoning’ning oddiy matn delta’lari sifatida kelayotganini (yoki alohida thinking bloklari sifatida) ko‘rishning eng yaxshi usuli.

CLI orqali yoqing:

```bash
pnpm gateway:watch --force --raw-stream
```

Ixtiyoriy yo‘lni almashtirish:

```bash
pnpm gateway:watch --force --raw-stream --raw-stream-path ~/.openclaw/logs/raw-stream.jsonl
```

Mos keluvchi env o‘zgaruvchilar:

```bash
OPENCLAW_RAW_STREAM=1
OPENCLAW_RAW_STREAM_PATH=~/.openclaw/logs/raw-stream.jsonl
```

Sukut bo‘yicha fayl:

`~/.openclaw/logs/raw-stream.jsonl`

## Raw chunk logging (pi-mono)

**raw OpenAI-compat chunklar** bloklarga ajratilishidan oldin ularni yozib olish uchun, pi-mono alohida logger taqdim etadi:

```bash
PI_RAW_STREAM=1
```

Ixtiyoriy yo‘l:

```bash
PI_RAW_STREAM_PATH=~/.pi-mono/logs/raw-openai-completions.jsonl
```

Standart fayl:

`~/.pi-mono/logs/raw-openai-completions.jsonl`

> Eslatma: bu faqat pi-mono’ning `openai-completions` provayderidan foydalanadigan jarayonlar tomonidan chiqariladi.

## Xavfsizlik bo‘yicha eslatmalar

- Raw stream loglari to‘liq promptlar, asbob chiqishi va foydalanuvchi ma’lumotlarini o‘z ichiga olishi mumkin.
- Loglarni lokal saqlang va debuggingdan keyin o‘chiring.
- Agar loglarni ulashsangiz, avval maxfiy kalitlar va PII ma’lumotlarini tozalang.
