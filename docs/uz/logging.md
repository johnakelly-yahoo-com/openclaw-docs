---
summary: "Loglash sharhi: fayl loglari, konsol chiqishi, CLI orqali kuzatish va Control UI"
read_when:
  - Sizga loglash bo‘yicha boshlovchilar uchun qulay sharh kerak
  - 1. Siz jurnal (log) darajalari yoki formatlarini sozlamoqchisiz
  - 2. Siz muammoni bartaraf etyapsiz va loglarni tezda topishingiz kerak
title: "3. Loglash"
---

# 4. Loglash

5. OpenClaw loglarni ikki joyda saqlaydi:

- 6. **Fayl loglari** (JSON qatorlari) Gateway tomonidan yoziladi.
- 7. **Konsol chiqishi** terminallarda va Control UI’da ko‘rsatiladi.

8. Ushbu sahifa loglar qayerda joylashganini, ularni qanday o‘qishni va log darajalari hamda formatlarini qanday sozlashni tushuntiradi.

## 9. Loglar qayerda joylashgan

10. Sukut bo‘yicha, Gateway aylanuvchi log faylini quyidagi manzil ostida yozadi:

11. `/tmp/openclaw/openclaw-YYYY-MM-DD.log`

12. Sana gateway xostining mahalliy vaqt mintaqasidan foydalanadi.

13. Buni `~/.openclaw/openclaw.json` da o‘zgartirishingiz mumkin:

```json
14. {
  "logging": {
    "file": "/path/to/openclaw.log"
  }
}
```

## 15. Loglarni qanday o‘qish

### 16. CLI: jonli tail (tavsiya etiladi)

17. Gateway log faylini RPC orqali tail qilish uchun CLI’dan foydalaning:

```bash
18. openclaw logs --follow
```

19. Chiqish rejimlari:

- 20. **TTY sessiyalari**: chiroyli, rangli, tuzilgan log qatorlari.
- 21. **TTY bo‘lmagan sessiyalar**: oddiy matn.
- 22. `--json`: qatorlarga bo‘lingan JSON (har bir qatorda bitta log hodisasi).
- 23. `--plain`: TTY sessiyalarida oddiy matnni majburlash.
- 24. `--no-color`: ANSI ranglarini o‘chirish.

25. JSON rejimida CLI `type` bilan belgilangan obyektlarni chiqaradi:

- 26. `meta`: oqim metama’lumotlari (fayl, kursor, hajm)
- 27. `log`: tahlil qilingan log yozuvi
- 28. `notice`: qisqartirish / aylantirish bo‘yicha eslatmalar
- 29. `raw`: tahlil qilinmagan log qatori

30. Agar Gateway bilan aloqa qilib bo‘lmasa, CLI quyidagini ishga tushirish bo‘yicha qisqa maslahatni chiqaradi:

```bash
31. openclaw doctor
```

### 32. Control UI (veb)

33. Control UI’dagi **Logs** yorlig‘i `logs.tail` yordamida xuddi shu faylni jonli kuzatadi.
34. Uni qanday ochishni bilish uchun [/web/control-ui](/web/control-ui) ga qarang.

### 35. Faqat kanal loglari

36. Kanal faoliyatini (WhatsApp/Telegram/va hokazo) filtrlash uchun quyidagidan foydalaning:

```bash
37. openclaw channels logs --channel whatsapp
```

## 38. Log formatlari

### 39. Fayl loglari (JSONL)

40. Log faylidagi har bir qator JSON obyektidir. 41. CLI va Control UI tuzilgan chiqishni (vaqt, daraja, quyi tizim, xabar) ko‘rsatish uchun ushbu yozuvlarni tahlil qiladi.

### 42. Konsol chiqishi

43. Konsol loglari **TTY’ga mos** va o‘qish qulayligi uchun formatlangan:

- 44. Quyi tizim prefikslari (masalan, `gateway/channels/whatsapp`)
- 45. Daraja bo‘yicha ranglash (info/warn/error)
- 46. Ixtiyoriy ixcham yoki JSON rejimi

47. Konsol formatlash `logging.consoleStyle` orqali boshqariladi.

## 48. Loglashni sozlash

49. Barcha loglash sozlamalari `~/.openclaw/openclaw.json` dagi `logging` ostida joylashgan.

```json
50. {
  "logging": {
    "level": "info",
    "file": "/tmp/openclaw/openclaw-YYYY-MM-DD.log",
    "consoleLevel": "info",
    "consoleStyle": "pretty",
    "redactSensitive": "tools",
    "redactPatterns": ["sk-.*"]
  }
}
```

### Log levels

- `logging.level`: **file logs** (JSONL) level.
- `logging.consoleLevel`: **console** verbosity level.

`--verbose` only affects console output; it does not change file log levels.

### Console styles

`logging.consoleStyle`:

- `pretty`: human-friendly, colored, with timestamps.
- `compact`: tighter output (best for long sessions).
- `json`: JSON per line (for log processors).

### Redaction

Tool summaries can redact sensitive tokens before they hit the console:

- `logging.redactSensitive`: `off` | `tools` (default: `tools`)
- `logging.redactPatterns`: list of regex strings to override the default set

Redaction affects **console output only** and does not alter file logs.

## Diagnostics + OpenTelemetry

Diagnostics are structured, machine-readable events for model runs **and**
message-flow telemetry (webhooks, queueing, session state). They do **not**
replace logs; they exist to feed metrics, traces, and other exporters.

Diagnostics events are emitted in-process, but exporters only attach when
diagnostics + the exporter plugin are enabled.

### OpenTelemetry vs OTLP

- **OpenTelemetry (OTel)**: the data model + SDKs for traces, metrics, and logs.
- **OTLP**: the wire protocol used to export OTel data to a collector/backend.
- OpenClaw exports via **OTLP/HTTP (protobuf)** today.

### Signals exported

- **Metrics**: counters + histograms (token usage, message flow, queueing).
- **Traces**: spans for model usage + webhook/message processing.
- **Logs**: exported over OTLP when `diagnostics.otel.logs` is enabled. Log
  volume can be high; keep `logging.level` and exporter filters in mind.

### Diagnostic event catalog

Model usage:

- `model.usage`: tokens, cost, duration, context, provider/model/channel, session ids.

Message flow:

- `webhook.received`: webhook ingress per channel.
- `webhook.processed`: webhook handled + duration.
- `webhook.error`: webhook handler errors.
- `message.queued`: message enqueued for processing.
- `message.processed`: outcome + duration + optional error.

Queue + session:

- `queue.lane.enqueue`: command queue lane enqueue + depth.
- `queue.lane.dequeue`: command queue lane dequeue + wait time.
- `session.state`: session state transition + reason.
- `session.stuck`: session stuck warning + age.
- `run.attempt`: run retry/attempt metadata.
- `diagnostic.heartbeat`: aggregate counters (webhooks/queue/session).

### Enable diagnostics (no exporter)

Use this if you want diagnostics events available to plugins or custom sinks:

```json
{
  "diagnostics": {
    "enabled": true
  }
}
```

### Diagnostics flags (targeted logs)

Use flags to turn on extra, targeted debug logs without raising `logging.level`.
Flags are case-insensitive and support wildcards (e.g. `telegram.*` or `*`).

```json
{
  "diagnostics": {
    "flags": ["telegram.http"]
  }
}
```

1. Muhit orqali bekor qilish (bir martalik):

```
2. OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload
```

3. Eslatmalar:

- 4. Flag loglari standart log fayliga yoziladi (`logging.file` bilan bir xil).
- 5. Chiqish hali ham `logging.redactSensitive` ga muvofiq yashiriladi.
- 6. To‘liq qo‘llanma: [/diagnostics/flags](/diagnostics/flags).

### 7. OpenTelemetry’ga eksport qilish

8. Diagnostikani `diagnostics-otel` plagini (OTLP/HTTP) orqali eksport qilish mumkin. 9. Bu
   OTLP/HTTP qabul qiladigan istalgan OpenTelemetry kollektor/backendi bilan ishlaydi.

```json
10. {
  "plugins": {
    "allow": ["diagnostics-otel"],
    "entries": {
      "diagnostics-otel": {
        "enabled": true
      }
    }
  },
  "diagnostics": {
    "enabled": true,
    "otel": {
      "enabled": true,
      "endpoint": "http://otel-collector:4318",
      "protocol": "http/protobuf",
      "serviceName": "openclaw-gateway",
      "traces": true,
      "metrics": true,
      "logs": true,
      "sampleRate": 0.2,
      "flushIntervalMs": 60000
    }
  }
}
```

11. Eslatmalar:

- 12. Plaginni `openclaw plugins enable diagnostics-otel` orqali ham yoqishingiz mumkin.
- 13. `protocol` hozircha faqat `http/protobuf` ni qo‘llab-quvvatlaydi. 14. `grpc` e’tiborga olinmaydi.
- 15. Metrikalar tokenlardan foydalanish, xarajat, kontekst hajmi, bajarilish davomiyligi va xabarlar oqimi
      hisoblagichlari/gistogrammalarini (webhooklar, navbatga qo‘yish, sessiya holati, navbat chuqurligi/kutish) o‘z ichiga oladi.
- 16. Traces/metrikalarni `traces` / `metrics` bilan yoqib-o‘chirish mumkin (standart: yoqilgan). 17. Traces
      yoqilganda modeldan foydalanish spanlari hamda webhook/xabarlarni qayta ishlash spanlarini o‘z ichiga oladi.
- 18. Kollektoringiz autentifikatsiya talab qilsa, `headers` ni sozlang.
- 19. Qo‘llab-quvvatlanadigan muhit o‘zgaruvchilari: `OTEL_EXPORTER_OTLP_ENDPOINT`,
      `OTEL_SERVICE_NAME`, `OTEL_EXPORTER_OTLP_PROTOCOL`.

### 20. Eksport qilingan metrikalar (nomlari + turlari)

21. Modeldan foydalanish:

- 22. `openclaw.tokens` (counter, atributlar: `openclaw.token`, `openclaw.channel`,
      `openclaw.provider`, `openclaw.model`)
- 23. `openclaw.cost.usd` (counter, atributlar: `openclaw.channel`, `openclaw.provider`,
      `openclaw.model`)
- 24. `openclaw.run.duration_ms` (histogram, atributlar: `openclaw.channel`,
      `openclaw.provider`, `openclaw.model`)
- 25. `openclaw.context.tokens` (histogram, atributlar: `openclaw.context`,
      `openclaw.channel`, `openclaw.provider`, `openclaw.model`)

26. Xabarlar oqimi:

- 27. `openclaw.webhook.received` (counter, atributlar: `openclaw.channel`,
      `openclaw.webhook`)
- 28. `openclaw.webhook.error` (counter, atributlar: `openclaw.channel`,
      `openclaw.webhook`)
- 29. `openclaw.webhook.duration_ms` (histogram, atributlar: `openclaw.channel`,
      `openclaw.webhook`)
- 30. `openclaw.message.queued` (counter, atributlar: `openclaw.channel`,
      `openclaw.source`)
- 31. `openclaw.message.processed` (counter, atributlar: `openclaw.channel`,
      `openclaw.outcome`)
- 32. `openclaw.message.duration_ms` (histogram, atributlar: `openclaw.channel`,
      `openclaw.outcome`)

33. Navbatlar + sessiyalar:

- 34. `openclaw.queue.lane.enqueue` (counter, atributlar: `openclaw.lane`)
- 35. `openclaw.queue.lane.dequeue` (counter, atributlar: `openclaw.lane`)
- 36. `openclaw.queue.depth` (histogram, atributlar: `openclaw.lane` yoki
      `openclaw.channel=heartbeat`)
- 37. `openclaw.queue.wait_ms` (histogram, atributlar: `openclaw.lane`)
- 38. `openclaw.session.state` (counter, atributlar: `openclaw.state`, `openclaw.reason`)
- 39. `openclaw.session.stuck` (counter, atributlar: `openclaw.state`)
- 40. `openclaw.session.stuck_age_ms` (histogram, atributlar: `openclaw.state`)
- 41. `openclaw.run.attempt` (counter, atributlar: `openclaw.attempt`)

### 42. Eksport qilingan spanlar (nomlari + asosiy atributlar)

- 43. `openclaw.model.usage`
  - 44. `openclaw.channel`, `openclaw.provider`, `openclaw.model`
  - 45. `openclaw.sessionKey`, `openclaw.sessionId`
  - 46. `openclaw.tokens.*` (input/output/cache_read/cache_write/total)
- 47. `openclaw.webhook.processed`
  - 48. `openclaw.channel`, `openclaw.webhook`, `openclaw.chatId`
- 49. `openclaw.webhook.error`
  - 50. `openclaw.channel`, `openclaw.webhook`, `openclaw.chatId`,
        `openclaw.error`
- `openclaw.message.processed`
  - `openclaw.channel`, `openclaw.outcome`, `openclaw.chatId`,
    `openclaw.messageId`, `openclaw.sessionKey`, `openclaw.sessionId`,
    `openclaw.reason`
- `openclaw.session.stuck`
  - `openclaw.state`, `openclaw.ageMs`, `openclaw.queueDepth`,
    `openclaw.sessionKey`, `openclaw.sessionId`

### Namuna olish + flush qilish

- Trace namuna olish: `diagnostics.otel.sampleRate` (0.0–1.0, faqat root spanlar).
- Metrikalarni eksport qilish oralig‘i: `diagnostics.otel.flushIntervalMs` (kamida 1000ms).

### Protokol bo‘yicha eslatmalar

- OTLP/HTTP endpointlari `diagnostics.otel.endpoint` yoki
  `OTEL_EXPORTER_OTLP_ENDPOINT` orqali sozlanishi mumkin.
- Agar endpoint allaqachon `/v1/traces` yoki `/v1/metrics` ni o‘z ichiga olsa, u o‘sha holicha ishlatiladi.
- Agar endpoint allaqachon `/v1/logs` ni o‘z ichiga olsa, loglar uchun u o‘sha holicha ishlatiladi.
- `diagnostics.otel.logs` asosiy logger chiqishi uchun OTLP log eksportini yoqadi.

### Log eksporti xatti-harakati

- OTLP loglari `logging.file` ga yoziladigan bir xil strukturaviy yozuvlardan foydalanadi.
- `logging.level` ga rioya qiling (fayl log darajasi). Konsol redaksiyasi OTLP loglariga **tatbiq etilmaydi**.
- Yuqori hajmli o‘rnatishlar OTLP kollektorida namuna olish/filtrlashni afzal ko‘rishi kerak.

## Nosozliklarni bartaraf etish bo‘yicha maslahatlar

- **Gateway ga ulanib bo‘lmayaptimi?** Avval `openclaw doctor` ni ishga tushiring.
- **Loglar bo‘shmi?** Gateway ishlayotganini va `logging.file` da ko‘rsatilgan fayl yo‘liga yozayotganini tekshiring.
- **Ko‘proq tafsilot kerakmi?** `logging.level` ni `debug` yoki `trace` ga o‘rnating va qayta urinib ko‘ring.
