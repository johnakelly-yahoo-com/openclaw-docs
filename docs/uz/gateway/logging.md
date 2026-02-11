---
summary: "Loglash sirtlari, fayl loglari, WS log uslublari va konsol formatlash"
read_when:
  - Loglash chiqishini yoki formatlarini o‘zgartirish
  - CLI yoki gateway chiqishini nosozliklarni tuzatish
title: "Loglash"
---

# Loglash

Foydalanuvchi uchun umumiy ko‘rinish (CLI + Control UI + konfiguratsiya) uchun qarang: [/logging](/logging).

OpenClaw ikkita log “sirtiga” ega:

- **Konsol chiqishi** (terminalda / Debug UI’da ko‘radiganingiz).
- **Fayl loglari** (JSON qatorlari) gateway logger tomonidan yoziladi.

## Faylga asoslangan logger

- Standart aylanuvchi log fayli `/tmp/openclaw/` ostida (kuniga bitta fayl): `openclaw-YYYY-MM-DD.log`
  - Sana gateway xostining lokal vaqt mintaqasidan foydalanadi.
- Log fayl yo‘li va darajasi `~/.openclaw/openclaw.json` orqali sozlanishi mumkin:
  - `logging.file`
  - `logging.level`

Fayl formati — har bir qatorda bitta JSON obyekt.

Control UI’dagi Logs yorlig‘i ushbu faylni gateway orqali kuzatadi (`logs.tail`).
CLI ham xuddi shuni qila oladi:

```bash
openclaw logs --follow
```

**Verbose va log darajalari**

- **Fayl loglari** faqat `logging.level` orqali boshqariladi.
- `--verbose` faqat **konsol batafsilligiga** (va WS log uslubiga) ta’sir qiladi; u fayl log darajasini **oshirmaydi**.
- Faqat verbose’da ko‘rinadigan tafsilotlarni fayl loglariga yozish uchun `logging.level` ni `debug` yoki `trace` ga o‘rnating.

## Konsolni ushlash

CLI `console.log/info/warn/error/debug/trace` ni ushlab, ularni fayl loglariga yozadi, shu bilan birga stdout/stderr’ga chiqarishni davom ettiradi.

Konsol batafsilligini mustaqil ravishda sozlashingiz mumkin:

- `logging.consoleLevel` (standart `info`)
- `logging.consoleStyle` (`pretty` | `compact` | `json`)

## Asboblar xulosasini yashirish

Verbose asboblar xulosalari (masalan, `🛠️ Exec: ...`) konsol oqimiga tushishidan oldin maxfiy tokenlarni yashirishi mumkin. Bu **faqat asboblar uchun** va fayl loglarini o‘zgartirmaydi.

- `logging.redactSensitive`: `off` | `tools` (standart: `tools`)
- `logging.redactPatterns`: regex satrlaridan iborat massiv (standartlarni bekor qiladi)
  - Xom regex satrlaridan foydalaning (avto `gi`), yoki maxsus flaglar kerak bo‘lsa `/pattern/flags`.
  - Mos kelishlar birinchi 6 + oxirgi 4 belgini saqlab yashiriladi (uzunligi >= 18), aks holda `***`.
  - Standartlar keng tarqalgan kalit tayinlashlari, CLI flaglari, JSON maydonlari, bearer sarlavhalari, PEM bloklari va mashhur token prefikslarini qamrab oladi.

## Gateway WebSocket loglari

Gateway WebSocket protokoli loglarini ikki rejimda chiqaradi:

- **Oddiy rejim (`--verbose` yo‘q)**: faqat “qiziqarli” RPC natijalari chiqariladi:
  - xatolar (`ok=false`)
  - sekin chaqiruvlar (standart chegarasi: `>= 50ms`)
  - tahlil (parse) xatolari
- **Verbose rejim (`--verbose`)**: barcha WS so‘rov/javob trafikini chiqaradi.

### WS log uslubi

`openclaw gateway` har bir gateway uchun uslubni almashtirishni qo‘llab-quvvatlaydi:

- `--ws-log auto` (standart): oddiy rejim optimallashtirilgan; verbose rejimda ixcham chiqish ishlatiladi
- `--ws-log compact`: verbose’da ixcham chiqish (juftlangan so‘rov/javob)
- `--ws-log full`: verbose’da har bir freym bo‘yicha to‘liq chiqish
- `--compact`: `--ws-log compact` uchun alias

Misollar:

```bash
# optimized (only errors/slow)
openclaw gateway

# show all WS traffic (paired)
openclaw gateway --verbose --ws-log compact

# show all WS traffic (full meta)
openclaw gateway --verbose --ws-log full
```

## Console formatting (subsystem logging)

The console formatter is **TTY-aware** and prints consistent, prefixed lines.
Subsystem loggers keep output grouped and scannable.

Behavior:

- **Subsystem prefixes** on every line (e.g. `[gateway]`, `[canvas]`, `[tailscale]`)
- **Subsystem colors** (stable per subsystem) plus level coloring
- **Color when output is a TTY or the environment looks like a rich terminal** (`TERM`/`COLORTERM`/`TERM_PROGRAM`), respects `NO_COLOR`
- **Shortened subsystem prefixes**: drops leading `gateway/` + `channels/`, keeps last 2 segments (e.g. `whatsapp/outbound`)
- **Sub-loggers by subsystem** (auto prefix + structured field `{ subsystem }`)
- **`logRaw()`** for QR/UX output (no prefix, no formatting)
- **Console styles** (e.g. `pretty | compact | json`)
- **Console log level** separate from file log level (file keeps full detail when `logging.level` is set to `debug`/`trace`)
- **WhatsApp xabar matnlari** `debug` darajasida log qilinadi (ularni ko‘rish uchun `--verbose` dan foydalaning)

This keeps existing file logs stable while making interactive output scannable.
