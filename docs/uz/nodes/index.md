---
summary: "Nodes: pairing, capabilities, permissions, and CLI helpers for canvas/camera/screen/system"
read_when:
  - 1. iOS/Android tugunlarini shlyuzga ulash
  - 2. Agent konteksti uchun tugun canvas/kameradan foydalanish
  - 3. Yangi tugun buyruqlari yoki CLI yordamchilarini qo‘shish
title: "4. Tugunlar"
---

# Nodes

6. **Tugun** — bu Gateway **WebSocket**’iga (operatorlar bilan bir xil port) `role: "node"` bilan ulanadigan va `node.invoke` orqali buyruqlar sirtini (masalan, `canvas.*`, `camera.*`, `system.*`) taqdim etadigan hamroh qurilma (macOS/iOS/Android/headless). 7. Protokol tafsilotlari: [Gateway protocol](/gateway/protocol).

Legacy transport: [Bridge protocol](/gateway/bridge-protocol) (TCP JSONL; deprecated/removed for current nodes).

macOS can also run in **node mode**: the menubar app connects to the Gateway’s WS server and exposes its local canvas/camera commands as a node (so `openclaw nodes …` works against this Mac).

Notes:

- 11. Tugunlar — **periferiyalar**, shlyuzlar emas. 12. Ular gateway xizmatini ishga tushirmaydi.
- 13. Telegram/WhatsApp va boshqalar xabarlari tugunlarga emas, **gateway**’ga keladi.
- 14. Nosozliklarni bartaraf etish qo‘llanmasi: [/nodes/troubleshooting](/nodes/troubleshooting)

## Pairing + status

**WS nodes use device pairing.** Nodes present a device identity during `connect`; the Gateway
creates a device pairing request for `role: node`. 17. Qurilmalar CLI (yoki UI) orqali tasdiqlang.

18. Tezkor CLI:

```bash
19. openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
```

20. Eslatmalar:

- 21. `nodes status` tugunni **juftlangan** deb belgilaydi, agar uning qurilma juftlash roli `node`ni o‘z ichiga olsa.
- 22. `node.pair.*` (CLI: `openclaw nodes pending/approve/reject`) — gatewayga tegishli alohida tugun juftlash ombori; u WS `connect` qo‘l siqish jarayonini **to‘sib qo‘ymaydi**.

## 23. Masofaviy tugun xosti (system.run)

24. Gateway bir mashinada ishlayotgan bo‘lsa va buyruqlarni boshqa mashinada bajarishni istasangiz, **tugun xosti**dan foydalaning. 25. Model baribir **gateway** bilan muloqot qiladi; `host=node` tanlanganda gateway `exec` chaqiruvlarini **tugun xosti**ga yo‘naltiradi.

### 26. Qayerda nima ishlaydi

- 27. **Gateway xosti**: xabarlarni qabul qiladi, modelni ishga tushiradi, asbob chaqiruvlarini marshrutlaydi.
- 28. **Tugun xosti**: tugun mashinasida `system.run`/`system.which` ni bajaradi.
- 29. **Tasdiqlar**: tugun xostida `~/.openclaw/exec-approvals.json` orqali majburlanadi.

### 30. Tugun xostini ishga tushirish (oldingi rejim)

31. Tugun mashinasida:

```bash
32. openclaw node run --host <gateway-host> --port 18789 --display-name "Build Node"
```

### 33. SSH tunneli orqali masofaviy gateway (loopback bind)

34. Agar Gateway loopback’ga bog‘lansa (`gateway.bind=loopback`, lokal rejimda sukut bo‘yicha), masofaviy tugun xostlari to‘g‘ridan-to‘g‘ri ulana olmaydi. 35. SSH tunnel yarating va tugun xostini tunnelning lokal uchiga yo‘naltiring.

36. Misol (tugun xosti -> gateway xosti):

```bash
37. # Terminal A (ishlab tursin): lokal 18790 -> gateway 127.0.0.1:18789 yo‘naltirish
ssh -N -L 18790:127.0.0.1:18789 user@gateway-host

# Terminal B: gateway tokenini eksport qiling va tunnel orqali ulaning
export OPENCLAW_GATEWAY_TOKEN="<gateway-token>"
openclaw node run --host 127.0.0.1 --port 18790 --display-name "Build Node"
```

38. Eslatmalar:

- 39. Token — gateway konfiguratsiyasidagi `gateway.auth.token` (`~/.openclaw/openclaw.json` gateway xostida).
- 40. `openclaw node run` autentifikatsiya uchun `OPENCLAW_GATEWAY_TOKEN`ni o‘qiydi.

### 41. Tugun xostini ishga tushirish (xizmat)

```bash
42. openclaw node install --host <gateway-host> --port 18789 --display-name "Build Node"
openclaw node restart
```

### 43. Juftlash + nomlash

44. Gateway xostida:

```bash
45. openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes list
```

46. Nomlash variantlari:

- 47. `openclaw node run` / `openclaw node install` dagi `--display-name` (tugunda `~/.openclaw/node.json` ichida saqlanadi).
- 48. `openclaw nodes rename --node <id|name|ip> --name "Build Node"` (gateway darajasida bekor qilish/ustuvor nom).

### 49. Buyruqlarni ruxsatlar ro‘yxatiga qo‘shish

50. Exec tasdiqlari **har bir tugun xosti uchun alohida**. 1. Shlyuzdan allowlist yozuvlarini qo‘shing:

```bash
2. openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/uname"
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/sw_vers"
```

3. Tasdiqlar (approvals) tugun xostida `~/.openclaw/exec-approvals.json` da saqlanadi.

### 4. exec’ni tugunga yo‘naltiring

5. Standart sozlamalarni sozlang (gateway config):

```bash
6. openclaw config set tools.exec.host node
openclaw config set tools.exec.security allowlist
openclaw config set tools.exec.node "<id-or-name>"
```

7. Yoki sessiya bo‘yicha:

```
8. /exec host=node security=allowlist node=<id-or-name>
```

9. O‘rnatilgandan so‘ng, `host=node` bilan chaqirilgan har qanday `exec` tugun xostida ishlaydi (tugun allowlist/tasdiqlariga bo‘ysunadi).

10. Bog‘liq:

- 11. [Node host CLI](/cli/node)
- 12. [Exec tool](/tools/exec)
- 13. [Exec approvals](/tools/exec-approvals)

## 14. Buyruqlarni chaqirish

15. Past daraja (raw RPC):

```bash
16. openclaw nodes invoke --node <idOrNameOrIp> --command canvas.eval --params '{"javaScript":"location.href"}'
```

17. Keng tarqalgan “agentga MEDIA ilovasini berish” ish jarayonlari uchun yuqori darajadagi yordamchilar mavjud.

## 18. Skrinshotlar (canvas snapshotlari)

19. Agar tugun Canvas’ni (WebView) ko‘rsatayotgan bo‘lsa, `canvas.snapshot` `{ format, base64 }` ni qaytaradi.

20. CLI yordamchisi (vaqtinchalik faylga yozadi va `MEDIA:<path>` ni chiqaradi):

```bash
21. openclaw nodes canvas snapshot --node <idOrNameOrIp> --format png
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format jpg --max-width 1200 --quality 0.9
```

### 22. Canvas boshqaruvlari

```bash
openclaw nodes canvas present --node <idOrNameOrIp> --target https://example.com
openclaw nodes canvas hide --node <idOrNameOrIp>
openclaw nodes canvas navigate https://example.com --node <idOrNameOrIp>
openclaw nodes canvas eval --node <idOrNameOrIp> --js "document.title"
```

24. Eslatmalar:

- 25. `canvas present` URL’larni yoki lokal fayl yo‘llarini (`--target`) qabul qiladi, shuningdek joylashuv uchun ixtiyoriy `--x/--y/--width/--height` parametrlarini qo‘llab-quvvatlaydi.
- 26. `canvas eval` inline JS (`--js`) yoki pozitsion argumentni qabul qiladi.

### 27. A2UI (Canvas)

```bash
28. openclaw nodes canvas a2ui push --node <idOrNameOrIp> --text "Hello"
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --jsonl ./payload.jsonl
openclaw nodes canvas a2ui reset --node <idOrNameOrIp>
```

29. Eslatmalar:

- 30. Faqat A2UI v0.8 JSONL qo‘llab-quvvatlanadi (v0.9/createSurface rad etiladi).

## 31. Fotosuratlar + videolar (tugun kamerasi)

32. Fotosuratlar (`jpg`):

```bash
33. openclaw nodes camera list --node <idOrNameOrIp>
openclaw nodes camera snap --node <idOrNameOrIp>            # standart: ikkala tomoni (2 ta MEDIA qatori)
openclaw nodes camera snap --node <idOrNameOrIp> --facing front
```

34. Video kliplar (`mp4`):

```bash
35. openclaw nodes camera clip --node <idOrNameOrIp> --duration 10s
openclaw nodes camera clip --node <idOrNameOrIp> --duration 3000 --no-audio
```

36. Eslatmalar:

- 37. `canvas.*` va `camera.*` uchun tugun **oldingi rejimda (foregrounded)** bo‘lishi kerak (fon chaqiruvlari `NODE_BACKGROUND_UNAVAILABLE` ni qaytaradi).
- 38. Klip davomiyligi haddan oshmasligi uchun cheklanadi (hozirda `<= 60s`) — katta base64 payloadlarning oldini olish uchun.
- 39. Android imkon bo‘lganda `CAMERA`/`RECORD_AUDIO` ruxsatlarini so‘raydi; rad etilgan ruxsatlar `*_PERMISSION_REQUIRED` bilan xato beradi.

## 40. Ekran yozuvlari (tugunlar)

41. Tugunlar `screen.record` (mp4) ni taqdim etadi. 42. Misol:

```bash
43. openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10 --no-audio
```

44. Eslatmalar:

- 45. `screen.record` uchun tugun ilovasi oldingi rejimda bo‘lishi kerak.
- 46. Android yozishni boshlashdan oldin tizimning ekran yozib olish oynasini ko‘rsatadi.
- 47. Ekran yozuvlari `<= 60s` bilan cheklanadi.
- 48. `--no-audio` mikrofon yozuvini o‘chiradi (iOS/Android’da qo‘llab-quvvatlanadi; macOS tizim audio yozuvini ishlatadi).
- 49. Bir nechta ekran mavjud bo‘lsa, displeyni tanlash uchun `--screen <index>` dan foydalaning.

## 50. Joylashuv (tugunlar)

1. Sozlamalarda Location yoqilgan bo‘lsa, tugunlar `location.get` ni taqdim etadi.

2. CLI yordamchisi:

```bash
3. openclaw nodes location get --node <idOrNameOrIp>
openclaw nodes location get --node <idOrNameOrIp> --accuracy precise --max-age 15000 --location-timeout 10000
```

Notes:

- Location is **off by default**.
- “Always” requires system permission; background fetch is best-effort.
- 7. Javob lat/lon, aniqlik (metrda) va vaqt tamg‘asini o‘z ichiga oladi.

## 8. SMS (Android tugunlari)

9. Android tugunlari foydalanuvchi **SMS** ruxsatini berganda va qurilma telefoniyani qo‘llab-quvvatlaganda `sms.send` ni taqdim etishi mumkin.

10. Past darajadagi chaqirish:

```bash
11. openclaw nodes invoke --node <idOrNameOrIp> --command sms.send --params '{"to":"+15555550123","message":"Hello from OpenClaw"}'
```

12. Eslatmalar:

- 13. Imkoniyat e’lon qilinishidan oldin Android qurilmada ruxsat so‘rovi qabul qilinishi kerak.
- 14. Telefoniyasiz, faqat Wi‑Fi qurilmalar `sms.send` ni e’lon qilmaydi.

## 15. Tizim buyruqlari (tugun xosti / mac tuguni)

The macOS node exposes `system.run`, `system.notify`, and `system.execApprovals.get/set`.
17. Headless tugun xosti `system.run`, `system.which` va `system.execApprovals.get/set` ni taqdim etadi.

18. Misollar:

```bash
19. openclaw nodes run --node <idOrNameOrIp> -- echo "Hello from mac node"
openclaw nodes notify --node <idOrNameOrIp> --title "Ping" --body "Gateway ready"
```

Notes:

- 21. `system.run` yuklamada stdout/stderr/chiqish kodini qaytaradi.
- 22. `system.notify` macOS ilovasidagi bildirishnoma ruxsati holatiga amal qiladi.
- `system.run` supports `--cwd`, `--env KEY=VAL`, `--command-timeout`, and `--needs-screen-recording`.
- `system.notify` supports `--priority <passive|active|timeSensitive>` and `--delivery <system|overlay|auto>`.
- 25. macOS tugunlari `PATH` override’larini tashlab yuboradi; headless tugun xostlari `PATH` ni faqat tugun xosti PATH’iga prefiks sifatida qo‘shilganda qabul qiladi.
- 26. macOS tugun rejimida `system.run` macOS ilovasidagi exec approvals orqali cheklanadi (Settings → Exec approvals).
  27. Ask/allowlist/full headless tugun xosti bilan bir xil ishlaydi; rad etilgan so‘rovlar `SYSTEM_RUN_DENIED` ni qaytaradi.
- 28. Headless tugun xostida `system.run` exec approvals orqali cheklanadi (`~/.openclaw/exec-approvals.json`).

## 29. Exec tugun bog‘lash

30. Bir nechta tugun mavjud bo‘lsa, exec’ni muayyan tugunga bog‘lashingiz mumkin.
31. Bu `exec host=node` uchun sukutiy tugunni o‘rnatadi (va har bir agent bo‘yicha alohida o‘zgartirilishi mumkin).

32. Global sukut:

```bash
33. openclaw config set tools.exec.node "node-id-or-name"
```

34. Agent bo‘yicha override:

```bash
35. openclaw config get agents.list
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"
```

36. Istalgan tugunga ruxsat berish uchun olib tashlash:

```bash
37. openclaw config unset tools.exec.node
openclaw config unset agents.list[0].tools.exec.node
```

## 38. Ruxsatlar xaritasi

39. Tugunlar `node.list` / `node.describe` da ruxsat nomi (masalan, `screenRecording`, `accessibility`) bo‘yicha kalitlangan va mantiqiy qiymatlarga (`true` = berilgan) ega `permissions` xaritasini o‘z ichiga olishi mumkin.

## 40. Headless tugun xosti (kross-platforma)

41. OpenClaw Gateway WebSocket’iga ulanadigan va `system.run` / `system.which` ni taqdim etadigan **headless tugun xosti**ni (UI’siz) ishga tushirishi mumkin. 42. Bu Linux/Windows’da
    yoki server yonida minimal tugunni ishga tushirish uchun foydali.

43. Uni ishga tushirish:

```bash
44. openclaw node run --host <gateway-host> --port 18789
```

45. Eslatmalar:

- 46. Juftlash hali ham talab qilinadi (Gateway tugunni tasdiqlash oynasini ko‘rsatadi).
- 47. Tugun xosti o‘z tugun identifikatori, tokeni, ko‘rinadigan nomi va gateway ulanish ma’lumotlarini `~/.openclaw/node.json` da saqlaydi.
- 48. Exec approvals mahalliy ravishda `~/.openclaw/exec-approvals.json` orqali majburiy qilinadi
      (qarang [Exec approvals](/tools/exec-approvals)).
- 49. macOS’da headless tugun xosti, agar mavjud bo‘lsa, hamroh ilova exec xostini afzal ko‘radi va
      ilova mavjud bo‘lmasa, mahalliy bajarishga qaytadi. 50. Ilovani majburiy qilish uchun `OPENCLAW_NODE_EXEC_HOST=app` ni o‘rnating,
      yoki fallback’ni o‘chirish uchun `OPENCLAW_NODE_EXEC_FALLBACK=0` ni belgilang.
- 1. Gateway WS TLS dan foydalanganda `--tls` / `--tls-fingerprint` qo‘shish.

## 2. Mac node rejimi

- 3. macOS menyu paneli ilovasi Gateway WS serveriga node sifatida ulanadi (shunda `openclaw nodes …` ushbu Mac’ga nisbatan ishlaydi).
- 4. Masofaviy rejimda ilova Gateway porti uchun SSH tunnel ochadi va `localhost` ga ulanadi.
